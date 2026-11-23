"""C6 main figure (protocol 8.5) and tables. Descriptive presentation of data/studies.csv and data/genera.csv;
it fits no inferential model (those are in the frozen run_models.py).
Panel A: mean primary-list share (95% CI, t) by control practice within each tissue.
Panel B: primary-list share by publication year (study points) with the pooled proportion per year and a
         descriptive binomial logistic trend (share ~ year only), 95% CI band.
Panel C: % of usable studies reporting each strict-list genus, by tissue.
Outputs: results/figure1.png, results/figure1.pdf, results/table1_characteristics.csv,
         results/table2_key_estimates.csv, results/table3_strict_genera_by_tissue.csv
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'
S = pd.read_csv(ROOT / 'data' / 'studies.csv')
G = pd.read_csv(ROOT / 'data' / 'genera.csv')
E = S[S.eligible_fulltext == 1].copy()
U = E[E.n_genera >= 3].copy()
U['year'] = pd.to_numeric(U.year, errors='coerce')
TIS = {'tumour': 'Tumour', 'placenta_fetal': 'Placenta / fetal', 'blood': 'Blood', 'other': 'Other sterile\n(incl. brain/CSF)'}
U['tissue'] = U.tissue_category.replace({'other_sterile': 'other', 'brain_csf': 'other'})
CTRL = [('sequenced', 'Controls sequenced', '#2a78d6', 'o'),
        ('included_not_sequenced', 'Controls not sequenced', '#eb6834', 's'),
        ('none_mentioned', 'No controls mentioned', '#1baf7a', '^')]
INK, MUTED, GRID = '#1f1f1e', '#6b6a64', '#e4e3df'
plt.rcParams.update({'font.size': 8.5, 'axes.edgecolor': MUTED, 'axes.labelcolor': INK, 'xtick.color': MUTED,
                     'ytick.color': MUTED, 'axes.spines.top': False, 'axes.spines.right': False, 'font.family': 'DejaVu Sans'})

fig = plt.figure(figsize=(11, 7.6))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1.15], width_ratios=[1.25, 1], hspace=0.42, wspace=0.28)

# Panel A
ax = fig.add_subplot(gs[0, 0])
for i, (c, lab, col, mk) in enumerate(CTRL):
    for j, t in enumerate(TIS):
        d = U[(U.tissue == t) & (U.controls == c)].share_primary
        if len(d) < 2:
            continue
        m, se = d.mean(), d.std(ddof=1) / np.sqrt(len(d))
        h = se * stats.t.ppf(0.975, len(d) - 1)
        x = j + (i - 1) * 0.22
        ax.plot([x, x], [max(0, m - h), m + h], color=col, lw=2, solid_capstyle='round')
        ax.plot(x, m, mk, color=col, ms=8, mec='white', mew=1.5, label=lab if j == 0 else None)
        ax.text(x, m + h + 0.012, f'{len(d)}', ha='center', va='bottom', fontsize=7, color=MUTED)
ax.set_xticks(range(len(TIS)), TIS.values())
ax.set_ylabel('Primary-list contaminant share\n(mean, 95% CI; n studies above)')
ax.set_ylim(0, 0.56)
ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.legend(frameon=False, loc='upper center', ncol=3, fontsize=7.5, handletextpad=0.3, columnspacing=1.0)
ax.set_title('A  Contaminant share by control practice and tissue', loc='left', fontsize=9.5, color=INK, fontweight='bold')

# Panel B
ax = fig.add_subplot(gs[0, 1])
d = U.dropna(subset=['year'])
ax.scatter(d.year + np.random.default_rng(6).uniform(-0.25, 0.25, len(d)), d.share_primary, s=10, color='#86b6ef',
           edgecolor='none', alpha=0.7, label='Study')
yr = d.groupby('year').agg(k=('n_primary', 'sum'), n=('n_genera', 'sum'), studies=('pmcid', 'count')).reset_index()
yr = yr[yr.studies >= 3]
ax.plot(yr.year, yr.k / yr.n, 'o', color='#1c5cab', ms=6, mec='white', mew=1.2, label='Pooled per year (≥3 studies)')
X = sm.add_constant(d.year - 2020)
m = sm.GLM(np.column_stack([d.n_primary, d.n_genera - d.n_primary]), X, family=sm.families.Binomial()).fit(scale='X2', cov_type='HC1')
xs = np.linspace(d.year.min(), d.year.max(), 100)
pr = m.get_prediction(sm.add_constant(xs - 2020)).summary_frame()
ax.fill_between(xs, pr.mean_ci_lower, pr.mean_ci_upper, color='#2a78d6', alpha=0.15, lw=0)
ax.plot(xs, pr['mean'], color='#2a78d6', lw=2, label='Descriptive logistic trend')
ax.set_ylim(0, 1); ax.set_xlabel('Publication year'); ax.set_ylabel('Primary-list contaminant share')
ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=7.5, loc='upper left')
ax.set_title('B  Share by publication year', loc='left', fontsize=9.5, color=INK, fontweight='bold')

# Panel C
ax = fig.add_subplot(gs[1, :])
g = G[G.pmcid.isin(U.pmcid) & (G.flagged_contaminant == 0) & ~G.name_status.astype(str).str.startswith('not_counted')
      & (G.name_status != 'duplicate') & (G.list_strict == 1)].copy()
g['tissue'] = g.tissue_category.replace({'other_sterile': 'other', 'brain_csf': 'other'})
nt = U.groupby('tissue').pmcid.nunique()
tab = (g.groupby(['genus', 'tissue']).pmcid.nunique().unstack(fill_value=0).reindex(columns=list(TIS), fill_value=0) / nt.reindex(list(TIS)) * 100)
tab = tab.loc[tab.mean(axis=1).sort_values(ascending=False).index]
tab.round(1).to_csv(OUT / 'table3_strict_genera_by_tissue.csv')
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('blue', ['#f4f8fe', '#cde2fb', '#86b6ef', '#3987e5', '#1c5cab', '#104281'])
im = ax.imshow(tab.T.values, aspect='auto', cmap=cmap, vmin=0, vmax=max(40, tab.values.max()))
ax.set_xticks(range(len(tab)), [f'$\\it{{{x}}}$' for x in tab.index], rotation=60, ha='right', fontsize=7.5)
ax.set_yticks(range(len(TIS)), [f'{v.splitlines()[0]} (n={nt.get(k, 0)})' for k, v in TIS.items()])
for (i, j), v in np.ndenumerate(tab.T.values):
    if v >= 10:
        ax.text(j, i, f'{v:.0f}', ha='center', va='center', fontsize=6.5, color='white' if v > 25 else INK)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
cb = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.01); cb.set_label('% of usable studies reporting the genus', fontsize=7.5)
cb.outline.set_visible(False)
ax.set_title('C  Strict-list contaminant genera reported, by tissue', loc='left', fontsize=9.5, color=INK, fontweight='bold')
fig.savefig(OUT / 'figure1.png', dpi=200, bbox_inches='tight', facecolor='white')
fig.savefig(OUT / 'figure1.pdf', bbox_inches='tight', facecolor='white')

# Table 1: characteristics of eligible and usable studies
rows = []
for name, d0 in (('Eligible', E), ('Usable (≥3 genera)', U)):
    r = {'set': name, 'n': len(d0)}
    for col in ('tissue_category', 'method', 'controls', 'decontamination', 'biomass_qpcr', 'data_source', 'list_type', 'figures_only'):
        for k, v in d0[col].fillna('').value_counts().items():
            r[f'{col}:{k}'] = v
    rows.append(r)
pd.DataFrame(rows).T.to_csv(OUT / 'table1_characteristics.csv', header=False)
R = pd.read_csv(OUT / 'models.csv')
keep = R.term.str.contains('controls|decon_yes|year5|method_class') & R.model.isin(
    ['A_main', 'B_main_excl_mining', 'C_pooled', 'C2_pooled_excl_mining', 'D_16S', 'F_excl_public_reuse', 'F_pooled_excl_public_reuse'])
R[keep][['model', 'term', 'n_studies', 'odds_ratio', 'or_ci_low', 'or_ci_high', 'p']].round(3).to_csv(OUT / 'table2_key_estimates.csv', index=False)
print('figure and tables written')
