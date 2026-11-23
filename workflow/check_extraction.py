"""Automatic source checks and contaminant matching for C6 extractions.

Reads pilot/extractions/<PMCID>.json. For every quoted field and every genus, checks that the
text appears in the cited evidence element of the downloaded full text (case- and
whitespace-normalised). Then matches genera to the fixed lists (script, not agent).

Writes pilot/pilot_results.csv (one row per paper), pilot/pilot_genera.csv (one row per genus)
and pilot/pilot_summary.json.
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import epmc
from build_contaminant_list import SYNONYMS

PILOT = epmc.ROOT / 'pilot'
norm = lambda s: re.sub(r'\s+', ' ', s).strip().lower()


def load_lists():
    rows = list(csv.DictReader(open(epmc.ROOT / 'reference' / 'contaminant_genera.csv')))
    return {k: {r['genus'] for r in rows if r[k] == '1'} for k in ('list_primary_environmental', 'list_strict', 'list_broad')}


def check(x, els):
    fails, n = [], 0
    for field in ('controls', 'decontamination', 'method', 'biomass_qpcr'):
        for ev in x.get(field, {}).get('evidence', []):
            n += 1
            e = els.get(ev['id'])
            if e is None or norm(ev['quote']) not in norm(e['text']):
                fails.append(f"{field}:{ev['id']}")
    for g in x.get('genera', []):
        n += 1
        e = els.get(g['evidence_id'])
        if e is None or g['name'].lower() not in e['text'].lower():
            fails.append(f"genus:{g['name']}:{g['evidence_id']}")
    return n, fails


def main():
    lists = load_lists()
    rows, grows = [], []
    for f in sorted((PILOT / 'extractions').glob('PMC*.json')):
        x = json.loads(f.read_text())
        els = {e['evidence_id']: e for e in epmc.elements(epmc.PAPERS / x['pmcid'] / 'fulltext.xml')}
        n, fails = check(x, els)
        names = sorted({SYNONYMS.get(g['name'], g['name']) for g in x.get('genera', []) if not g.get('flagged_contaminant')})
        flagged = sorted({SYNONYMS.get(g['name'], g['name']) for g in x.get('genera', []) if g.get('flagged_contaminant')})
        top5 = [SYNONYMS.get(g, g) for g in x.get('top5', [])]
        row = {'pmcid': x['pmcid'], 'block': x['block'], 'tissue_category': x['tissue_category'], 'year': x.get('year', ''),
               'eligible_fulltext': x['eligible_fulltext'], 'method': x.get('method', {}).get('value', ''),
               'controls': x.get('controls', {}).get('value', ''), 'decontamination': x.get('decontamination', {}).get('value', ''),
               'biomass_qpcr': x.get('biomass_qpcr', {}).get('value', ''), 'figures_only': x.get('genera_in_figures_only', ''),
               'n_genera': len(names), 'usable_list': int(len(names) >= 3), 'n_flagged_removed': len(flagged),
               'checks': n, 'check_fails': len(fails), 'fail_detail': ';'.join(fails)}
        for k, s in lists.items():
            hit = [g for g in names if g in s]
            row[f'n_{k}'] = len(hit)
            row[f'share_{k}'] = round(len(hit) / len(names), 3) if names else ''
        row['top5_primary_hit'] = int(any(g in lists['list_primary_environmental'] for g in top5)) if top5 else ''
        row['primary_hits'] = ';'.join(g for g in names if g in lists['list_primary_environmental'])
        rows.append(row)
        for g in names + flagged:
            grows.append({'pmcid': x['pmcid'], 'tissue_category': x['tissue_category'], 'genus': g, 'flagged_removed': int(g in flagged),
                          **{k: int(g in s) for k, s in lists.items()}})
    with open(PILOT / 'pilot_results.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(PILOT / 'pilot_genera.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(grows[0])); w.writeheader(); w.writerows(grows)
    el = [r for r in rows if r['eligible_fulltext']]
    summ = {'papers': len(rows), 'eligible_fulltext': len(el), 'usable_list': sum(r['usable_list'] for r in el),
            'controls_classified': sum(r['controls'] in ('none_mentioned', 'included_not_sequenced', 'sequenced') for r in el),
            'checks': sum(r['checks'] for r in rows), 'check_fails': sum(r['check_fails'] for r in rows)}
    summ['usable_rate'] = round(summ['usable_list'] / max(1, len(el)), 3)
    summ['controls_rate'] = round(summ['controls_classified'] / max(1, len(el)), 3)
    summ['check_pass_rate'] = round(1 - summ['check_fails'] / max(1, summ['checks']), 4)
    (PILOT / 'pilot_summary.json').write_text(json.dumps(summ, indent=1))
    print(json.dumps(summ, indent=1))
    for r in rows:
        print(r['pmcid'], r['tissue_category'], r['controls'], r['decontamination'], r['n_genera'], r['share_list_primary_environmental'], r['fail_detail'])


if __name__ == '__main__':
    main()
