"""C6 search v2 (amendment 0.2): tighter tissue blocks and a human filter.

Why: in the v1 screening sample (30 per block) 0/30 placenta and 0/30 brain records were
eligible (animal, infant gut, meconium, diagnostic CSF mNGS), and 22/30 tumour records were
mucosal (mostly colorectal) tumours. Writes search/search_log_v2.json and search/epmc_oa_records_v2.csv.
"""
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import epmc

OUT = epmc.ROOT / 'search'
MICRO = '(microbiome OR microbiota OR "16S rRNA" OR "16S rDNA" OR "bacterial DNA" OR "microbial DNA" OR metagenomic OR metagenomics OR "microbial reads")'
MICRO_STRICT = '(microbiome OR microbiota OR "16S rRNA" OR "16S rDNA" OR "bacterial DNA" OR "microbial DNA")'
MUCOSAL_TITLE = ('(colorectal OR colon OR rectal OR gastric OR stomach OR esophageal OR oesophageal OR oral OR "head and neck" '
                 'OR cervical OR bladder OR nasopharyngeal OR laryngeal OR gut OR fecal OR faecal OR stool OR intestinal)')
ANIMAL_TITLE = ('(mice OR mouse OR murine OR rat OR rats OR porcine OR pig OR pigs OR bovine OR cattle OR cow OR cows OR calves '
                'OR dog OR dogs OR canine OR cat OR cats OR feline OR horse OR equine OR sheep OR goat OR goats OR chicken OR fish OR primate OR macaque)')
EXCL_TITLE = '(meningitis OR encephalitis OR sepsis OR "case report" OR diagnosis OR diagnostic OR "next-generation sequencing" OR mNGS)'
HUMAN_ABS = '(patients OR participants OR women OR men OR human OR humans OR subjects OR donors OR individuals OR cohort OR pregnancies OR autopsy OR postmortem)'

BLOCKS = {
    'tumour': (MICRO, '(intratumoral OR intratumoural OR intratumor OR intratumour OR "tumor microbiome" OR "tumour microbiome" '
               'OR "tumor microbiota" OR "tumour microbiota" OR "tumor tissue" OR "tumour tissue" OR "tumor tissues" OR "tumour tissues" '
               'OR "cancer tissue" OR "cancer tissues")', MUCOSAL_TITLE),
    'placenta_fetal': (MICRO, '("placental microbiome" OR "placental microbiota" OR "placenta microbiome" OR "placenta microbiota" '
                       'OR "amniotic fluid microbiome" OR "amniotic fluid microbiota" OR "intrauterine colonization" OR "in utero colonization" '
                       'OR "fetal microbiome" OR "fetal microbiota" OR "cord blood microbiome" OR "cord blood microbiota" OR "placental tissue" '
                       'OR "placental tissues" OR "placental samples" OR "placental bacteria" OR "fetal membranes" OR "amniotic fluid samples")',
                       '(meconium OR infant OR infants OR neonatal OR vaginal OR gut OR fecal OR faecal OR stool)'),
    'blood': (MICRO, '("blood microbiome" OR "blood microbiota" OR "circulating microbiome" OR "circulating microbiota" OR "blood bacterial DNA" '
              'OR "plasma microbiome" OR "serum microbiome" OR "circulating bacterial DNA" OR "microbial cell-free DNA" OR "blood microbial")', None),
    'brain_csf': (MICRO_STRICT, '("brain microbiome" OR "brain microbiota" OR "brain tissue" OR "brain tissues" OR "postmortem brain" '
                  'OR "post-mortem brain" OR "cerebrospinal fluid microbiome" OR "cerebrospinal fluid microbiota" OR "CSF microbiome" OR "CSF microbiota")',
                  '(gut OR fecal OR faecal OR stool OR intestinal OR "gut-brain")'),
    'other_sterile': (MICRO_STRICT, '("synovial fluid" OR "adipose tissue" OR "liver tissue" OR "atherosclerotic plaque" OR "atherosclerotic plaques" '
                      'OR "heart valve" OR "heart valves" OR intraocular OR vitreous OR "aqueous humor" OR "follicular fluid" OR "breast tissue" '
                      'OR "lung tissue" OR thrombus OR thrombi OR "kidney tissue" OR "tissue microbiome" OR "tissue microbiota" OR "endometrial tissue")',
                      '(gut OR fecal OR faecal OR stool OR intestinal OR oral OR vaginal OR cervical OR colorectal OR colon OR gastric)'),
}


def pm_block(s):
    """'(a OR "b c")' -> '(a[tiab] OR "b c"[tiab])'."""
    import re
    terms = re.findall(r'"[^"]+"|[^()\s]+', s)
    return '(' + ' '.join(t if t == 'OR' else t + '[tiab]' for t in terms) + ')'


def pm_title(s):
    import re
    terms = re.findall(r'"[^"]+"|[^()\s]+', s)
    return '(' + ' '.join(t if t == 'OR' else t + '[ti]' for t in terms) + ')'


def main():
    log = {'date': time.strftime('%Y-%m-%d'), 'version': 'v2 (amendment 0.2)', 'tissues': {}}
    records = {}
    for t, (micro, tis, excl) in BLOCKS.items():
        ep = (f'ABSTRACT:{micro} AND ABSTRACT:{tis} AND ABSTRACT:{HUMAN_ABS} NOT TITLE:{ANIMAL_TITLE} NOT TITLE:{EXCL_TITLE}'
              + (f' NOT TITLE:{excl}' if excl else '') + ' NOT PUB_TYPE:"review" AND PUB_YEAR:[2012 TO 2026]')
        pm = (f'{pm_block(micro)} AND {pm_block(tis)} NOT {pm_title(ANIMAL_TITLE)} NOT {pm_title(EXCL_TITLE)}'
              + (f' NOT {pm_title(excl)}' if excl else '')
              + ' NOT (animals[mh] NOT humans[mh]) NOT (review[pt] OR "systematic review"[pt] OR comment[pt] OR editorial[pt] OR "case reports"[pt])'
              + ' AND ("2012/01/01"[dp] : "2026/11/22"[dp])')
        n_pm = epmc.pubmed_count(pm)
        n_ep = epmc.epmc_search(ep, page_size=1, max_records=1)[0]
        ep_oa = ep + ' AND OPEN_ACCESS:Y AND HAS_FT:Y'
        n_oa, recs = epmc.epmc_search(ep_oa, page_size=1000)
        recs = [r for r in recs if r.get('source') != 'PPR' and r.get('pmcid')]
        for r in recs:
            row = records.setdefault(r['pmcid'], {k: r.get(k, '') for k in ('pmcid', 'pmid', 'doi', 'title', 'journalTitle', 'pubYear', 'authorString')} | {'tissues': []})
            row['tissues'].append(t)
        log['tissues'][t] = {'pubmed_query': pm, 'pubmed_count': n_pm, 'epmc_query': ep, 'epmc_count': n_ep,
                             'epmc_oa_query': ep_oa, 'epmc_oa_fulltext_count': n_oa, 'epmc_oa_records_kept': len(recs)}
        print(t, n_pm, n_ep, n_oa, len(recs), flush=True)
    log['epmc_oa_unique_records'] = len(records)
    (OUT / 'search_log_v2.json').write_text(json.dumps(log, indent=1))
    with open(OUT / 'epmc_oa_records_v2.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['pmcid', 'pmid', 'doi', 'pubYear', 'journalTitle', 'title', 'authorString', 'tissues'])
        w.writeheader()
        for r in records.values():
            w.writerow(r | {'tissues': ';'.join(r['tissues'])})
    print('unique OA records', len(records))


if __name__ == '__main__':
    main()
