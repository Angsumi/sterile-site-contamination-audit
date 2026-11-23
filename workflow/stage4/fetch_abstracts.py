"""Stage 4 step 2 input: titles, abstracts, publication types and MeSH-free metadata for all merged
records from Europe PMC (resultType=core). Local only: papers/_screening/abstracts.json
(abstract text is not committed)."""
import csv, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc

out = epmc.PAPERS / '_screening'; out.mkdir(parents=True, exist_ok=True)
path = out / 'abstracts.json'
have = json.loads(path.read_text()) if path.exists() else {}
ids = [r['pmcid'] for r in csv.DictReader(open(epmc.ROOT / 'data' / 'records_merged.csv')) if r['pmcid'] and r['pmcid'] not in have]
for i in range(0, len(ids), 50):
    q = ' OR '.join(f'PMCID:{p}' for p in ids[i:i + 50])
    _, rr = epmc.epmc_search(q, page_size=100, max_records=100, fields='core')
    for r in rr:
        if r.get('pmcid') in ids[i:i + 50]:
            have[r['pmcid']] = {'abstract': epmc.clean(r.get('abstractText', '') or ''),
                                'pubTypes': (r.get('pubTypeList') or {}).get('pubType', []),
                                'keywords': (r.get('keywordList') or {}).get('keyword', []),
                                'language': r.get('language', '')}
    if i % 500 == 0:
        print(i, len(have), flush=True); path.write_text(json.dumps(have))
path.write_text(json.dumps(have))
print('done', len(have), 'with abstract', sum(bool(v['abstract']) for v in have.values()))
