"""Amendment 0.4 rule 5: NCBI Taxonomy genus dictionary (new_taxdump downloaded 2026-11-23,
SHA-256 61710d80edf22ae2b18af9aba2b80f92c6258e91fd115432ffcb690350c090ea, local copy in
data_local/.../taxonomy). Writes reference/ncbi_genera.tsv: name, name_class (scientific/synonym/...),
taxid, accepted scientific name, domain. Only Bacteria and Archaea genera are kept."""
import csv, sys
from pathlib import Path
T = Path(__file__).resolve().parents[2] / 'papers' / '..' / '..' / '..' / '..' / 'data_local' / 'sterile-site-contamination-audit' / 'taxonomy'
T = Path('/home/angsuman/extra_spac/META/data_local/sterile-site-contamination-audit/taxonomy') if not T.exists() else T
genus = set()
for line in open(T / 'nodes.dmp'):
    f = line.split('\t|\t')
    if f[2] == 'genus':
        genus.add(f[0])
dom = {}
for line in open(T / 'rankedlineage.dmp'):
    f = [x.strip() for x in line.rstrip('\t|\n').split('\t|\t')]
    if f[0] in genus:
        dom[f[0]] = f[-1] or f[-2]
sci, rows = {}, []
for line in open(T / 'names.dmp'):
    f = [x.strip() for x in line.rstrip('\t|\n').split('\t|\t')]
    if f[0] in genus and f[3] in ('scientific name', 'synonym', 'equivalent name', 'includes'):
        if f[3] == 'scientific name': sci[f[0]] = f[1]
        rows.append((f[1], f[3], f[0]))
out = Path(__file__).resolve().parents[2] / 'reference' / 'ncbi_genera.tsv'
with open(out, 'w', newline='') as fh:
    w = csv.writer(fh, delimiter='\t'); w.writerow(['name', 'name_class', 'taxid', 'scientific_name', 'domain'])
    for n, c, t in sorted(rows):
        if ' ' in n or not n[:1].isupper() or dom.get(t, '') not in ('Bacteria', 'Archaea'): continue
        w.writerow([n, c, t, sci.get(t, ''), dom.get(t, '')])
import collections
print(collections.Counter(dom.values()).most_common(6), len(rows))
