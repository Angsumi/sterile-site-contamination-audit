"""Log the agent's decisions for one title batch exactly as shown by `screen_view.py titles 0 N`.
Every shown record is logged as exclude with the agent-confirmed reason for its first suggestion,
except records listed after N: 'PMCID' (= needs abstract) or 'PMCID=decision:category:reason'.
Usage: log_titles.py <batch_name> <N> [overrides...]"""
import csv, json, sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
S = epmc.PAPERS / '_screening'; D = epmc.ROOT / 'screening' / 'agent_decisions'
P = json.loads((S / 'presort.json').read_text())
R = [r for r in csv.DictReader(open(epmc.ROOT / 'data' / 'records_merged.csv')) if r['pmcid']]
done, needs = set(), set()
for f in D.glob('*.tsv'):
    for line in open(f):
        if line.strip() and not line.startswith('#'):
            (needs if line.split('\t')[1] == 'needs_abstract' else done).add(line.split('\t')[0])
REASON = {'review_or_nonprimary': 'not primary research (review, editorial, protocol, meta-analysis)',
          'animal_or_environment_title': 'animal, environmental or other non-human study',
          'mucosal_or_high_biomass_title': 'mucosal or high-biomass site only (gut, stool, oral, vaginal, airway, mucosal tumour)',
          'diagnostic_or_infection_title': 'diagnostic sequencing or infection study (C1 scope) or not microbiome profiling',
          'no_sequencing_terms': 'no sequencing-based community profiling',
          'no_target_site_terms': 'no target sterile site'}
name, n = sys.argv[1], int(sys.argv[2])
over = {}
for o in sys.argv[3:]:
    if '=' in o:
        k, v = o.split('=', 1); d, c, why = v.split(':', 2); over[k] = (d, c, why)
    else:
        over[o] = ('needs_abstract', '', 'title does not settle it')
rows = sorted([r for r in R if P[r['pmcid']] and r['pmcid'] not in done and r['pmcid'] not in needs], key=lambda r: (P[r['pmcid']][0], r['title']))[:n]
bad = set(over) - {r['pmcid'] for r in rows}
assert not bad, f'overrides not in batch: {bad}'
with open(D / f'{name}.tsv', 'w') as f:
    f.write('# pmcid\tdecision\ttissue_category\treason\tsource\n')
    for r in rows:
        d, c, why = over.get(r['pmcid'], ('exclude', '', REASON[P[r['pmcid']][0]]))
        f.write(f"{r['pmcid']}\t{d}\t{c}\t{why}\tAI agent (Claude Opus 5.5), title, 2026-11-23\n")
print(name, len(rows), 'logged;', sum(1 for v in over.values() if v[0] == 'needs_abstract'), 'to abstract')
