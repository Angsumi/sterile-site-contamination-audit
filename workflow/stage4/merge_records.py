"""Stage 4 step 1: merge and de-duplicate the v1 and v2 Europe PMC OA record lists
(feasibility runs of 22 Nov and the re-runs). Key = PMCID; then DOI and PMID duplicates
across different PMCIDs are flagged. Writes data/records_merged.csv and data/merge_counts.json."""
import csv, json, sys, glob
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc

S = epmc.ROOT / 'search'
srcs = [('v1_2026-11-22', S / 'epmc_oa_records.csv'), ('v2_2026-11-22', S / 'epmc_oa_records_v2.csv')]
for d in sorted(glob.glob(str(S / 'rerun_*'))):
    tag = Path(d).name.replace('rerun_', '')
    srcs += [(f'v1_{tag}', Path(d) / 'v1' / 'epmc_oa_records.csv'), (f'v2_{tag}', Path(d) / 'v2' / 'epmc_oa_records_v2.csv')]
merged, counts = {}, {}
for tag, p in srcs:
    rows = list(csv.DictReader(open(p)))
    counts[tag] = len(rows)
    for r in rows:
        k = r['pmcid'] or ('NOPMC_' + (r['pmid'] or r['doi']))
        m = merged.setdefault(k, {**{f: r[f] for f in ('pmcid', 'pmid', 'doi', 'pubYear', 'journalTitle', 'title', 'authorString')},
                                  'blocks_v1': set(), 'blocks_v2': set(), 'sources': set()})
        m['blocks_' + tag[:2]].update(x for x in r['tissues'].split(';') if x)
        m['sources'].add(tag)
# duplicates under different PMCIDs (same DOI or PMID)
seen, dup = {}, 0
for k, m in merged.items():
    m['duplicate_of'] = ''
    for key in (('doi', m['doi'].lower()), ('pmid', m['pmid'])):
        if key[1]:
            if key in seen:
                m['duplicate_of'] = seen[key]; dup += 1; break
            seen[key] = k
rows = []
for k, m in sorted(merged.items()):
    rows.append({**{f: m[f] for f in ('pmcid', 'pmid', 'doi', 'pubYear', 'journalTitle', 'title', 'authorString')},
                 'blocks_v1': ';'.join(sorted(m['blocks_v1'])), 'blocks_v2': ';'.join(sorted(m['blocks_v2'])),
                 'in_v1': int(any(s.startswith('v1') for s in m['sources'])), 'in_v2': int(any(s.startswith('v2') for s in m['sources'])),
                 'sources': ';'.join(sorted(m['sources'])), 'duplicate_of': m['duplicate_of']})
with open(epmc.ROOT / 'data' / 'records_merged.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
out = {'source_counts': counts, 'unique_keys': len(rows), 'no_pmcid': sum(1 for r in rows if not r['pmcid']),
       'doi_or_pmid_duplicates': dup, 'unique_after_dedup': sum(1 for r in rows if not r['duplicate_of']),
       'in_v1_only': sum(r['in_v1'] and not r['in_v2'] for r in rows), 'in_v2_only': sum(r['in_v2'] and not r['in_v1'] for r in rows),
       'in_both': sum(r['in_v1'] and r['in_v2'] for r in rows),
       'only_in_rerun': sum(1 for r in rows if all('2026-11-22' not in s for s in r['sources'].split(';')))}
(epmc.ROOT / 'data' / 'merge_counts.json').write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
