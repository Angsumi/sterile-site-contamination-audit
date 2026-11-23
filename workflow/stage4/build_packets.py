"""Amendment 0.5: per-paper reading packets for the extraction agents (local only, they contain text
excerpts): papers/<PMCID>/packet.md. Packets are reading aids, not decisions.
Contents: metadata; abstract; every paragraph/caption/table row mentioning controls, blanks, extraction,
sequencing method, decontamination or biomass (with evidence IDs); every NCBI Bacteria/Archaea genus
name found in the paper with the evidence IDs and sections where it occurs (Results/tables/captions
first); figure/table captions; supplement list (markitdown files)."""
import csv, json, re, sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
ROOT = epmc.ROOT
G = {}
for r in csv.DictReader(open(ROOT / 'reference' / 'ncbi_genera.tsv'), delimiter='\t'):
    G.setdefault(r['name'], r['scientific_name'])
CTRL = re.compile(r'negative control|blank|no[- ]template|\bNTC|contamina|decontam|SourceTracker|microDecon|SCRuB|kitome|reagent|'
                  r'extraction kit|DNA was extracted|DNA extraction|extracted using|qPCR|quantitative PCR|biomass|mock community|positive control|'
                  r'16S rRNA|16S rDNA|V3|V4|shotgun|metagenom|metatranscriptom|RNA-seq|RNA sequencing|whole[- ]genome|whole[- ]exome|TCGA|'
                  r'Kraken|MetaPhlAn|PathSeq|QIIME|DADA2|SILVA|Greengenes|2bRAD|Illumina|MiSeq|NovaSeq|HiSeq|nanopore|PacBio|'
                  r'removed|filtered|prevalence|relative abundance (below|less)', re.I)
SKIP_SEC = re.compile(r'^(introduction|background)$', re.I)
TOK = re.compile(r'(?:g__|\b)([A-Z][a-z]{2,}(?:[-_][A-Z][a-z]+)*)\b')

def top_sections(path):
    """Map element text -> top-level body section title (same walk as epmc.elements)."""
    import xml.etree.ElementTree as ET
    root = ET.parse(path).getroot(); out = {}
    def walk(node, top):
        for ch in node:
            tag = ch.tag.split('}')[-1]
            if tag == 'sec':
                t = ch.find('title')
                walk(ch, top or (epmc.clean(' '.join(t.itertext())) if t is not None else ''))
            elif tag in ('p', 'fig', 'table-wrap', 'list', 'list-item', 'disp-quote', 'boxed-text'):
                for sub in ch.iter():
                    st = sub.tag.split('}')[-1]
                    if st in ('p', 'caption', 'tr', 'table-wrap-foot'):
                        out.setdefault(epmc.clean(' '.join(sub.itertext())), top)
                if tag in ('list', 'list-item', 'disp-quote', 'boxed-text'): walk(ch, top)
    b = root.find('.//body')
    if b is not None: walk(b, '')
    return out

TOP = {}

def sec_tag(e):
    t = e['text']
    if t.startswith('[') and ' row]' in t[:40]: return 'TABLE'
    if t.startswith('[') and 'caption]' in t[:40]: return 'CAPTION'
    if t.startswith('[supplement]'): return 'SUPPL-LIST'
    body = t.split('] ', 1)[-1] if t.startswith('[') else t
    s = (TOP.get(body) or TOP.get(t) or '').lower() + ' ' + e['section'].lower()
    for k in ('abstract', 'result', 'discussion', 'method', 'material', 'introduction', 'background', 'conclusion'):
        if k in s: return k.upper()
    return e['section'][:25]

def build(p):
    path = epmc.PAPERS / p / 'fulltext.xml'
    els = epmc.elements(path); m = epmc.meta(path)
    TOP.clear(); TOP.update(top_sections(path))
    out = [f"# PACKET {p}\n", f"title: {m['title']}\njournal: {m['journal']} | year: {m['year']} | doi: {m['doi']} | n_elements: {len(els)}\n"]
    ab = [e for e in els if e['section'] == 'Abstract']
    out.append('## ABSTRACT')
    out += [f"{e['evidence_id']}: {e['text'][:2500]}" for e in ab]
    out.append('\n## METHODS / CONTROLS / DECONTAMINATION PASSAGES (keyword windows; run `python workflow/show_el.py <PMCID> <ID>` for the full element before quoting)')
    for e in els:
        if e['section'] != 'Abstract' and CTRL.search(e['text']) and not (e['text'].startswith('[') and ' row]' in e['text'][:40]):
            t = e['text']; segs, last = [], -1
            for mm in CTRL.finditer(t):
                h = mm.start()
                if h < last: continue
                a = max(0, h - 160); segs.append(t[a:h + 220]); last = h + 220
            out.append(f"{e['evidence_id']} [{sec_tag(e)}|{e['section'][:30]}]: " + ' … '.join(segs)[:900])
    occ = defaultdict(list)
    for e in els:
        for g in set(TOK.findall(e['text'])):
            base = g.replace('_', '-').split('-')[0]
            if g in G or base in G:
                occ[g].append(e)
    out.append('\n## GENUS-NAME CANDIDATES (NCBI Bacteria/Archaea names found anywhere; sections shown; you decide which are genera DETECTED IN TARGET SAMPLES)')
    order = sorted(occ, key=lambda g: (-sum(sec_tag(e) in ('RESULT', 'TABLE', 'CAPTION') for e in occ[g]), g))
    for g in order:
        es = occ[g]
        tags = defaultdict(list)
        for e in es: tags[sec_tag(e)].append(e['evidence_id'])
        first = next((e for e in es if sec_tag(e) in ('RESULT', 'TABLE', 'CAPTION')), es[0])
        i = first['text'].find(g)
        ctx = first['text'][max(0, i - 90): i + 70].replace('\n', ' ')
        out.append(f"- {g} " + ' '.join(f"{k}:{','.join(v[:6])}{'…' if len(v) > 6 else ''}" for k, v in tags.items()) + f" | ctx[{first['evidence_id']}]: …{ctx}…")
    out.append('\n## FIGURE AND TABLE CAPTIONS')
    out += [f"{e['evidence_id']}: {e['text'][:400]}" for e in els if e['text'].startswith('[') and 'caption]' in e['text'][:40]]
    sd = epmc.PAPERS / p / 'supp_md'
    out.append('\n## SUPPLEMENTS converted with markitdown (open papers/<PMCID>/supp_md/S<k>.md only if the main text gives < 3 genera)')
    if sd.exists():
        for f in sorted(sd.glob('S*.md')):
            n = sum(1 for _ in open(f, errors='ignore'))
            out.append(f"- {f.name}: {n} lines")
    else:
        out.append('- none available')
    (epmc.PAPERS / p / 'packet.md').write_text('\n'.join(out))
    return len(els), len(occ), sum(len(x) for x in out)

if __name__ == '__main__':
    ids = sys.argv[1:] or [r['pmcid'] for r in csv.DictReader(open(ROOT / 'data' / 'fulltext_download_log.csv')) if r['fulltext_ok'] == '1']
    stats = []
    for p in ids:
        stats.append((p, *build(p)))
    chars = sorted(s[3] for s in stats)
    print(len(stats), 'packets; median chars', chars[len(chars) // 2], 'p90', chars[int(len(chars) * .9)], 'max', chars[-1])
