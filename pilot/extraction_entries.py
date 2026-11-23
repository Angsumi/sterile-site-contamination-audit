"""C6 pilot extractions by the AI agent (Claude), 22 Nov 2026. First pass; to be checked by a person.

Each entry: field values with evidence IDs and verbatim quotes from the OA full text
(papers/<PMCID>/fulltext.xml, evidence IDs from workflow/epmc.py elements()).
genera: 'Name:E0000' (detected in target samples, after the authors' own filtering);
'!Name:E0000' = flagged by the authors as contaminant (removed or interpreted as contamination).
top5: the five most abundant reported genera, only when the paper ranks them.
Run: python pilot/extraction_entries.py  -> writes pilot/extractions/<PMCID>.json
"""
import json
from pathlib import Path
OUT = Path(__file__).parent / 'extractions'
ENTRIES = []


def E(pmcid, block, cat, year, eligible, method=None, controls=None, decon=None, qpcr=None, genera='', top5='',
      figonly='', conclusion='', notes='', excl=''):
    ev = lambda t: [{'id': i, 'quote': q} for i, q in t[1]] if t else []
    g = []
    for tok in genera.split():
        flag = tok.startswith('!')
        name, eid = tok.lstrip('!').rsplit(':', 1)
        g.append({'name': name, 'evidence_id': eid, 'flagged_contaminant': flag})
    ENTRIES.append({'pmcid': pmcid, 'block': block, 'tissue_category': cat, 'year': year, 'eligible_fulltext': eligible,
                    'exclusion_reason': excl,
                    'method': {'value': method[0], 'evidence': ev(method)} if method else {},
                    'controls': {'value': controls[0], 'evidence': ev(controls)} if controls else {},
                    'decontamination': {'value': decon[0], 'evidence': ev(decon)} if decon else {},
                    'biomass_qpcr': {'value': qpcr[0], 'evidence': ev(qpcr)} if qpcr else {},
                    'genera': g, 'top5': top5.split(), 'genera_in_figures_only': figonly,
                    'authors_conclusion': conclusion, 'notes': notes, 'extractor': 'AI agent (Claude Opus 5.5)', 'date': '2026-11-22'})


# ---------------- tumour ----------------
E('PMC12618227', 'tumour', 'tumour', 2025, True,
  method=('16S+shotgun', [('E0051', 'All tumor samples and associated controls were sequenced using V3-V4 16S rRNA amplicon sequencing')]),
  controls=('sequenced', [('E0051', 'Reagent controls were taken at the time of DNA extraction for each extraction kit and each batch')]),
  decon=('tool', [('E0059', 'We used Source tracking for Contamination Removal in microBiomes (SCRuB'), ('E0064', 'Taxa identified in negative controls were removed as contaminants.')]),
  qpcr=('yes', [('E0070', 'Nuclease-free water was used as a negative control.')]),
  genera='Fusobacterium:E0017 Veillonella:E0017 Prevotella:E0017 Capnocytophaga:E0017 Enterococcus:E0017 Porphyromonas:E0018 Neisseria:E0039 Gemella:E0039 Streptococcus:E0033 Bifidobacterium:E0033',
  figonly='partial', conclusion='claimed', notes='34 taxa after filtering shown in bubble plots (figure); text names 10. Also FISH, culture, dPCR. Drops 46.6% of tumours with no signal after filtering.')
E('PMC12375787', 'tumour', 'tumour', 2025, True,
  method=('host_seq_mining', [('E0008', 'Non-human, unmapped reads were retained and mapped to the Kraken2 32GB database')]),
  controls=('none_mentioned', [('E0037', 'there is a lack of microbiome controls to rule out environmental contamination')]),
  decon=('abundance_filter_only', [('E0037', 'We attempted to reduce the effect of this on our findings by applying appropriate prevalence filtering')]),
  qpcr=('yes', [('E0024', 'we conducted an in vitro validation of microbial abundance using qPCR amplification of the bacterial 16S V3V4 region')]),
  genera='Pseudomonas:E0014 Bacillus:E0014 Escherichia:E0014 Klebsiella:E0014 Streptomyces:E0014 Priestia:E0014 Cutibacterium:E0014 Serratia:E0014 Acinetobacter:E0014 '
         'Sulfidibacter:E0020 Bifidobacterium:E0020 Microbacterium:E0020 Kocuria:E0020 Pseudolysobacter:E0020 Dietzia:E0020 Stenotrophomonas:E0020 Curtobacterium:E0020 '
         'Pseudonocardia:E0020 Paraburkholderia:E0020 Alcanivorax:E0020 Gordonia:E0020 Mycobacteroides:E0020 Kinneretia:E0020 Dolosigranulum:E0020 Rhizobium:E0020 '
         'Micrococcus:E0020 Erythrobacter:E0020 Pseudoalteromonas:E0020 Mycobacterium:E0020',
  top5='Pseudomonas Bacillus Escherichia Klebsiella Streptomyces', conclusion='claimed', notes='Existing RNA-seq of 977 breast tumours re-mined; Siphoviridae (viral family) not counted.')
E('PMC8085784', 'tumour', 'tumour', 2021, True,
  method=('host_seq_mining', [('E0007', 'RNA-sequencing data were filtered for bacterial reads via direct alignment to a reference library of bacterial sequences using the Pathoscope 2.0 software')]),
  controls=('none_mentioned', [('E0006', 'Raw whole-transcriptome RNA-sequencing, Level 3 normalized mRNA expression read counts')]),
  decon=('tool', [('E0017', 'In all, we identified 202 potential contaminants to be eliminated from further investigation')]),
  genera='Rhodococcus:E0018 Acinetobacter:E0018 Bradyrhizobium:E0018 Trueperella:E0018 Stenotrophomonas:E0018 Micrococcus:E0018 Frankia:E0020 Anabaena:E0020 Synechococcus:E0019 Chroococcidiopsis:E0027',
  conclusion='claimed', notes='TCGA thyroid RNA-seq; contaminants by sequencing date/plate, abundance pattern and a 175-genus published list. No sequenced controls exist for TCGA. Controls quote shows data source only (no controls mentioned).')
E('PMC8638380', 'tumour', 'tumour', 2021, True,
  method=('16S', [('E0001', 'We performed 16s rRNA gene sequencing using tumor tissues and matched peritumor tissues from 30 patients')]),
  controls=('sequenced', [('E0007', 'six sterile Petri dishes with sterile water and sterile filter paper were placed in different corners of the operating room for 24 h')]),
  decon=('removed_control_taxa', [('E0013', 'after elimination of environmental contamination')]),
  genera='Sphingomonas:E0001 Comamonas:E0001 Acinetobacter:E0001 Pseudomonas:E0001 Microvirgula:E0001 Soonwooa:E0001 Aeromonas:E0001 Peptostreptococcus:E0001 Proteus:E0014 !Chryseobacterium:E0012',
  conclusion='claimed', notes='Controls are operating-room sampling blanks only (no extraction blanks). Chryseobacterium is in the QC core and the pre-elimination thyroid core; treated as removed. Gut genera from faecal samples not counted.')
# ---------------- placenta ----------------
E('PMC4917942', 'placenta_fetal', 'placenta_fetal', 2016, True,
  method=('16S', [('E0012', 'DNA samples were PCR amplified using bar-coded primers flanking the V1V2 region of the 16S rRNA gene')]),
  controls=('sequenced', [('E0005', 'Three types of negative controls were collected.')]),
  decon=('none', [('E0028', 'we can only conclude that we could not use our data to distinguish placental samples from contamination controls')]),
  qpcr=('yes', [('E0037', 'Bacterial DNA abundance was quantified by quantitative PCR (qPCR) amplification of the V1V2 region of the 16S rRNA gene.')]),
  genera='!Sediminibacterium:E0015 !Methylobacterium:E0015 !Propionibacterium:E0015 Prevotella:E0016 !Clostridium:E0017',
  conclusion='not_claimed', notes='Placental signal indistinguishable from controls; genera presented as contaminants. Decontamination not applied (comparison only).')
E('PMC10139004', 'placenta_fetal', 'placenta_fetal', 2023, False, excl='metaproteomics (LC-ESI-MS/MS), not sequencing',
  method=('proteomics', [('E0001', 'the microbiome of normal and FGR placentas was analyzed by LC-ESI-MS/MS mass spectrometry')]))
E('PMC7609904', 'placenta_fetal', 'placenta_fetal', 2020, True,
  method=('16S', [('E0001', 'V3–V4 hypervariable regions of the 16S ribosomal RNA gene')]),
  controls=('included_not_sequenced', [('E0040', 'Negative control sample from DNA isolation and blank PCR reagent were both negative after PCR step')]),
  decon=('none', [('E0108', 'We detected microbiota in all placental samples but not in the negative control sample.')]),
  genera='Prevotella:E0057 Blautia:E0058 Bacteroides:E0059 Faecalibacterium:E0060 Rhodococcus:E0061 Bifidobacterium:E0062 Escherichia-Shigella:E0065 '
         'Coprococcus:E0068 Anaerotruncus:E0068 Ruminococcus:E0068 Dorea:E0068 Paraprevotella:E0068 Veillonella:E0001 Lactobacillus:E0001',
  top5='Prevotella Blautia Bacteroides Faecalibacterium Rhodococcus', conclusion='claimed', notes='Controls judged negative by PCR band, not sequenced. Cord blood: 1/15 positive.')
E('PMC13143940', 'placenta_fetal', 'placenta_fetal', 2026, True,
  method=('16S', [('E0008', 'In this study, we amplified and sequenced the bacterial V4 region.')]),
  controls=('included_not_sequenced', [('E0008', 'No template control was set for each batch, and the CT value was greater than 35.')]),
  decon=('none', []),
  genera='Psychromicrobium:E0026 Halomonas:E0026 Nesterenkonia:E0026 Sphingomonas:E0026 Nocardiopsis:E0026 Ralstonia:E0026 Dietzia:E0026 Cutibacterium:E0026 '
         'Brevundimonas:E0026 Cupriavidus:E0026 Mycobacterium:E0026 Acinetobacter:E0026 Staphylococcus:E0026 Diaphorobacter:E0026 Aquabacterium:E0026 '
         'Moraxella:E0026 Leifsonia:E0026 Pelomonas:E0026 Chroococcidiopsis:E0051 Aerococcus:E0051 Bosea:E0052',
  top5='Psychromicrobium Halomonas Nesterenkonia Sphingomonas Nocardiopsis', conclusion='claimed', notes='No decontamination mentioned (no evidence quote possible).')

# ---------------- blood ----------------
E('PMC8873459', 'blood', 'blood', 2022, True,
  method=('host_seq_mining', [('E0036', 'yielding bam files that served as input into PathSeq')]),
  controls=('none_mentioned', [('E0006', 'DNA extracted from all samples was subjected to whole-genome sequencing, initially with the goal of comprehensively profiling somatic mutations in human DNA.')]),
  decon=('literature_list', [('E0037', 'we curated a list of genera and species that were reported in the literature as being problematic')]),
  genera='Dermabacter:E0020 Kytococcus:E0020 Staphylococcus:E0020 Streptomyces:E0020 Rothia:E0020 Gordonia:E0020 Pandoraea:E0020',
  figonly='partial', conclusion='claimed', notes='Mostly bone marrow (1756) with 114 blood; 12 healthy bone marrow donors are biological, not negative, controls. Most genera only in figures.')
E('PMC12312234', 'blood', 'blood', 2025, True,
  method=('2bRAD-M', [('E0022', '2bRAD-M utilizes type IIB restriction enzymes')]),
  controls=('none_mentioned', []),
  decon=('abundance_filter_only', [('E0009', 'The threshold of G score for a false positive discovery of microbial species was set 5')]),
  genera='Acinetobacter:E0015 Cupriavidus:E0015 Sphingomonas:E0015 Pseudomonas:E0015 Staphylococcus:E0015 Lactobacillus:E0015 Clostridium:E0015 Escherichia:E0015 '
         'Alcaligenes:E0018 Kocuria:E0019 Klebsiella:E0016',
  top5='Acinetobacter Cupriavidus Sphingomonas Pseudomonas Staphylococcus', conclusion='claimed', notes='Serum. No negative controls found in the text.')
E('PMC12475220', 'blood', 'blood', 2025, True,
  method=('16S', [('E0007', 'The extracted DNA was then used for 16S rRNA sequencing')]),
  controls=('none_mentioned', [('E0007', 'To minimise the risk of contamination, bacterial DNA was extracted from EVs rather than directly from whole blood.')]),
  decon=('none', []),
  genera='Corynebacterium:E0015 Pseudomonas:E0015 Acinetobacter:E0015 Sphingomonas:E0015 Bacteroides:E0015 Bifidobacterium:E0015 Klebsiella:E0015 Enterobacter:E0015 '
         'Actinomyces:E0018 Brevibacterium:E0018 Burkholderia:E0018 Comamonas:E0018 Cronobacter:E0018 Deinococcus:E0018 Faecalibacterium:E0018 Helicobacter:E0018 '
         'Herbaspirillum:E0018 Herminiimonas:E0018 Kluyvera:E0018 Lautropia:E0018 Leuconostoc:E0018 Ligilactobacillus:E0018 Limosilactobacillus:E0018 Ralstonia:E0018 '
         'Staphylococcus:E0018 Subdoligranulum:E0018 Vaulcaiibacterium:E0018',
  conclusion='claimed', notes='Serum EVs. Burkholderia-Caballeronia-Paraburkholderia (SILVA group) counted as Burkholderia. Genera from ML feature tables.')
E('PMC6417675', 'blood', 'blood', 2019, True,
  method=('16S', [('E0001', 'Fecal and blood microbiota communities were analyzed by sequencing of the V3-V4 domains of the 16S rRNA genes.')]),
  controls=('none_mentioned', []), decon=('none', []),
  genera='Deinococcus:E0112 Leuconostoc:E0115 Clostridium:E0117 Norcadioides:E0121 Chryseoglobus:E0123 Beijerinckia:E0126 Caldithrix:E0132 Anaerobiospirillum:E0135 '
         'Lysobacter:E0138 Alcanivorax:E0139 Legionella:E0140 Rubritalea:E0143 Maribacter:E0149 Actibacter:E0150 Aestuariicola:E0151 Parabacteroides:E0153 Delftia:E0155',
  conclusion='claimed', notes='Buffy coat. Only NAFLD-associated blood genera (Table 6) are named; overall blood profile only in figures. Nocardioides spelt Norcadioides in source.')
# ---------------- brain ----------------
E('PMC11274863', 'brain_csf', 'brain_csf', 2024, True,
  method=('16S', [('E0004', 'using 16S rRNA gene sequencing')]),
  controls=('sequenced', [('E0009', 'water blank reagent control samples were run through every step of the process from DNA extraction to sequencing')]),
  decon=('unclear', []), genera='', figonly='yes', conclusion='claimed',
  notes='Results reported at phylum, class and order level only; no genus list in text or tables.')
E('PMC10857729', 'brain_csf', 'brain_csf', 2024, True,
  method=('16S', [('E0042', 'the V3-V4 regions of the 16S rRNA gene were amplified')]),
  controls=('sequenced', [('E0042', 'Three negative controls, one DNA extraction control (NC1) and two no-template controls (NC2 and NC3) were included in the PCR and sequencing')]),
  decon=('tool', [('E0048', 'potential contaminants were removed using the exact binomial test (Filter 3)')]),
  qpcr=('yes', [('E0041', 'Real-time quantitative PCR (qPCR) was performed')]),
  genera='Bradyrhizobium:E0057 Proteus:E0057 Cloacibacterium:E0057 Stenotrophomonas:E0057 Anaerococcus:E0062 Pseudomonas:E0062 Massilia:E0062 Nocardia:E0062 Helicobacter:E0062 !Cutibacterium:E0067',
  conclusion='claimed', notes='Bradyrhizobium most abundant in many samples after filtering. Genera in E0064 are cited literature, not results.')
E('PMC6861841', 'brain_csf', 'brain_csf', 2019, True,
  method=('16S', [('E0014', 'For bacterial DNA, primers were designed to amplify the region between V3 and V4 of 16S rDNA gene.')]),
  controls=('included_not_sequenced', [('E0015', 'a control without DNA indicated that it was clean without any apparent DNA fragment')]),
  decon=('none', []),
  genera='Pseudomonas:E0001 Acinetobacter:E0001 Burkholderia:E0001 Cutibacterium:E0044 Escherichia:E0044 Streptococcus:E0044',
  conclusion='claimed', notes='Fungal genera (ITS) also reported; not counted (bacterial list).')
E('PMC13115908', 'brain_csf', 'brain_csf', 2026, True,
  method=('host_seq_mining', [('E0029', 'High-quality, cleaned reads were taxonomically classified using Kraken2')]),
  controls=('none_mentioned', [('E0028', 'did not include extraction blanks or library blanks')]),
  decon=('none', [('E0028', 'formal contaminant modeling/decontamination could not be performed')]),
  genera='Acinetobacter:E0011 Lactobacillus:E0011 Arthrobacter:E0011 Actinomyces:E0011 Staphylococcus:E0011 Nocardioides:E0018 Streptococcus:E0021',
  conclusion='unclear', notes='Authors call several taxa plausible contaminants but do not remove them; hypothesis-generating.')
# ---------------- other sterile ----------------
E('PMC9426487', 'other_sterile', 'other_sterile', 2022, True,
  method=('16S', [('E0001', 'The microbial compositions of all samples were compared using 16S rRNA gene amplicon next-generation sequencing.')]),
  controls=('included_not_sequenced', [('E0118', 'Blank extractions (as reagent controls) were also processed and used to identify potential contamination.')]),
  decon=('none', []),
  qpcr=('yes', [('E0037', 'of the isolated plasma samples in qPCR')]),
  genera='Acinetobacter:E0040 Burkholderia:E0040 Sphingomonas:E0040 Pedobacter:E0040 Serratia:E0040 Stenotrophomonas:E0040 Brevundimonas:E0040 Bradyrhizobium:E0040 '
         'Bacillus:E0040 Elizabethkingia:E0040 Prevotella:E0040 Ochrobactrum:E0040 Ralstonia:E0040 Herbaspirillum:E0040 Chryseobacterium:E0040 Methylobacterium:E0040 '
         'Staphylococcus:E0040 Enhydrobacter:E0040 Streptococcus:E0040 Clostridium:E0040 Paracoccus:E0060 Mesorhizobium:E0101',
  top5='Acinetobacter Burkholderia Sphingomonas Pedobacter Serratia', conclusion='claimed',
  notes='Cerebral thrombi. Blanks and periprocedural controls judged negative by PCR gel; sequencing of blanks not stated.')
E('PMC13314463', 'other_sterile', 'other_sterile', 2026, True,
  method=('2bRAD-M', [('E0001', '2bRAD-M gene sequencing was used to characterize the aqueous humor microbiome')]),
  controls=('sequenced', [('E0016', 'we set up negative controls for identifying and removing contaminating sequences from the experimental samples')]),
  decon=('removed_control_taxa', [('E0016', 'a certain number of sequences were randomly drawn from the negative control pool')]),
  genera='Escherichia:E0001 Neisseria:E0001 Capnocytophaga:E0001 Veillonella:E0001 Rhodococcus:E0001 Jensenia:E0001 Corynebacterium:E0001',
  conclusion='claimed', notes='Aqueous humor; 3 per group.')
E('PMC12462036', 'other_sterile', 'other_sterile', 2025, False, excl='rat model (animal); screening error at title/abstract',
  method=('16S', [('E0009', 'extract bacterial DNA from rat follicular fluid samples')]))
E('PMC9239270', 'other_sterile', 'other_sterile', 2022, True,
  method=('16S', [('E0001', 'Illumina MiSeq paired-end sequencing of the V3-V4 region of the 16S gene')]),
  controls=('sequenced', [('E0123', 'performed 9 extractions from negative controls')]),
  decon=('tool', [('E0130', 'were removed from all samples using the decontam package')]),
  genera='Streptococcus:E0043 Corynebacterium:E0043 Bradyrhizobium:E0043 Enterococcus:E0043 Pseudomonas:E0043 Lodobacter:E0043 Sphingomonas:E0043',
  conclusion='claimed', notes='Normal (pre-diagnostic and healthy) breast tissue; from v1 sample (replaces the rat follicular fluid paper). Positive control (ZymoBIOMICS) used.')
E('PMC7943566', 'other_sterile', 'other_sterile', 2021, True,
  method=('shotgun', [('E0042', 'DNA libraries were sequenced to a depth of 10~50 million reads per sample')]),
  controls=('sequenced', [('E0013', 'Three blank samples without AH specimens were processed along the metagenomic sequenc')]),
  decon=('none', [('E0014', 'the intraocular microbial communities in all patients were significantly different from all specimen-free negative controls')]),
  genera='Propionibacterium:E0005 Staphylococcus:E0008', figonly='yes', conclusion='claimed',
  notes='Intraocular (aqueous humor) metagenomes; genus profiles only in figures. Replacement for the rat paper (v1 sample).')

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for e in ENTRIES:
        (OUT / f"{e['pmcid']}.json").write_text(json.dumps(e, ensure_ascii=False, indent=1))
    print(len(ENTRIES), 'extractions written')
