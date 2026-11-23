"""C6 pre-specified analysis (protocol section 8 with amendments 0.3-0.8). FROZEN before its first run on
the full data set; SHA-256 recorded in analysis/FROZEN.txt. Any later change needs a dated amendment.

Input : data/studies.csv (built by workflow/stage4/build_dataset.py; provisional AI first-pass data)
Output: results/models.csv (every coefficient of every model), results/hypotheses.json (decision rules),
        results/descriptives.json, results/model_log.txt

Coding (amendment 0.4 rule 7):
  controls: reference 'sequenced'; levels included_not_sequenced, none_mentioned
  decon_yes: removed_control_taxa | tool | literature_list  (no: none, abundance_filter_only, unclear)
  tissue: tumour (ref), placenta_fetal, blood, other (= other_sterile + brain_csf); a level with < 5 studies
          in a model's data set is merged into 'other' for that model
  method_class: 16S | shotgun (shotgun, metatranscriptomic, host_seq_mining) | other (2bRAD-M, 16S+shotgun, other)
  year5 = (year - 2020) / 5
Model: binomial GLM (logit), successes = primary-list genera, trials = counted genera; Pearson chi2 scale;
       HC1 robust SE; Wald 95% CI. Studies with < 3 counted genera excluded.
Main-analysis rule (8.2): >= 30 usable shotgun-class studies -> main = shotgun-class model (no method term),
       16S model secondary; else pooled model with method term is main.
H4 (16S vs shotgun) is evaluated in the pooled model, the only model with a method term (amendment 0.8).
"""
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

warnings.filterwarnings('ignore')
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
LOG = []
log = lambda *a: LOG.append(' '.join(str(x) for x in a))

S = pd.read_csv(ROOT / 'data' / 'studies.csv')
U = S[(S.eligible_fulltext == 1) & (S.n_genera >= 3)].copy()
U['year'] = pd.to_numeric(U['year'], errors='coerce')
U['year5'] = (U['year'] - 2020) / 5
U['decon_yes'] = U['decontamination'].isin(['removed_control_taxa', 'tool', 'literature_list']).astype(int)
U['tissue'] = U['tissue_category'].replace({'other_sterile': 'other', 'brain_csf': 'other'})
U['method_class'] = U['method'].map(lambda m: '16S' if m == '16S' else ('shotgun' if m in ('shotgun', 'metatranscriptomic', 'host_seq_mining') else 'other'))
U['mining'] = (U['method'] == 'host_seq_mining').astype(int)
CTRL_LEVELS = ['sequenced', 'included_not_sequenced', 'none_mentioned']
TISSUES = ['tumour', 'placenta_fetal', 'blood', 'other']
log('usable studies:', len(U), dict(U.method_class.value_counts()))

rows, fits = [], {}


def prep(d, list_name='primary', min_genera=3):
    d = d[d.n_genera >= min_genera].copy()
    d['k'] = d[f'n_{list_name}']
    d['n'] = d['n_genera']
    small = [t for t in TISSUES if t != 'other' and (d.tissue == t).sum() < 5]
    d['tissue_m'] = d['tissue'].where(~d['tissue'].isin(small), 'other')
    return d, small


def formula(d, method_term):
    terms = []
    terms.append("C(controls, Treatment('sequenced'))")
    if d['decon_yes'].nunique() > 1:
        terms.append('decon_yes')
    lv = [t for t in TISSUES if t in set(d.tissue_m)]
    if len(lv) > 1:
        ref = 'tumour' if 'tumour' in lv else lv[0]
        terms.append(f"C(tissue_m, Treatment('{ref}'))")
    if method_term and d['method_class'].nunique() > 1:
        terms.append("C(method_class, Treatment('16S'))")
    terms.append('year5')
    return ' + '.join(terms)


def fit(name, d, list_name='primary', method_term=False, min_genera=3, ols=False):
    d, small = prep(d, list_name, min_genera)
    d = d.dropna(subset=['year5'])
    if len(d) < 10:
        log(name, 'SKIPPED: < 10 studies'); return None
    f = formula(d, method_term)
    try:
        if ols:
            d['y'] = np.log((d.k + 0.5) / (d.n - d.k + 0.5))
            m = smf.ols('y ~ ' + f, data=d).fit(cov_type='HC1')
            disp = np.nan
        else:
            d['fail'] = d.n - d.k
            m = smf.glm('k + fail ~ ' + f, data=d, family=sm.families.Binomial()).fit(scale='X2', cov_type='HC1')
            disp = m.scale
    except Exception as e:
        log(name, 'FAILED:', repr(e)); return None
    ctrl_n = {c: int((d.controls == c).sum()) for c in CTRL_LEVELS}
    log(f'{name}: n={len(d)} formula={f} merged_tissues={small} controls={ctrl_n} dispersion={disp}')
    ci = m.conf_int()
    for term in m.params.index:
        est, lo, hi = m.params[term], ci.loc[term, 0], ci.loc[term, 1]
        estimable = True
        for c in CTRL_LEVELS[1:]:
            if c in term and ctrl_n[c] < 3:
                estimable = False
        rows.append({'model': name, 'term': term, 'estimate': est, 'ci_low': lo, 'ci_high': hi, 'p': m.pvalues[term],
                     'odds_ratio': np.exp(est) if not ols else np.nan, 'or_ci_low': np.exp(lo) if not ols else np.nan,
                     'or_ci_high': np.exp(hi) if not ols else np.nan, 'n_studies': len(d), 'estimable': estimable,
                     'scale': 'logit-share OLS' if ols else 'log-odds (quasi-binomial)', 'dispersion': disp,
                     **{f'n_{c}': v for c, v in ctrl_n.items()}})
    fits[name] = (m, d)
    return m


n_shot = int((U.method_class == 'shotgun').sum())
MAIN_IS_SHOTGUN = n_shot >= 30
log('usable shotgun-class studies:', n_shot, '-> main analysis =', 'shotgun-class model' if MAIN_IS_SHOTGUN else 'pooled model')
MAIN = U[U.method_class == 'shotgun'] if MAIN_IS_SHOTGUN else U
MT = not MAIN_IS_SHOTGUN

# A main; B H1 co-primary without host-sequencing mining; C pooled (+/- mining); D 16S secondary
fit('A_main', MAIN, method_term=MT)
fit('B_main_excl_mining', MAIN[MAIN.mining == 0], method_term=MT)
fit('C_pooled', U, method_term=True)
fit('C2_pooled_excl_mining', U[U.mining == 0], method_term=True)
fit('D_16S', U[U.method_class == '16S'], method_term=False)
# E robustness (section 8.4 as amended 0.3), on the main data set
fit('E1_strict', MAIN, 'strict', method_term=MT)
fit('E2_salter_full', MAIN, 'salter_full', method_term=MT)
fit('E3_ge10_genera', MAIN, method_term=MT, min_genera=10)
fit('E4_ols_logit', MAIN, method_term=MT, ols=True)
# same robustness set for the pooled model (needed for H4)
fit('E1p_strict', U, 'strict', method_term=True)
fit('E2p_salter_full', U, 'salter_full', method_term=True)
fit('E3p_ge10_genera', U, method_term=True, min_genera=10)
fit('E4p_ols_logit', U, method_term=True, ols=True)
# F further sensitivity on main
for t in TISSUES:
    fit(f'F_leave_out_{t}', MAIN[MAIN.tissue != t], method_term=MT)
fit('F_full_profile_only', MAIN[MAIN.list_type == 'full_profile'], method_term=MT)
fit('F_excl_figures_partial', MAIN[MAIN.figures_only == 'no'], method_term=MT)
fit('F_excl_supplement_lists', MAIN[MAIN.genera_from_supplement == 0], method_term=MT)
fit('F_excl_public_reuse', MAIN[MAIN.data_source != 'public_reuse'], method_term=MT)
fit('F_pooled_excl_public_reuse', U[U.data_source != 'public_reuse'], method_term=True)

# G secondary outcome: any primary-list genus in the top 5 (studies that rank genera), logistic, HC1
for nm, d0, mt in (('G_top5_main', MAIN, MT), ('G_top5_pooled', U, True)):
    d = d0[d0.top5_ranked == 1].copy()
    d['y'] = pd.to_numeric(d.top5_primary_hit)
    d, small = prep(d)
    d = d.dropna(subset=['year5', 'y'])
    if len(d) >= 15 and d.y.nunique() == 2:
        try:
            m = smf.glm('y ~ ' + formula(d, mt), data=d, family=sm.families.Binomial()).fit(cov_type='HC1')
            ci = m.conf_int()
            for term in m.params.index:
                rows.append({'model': nm, 'term': term, 'estimate': m.params[term], 'ci_low': ci.loc[term, 0], 'ci_high': ci.loc[term, 1],
                             'p': m.pvalues[term], 'odds_ratio': np.exp(m.params[term]), 'or_ci_low': np.exp(ci.loc[term, 0]),
                             'or_ci_high': np.exp(ci.loc[term, 1]), 'n_studies': len(d), 'estimable': True, 'scale': 'log-odds (logistic)'})
            log(nm, 'n=', len(d))
        except Exception as e:
            log(nm, 'FAILED', repr(e))
    else:
        log(nm, 'SKIPPED: too few ranked studies', len(d))

R = pd.DataFrame(rows)
R.to_csv(OUT / 'models.csv', index=False)


def get(model, key):
    r = R[(R.model == model) & (R.term.str.contains(key, regex=False))]
    return None if r.empty else r.iloc[0]


def verdict(model, key, direction):
    """direction: '+' OR>1 / coef>0 ; '-' OR<1 / coef<0 ; '2' either side."""
    r = get(model, key)
    if r is None or not bool(r.estimable):
        return {'model': model, 'estimable': False}
    lo, hi, est = r.ci_low, r.ci_high, r.estimate
    excl = (lo > 0) or (hi < 0)
    ok_dir = {'+': est > 0, '-': est < 0, '2': True}[direction]
    return {'model': model, 'estimate': est, 'ci': [lo, hi], 'OR': r.odds_ratio, 'OR_ci': [r.or_ci_low, r.or_ci_high],
            'p': r.p, 'n': int(r.n_studies), 'direction_ok': bool(ok_dir), 'ci_excludes_null': bool(excl),
            'supported': bool(ok_dir and excl), 'estimable': True}


H = {}
spec = {'H1': ("none_mentioned]", '+'), 'H2': ('decon_yes', '-'), 'H3': ('year5', '-'), 'H4': ("method_class, Treatment('16S'))[T.shotgun]", '2')}
for h, (key, dirn) in spec.items():
    base = 'C_pooled' if h == 'H4' else 'A_main'
    rob = ['E1p_strict', 'E2p_salter_full', 'E3p_ge10_genera', 'E4p_ols_logit'] if h == 'H4' else ['E1_strict', 'E2_salter_full', 'E3_ge10_genera', 'E4_ols_logit']
    main_v = verdict(base, key, dirn)
    rv = [verdict(m, key, dirn) for m in rob]
    if dirn == '2' and main_v.get('estimable'):
        sign = np.sign(main_v['estimate'])
        for v in rv:
            if v.get('estimable'):
                v['direction_ok'] = bool(np.sign(v['estimate']) == sign)
                v['supported'] = v['direction_ok'] and v['ci_excludes_null']
    n_rob = sum(1 for v in rv if v.get('supported'))
    H[h] = {'main': main_v, 'robustness': rv, 'n_robustness_supported': n_rob,
            'robust': bool(main_v.get('supported') and n_rob >= 3)}
H['H1_coprimary_excl_mining'] = verdict('B_main_excl_mining', "none_mentioned]", '+')
H['H1_pooled'] = verdict('C_pooled', "none_mentioned]", '+')
H['H1_pooled_excl_mining'] = verdict('C2_pooled_excl_mining', "none_mentioned]", '+')
H['H1_excl_public_reuse'] = verdict('F_excl_public_reuse', "none_mentioned]", '+')
H['main_analysis'] = 'shotgun-class model' if MAIN_IS_SHOTGUN else 'pooled model'
H['n_usable_shotgun_class'] = n_shot
(OUT / 'hypotheses.json').write_text(json.dumps(H, indent=1, default=float))

# Descriptives (H5 and the 'also reported' items of section 1)
E = S[S.eligible_fulltext == 1].copy()
E['year'] = pd.to_numeric(E['year'], errors='coerce')
E['period'] = pd.cut(E['year'], [0, 2016, 2020, 2023, 2100], labels=['2012-2016', '2017-2020', '2021-2023', '2024-2026'])
E['tissue'] = E['tissue_category']
D = {'n_eligible': len(E), 'n_usable': len(U)}
D['controls_by_tissue'] = pd.crosstab(E.tissue, E.controls).to_dict()
D['controls_by_period'] = pd.crosstab(E.period, E.controls).to_dict()
D['decon_by_period'] = pd.crosstab(E.period, E.decontamination).to_dict()
D['qpcr_by_period'] = pd.crosstab(E.period, E.biomass_qpcr).to_dict()
D['method_by_tissue'] = pd.crosstab(E.tissue, E.method).to_dict()
for lst in ('primary', 'strict', 'salter_full', 'broad'):
    s = U[f'share_{lst}']
    D[f'share_{lst}'] = {'median': float(s.median()), 'q1': float(s.quantile(.25)), 'q3': float(s.quantile(.75)),
                         'mean': float(s.mean()), 'any_hit_share': float((U[f'n_{lst}'] > 0).mean())}
D['share_primary_by_tissue'] = U.groupby('tissue_category')['share_primary'].describe().to_dict()
D['share_primary_by_controls'] = U.groupby('controls')['share_primary'].describe().to_dict()
D['pooled_proportion_primary'] = float(U.n_primary.sum() / U.n_genera.sum())
G = pd.read_csv(ROOT / 'data' / 'genera.csv')
G = G[G.pmcid.isin(U.pmcid) & (G.flagged_contaminant == 0) & ~G.name_status.str.startswith('not_counted') & (G.name_status != 'duplicate')]
D['top_primary_genera'] = G[G.list_primary == 1].genus.value_counts().head(25).to_dict()
D['top_strict_genera'] = G[G.list_strict == 1].genus.value_counts().head(30).to_dict()
D['top_all_genera'] = G.genus.value_counts().head(30).to_dict()
(OUT / 'descriptives.json').write_text(json.dumps(D, indent=1, default=str))
(OUT / 'model_log.txt').write_text('\n'.join(LOG) + '\n')
print('\n'.join(LOG))
print(json.dumps({h: {k: v for k, v in H[h].items() if k in ('robust', 'n_robustness_supported')} | {'main_supported': H[h]['main'].get('supported')} for h in ('H1', 'H2', 'H3', 'H4')}, indent=1))
