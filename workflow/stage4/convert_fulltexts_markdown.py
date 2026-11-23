"""Convert downloaded C6 JATS full texts to local Markdown via markitdown.

The source XML remains unchanged. We first render its indexed article elements as
simple HTML, then let markitdown produce the Markdown reading copy.
"""
import csv
import html
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
from markitdown import MarkItDown

MD = MarkItDown()
LOG = epmc.ROOT / 'data' / 'fulltext_markdown_log.csv'
rows = list(csv.DictReader(open(epmc.ROOT / 'data' / 'fulltext_download_log.csv')))
out = []
for i, row in enumerate(rows):
    pmcid = row['pmcid']
    src = epmc.PAPERS / pmcid / 'fulltext.xml'
    dest = epmc.PAPERS / pmcid / 'fulltext.md'
    rec = {'pmcid': pmcid, 'status': 'failed', 'markdown_path': str(dest.relative_to(epmc.ROOT))}
    try:
        meta = epmc.meta(src)
        chunks = [f"<h1>{html.escape(meta['title'])}</h1>",
                  f"<p>PMCID: {html.escape(pmcid)} | {html.escape(meta['journal'])} | {html.escape(meta['year'])}</p>"]
        for el in epmc.elements(src):
            chunks.append(f"<h2>{html.escape(el['section'])}</h2><p>{html.escape(el['text'])}</p>")
        with tempfile.NamedTemporaryFile('w', suffix='.html', encoding='utf-8') as fh:
            fh.write('<!doctype html><html><body>' + '\n'.join(chunks) + '</body></html>')
            fh.flush()
            result = MD.convert(fh.name)
        dest.write_text(result.markdown, encoding='utf-8')
        rec.update(status='ok', markdown_chars=len(result.markdown))
    except Exception as e:
        rec['status'] = f'failed: {type(e).__name__}: {e}'
    out.append(rec)
    if i % 50 == 0:
        print(i, rec['status'], flush=True)
with open(LOG, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['pmcid', 'status', 'markdown_path', 'markdown_chars'])
    w.writeheader()
    w.writerows(out)
from collections import Counter
print('done', len(out), dict(Counter(r['status'].split(':')[0] for r in out)))
