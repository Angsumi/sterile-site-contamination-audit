"""Stage 4 final step: merge all extractions (extraction/json/*.json: agent batches + converted pilot), run
the automatic checks, normalise genus names and match them to the fixed contaminant lists BY SCRIPT.
Name normalisation order: fixed synonym table (build_contaminant_list.SYNONYMS) -> composite names to
first genus -> reviewed name table reference/genus_name_review.csv (misspellings and recent NCBI renames,
amendment 0.6) -> must be an NCBI Bacteria genus to count (archaea logged, not counted).
Outputs (all provisional, AI first pass):
  data/studies.csv   one row per extracted paper (eligibility, design fields, counts, shares)
  data/genera.csv    one row per paper x genus
  data/check_summary.json
"""
import csv, json, re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import epmc
from build_contaminant_list import SYNONYMS
import check_one
ROOT = epmc.ROOT
NCBI = check_one.NCBI
L = list(csv.DictReader(open(ROOT / 'reference' / 'contaminant_genera.csv')))
LISTS = {'primary': {r['genus'] for r in L if r['list_primary_environmental'] == '1'},
         'strict': {r['genus'] for r in L if r['list_strict'] == '1'},
         'salter_full': {r['genus'] for r in L if r['salter2014_evidence']},
         'broad': {r['genus'] for r in L if r['list_broad'] == '1'}}
REV = {}
rp = ROOT / 'reference' / 'genus_name_review.csv'
if rp.exists():
    for r in csv.DictReader(open(rp)):
        REV[r['name']] = r

def normalise(name):
    # Composite SILVA labels may use hyphen-minus, en dash, em dash, or Unicode hyphen.
    # Preserve the original label in extraction JSON; normalize only for counting.
    n = name.strip().replace('[', '').replace(']', '')
    n = re.sub(r'^(g__|Candidatus\s+)', '', n)
    n = re.sub(r'[‐‑‒–—−]', '-', n)
    if n not in NCBI:
        # Genus names in paper prose can be lowercased (or sentence-initially capitalized).
        canonical = next((g for g in NCBI if g.casefold() == n.casefold()), None)
        if canonical:
            n = canonical
    n = SYNONYMS.get(n, n)
    if n not in NCBI and n not in REV:
        n = SYNONYMS.get(re.split(r'[-_ /]', n)[0], re.split(r'[-_ /]', n)[0])
    status = 'ncbi'
    if n in REV:
        r = REV[n]
        if r['action'] == 'count_as':
            n, status = SYNONYMS.get(r['count_as'], r['count_as']), 'reviewed'
        else:
            return n, 'not_counted:' + r['reason']
    if n in NCBI:
        if NCBI[n][1] == 'Archaea': return n, 'not_counted:archaeal'
        sci = NCBI[n][0]
        # keep list spelling when the NCBI scientific name differs only by a later rename the lists do not use
        if n not in LISTS['broad'] and sci in LISTS['broad']: n = sci
        return n, status
    if status == 'reviewed': return n, status
    return n, 'not_counted:not an NCBI bacterial genus'

studies, grows, allfails, warn_names = [], [], {}, Counter()
for f in sorted((ROOT / 'extraction' / 'json').glob('PMC*.json')):
    p = f.stem
    x = json.loads(f.read_text())
    probs = check_one.check(p)
    fails = [q for q in probs if q.startswith('FAIL')]
    allfails[p] = fails
    for q in probs:
        m = re.match(r'WARN genus (\S+) not an NCBI', q)
        if m: warn_names[m.group(1)] += 1
    g = lambda k: (x.get(k) or {}).get('value', '')
    row = {'pmcid': p, 'source': 'pilot' if 'pilot' in x.get('extractor', '') else 'agent', 'extractor': x.get('extractor', ''),
           'eligible_fulltext': int(bool(x.get('eligible_fulltext'))), 'exclusion_reason': x.get('exclusion_reason', ''),
           'tissue_category': x.get('tissue_category', ''), 'sub_site': x.get('sub_site', ''), 'year': x.get('year', ''),
           'country': x.get('country', ''), 'data_source': g('data_source'), 'dataset': (x.get('data_source') or {}).get('dataset', ''),
           'method': g('method'), 'controls': g('controls'), 'decontamination': g('decontamination'),
           'decon_tool': (x.get('decontamination') or {}).get('tool', ''), 'biomass_qpcr': g('biomass_qpcr'),
           'n_target_samples': x.get('n_target_samples') or '', 'list_type': x.get('list_type', ''), 'figures_only': x.get('figures_only', ''),
           'authors_conclusion': x.get('authors_conclusion', ''), 'check_fails': len(fails)}
    counted, flagged, notc = [], [], []
    supp = False
    for ge in x.get('genera', []):
        n, st = normalise(ge.get('name', ''))
        supp |= ge.get('evidence_id', '').startswith('S')
        rec = {'pmcid': p, 'tissue_category': row['tissue_category'], 'name_as_written': ge.get('name', ''), 'genus': n,
               'evidence_id': ge.get('evidence_id', ''), 'flagged_contaminant': int(bool(ge.get('flagged_contaminant'))),
               'name_status': st, **{f'list_{k}': int(n in s) for k, s in LISTS.items()}}
        if st.startswith('not_counted'): notc.append(n)
        elif rec['flagged_contaminant']: flagged.append(n)
        elif n not in counted: counted.append(n)
        else: rec['name_status'] = 'duplicate'
        grows.append(rec)
    top5 = [normalise(t)[0] for t in x.get('top5', [])]
    row |= {'n_genera': len(counted), 'n_flagged_removed': len(set(flagged)), 'n_not_counted': len(notc),
            'usable': int(row['eligible_fulltext'] and len(counted) >= 3), 'genera_from_supplement': int(supp)}
    for k, s in LISTS.items():
        h = [c for c in counted if c in s]
        row[f'n_{k}'] = len(h)
        row[f'share_{k}'] = round(len(h) / len(counted), 4) if counted else ''
    row['top5_ranked'] = int(bool(top5))
    row['top5_primary_hit'] = int(any(t in LISTS['primary'] for t in top5)) if top5 else ''
    row['primary_hits'] = ';'.join(c for c in counted if c in LISTS['primary'])
    studies.append(row)
for name, rows_ in (('studies.csv', studies), ('genera.csv', grows)):
    with open(ROOT / 'data' / name, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows_[0])); w.writeheader(); w.writerows(rows_)
el = [s for s in studies if s['eligible_fulltext']]
summ = {'extracted': len(studies), 'eligible': len(el), 'usable_ge3_genera': sum(s['usable'] for s in el),
        'papers_with_check_fails': sum(1 for v in allfails.values() if v), 'fail_detail': {k: v for k, v in allfails.items() if v},
        'usable_by_tissue': dict(Counter(s['tissue_category'] for s in el if s['usable'])),
        'controls_eligible': dict(Counter(s['controls'] for s in el)), 'method_usable': dict(Counter(s['method'] for s in el if s['usable'])),
        'not_ncbi_names': dict(warn_names.most_common())}
(ROOT / 'data' / 'check_summary.json').write_text(json.dumps(summ, indent=1))
print(json.dumps({k: v for k, v in summ.items() if k not in ('fail_detail', 'not_ncbi_names')}, indent=1))
print('not-NCBI names:', len(warn_names))
