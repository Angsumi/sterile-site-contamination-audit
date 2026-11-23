"""Combine agent decision files into screening/screening_log_full.csv (one row per merged record) and
screening/screening_counts.json. Later files override 'needs_abstract' entries. Records without PMCID are
logged as excluded (no PMC OA full text). PROVISIONAL: AI first pass, not yet checked by a person."""
import csv, json, sys, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
D = epmc.ROOT / 'screening' / 'agent_decisions'
R = list(csv.DictReader(open(epmc.ROOT / 'data' / 'records_merged.csv')))
dec = {}
for f in sorted(D.glob('*.tsv')):
    for line in open(f):
        if not line.strip() or line.startswith('#'):
            continue
        p, d, c, why, src = line.rstrip('\n').split('\t')
        if d == 'needs_abstract' and p in dec:
            continue
        if p in dec and dec[p]['decision'] != 'needs_abstract' and not f.name.startswith('00_'):
            raise SystemExit(f'duplicate decision {p} in {f.name}')
        dec[p] = {'decision': d, 'tissue_category': c, 'reason': why, 'source': src, 'file': f.name}
rows, missing = [], []
for r in R:
    p = r['pmcid']
    if not p:
        x = {'decision': 'exclude', 'tissue_category': '', 'reason': 'no PMCID (no PMC open-access full text)', 'source': 'script', 'file': ''}
    else:
        x = dec.get(p)
        if x is None or x['decision'] == 'needs_abstract':
            missing.append(p); continue
    rows.append({'pmcid': p, 'pmid': r['pmid'], 'doi': r['doi'], 'pubYear': r['pubYear'], 'title': r['title'],
                 'blocks_v1': r['blocks_v1'], 'blocks_v2': r['blocks_v2'], **{k: x[k] for k in ('decision', 'tissue_category', 'reason', 'source')},
                 'status': 'provisional (AI first pass)'})
assert not missing, missing[:10]
out = epmc.ROOT / 'screening' / 'screening_log_full.csv'
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
c = collections.Counter(r['decision'] for r in rows)
bycat = collections.Counter((r['decision'], r['tissue_category']) for r in rows if r['decision'] != 'exclude')
why = collections.Counter(r['reason'].split(';')[0] for r in rows if r['decision'] == 'exclude')
stage = collections.Counter('title' if ', title,' in r['source'] else ('title+abstract' if 'abstract' in r['source'] else r['source'][:40]) for r in rows)
summ = {'records': len(rows), 'decisions': dict(c), 'include_unclear_by_category': {f'{a}:{b}': n for (a, b), n in sorted(bycat.items())},
        'exclusion_reasons': dict(why.most_common()), 'decided_on': dict(stage)}
(epmc.ROOT / 'screening' / 'screening_counts.json').write_text(json.dumps(summ, indent=1))
print(json.dumps(summ, indent=1))
