"""Draw the fixed random screening sample (seed 6): 30 OA records per tissue block, then the
pilot order. Writes screening/sample_abstracts.json (title + abstract) for the AI screener."""
import csv, json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import epmc

TISSUES = ['tumour', 'placenta_fetal', 'blood', 'brain_csf', 'other_sterile']
recs = list(csv.DictReader(open(epmc.ROOT / 'search' / (sys.argv[2] if len(sys.argv) > 2 else 'epmc_oa_records.csv'))))
rng = random.Random(6)
order = {t: [r for r in recs if t in r['tissues'].split(';')] for t in TISSUES}
for t in TISSUES:
    rng.shuffle(order[t])
taken, sample = set(), []
for t in TISSUES:
    k = 0
    for r in order[t]:
        if r['pmcid'] in taken:
            continue
        taken.add(r['pmcid']); sample.append({'block': t, 'rank': k + 1, **r}); k += 1
        if k == int(sys.argv[1] if len(sys.argv) > 1 else 30):
            break
# abstracts in batches
ids = [s['pmcid'] for s in sample]
abst = {}
for i in range(0, len(ids), 40):
    q = ' OR '.join(f'PMCID:{p}' for p in ids[i:i + 40])
    _, rr = epmc.epmc_search(q, page_size=100, max_records=100, fields='core')
    for r in rr:
        abst[r.get('pmcid')] = epmc.clean(r.get('abstractText', '') or '')
for s in sample:
    s['abstract'] = abst.get(s['pmcid'], '')
json.dump(sample, open(epmc.ROOT / 'screening' / ('sample_abstracts_v2.json' if len(sys.argv) > 2 else 'sample_abstracts.json'), 'w'), indent=1)
json.dump({t: [r['pmcid'] for r in order[t]] for t in TISSUES}, open(epmc.ROOT / 'screening' / ('random_order_seed6_v2.json' if len(sys.argv) > 2 else 'random_order_seed6.json'), 'w'))
print(len(sample), sum(bool(s['abstract']) for s in sample))
