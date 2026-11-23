"""Build manuscript supplementary files S1-S6 from committed data (no new analysis).
S1 flow diagram (PNG/PDF) + counts table; S2 search strategies; S3 contaminant reference lists;
S4 study- and genus-level data; S5 all model and sensitivity estimates; S6 protocol with amendments.
Output: manuscript/supplementary/
"""
import json, re, shutil
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'manuscript' / 'supplementary'
OUT.mkdir(parents=True, exist_ok=True)

mc = json.loads((ROOT / 'data' / 'merge_counts.json').read_text())
sc = json.loads((ROOT / 'screening' / 'screening_counts.json').read_text())
S = pd.read_csv(ROOT / 'data' / 'studies.csv')
dl = pd.read_csv(ROOT / 'data' / 'fulltext_download_log.csv')
X = S[S.eligible_fulltext == 0]
E = S[S.eligible_fulltext == 1]


def cat(r):
    r = str(r).lower()
    if re.search(r'same .*cohort|same .*specimen|previously characterized|reused', r): return 'Duplicate cohort'
    if re.search(r'review|commentary|protocol', r): return 'Not primary research'
    if re.search(r'mouse|murine|rat model|animal', r): return 'Animal or in-vitro only'
    if re.search(r'diagnostic|suspected|infection|febrile', r): return 'Diagnostic / infection study'
    if re.search(r'qpcr|pcr|fish|ihc|immunohisto|proteom|microarray|metabol|ultrastructural|is-pro', r): return 'No sequencing-based profiling'
    if re.search(r'mucosal|bal|bronchoalveolar|stool|gut|airway|meconium|colorectal|cervical|vaginal', r): return 'Mucosal/high-biomass samples only'
    return 'Other (virome-only, unverifiable, off-aim)'


fx = X.exclusion_reason.map(cat).value_counts()
ta = {k: v for k, v in sc['exclusion_reasons'].items()}
groups = {'Animal / non-human / in vitro': 0, 'Mucosal or high-biomass sites only': 0, 'Diagnostic / infection (mNGS)': 0,
          'Not primary research': 0, 'No sequencing-based profiling': 0, 'Other': 0}
for k, v in ta.items():
    kl = k.lower()
    g = ('Diagnostic / infection (mNGS)' if re.search(r'^diagnostic|suspected sepsis|shunt infection|cf lungs|periprosthetic', kl) else
         'No sequencing-based profiling' if re.search(r'sequencing-based|culture isolation|not microbiome|single-organism', kl) else
         'Animal / non-human / in vitro' if re.search(r'animal|mouse|horse|\bfish\b|cats|goats|non-human|in vitro|in-vitro|cell-line', kl) else
         'Mucosal or high-biomass sites only' if re.search(r'mucosal|gut|colorectal|colon|cervical|bladder|head and neck|oral|vaginal|seminal|nipple|airway', kl) else
         'Diagnostic / infection (mNGS)' if re.search(r'diagnostic|infection|sepsis|periprosthetic|shunt|cf lungs', kl) else
         'Not primary research' if re.search(r'review|protocol|meta-analysis|case report|primary research', kl) else 'Other')
    groups[g] += v
n_ft = int(dl.shape[0]); n_ok = int(dl.fulltext_ok.sum())
counts = {'records_v1': mc['source_counts']['v1_2026-11-23'], 'records_v2': mc['source_counts']['v2_2026-11-23'],
          'unique_records': mc['unique_after_dedup'], 'excluded_title_abstract': sc['decisions']['exclude'],
          'excluded_title_abstract_by_reason': groups, 'full_text_sought': n_ft, 'full_text_not_retrieved': n_ft - n_ok,
          'full_text_assessed': n_ok, 'excluded_full_text': int(len(X)), 'excluded_full_text_by_reason': fx.to_dict(),
          'eligible': int(len(E)), 'eligible_lt3_genera': int((E.n_genera < 3).sum()), 'usable': int((E.n_genera >= 3).sum())}
(OUT / 'S1_flow_counts.json').write_text(json.dumps(counts, indent=1))

# S1 flow diagram
fig, ax = plt.subplots(figsize=(8.2, 9.6)); ax.axis('off'); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
INK, EDGE = '#1f1f1e', '#6b6a64'


def box(x, y, w, h, text, fs=8):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc='white', ec=EDGE, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=fs, color=INK, wrap=True)


def arrow(x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color=EDGE, lw=1))


box(5, 88, 55, 9, f"Europe PMC open-access records\nsearch v1: {counts['records_v1']:,}   search v2: {counts['records_v2']:,}\n(2012–2026; searches run 22–23 Nov 2026)")
box(5, 74, 55, 7, f"Unique records after de-duplication\nn = {counts['unique_records']:,}")
gtxt = '\n'.join(f'{k}: {v:,}' for k, v in groups.items())
box(64, 60, 34, 21, f"Excluded on title/abstract\nn = {counts['excluded_title_abstract']:,}\n\n{gtxt}", fs=6.8)
box(5, 60, 55, 7, f"Full texts sought (include + unclear)\nn = {n_ft}")
box(64, 50, 34, 6, f"Full text not available\nn = {n_ft - n_ok}", fs=7)
box(5, 46, 55, 7, f"Full texts assessed for eligibility\nn = {n_ok}")
ftxt = '\n'.join(f'{k}: {v}' for k, v in fx.items())
box(64, 24, 34, 22, f"Excluded on full text\nn = {len(X)}\n\n{ftxt}", fs=6.3)
box(5, 32, 55, 7, f"Eligible studies (descriptive analyses)\nn = {len(E)}")
box(64, 15, 34, 6, f"Fewer than 3 counted genera\nn = {counts['eligible_lt3_genera']}", fs=7)
box(5, 12, 55, 9, f"Usable studies (≥ 3 genera; models)\nn = {counts['usable']}\ntumour 206 · blood 85 · placenta/fetal 50 ·\nother sterile 46 · brain/CSF 11", fs=7.5)
for y1, y2 in ((88, 81), (74, 67), (60, 53), (46, 39), (32, 21)):
    arrow(32.5, y1, 32.5, y2)
for y in (77.5, 63.5, 49.5, 35.5, 16.5):
    pass
arrow(60, 77.5, 64, 70); arrow(60, 63.5, 64, 53); arrow(60, 49.5, 64, 35); arrow(60, 35.5, 64, 18)
ax.text(0, 100, 'Supplementary Figure S1. Study selection', fontsize=10, fontweight='bold', va='top', color=INK)
fig.savefig(OUT / 'S1_flow_diagram.png', dpi=200, bbox_inches='tight', facecolor='white')
fig.savefig(OUT / 'S1_flow_diagram.pdf', bbox_inches='tight', facecolor='white')

# S2 search strategies
lines = ['# Supplementary File S2. Search strategies\n',
         'Europe PMC REST API (searchPOST) and PubMed E-utilities. Run 22 Nov 2026 and re-run unchanged 23 Nov 2026. '
         'Open-access subset: `OPEN_ACCESS:Y AND HAS_FT:Y`; preprints removed.\n']
for f, title in (('search_log.json', 'Search v1 (broad)'), ('search_log_v2.json', 'Search v2 (tight, amendment 0.2)')):
    d = json.loads((ROOT / 'search' / f).read_text())
    lines.append(f'\n## {title}\n')
    for t, v in d['tissues'].items():
        lines.append(f"\n### {t}\n\nPubMed ({v['pubmed_count']} records):\n\n```\n{v['pubmed_query']}\n```\n\nEurope PMC open access ({v['epmc_oa_fulltext_count']} records):\n\n```\n{v['epmc_oa_query']}\n```\n")
(OUT / 'S2_search_strategies.md').write_text(''.join(lines))

# S3-S6
shutil.copy(ROOT / 'reference' / 'contaminant_genera.csv', OUT / 'S3_contaminant_reference_lists.csv')
shutil.copy(ROOT / 'reference' / 'genus_name_review.csv', OUT / 'S3b_genus_name_review.csv')
keep = [c for c in S.columns if c not in ('extractor', 'check_fails')]
S[keep].to_csv(OUT / 'S4a_study_level_data.csv', index=False)
shutil.copy(ROOT / 'data' / 'genera.csv', OUT / 'S4b_genus_level_data.csv')
shutil.copy(ROOT / 'results' / 'models.csv', OUT / 'S5_all_model_estimates.csv')
shutil.copy(ROOT / 'results' / 'hypotheses.json', OUT / 'S5b_hypothesis_decisions.json')
shutil.copy(ROOT / 'C6_protocol.md', OUT / 'S6_protocol_with_amendments.md')
(OUT / 'README.md').write_text('''# Supplementary material

| File | Content |
|---|---|
| S1_flow_diagram.png / .pdf, S1_flow_counts.json | Study selection flow and counts |
| S2_search_strategies.md | Exact search strings and record counts |
| S3_contaminant_reference_lists.csv | Fixed contaminant genus lists (primary, strict, full Salter, broad) with source evidence |
| S3b_genus_name_review.csv | Adjudication of genus names not in NCBI Taxonomy |
| S4a_study_level_data.csv | One row per extracted study (design fields, counts, shares) |
| S4b_genus_level_data.csv | One row per study x reported genus, with list membership |
| S5_all_model_estimates.csv, S5b_hypothesis_decisions.json | All pre-specified, robustness and sensitivity model estimates; decision rules |
| S6_protocol_with_amendments.md | Protocol v0.1 with dated amendments 0.2-0.8 |
''')
print(json.dumps(counts, indent=1))
