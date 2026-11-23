"""Stage 4 step 3: download OA JATS XML for all include + unclear records (screening_log_full.csv)
to local-only papers/<PMCID>/fulltext.xml (URL, size, SHA-256 in retrieval.json). Writes
data/fulltext_download_log.csv (committed; no copyrighted text)."""
import csv, json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
rows = [r for r in csv.DictReader(open(epmc.ROOT / 'screening' / 'screening_log_full.csv')) if r['decision'] in ('include', 'unclear')]
out = []
for i, r in enumerate(rows):
    p = r['pmcid']
    try:
        path = epmc.fulltext_xml(p)
    except Exception as e:
        path = None
    rec = {'pmcid': p, 'decision': r['decision'], 'tissue_category': r['tissue_category'], 'fulltext_ok': int(path is not None)}
    if path:
        meta = json.loads((path.parent / 'retrieval.json').read_text()) if (path.parent / 'retrieval.json').exists() else {}
        rec |= {k: meta.get(k, '') for k in ('url', 'bytes', 'sha256', 'retrieved')}
    out.append(rec)
    if i % 50 == 0:
        print(i, sum(o['fulltext_ok'] for o in out), flush=True)
    time.sleep(0.2)
keys = ['pmcid', 'decision', 'tissue_category', 'fulltext_ok', 'url', 'bytes', 'sha256', 'retrieved']
with open(epmc.ROOT / 'data' / 'fulltext_download_log.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows([{k: o.get(k, '') for k in keys} for o in out])
print('done', len(out), 'ok', sum(o['fulltext_ok'] for o in out))
