"""Log the agent's title+abstract decisions. stdin lines: 'PMCID code [free-text reason]'.
code: i<cat> include, u<cat> unclear (to full text), x<reason> exclude.
cat: t tumour, p placenta_fetal, b blood, c brain_csf, o other_sterile.
reason: A animal/environmental, R not primary research, M mucosal/high-biomass site only, D diagnostic or infection (C1 scope),
N no sequencing-based community profiling (culture, qPCR, FISH, metabolomics, single organism), T not a target sterile site
(e.g. gut/oral microbiome related to a disease), C case report, P in vitro / cell line, E method or database paper without target-site profiling.
Usage: log_abstracts.py <batch_name> < decisions.txt"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
CAT = dict(t='tumour', p='placenta_fetal', b='blood', c='brain_csf', o='other_sterile')
WHY = dict(A='animal, environmental or other non-human study', R='not primary research (review, editorial, protocol, meta-analysis)',
           M='mucosal or high-biomass site only (gut, stool, oral, vaginal, airway, mucosal tumour)',
           D='diagnostic sequencing or infection study (C1 scope)', N='no sequencing-based community profiling (culture, PCR/qPCR, FISH, metabolomics or single organism)',
           T='no target sterile-site samples profiled (e.g. gut or oral microbiome related to a disease)', C='case report',
           P='in vitro or cell-line study', E='method, database or simulation study without target-site profiling')
out = []
for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    parts = line.split(None, 2)
    p, code = parts[0], parts[1]
    extra = parts[2] if len(parts) > 2 else ''
    if code[0] in 'iu':
        d, c, why = ('include' if code[0] == 'i' else 'unclear'), CAT[code[1]], extra or ('meets section 3 on title/abstract' if code[0] == 'i' else 'needs full text')
    else:
        d, c, why = 'exclude', '', WHY[code[1]] + (f'; {extra}' if extra else '')
    out.append(f"{p}\t{d}\t{c}\t{why}\tAI agent (Claude Opus 5.5), title+abstract, 2026-11-23\n")
D = epmc.ROOT / 'screening' / 'agent_decisions'
f = D / f'{sys.argv[1]}.tsv'
assert not f.exists(), f
f.write_text('# pmcid\tdecision\ttissue_category\treason\tsource\n' + ''.join(out))
print(sys.argv[1], len(out))
