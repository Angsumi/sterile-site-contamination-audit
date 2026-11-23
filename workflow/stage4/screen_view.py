"""Print compact screening views for the AI agent. mode=titles: suggested-exclusion records (title only);
mode=abstracts: records needing abstract reading. Records already decided (carried over or logged) are skipped."""
import csv, json, sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
S = epmc.PAPERS / '_screening'
A = json.loads((S / 'abstracts.json').read_text()); P = json.loads((S / 'presort.json').read_text())
R = [r for r in csv.DictReader(open(epmc.ROOT / 'data' / 'records_merged.csv')) if r['pmcid']]
done, needs = set(), set()
for f in (epmc.ROOT / 'screening' / 'agent_decisions').glob('*.tsv'):
    for line in open(f):
        if line.strip() and not line.startswith('#'):
            (needs if line.split('\t')[1] == 'needs_abstract' else done).add(line.split('\t')[0])
code = {'review_or_nonprimary': 'R', 'animal_or_environment_title': 'A', 'mucosal_or_high_biomass_title': 'M',
        'diagnostic_or_infection_title': 'D', 'no_sequencing_terms': 'N', 'no_target_site_terms': 'T'}
mode, start, n = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
if mode == 'titles':
    rows = sorted([r for r in R if P[r['pmcid']] and r['pmcid'] not in done and r['pmcid'] not in needs], key=lambda r: (P[r['pmcid']][0], r['title']))
else:
    rows = [r for r in R if r['pmcid'] not in done]
print('remaining', len(rows))
for r in rows[start:start + n]:
    t = re.sub(r'&lt;/?i&gt;|<[^>]+>', '', r['title'])
    if mode == 'titles':
        print(f"{r['pmcid']}|{''.join(code[x] for x in P[r['pmcid']])}|{t[:150]}")
    else:
        ab = A.get(r['pmcid'], {}).get('abstract', '')
        ab = re.sub(r'<[^>]+>', '', ab)
        print(f"## {r['pmcid']} {r['pubYear']} [{r['blocks_v1'] or '-'}|{r['blocks_v2'] or '-'}] {t[:200]}\n{ab[:int(sys.argv[4]) if len(sys.argv)>4 else 900]}")
