"""Print evidence elements: show_el.py PMCID E0001 E0002 ... (optional max chars via MAX=n env)."""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import epmc
els = {e['evidence_id']: e for e in epmc.elements(epmc.PAPERS / sys.argv[1] / 'fulltext.xml')}
for i in sys.argv[2:]:
    e = els.get(i); print(i, f"[{e['section'][:30]}]", e['text'][:int(os.environ.get('MAX', 1200))], '\n')
