"""Small Europe PMC / PubMed helpers for C6 (search counts, OA full-text XML, text index).

Modelled on R2's workflow (download_papers.py, extraction_agent.py), simplified.
Full texts are saved under sterile-site-contamination-audit/papers/ (local only: linked from `data_local/`).
"""
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / 'papers'
UA = {'User-Agent': 'C6LiteratureAudit/0.1 (academic literature retrieval)'}
EPMC = 'https://www.ebi.ac.uk/europepmc/webservices/rest'
EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'


def get(url, timeout=40, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 + 3 * i)


def _post(url, data, timeout=90, tries=3):
    import requests
    for i in range(tries):
        try:
            r = requests.post(url, data=data, headers=UA, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 + 3 * i)


def epmc_search(query, page_size=1000, max_records=None, fields='lite'):
    """Return (hitCount, records) using cursorMark paging (POST, so long queries work)."""
    out, cursor, hit = [], '*', None
    while True:
        d = _post(f'{EPMC}/searchPOST', {'query': query, 'format': 'json', 'pageSize': page_size,
                                         'cursorMark': cursor, 'resultType': fields})
        hit = d['hitCount']
        res = d.get('resultList', {}).get('result', [])
        out += res
        nxt = d.get('nextCursorMark')
        if not nxt or nxt == cursor or not res or (max_records and len(out) >= max_records) or len(out) >= hit:
            break
        cursor = nxt
    return hit, out


def pubmed_count(term):
    d = _post(f'{EUTILS}/esearch.fcgi', {'db': 'pubmed', 'term': term, 'retmode': 'json', 'retmax': 0})
    return int(d['esearchresult']['count'])


def fulltext_xml(pmcid):
    """Download OA JATS XML from Europe PMC; returns path or None."""
    folder = PAPERS / pmcid
    path = folder / 'fulltext.xml'
    if path.exists():
        return path
    b, url = None, None
    for url in (f'{EUTILS}/efetch.fcgi?db=pmc&id={pmcid.replace("PMC", "")}&retmode=xml',
                f'{EPMC}/{pmcid}/fullTextXML'):
        try:
            b = get(url, timeout=60, tries=2)
        except Exception:
            b = None
        if b and b'<article' in b[:5000] and b'<body' in b:
            break
        b = None
    if b is None:
        return None
    folder.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b)
    (folder / 'retrieval.json').write_text(json.dumps({
        'pmcid': pmcid, 'url': url, 'bytes': len(b),
        'sha256': hashlib.sha256(b).hexdigest(), 'retrieved': time.strftime('%Y-%m-%d')}, indent=1))
    return path


def clean(s):
    return re.sub(r'\s+', ' ', s).strip()


def elements(path):
    """Paragraphs, captions and table rows with stable evidence IDs (E0001...)."""
    root = ET.parse(path).getroot()
    rows = []
    for ab in root.findall('.//front//abstract'):
        rows.append(('Abstract', clean(' '.join(ab.itertext()))))

    def walk(node, section):
        for ch in node:
            tag = ch.tag.split('}')[-1]
            if tag == 'sec':
                t = ch.find('title')
                walk(ch, clean(' '.join(t.itertext())) if t is not None else section)
            elif tag == 'p':
                rows.append((section, clean(' '.join(ch.itertext()))))
            elif tag in ('fig', 'table-wrap'):
                cap = ch.find('caption')
                lab = ch.find('label')
                lab = clean(' '.join(lab.itertext())) if lab is not None else tag
                if cap is not None:
                    rows.append((section, f'[{lab} caption] ' + clean(' '.join(cap.itertext()))))
                for tr in ch.iter():
                    if tr.tag.split('}')[-1] == 'tr':
                        cells = [clean(' '.join(c.itertext())) for c in tr]
                        rows.append((section, f'[{lab} row] ' + ' | '.join(cells)))
                for fn in ch.iter():
                    if fn.tag.split('}')[-1] == 'table-wrap-foot':
                        rows.append((section, f'[{lab} footnote] ' + clean(' '.join(fn.itertext()))))
            elif tag in ('list', 'disp-quote', 'boxed-text'):
                walk(ch, section)
            elif tag == 'list-item':
                walk(ch, section)
    body = root.find('.//body')
    if body is not None:
        walk(body, 'Body')
    for sm in root.iter():
        if sm.tag.split('}')[-1] == 'supplementary-material':
            rows.append(('Supplementary', '[supplement] ' + clean(' '.join(sm.itertext()))
                         + ' ' + ' '.join(v for k, v in sm.attrib.items() if k.endswith('href'))))
    seen, out = set(), []
    for sec, txt in rows:
        if txt and txt not in seen:
            seen.add(txt)
            out.append({'evidence_id': f'E{len(out)+1:04}', 'section': sec, 'text': txt})
    return out


def meta(path):
    root = ET.parse(path).getroot()
    g = lambda x: clean(' '.join(root.find(x).itertext())) if root.find(x) is not None else ''
    return {'title': g('.//front//article-title'), 'journal': g('.//front//journal-title'),
            'year': g('.//front//pub-date/year'),
            'doi': g(".//front//article-id[@pub-id-type='doi']"),
            'pmid': g(".//front//article-id[@pub-id-type='pmid']")}
