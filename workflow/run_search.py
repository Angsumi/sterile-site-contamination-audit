"""C6 feasibility search: PubMed and Europe PMC counts by tissue, plus the OA record list.

Saves exact queries, date and counts to search/search_log.json and the Europe PMC
records (OA subset with PMCID) to search/epmc_records.csv.
"""
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import epmc

OUT = epmc.ROOT / 'search'
OUT.mkdir(exist_ok=True)

# Method block: sequencing-based microbiome profiling
METHOD_PM = ('(microbiome[tiab] OR microbiota[tiab] OR "16S rRNA"[tiab] OR "16S rDNA"[tiab] OR metagenom*[tiab] '
             'OR "bacterial DNA"[tiab] OR "microbial DNA"[tiab])')
METHOD_EP = ('(ABSTRACT:"microbiome" OR ABSTRACT:"microbiota" OR ABSTRACT:"16S rRNA" OR ABSTRACT:"16S rDNA" '
             'OR ABSTRACT:"metagenomic" OR ABSTRACT:"metagenomics" OR ABSTRACT:"bacterial DNA" OR ABSTRACT:"microbial DNA")')
SEQ_PM = '(sequencing[tiab] OR "16S"[tiab] OR metagenom*[tiab])'
SEQ_EP = '(ABSTRACT:"sequencing" OR ABSTRACT:"16S" OR ABSTRACT:metagenomic*)'

# Tissue blocks (title/abstract); PubMed and Europe PMC versions
TISSUES = {
    'tumour': ('(intratumoral[tiab] OR intratumoural[tiab] OR intratumor[tiab] OR intratumour[tiab] OR "tumor microbiome"[tiab] '
               'OR "tumour microbiome"[tiab] OR "tumor microbiota"[tiab] OR "tumour microbiota"[tiab] OR "tumor tissue"[tiab] '
               'OR "tumour tissue"[tiab] OR "cancer tissue"[tiab] OR "tumor tissues"[tiab] OR "tumour tissues"[tiab] OR "cancer tissues"[tiab])',
               '(ABSTRACT:"intratumoral" OR ABSTRACT:"intratumoural" OR ABSTRACT:"intratumor" OR ABSTRACT:"intratumour" '
               'OR ABSTRACT:"tumor microbiome" OR ABSTRACT:"tumour microbiome" OR ABSTRACT:"tumor microbiota" OR ABSTRACT:"tumour microbiota" '
               'OR ABSTRACT:"tumor tissue" OR ABSTRACT:"tumour tissue" OR ABSTRACT:"cancer tissue" OR ABSTRACT:"tumor tissues" '
               'OR ABSTRACT:"tumour tissues" OR ABSTRACT:"cancer tissues")'),
    'placenta_fetal': ('(placenta*[tiab] OR "amniotic fluid"[tiab] OR meconium[tiab] OR fetal[tiab] OR foetal[tiab] OR "in utero"[tiab] OR chorioamni*[tiab])',
                       '(ABSTRACT:placenta* OR ABSTRACT:"amniotic fluid" OR ABSTRACT:"meconium" OR ABSTRACT:"fetal" OR ABSTRACT:"foetal" '
                       'OR ABSTRACT:"in utero" OR ABSTRACT:chorioamnionitis)'),
    'blood': ('("blood microbiome"[tiab] OR "blood microbiota"[tiab] OR "circulating microbiome"[tiab] OR "circulating microbiota"[tiab] '
              'OR "blood bacterial DNA"[tiab] OR "plasma microbiome"[tiab] OR "serum microbiome"[tiab] OR "circulating bacterial DNA"[tiab] '
              'OR "microbial cell-free DNA"[tiab] OR "blood microbial"[tiab])',
              '(ABSTRACT:"blood microbiome" OR ABSTRACT:"blood microbiota" OR ABSTRACT:"circulating microbiome" OR ABSTRACT:"circulating microbiota" '
              'OR ABSTRACT:"blood bacterial DNA" OR ABSTRACT:"plasma microbiome" OR ABSTRACT:"serum microbiome" OR ABSTRACT:"circulating bacterial DNA" '
              'OR ABSTRACT:"microbial cell-free DNA" OR ABSTRACT:"blood microbial")'),
    'brain_csf': ('("brain microbiome"[tiab] OR "brain microbiota"[tiab] OR "brain tissue"[tiab] OR "brain tissues"[tiab] OR "post-mortem brain"[tiab] '
                  'OR "postmortem brain"[tiab] OR "cerebrospinal fluid"[tiab])',
                  '(ABSTRACT:"brain microbiome" OR ABSTRACT:"brain microbiota" OR ABSTRACT:"brain tissue" OR ABSTRACT:"brain tissues" '
                  'OR ABSTRACT:"post-mortem brain" OR ABSTRACT:"postmortem brain" OR ABSTRACT:"cerebrospinal fluid")'),
    'other_sterile': ('("synovial fluid"[tiab] OR "adipose tissue microbio*"[tiab] OR "liver tissue"[tiab] OR "atherosclerotic plaque*"[tiab] '
                      'OR "heart valve*"[tiab] OR "intraocular"[tiab] OR "vitreous"[tiab] OR "aqueous humor"[tiab] OR "follicular fluid"[tiab] '
                      'OR "breast tissue"[tiab] OR "lung tissue"[tiab] OR "thrombus"[tiab] OR "kidney tissue"[tiab] OR "tissue microbiome"[tiab] OR "tissue microbiota"[tiab])',
                      '(ABSTRACT:"synovial fluid" OR ABSTRACT:"adipose tissue microbiome" OR ABSTRACT:"adipose tissue microbiota" OR ABSTRACT:"liver tissue" OR ABSTRACT:"atherosclerotic plaque" OR ABSTRACT:"atherosclerotic plaques" '
                      'OR ABSTRACT:"heart valve" OR ABSTRACT:"heart valves" OR ABSTRACT:"intraocular" OR ABSTRACT:"vitreous" OR ABSTRACT:"aqueous humor" OR ABSTRACT:"follicular fluid" '
                      'OR ABSTRACT:"breast tissue" OR ABSTRACT:"lung tissue" OR ABSTRACT:"thrombus" OR ABSTRACT:"kidney tissue" OR ABSTRACT:"tissue microbiome" OR ABSTRACT:"tissue microbiota")'),
}
HUMAN_PM = 'NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt])'
HUMAN_EP = 'NOT PUB_TYPE:"review"'  # preprints (source PPR) dropped from the record list below
YEARS_PM = 'AND ("2012/01/01"[dp] : "2026/11/22"[dp])'
YEARS_EP = 'AND PUB_YEAR:[2012 TO 2026]'


def compact(block):
    """'(ABSTRACT:"a" OR ABSTRACT:b)' -> 'ABSTRACT:("a" OR b)'; Europe PMC runs this form much faster."""
    return 'ABSTRACT:(' + block.strip()[1:-1].replace('ABSTRACT:', '') + ')'


def main():
    log = {'date': time.strftime('%Y-%m-%d'), 'note': 'Feasibility counts; final search to be re-run at the start of the review.',
           'method_block_pubmed': METHOD_PM, 'method_block_epmc': METHOD_EP, 'tissues': {}}
    records = {}
    for t, (pm, ep) in TISSUES.items():
        qpm = f'{METHOD_PM} AND {SEQ_PM} AND {pm} {HUMAN_PM} {YEARS_PM}'
        qep = f'{compact(METHOD_EP)} AND {compact(ep)} {HUMAN_EP} {YEARS_EP}'
        qep_oa = qep + ' AND OPEN_ACCESS:Y AND HAS_FT:Y'
        n_pm = epmc.pubmed_count(qpm)
        n_ep = epmc.epmc_search(qep, page_size=1, max_records=1)[0]
        n_oa, recs = epmc.epmc_search(qep_oa, page_size=1000)
        recs = [r for r in recs if r.get('source') != 'PPR']
        for r in recs:
            key = r.get('pmcid') or r.get('id')
            row = records.setdefault(key, {k: r.get(k, '') for k in ('pmcid', 'pmid', 'doi', 'title', 'journalTitle', 'pubYear', 'authorString')} | {'tissues': []})
            row['tissues'].append(t)
        log['tissues'][t] = {'pubmed_query': qpm, 'pubmed_count': n_pm, 'epmc_query': qep, 'epmc_count': n_ep,
                             'epmc_oa_query': qep_oa, 'epmc_oa_fulltext_count': n_oa}
        print(t, n_pm, n_ep, n_oa, flush=True)
    log['epmc_oa_unique_records'] = len(records)
    (OUT / 'search_log.json').write_text(json.dumps(log, indent=1))
    with open(OUT / 'epmc_oa_records.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['pmcid', 'pmid', 'doi', 'pubYear', 'journalTitle', 'title', 'authorString', 'tissues'])
        w.writeheader()
        for r in records.values():
            w.writerow(r | {'tissues': ';'.join(r['tissues'])})
    print('unique OA records', len(records))


if __name__ == '__main__':
    main()
