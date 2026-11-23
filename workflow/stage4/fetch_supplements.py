"""Stage 4 step 3b (amendment 0.5): OA supplementary files from the PMC Open Access dataset on AWS
(public bucket pmc-oa-opendata, https://pmc-oa-opendata.s3.amazonaws.com/<PMCID>.<v>/...). Only files
listed as <supplementary-material> in the article XML with extension xlsx/xls/csv/tsv/txt/docx/doc/pdf
(<= 25 MB) are fetched to local-only papers/<PMCID>/supp/, then converted to Markdown with Microsoft
markitdown (papers/<PMCID>/supp_md/<file>.md). Log: data/supplement_log.csv (committed)."""
import csv, hashlib, json, re, sys, time, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
import subprocess
S3 = 'https://pmc-oa-opendata.s3.amazonaws.com'
EXT = ('.xlsx', '.xls', '.csv', '.tsv', '.txt', '.docx', '.doc', '.pdf')
MAX = 25 * 2**20
MD = str(epmc.ROOT / '.venv' / 'bin' / 'markitdown')

def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=epmc.UA), timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 404): return None
        except Exception:
            time.sleep(2 + 3 * i)
    return None

def meta(p):
    best = None
    for v in range(1, 6):
        b = get(f'{S3}/{p}.{v}/{p}.{v}.json')
        if b is None:
            if best: break
            continue
        best = json.loads(b)
    return best

rows = [r for r in csv.DictReader(open(epmc.ROOT / 'data' / 'fulltext_download_log.csv')) if r['fulltext_ok'] == '1']
log = []
for i, r in enumerate(rows):
    p = r['pmcid']
    xml = (epmc.PAPERS / p / 'fulltext.xml').read_text(errors='ignore')
    hrefs = []
    for sm in re.findall(r'<supplementary-material.*?</supplementary-material>|<supplementary-material[^>]*/>', xml, re.S):
        hrefs += re.findall(r'xlink:href="([^"]+)"', sm)
    hrefs = [h for h in dict.fromkeys(hrefs) if h.lower().endswith(EXT) and not h.startswith('http')]
    if not hrefs:
        log.append({'pmcid': p, 'file': '', 'status': 'no tabular/text supplement listed'}); continue
    m = meta(p)
    if not m:
        for h in hrefs: log.append({'pmcid': p, 'file': h, 'status': 'not in PMC OA dataset'})
        continue
    urls = {u.split('/')[-1].split('?')[0]: u for u in m.get('media_urls', [])}
    for k, h in enumerate(hrefs, 1):
        u = urls.get(h.split('/')[-1])
        rec = {'pmcid': p, 'file': h, 'supp_no': k}
        if not u:
            rec['status'] = 'listed in XML but not in OA dataset'; log.append(rec); continue
        https = u.replace('s3://pmc-oa-opendata', S3).split('?')[0]
        b = get(https)
        if b is None:
            rec['status'] = 'download failed'; log.append(rec); continue
        if len(b) > MAX:
            rec |= {'status': 'skipped >25MB', 'bytes': len(b)}; log.append(rec); continue
        d = epmc.PAPERS / p / 'supp'; d.mkdir(parents=True, exist_ok=True)
        f = d / f'S{k}_{Path(h).name}'
        if not f.exists(): f.write_bytes(b)
        rec |= {'url': https, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'retrieved': time.strftime('%Y-%m-%d')}
        o = epmc.PAPERS / p / 'supp_md'; o.mkdir(exist_ok=True)
        try:  # markitdown CLI in a subprocess with a time limit (large spreadsheets can exhaust memory)
            if not (o / f'S{k}.md').exists():
                subprocess.run([MD, str(f), '-o', str(o / f'S{k}.md')], timeout=180, check=True, capture_output=True)
            rec |= {'status': 'ok', 'md_chars': (o / f'S{k}.md').stat().st_size}
        except subprocess.TimeoutExpired:
            rec['status'] = 'downloaded; markitdown timeout (180 s)'
        except Exception as e:
            rec['status'] = f'downloaded; markitdown failed: {type(e).__name__}'
        log.append(rec)
    if i % 25 == 0: print(i, len(log), flush=True)
keys = ['pmcid', 'supp_no', 'file', 'status', 'url', 'bytes', 'sha256', 'retrieved', 'md_chars']
with open(epmc.ROOT / 'data' / 'supplement_log.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=keys); w.writeheader(); w.writerows([{k: x.get(k, '') for k in keys} for x in log])
import collections
print('done', collections.Counter(x['status'].split(';')[0] for x in log))
