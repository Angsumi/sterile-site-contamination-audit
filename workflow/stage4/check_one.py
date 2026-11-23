"""Automatic checks for one or more extraction files (extraction/json/<PMCID>.json); used by the
extraction agents on their own output and by the coordinator. Checks: schema/allowed values; every
quote occurs in its cited evidence element (whitespace/case-normalised); every genus name occurs in its
cited element; supplement locators S<k>:L<n> resolve to papers/<PMCID>/supp_md/S<k>.md line n;
genus names are NCBI Bacteria/Archaea genera (after the fixed synonym map; composite names use the
first genus). Usage: check_one.py PMCID [PMCID ...]  -> prints OK or problems; exit 1 if any FAIL."""
import csv, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc
from build_contaminant_list import SYNONYMS
ROOT = epmc.ROOT
norm = lambda s: re.sub(r'\s+', ' ', s).strip().lower()
NCBI = {}
for r in csv.DictReader(open(ROOT / 'reference' / 'ncbi_genera.tsv'), delimiter='\t'):
    NCBI.setdefault(r['name'], (r['scientific_name'], r['domain']))
ALLOWED = {
    'tissue_category': {'tumour', 'placenta_fetal', 'blood', 'brain_csf', 'other_sterile'},
    'method': {'16S', 'shotgun', 'metatranscriptomic', 'host_seq_mining', '2bRAD-M', '16S+shotgun', 'other'},
    'controls': {'sequenced', 'included_not_sequenced', 'none_mentioned'},
    'decontamination': {'none', 'removed_control_taxa', 'tool', 'literature_list', 'abundance_filter_only', 'unclear'},
    'biomass_qpcr': {'yes', 'no'},
    'data_source': {'own_samples', 'public_reuse'},
    'list_type': {'full_profile', 'differential_only', 'mixed', ''},
    'figures_only': {'no', 'partial', 'yes', ''},
    'authors_conclusion': {'claimed', 'not_claimed', 'unclear', ''},
}

def canon(name):
    n = SYNONYMS.get(name, name)
    first = re.split(r'[-_ ]', n)[0]
    n = SYNONYMS.get(n, n) if n in NCBI else SYNONYMS.get(first, first)
    return n

def element_text(p, els, eid):
    m = re.match(r'S(\d+):L(\d+)$', eid)
    if m:
        f = epmc.PAPERS / p / 'supp_md' / f'S{m.group(1)}.md'
        if not f.exists(): return None
        lines = f.read_text(errors='ignore').split('\n')
        k = int(m.group(2))
        return lines[k - 1] if 0 < k <= len(lines) else None
    e = els.get(eid)
    return e['text'] if e else None

def check(p):
    probs = []
    f = ROOT / 'extraction' / 'json' / f'{p}.json'
    if not f.exists(): return [f'FAIL missing {f}']
    x = json.loads(f.read_text())
    els = {e['evidence_id']: e for e in epmc.elements(epmc.PAPERS / p / 'fulltext.xml')}
    if x.get('pmcid') != p: probs.append('FAIL pmcid mismatch')
    if not isinstance(x.get('eligible_fulltext'), bool): probs.append('FAIL eligible_fulltext must be true/false')
    if x.get('tissue_category') not in ALLOWED['tissue_category']: probs.append(f"FAIL tissue_category {x.get('tissue_category')}")
    if not x.get('eligible_fulltext'):
        if not x.get('exclusion_reason'): probs.append('FAIL ineligible without exclusion_reason')
        return probs
    for k in ('method', 'controls', 'decontamination', 'biomass_qpcr', 'data_source'):
        v = x.get(k) or {}
        if v.get('value') not in ALLOWED[k]: probs.append(f"FAIL {k}.value={v.get('value')}"); continue
        ev = v.get('evidence', [])
        if not ev and not (k == 'controls' and v['value'] == 'none_mentioned') and not (k in ('decontamination',) and v['value'] in ('none', 'unclear')) \
           and not (k == 'biomass_qpcr' and v['value'] == 'no') and not (k == 'data_source' and v['value'] == 'own_samples'):
            probs.append(f'FAIL {k} has no evidence quote')
        for q in ev:
            t = element_text(p, els, q.get('id', ''))
            if t is None: probs.append(f"FAIL {k}: evidence id {q.get('id')} not found")
            elif norm(q.get('quote', '')) not in norm(t) or len(q.get('quote', '')) < 8: probs.append(f"FAIL {k}: quote not in {q.get('id')}")
    for k in ('list_type', 'figures_only', 'authors_conclusion'):
        if x.get(k, '') not in ALLOWED[k]: probs.append(f'FAIL {k}={x.get(k)}')
    seen = set()
    for g in x.get('genera', []):
        n, eid = g.get('name', ''), g.get('evidence_id', '')
        t = element_text(p, els, eid)
        if t is None: probs.append(f'FAIL genus {n}: evidence id {eid} not found'); continue
        if n.lower() not in t.lower() and n.replace('_', ' ').lower() not in t.lower(): probs.append(f'FAIL genus {n} not in {eid}')
        c = canon(n)
        if c not in NCBI: probs.append(f'WARN genus {n} not an NCBI Bacteria/Archaea genus (will not be counted)')
        elif NCBI[c][1] == 'Archaea': probs.append(f'WARN genus {n} is archaeal (logged, not counted)')
        if c in seen and not g.get('flagged_contaminant'): probs.append(f'WARN duplicate genus {n}')
        seen.add(c)
    for g in x.get('top5', []):
        if canon(g) not in {canon(h['name']) for h in x.get('genera', [])}: probs.append(f'WARN top5 genus {g} not in genera list')
    return probs

if __name__ == '__main__':
    bad = 0
    for p in sys.argv[1:]:
        pr = check(p)
        fails = [q for q in pr if q.startswith('FAIL')]
        bad += bool(fails)
        print(p, 'OK' if not fails else 'FAIL', ('; '.join(pr))[:2000])
    sys.exit(1 if bad else 0)
