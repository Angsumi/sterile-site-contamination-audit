"""Pilot descriptives and go/no-go projection (protocol section 9). Writes pilot/pilot_projection.json."""
import csv, json, statistics as st, collections
from pathlib import Path
R = Path(__file__).resolve().parents[1]
rows = list(csv.DictReader(open(R / 'pilot' / 'pilot_results.csv')))
el = [r for r in rows if r['eligible_fulltext'] == 'True']
us = [r for r in el if r['usable_list'] == '1']
log = json.load(open(R / 'search' / 'search_log_v2.json'))['tissues']
scr = list(csv.DictReader(open(R / 'screening' / 'screening_log_v2.csv')))
out = {'pilot_papers_read': len(rows), 'eligible_fulltext': len(el), 'usable': len(us),
       'fulltext_eligibility_rate': round(len(el) / len(rows), 3), 'usable_rate': round(len(us) / len(el), 3)}
proj = {}
for b, v in log.items():
    inc = sum(1 for s in scr if s['block'] == b and s['decision'] == 'include')
    n = v['epmc_oa_records_kept']
    proj[b] = {'oa_records': n, 'screen_include_rate': round(inc / 30, 3),
               'projected_usable': round(n * inc / 30 * out['fulltext_eligibility_rate'] * out['usable_rate'], 1)}
out['projection_by_block'] = proj
out['projected_usable_total'] = round(sum(p['projected_usable'] for p in proj.values()), 1)
out['blocks_with_15_plus'] = [b for b, p in proj.items() if p['projected_usable'] >= 15]
out['controls'] = dict(collections.Counter(r['controls'] for r in el))
out['decontamination'] = dict(collections.Counter(r['decontamination'] for r in el))
out['method'] = dict(collections.Counter(r['method'] for r in el))
out['figures_only_or_partial'] = sum(r['figures_only'] in ('yes', 'partial') for r in el)
for k in ('list_primary_environmental', 'list_strict', 'list_broad'):
    s = [float(r[f'share_{k}']) for r in us]
    out[f'share_{k}'] = {'median': round(st.median(s), 3), 'mean': round(st.mean(s), 3), 'min': min(s), 'max': max(s)}
by = collections.defaultdict(list)
for r in us:
    by[r['controls']].append(float(r['share_list_primary_environmental']))
out['primary_share_by_controls'] = {k: {'n': len(v), 'median': round(st.median(v), 3)} for k, v in by.items()}
out['studies_with_any_primary_hit'] = sum(int(r['n_list_primary_environmental']) > 0 for r in us)
gen = collections.Counter(g for r in us for g in r['primary_hits'].split(';') if g)
out['most_common_primary_genera'] = gen.most_common(10)
(R / 'pilot' / 'pilot_projection.json').write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
