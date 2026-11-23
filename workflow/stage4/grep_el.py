"""Search a paper's evidence elements: grep_el.py PMCID "<regex>" -> matching IDs with ~200-char windows."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
rx = re.compile(sys.argv[2], re.I)
for e in epmc.elements(epmc.PAPERS / sys.argv[1] / 'fulltext.xml'):
    m = rx.search(e['text'])
    if m:
        a = max(0, m.start() - 100)
        print(e['evidence_id'], f"[{e['section'][:25]}]", e['text'][a:m.end() + 120].replace('\n', ' '))
