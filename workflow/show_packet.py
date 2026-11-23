"""Compact view of a pilot packet: control/method keyword windows and genus-candidate contexts."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import epmc
ROOT = epmc.ROOT
K = re.compile(r'negative control|blank|no[- ]template|NTC|contamina|decontam|SourceTracker|microDecon|SCRuB|kitome|qPCR|biomass|mock|16S rRNA gene|V3|V4|shotgun|RNA-seq|whole[- ]genome|Kraken|PathSeq', re.I)
for pmcid in sys.argv[1:]:
    p = json.loads((ROOT / 'pilot' / 'packets' / f'{pmcid}.json').read_text())
    els = {e['evidence_id']: e for e in epmc.elements(epmc.PAPERS / pmcid / 'fulltext.xml')}
    m = p['meta']; print(f"##### {pmcid} | {m['year']} | {m['journal'][:40]} | {m['title'][:110]}")
    for e in p['control_method_passages']:
        t = e['text']; hits = [mm.start() for mm in K.finditer(t)]
        if not hits: continue
        segs, last = [], -1
        for h in hits:
            if h < last: continue
            s = max(0, h - 120); segs.append(t[s:h + 180]); last = h + 180
        print(f"  {e['evidence_id']} [{e['section'][:20]}] " + ' ... '.join(segs)[:900])
    print('  GENUS CANDIDATES:')
    for g, ids in p['italic_candidates'].items():
        t = els[ids[0]]['text']; i = t.find(g)
        print(f"   {g} {chr(44).join(ids[:4])}: …{t[max(0,i-50):i+30]}…")
