"""Pilot reading aids: download OA XML for the pilot papers and build per-paper packets.

A packet holds (a) passages about methods, controls and decontamination, and (b) every
capitalised italic word in the paper with its evidence IDs (candidate genus names).
The agent decides which candidates are genera reported as detected in target samples.
Packets are reading aids, not decisions. Output: pilot/packets/<PMCID>.json.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import epmc

PILOT = epmc.ROOT / 'pilot'
CTRL = re.compile(r'negative control|blank|no[- ]template|NTC|contamina|decontam|SourceTracker|microDecon|SCRuB|kitome|'
                  r'reagent|extraction kit|DNA was extracted|DNA extraction|qPCR|biomass|mock community|positive control|'
                  r'16S rRNA gene|V3|V4|shotgun|metagenomic sequencing|RNA-seq|whole[- ]genome|Kraken|MetaPhlAn|PathSeq|QIIME|DADA2', re.I)


def italic_index(path):
    """Map evidence text -> italic capitalised tokens, using the same element order as epmc.elements."""
    root = ET.parse(path).getroot()
    out = {}
    for node in root.iter():
        tag = node.tag.split('}')[-1]
        if tag in ('p', 'caption', 'tr', 'abstract', 'table-wrap-foot', 'supplementary-material'):
            txt = epmc.clean(' '.join(node.itertext()))
            its = set()
            for it in node.iter():
                if it.tag.split('}')[-1] == 'italic':
                    w = epmc.clean(' '.join(it.itertext()))
                    m = re.match(r'(?:Candidatus\s+)?([A-Z][a-z]{2,}(?:[-_][A-Z][a-z]+)?)\b', w)
                    if m:
                        its.add(m.group(1))
            if its:
                out.setdefault(txt, set()).update(its)
    return out


def packet(pmcid):
    path = epmc.fulltext_xml(pmcid)
    if path is None:
        return None
    els = epmc.elements(path)
    ital = italic_index(path)
    cands = {}
    for e in els:
        body = e['text']
        for txt, its in ital.items():
            if txt and (txt in body or body.endswith(txt) or txt.endswith(body.split('] ', 1)[-1])):
                for g in its:
                    if g in body:
                        cands.setdefault(g, []).append(e['evidence_id'])
    # non-italic table rows often hold genus names (e.g. g__Ralstonia, Ralstonia)
    for e in els:
        if '] ' in e['text'][:30] and ('row' in e['text'][:30]):
            for g in re.findall(r'(?:g__)?\b([A-Z][a-z]{3,}(?:[-_][A-Z][a-z]+)?)\b', e['text']):
                if g in cands and e['evidence_id'] not in cands[g]:
                    cands[g].append(e['evidence_id'])
    ctrl = [e for e in els if CTRL.search(e['text'])]
    return {'pmcid': pmcid, 'meta': epmc.meta(path), 'n_elements': len(els),
            'control_method_passages': ctrl, 'italic_candidates': {g: sorted(set(v)) for g, v in sorted(cands.items())}}


if __name__ == '__main__':
    (PILOT / 'packets').mkdir(parents=True, exist_ok=True)
    for pmcid in sys.argv[1:]:
        p = packet(pmcid)
        if p is None:
            print(pmcid, 'NO FULL TEXT', flush=True)
            continue
        (PILOT / 'packets' / f'{pmcid}.json').write_text(json.dumps(p, ensure_ascii=False, indent=1))
        print(pmcid, p['n_elements'], 'elements', len(p['control_method_passages']), 'ctrl passages',
              len(p['italic_candidates']), 'candidates', flush=True)
