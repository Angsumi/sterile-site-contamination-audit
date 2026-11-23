"""Stage 4 step 2 aid: keyword pre-sort of all merged records (amendment 0.4). It only SUGGESTS a
reason; the AI agent reads every title (and the abstract unless the title alone settles it) and
makes the decision. Writes papers/_screening/presort.json (local) and prints counts."""
import csv, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import epmc

A = json.loads((epmc.PAPERS / '_screening' / 'abstracts.json').read_text())
R = list(csv.DictReader(open(epmc.ROOT / 'data' / 'records_merged.csv')))
I = re.I
REVIEW = re.compile(r'\breview\b|meta-analys|systematic|perspective|commentary|editorial|\bprotocol\b|guideline|consensus|overview|state of the art|\bletter\b|erratum|correction|retraction|viewpoint|opinion', I)
ANIMAL = re.compile(r'\b(mice|mouse|murine|rats?|porcine|pigs?|piglets?|swine|bovine|cattle|cows?|calves|heifers?|dogs?|canine|cats?|feline|horses?|equine|sheep|ovine|goats?|chickens?|broilers?|poultry|fish|zebrafish|primates?|macaques?|monkeys?|rabbits?|hamsters?|ferrets?|bats?|birds?|insects?|drosophila|honeybees?|shrimp|oysters?|dairy|buffalo|deer|wildlife|camels?|lambs?|bees?|mosquito\w*|ticks?|nematodes?|plants?|maize|rice|wheat|soil|seawater|wastewater|sediment)\b', I)
HUMAN = re.compile(r'\b(human|humans|patients?|women|men|children|people|individuals|participants|subjects|donors|pregnan\w*|cohort|adults?)\b', I)
SEQ = re.compile(r'16S|sequenc|metagenom|metatranscriptom|RNA-seq|microbiome|microbiota', I)
MUCOSAL = re.compile(r'colorectal|\bcolon|rectal|gastric|stomach|esophag|oesophag|\boral\b|head and neck|oropharyn|nasopharyn|laryn|cervical|cervix|bladder|urin|\bgut\b|fecal|faecal|stool|feces|faeces|intestin|vagin|skin|airway|sputum|bronchoalveolar|\bBAL\b|nasal|saliva|dental|periodont|tongue|tonsil|meconium|breast milk|human milk|semen|seminal|endometri|uterine|tear|conjunctiv|wound|ulcer|caries|plaque biofilm|subgingival', I)
DIAG = re.compile(r'mNGS|next[- ]generation sequencing|metagenomic next|diagnos|sepsis|septic|meningitis|encephalitis|infection|infectious|pathogen detection|bloodstream|endophthalmitis|keratitis|periprosthetic|prosthetic joint|osteomyelitis|pneumonia|empyema|abscess|tuberculosis', I)
TARGET = re.compile(r'tumou?r|cancer|carcinoma|neoplas|malignan|glioma|glioblastoma|melanoma|sarcoma|lymphoma|leukemia|placent|amniotic|fetal|foetal|fetus|cord blood|in utero|chorio|intrauterine|\bblood\b|plasma|serum|circulating|cell-free|cfDNA|buffy|brain|cerebr|CSF|neur|adipose|liver|hepat|kidney|renal|heart valve|valv|atheroscl|plaque|thromb|synovial|joint|intraocular|vitreous|aqueous|follicular|breast|lung|pancrea|prostat|ovar|thyroid|bone|bile|biliary|tissue|organ|sterile|low[- ]biomass|lymph node|muscle|spleen|pericard|pleural|ascit|peritoneal|cyst|aneurysm|aort|vascular|artery|arter|myocard|cardiac|heart', I)

out = {}
cnt = {}
for r in R:
    p = r['pmcid']
    a = A.get(p, {})
    t, ab = r['title'], a.get('abstract', '')
    pt = ' '.join(a.get('pubTypes', []))
    s = []
    if not p: s.append('no_pmcid')
    if re.search(r'review|editorial|comment|letter|erratum|retract|published erratum', pt, I) or REVIEW.search(t): s.append('review_or_nonprimary')
    if ANIMAL.search(t) and not HUMAN.search(t): s.append('animal_or_environment_title')
    if not SEQ.search(t + ' ' + ab): s.append('no_sequencing_terms')
    if MUCOSAL.search(t) and not re.search(r'tumou?r tissue|blood|plasma|serum|placent|brain|adipose|liver|breast|lung|pancrea|thromb|synovial|valv|plaque|intraocular|vitreous|follicular|kidney|prostat|thyroid|ovar', t, I): s.append('mucosal_or_high_biomass_title')
    if DIAG.search(t): s.append('diagnostic_or_infection_title')
    if not TARGET.search(t + ' ' + ab): s.append('no_target_site_terms')
    out[p or r['doi']] = s
    k = s[0] if s else 'none'
    cnt[k] = cnt.get(k, 0) + 1
(epmc.PAPERS / '_screening' / 'presort.json').write_text(json.dumps(out, indent=0))
print(cnt, sum(1 for v in out.values() if not v))
