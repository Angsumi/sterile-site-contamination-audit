# Known laboratory contaminant genera are routinely reported in human "sterile-site" microbiome studies: a pre-registered audit of 475 studies

**Ananda Prasad**¹ (ORCID [0009-0005-1736-8148](https://orcid.org/0009-0005-1736-8148)) and **Angsuman Das**²* (ORCID [0000-0001-8146-7697](https://orcid.org/0000-0001-8146-7697))

¹ Department of Zoology, Rajiv Gandhi University, Itanagar, Arunachal Pradesh, India. anandaprasad01@gmail.com
² Department of Zoology, Pachhunga University College (a constituent college of Mizoram University), Aizawl, Mizoram, India. angsuman.das@rgu.ac.in

\*Corresponding author: Angsuman Das, angsuman.das@rgu.ac.in

*Manuscript v2, 23 Nov 2026. A traceable version, in which every number cites its source file, is `manuscript/draft_v1.md`.*

---

## Abstract

**Background.** Tumours, the placenta, blood and other normally sterile human tissues contain little microbial DNA, so DNA from extraction kits and laboratory reagents can dominate sequencing results. How often published studies of these sites report known contaminant genera, and whether this depends on the use of negative controls, has not been measured across tissues.

**Methods.** We searched Europe PMC for open-access studies published from 2012 to 2026 that profiled microbes in human tumours, placental and fetal samples, blood, brain or cerebrospinal fluid and other sterile tissues by sequencing. An AI agent screened records and extracted data, with every value linked to a verbatim quote that was checked automatically; a human reviewer verified a random sample. Every genus that a study reported as detected was matched by script to a fixed list of 78 environmental genera found in sequenced blank controls. The protocol, hypotheses and analysis code were fixed before the analysis.

**Results.** Of 3,462 records, 475 studies were eligible and 398 reported at least three genera. A median of 19% (interquartile range 6–29%) of reported genera were known contaminant genera, and 77% of studies reported at least one. *Sphingomonas*, *Bacillus*, *Ralstonia*, *Methylobacterium* and *Burkholderia* were reported in every tissue group. Half of the studies (50%) mentioned no negative controls, 35% sequenced them, 56% applied no decontamination and 16% measured bacterial load, with no improvement over time; 92% concluded that a microbial community was present. Contrary to our pre-specified hypothesis, studies without negative controls did not report more contaminant genera; in the pooled model they reported fewer (odds ratio 0.63, 95% CI 0.48–0.83). Decontamination, publication year and sequencing method were not robustly associated with the contaminant share.

**Conclusions.** About one in five genera reported from human low-biomass sites is a known reagent contaminant genus, and half of these studies report no negative controls. Including controls does not by itself lower the reported contaminant load. Low-biomass studies should report the sequencing results of their controls and flag contaminant genera, rather than only stating that controls were included.

**Keywords:** low-biomass microbiome; contamination; kitome; negative controls; tumour microbiome; placental microbiome; blood microbiome; meta-research

---

## Introduction

Reports of microbial communities in tissues long considered sterile — tumours, the placenta, blood and the brain — have multiplied over the past decade [1–4]. These samples contain very little bacterial DNA, so DNA introduced by extraction kits, PCR reagents and the laboratory environment (the "kitome") can make up much or all of the sequencing signal [5–7]. Several prominent claims have been challenged on these grounds. A placental microbiome [1] was not distinguishable from contamination in later controlled studies [8–10], and fetal colonisation in utero has been questioned [11]. A pan-cancer study of microbial signatures in tumours and blood [12] was retracted after data-analysis errors were identified [13], and a population-scale study found no evidence for a common blood microbiome [14]. Consensus guidance now recommends sequenced negative controls, statistical decontamination and measurement of microbial biomass in low-biomass studies [7, 15, 16].

What has not been measured is the published literature itself. Systematic reviews of single tissues have noted overlap between reported taxa and known contaminants [10, 17], and an audit of insect microbiota studies found that few control for contamination [18], but no study has quantified across human tissues how many of the genera reported as detected are known laboratory contaminants, or whether studies that sequence negative controls report fewer of them.

We therefore audited open-access human low-biomass microbiome studies against a fixed contaminant reference. We pre-specified four hypotheses: the contaminant share is higher in studies without sequenced negative controls (H1), lower in studies that apply decontamination (H2), falls with publication year (H3) and differs between 16S amplicon and shotgun studies (H4). We also pre-specified a description of control practice by tissue and period.

## Methods

### Protocol and pre-registration
The protocol — question, eligibility criteria, search, contaminant lists, models and main figure — was committed to a version-controlled repository before any study data were extracted. Eight dated amendments, each committed before the step it governs, record changes to search precision, extraction set-up, genus-name normalisation and model details (Supplementary File S6). The analysis script was frozen, and its SHA-256 checksum recorded, before its first run on the full data set.

### Eligibility criteria
We included peer-reviewed, open-access, English-language studies published from 2012 to 2026 that profiled the microbial community of human samples from a target site by sequencing — 16S rRNA or other amplicon sequencing, shotgun metagenomics or metatranscriptomics, reduced-representation metagenomics (2bRAD-M) or mining of host RNA or DNA sequencing data for microbial reads — with the aim of describing the microbes in that site. Target sites were (i) internal tumours not open to a mucosal surface (for example breast, pancreas, liver, bile duct, kidney, prostate, ovary, endometrium, thyroid, brain, bone, soft tissue and lung tumours); (ii) placenta, fetal membranes, amniotic fluid, cord blood and fetal tissue; (iii) whole blood, plasma, serum, buffy coat and blood-derived extracellular vesicles from people without suspected bloodstream infection; (iv) brain tissue and cerebrospinal fluid; and (v) other sterile sites, including adipose tissue, liver, kidney, non-infected heart valve, atherosclerotic plaque, thrombus, aneurysm wall, synovial fluid, intraocular fluid, follicular fluid, and non-tumour breast and lung tissue. We excluded animal and in-vitro studies, diagnostic metagenomics for suspected infection, studies using culture or targeted PCR only, reviews and protocols, and studies of mucosal or high-biomass sites only (stool, oral, vaginal, airway and urine samples and colorectal, gastric, oesophageal, head-and-neck, cervical and bladder tumours).

### Search and screening
Two searches of Europe PMC were run: a broad search and a narrower search with tissue-specific phrases and title exclusions. Each combined a microbiome or sequencing term block with tissue term blocks and was restricted to open-access full texts; preprints were removed (full strategies in Supplementary File S2). Both searches were run on 22 November 2026 and re-run unchanged on 23 November 2026. Records were merged and de-duplicated by PMCID, DOI and PMID. An AI agent (Claude, Anthropic) read every title and, when the title did not settle the decision, the abstract, and logged a decision (include, unclear or exclude) with a reason for each record; a keyword pre-sort only suggested reasons. Records marked include or unclear went to full-text assessment.

### Data extraction
Open-access full texts (JATS XML) were split into numbered evidence elements (paragraphs, figure and table captions, table rows). For each study the AI agent recorded tissue; data source (own samples, or re-use of public data such as The Cancer Genome Atlas); sequencing method; negative-control practice (sequenced; included but not sequenced or not stated to be sequenced; none mentioned); decontamination (none; removal of taxa found in the study's own controls; a statistical tool such as decontam [19] or SCRuB [20]; removal of taxa on a published contaminant list; abundance or prevalence filtering only); measurement of bacterial load; the authors' conclusion about a resident microbiome; and every genus presented as detected in the target samples after the authors' own filtering. Genera that authors removed or interpreted as contaminants were recorded separately and not counted. Every value carried an evidence identifier and a verbatim quote, and a script checked that each quote and each genus name occurred in its cited element. Supplementary tables (converted to text with markitdown) were used only when the main text named fewer than three genera. Genus names were validated against NCBI Taxonomy; misspellings and recent renames were adjudicated once on taxonomic grounds (Supplementary File S3b).

### Human verification
One reviewer checked a random 10% of eligible non-pilot studies (n = 46), all 21 pilot studies, 17 priority cases and a stratified random 5% of screening decisions (n = 175) against the source articles, and found complete agreement with the AI first pass.

### Contaminant reference lists
The reference lists were fixed before extraction from the tables of three studies that sequenced blank controls [5–7] (Supplementary File S3). The primary list (78 genera) contains the genera found in blank controls by Salter et al. [5], excluding 14 genera that are common human commensals or pathogens. The strict list (30 genera) contains primary-list genera also reported by at least one of the other two sources [6, 7]. The full Salter list (92 genera) and the union of all three sources (185 genera) were used for sensitivity analyses and description. Matching of reported genera to the lists was done by script, never by the extractor.

### Outcome and statistical analysis
The outcome was the study-level contaminant share: the number of primary-list genera divided by the number of counted genera, in studies reporting at least three genera. We fitted binomial logistic models with dispersion estimated from Pearson's χ² (quasi-binomial) and heteroscedasticity-robust (HC1) standard errors, with control practice, decontamination, tissue, sequencing method and publication year (per 5 years) as covariates. Under a pre-specified rule, because at least 30 studies used shotgun-type methods (shotgun metagenomics, metatranscriptomics or host-sequencing mining), the main model was restricted to these studies, 16S studies formed a secondary model, and H4 was tested in the pooled model containing a method term. H1 was also tested after excluding host-sequencing mining studies (co-primary analysis). A hypothesis was supported if the 95% confidence interval excluded the null value in the pre-specified direction, and robust if this also held in at least three of four sensitivity analyses: the strict list, the full Salter list, studies reporting at least 10 genera, and an unweighted linear model of the logit share. Further sensitivity analyses excluded each tissue in turn, studies whose genus profiles were partly shown only in figures, lists taken from supplements and re-analyses of public data. Analyses used Python 3 with statsmodels.

## Results

### Study selection and characteristics
The searches identified 3,462 unique open-access records. After title and abstract screening, 524 full texts were sought and 523 were assessed; 475 studies were eligible and 398 reported at least three genera (Supplementary Figure S1). The eligible studies were published between 2013 and 2026 and covered tumours (n = 234), blood (n = 109), placental and fetal samples (n = 64), other sterile sites (n = 53) and brain or cerebrospinal fluid (n = 15) (Table 1). Most used 16S sequencing (n = 338); 76 mined host sequencing data, 34 used shotgun metagenomics and 27 used other or mixed methods. Seventy-five studies re-analysed public data, mostly from The Cancer Genome Atlas. The 398 usable studies reported a median of 10 genera each (5,978 genus records in total).

### Control practice
Half of the eligible studies (239 of 475, 50%) mentioned no negative controls, 167 (35%) sequenced them, and 69 (15%) included controls that were checked only by PCR or gel or were not stated to be sequenced (Table 1). Sequenced controls were reported in 62% of placental and fetal studies and 67% of brain and cerebrospinal fluid studies, but in only 27% of tumour studies and 30% of blood studies. Of the 75 re-analyses of public data, 71 mentioned no controls; among the 400 studies of the authors' own samples, 168 (42%) mentioned none. The proportion of studies that sequenced controls did not rise over time (2012–2016, 6 of 15; 2017–2020, 26 of 70; 2021–2023, 62 of 152; 2024–2026, 73 of 238). More than half of the studies applied no decontamination (267, 56%), although the use of statistical decontamination tools increased (2012–2016, 1 of 15; 2024–2026, 50 of 238). Only 75 studies (16%) measured bacterial load. In 435 of 475 studies (92%) the authors concluded that a microbial community was present in the sampled site.

### Contaminant genera in published profiles
A median of 19% (interquartile range 6–29%) of the genera reported by each study were primary-list contaminant genera, and 77% of studies reported at least one (Figure 1). Across all studies, 19.8% of reported genera were contaminant genera. With the strict list the median share was 11% (68% of studies reporting at least one), and with the full Salter list 40% (93%). Median shares were similar across tissues: 0.20 for tumours, 0.23 for other sterile sites, 0.18 for blood, 0.14 for brain and cerebrospinal fluid, and 0.12 for placental and fetal samples. The contaminant genera most often reported were *Sphingomonas* (97 studies), *Bacillus* (79), *Ralstonia* (70), *Methylobacterium* (52), *Burkholderia* (50), *Brevundimonas* (46), *Bradyrhizobium* (44) and *Rhodococcus* (38), and the same genera led in every tissue group (Figure 1C). Thirty-four usable studies named genera that they removed or interpreted as contaminants.

### Pre-specified hypotheses
In the main shotgun-type model (94 studies, 75 of which reported no controls), no hypothesis was supported (Table 2). Studies with no controls did not differ from studies with sequenced controls (odds ratio [OR] 0.64, 95% CI 0.37–1.09; H1); nor did decontamination (OR 0.66, 0.39–1.09; H2) or publication year (OR 0.74 per 5 years, 0.51–1.09; H3) show an association. The co-primary H1 analysis excluding host-sequencing mining studies (26 studies) was also null (OR 0.85, 0.45–1.60). In the pooled model (398 studies), shotgun-type and 16S studies did not differ (OR 0.77, 0.59–1.00; H4).

The pooled model showed an association in the direction opposite to H1: studies that mentioned no negative controls reported a lower contaminant share than studies that sequenced their controls (OR 0.63, 95% CI 0.48–0.83). This association held with the strict list (OR 0.67, 0.51–0.89) and the full Salter list (OR 0.57, 0.42–0.78), in studies reporting at least 10 genera (OR 0.59, 0.43–0.81), in the unweighted model of the logit share (β = −0.48, −0.75 to −0.20), after excluding host-sequencing mining studies (OR 0.69, 0.50–0.94) or re-analyses of public data (OR 0.66, 0.48–0.91), and among 16S studies only (OR 0.65, 0.45–0.93). Including controls without sequencing them was not associated with the share (OR 0.87, 0.61–1.22). Decontamination was associated with a lower share in the pooled model (OR 0.74, 0.55–0.99), but this was not robust: the confidence interval excluded 1 in only two of four sensitivity analyses. All model estimates are given in Supplementary File S5.

## Discussion

About one in five genera reported from human tumours, blood, placenta and other low-biomass sites belongs to a fixed set of genera found in laboratory blank controls, and three quarters of studies report at least one of them. The same few genera — *Sphingomonas*, *Ralstonia*, *Bacillus*, *Methylobacterium*, *Burkholderia* and *Bradyrhizobium* — recur across unrelated tissues, diseases and laboratories, which is the pattern expected from shared reagent contamination [5–7] rather than from tissue-specific biology. At the same time, half of these studies report no negative controls, only a third sequence them, few measure biomass, and these proportions have not improved despite widely discussed retractions [12, 13] and published guidance [7, 15, 16]; yet nine in ten studies conclude that a microbiome is present.

Our main hypothesis was not supported, and in the pooled analysis the association ran the other way: studies that sequenced their negative controls reported more known contaminant genera, not fewer. Three explanations are plausible and not mutually exclusive. First, sequencing controls makes contaminants visible, and many authors then report them as detected taxa or alongside caveats, whereas studies without controls tend to report only differentially abundant or disease-associated genera. Second, studies without controls are dominated by re-analyses of host sequencing data, in which reported taxa reflect reference databases and analysis pipelines [13] more than reagents; however, the reversed association persisted after these studies were excluded. Third, laboratories that sequence controls more often study the lowest-biomass sites, such as placenta and brain, where contaminants form a larger share of any signal [8, 11]. Whatever the mechanism, the result shows that "negative controls included" is not a sufficient marker of quality. What matters is whether control results are reported and used to remove or flag taxa.

These findings have practical implications. Journals and reviewers could require low-biomass studies to report the sequencing results of their negative controls, to list genera removed as contaminants with the method used [19, 20], and to state which reported genera appear on published contaminant lists. A machine-readable contaminant reference matched by script, as used here, could become a routine check during peer review.

### Strengths and limitations
The protocol, contaminant lists and analysis code were fixed before the analysis, every extracted value is linked to a verbatim quote that was checked automatically, and the audit spans five tissue groups and 475 studies. The study has limitations. Only open-access studies were included. Screening and extraction were done by an AI agent and verified by one reviewer on a random 10% sample plus the pilot studies. Most studies show their full genus profiles only in figures, so the genera named in text and tables are a subset, and some studies report only differentially abundant genera. The unit of analysis is the published study, not the cohort, and unconfirmed overlaps between cohorts were not merged. The contaminant lists come from three laboratories and specific kits, and some listed genera, such as *Bacillus*, may be genuinely present in some samples; the contaminant share is therefore a marker of contamination risk rather than proof. The associations are observational.

### Conclusions
Known laboratory contaminant genera are a routine part of published human "sterile-site" microbiomes, and the use of negative controls has not improved. Reporting the results of controls and flagging contaminant genera, not just stating that controls were included, should become standard for low-biomass microbiome studies.

---

## Declarations

**Use of artificial intelligence.** Title and abstract screening, full-text data extraction and the first draft of this manuscript were produced with an AI agent (Claude, Anthropic), under a pre-registered protocol and with automatic source checks. A human reviewer verified a random sample of screening decisions and extractions. The authors reviewed and take responsibility for the content.

**Ethics approval and consent.** Not applicable; the study used only published, open-access articles.

**Data and code availability.** Search logs, screening decisions, extractions with evidence quotes, analysis code and all results are available in the project repository [repository URL / DOI to be added before submission]. Copyrighted full texts are not redistributed.

**Competing interests.** [Authors to confirm: none declared.]

**Funding.** [Authors to confirm: no specific funding.]

**Author contributions.** [Authors to confirm, e.g. AP: conceptualisation, methodology, data curation, verification, writing – review and editing; AD: supervision, writing – review and editing.]

---

## Figure and table legends

**Figure 1.** Contaminant genera in 398 human low-biomass microbiome studies. (A) Mean primary-list contaminant share (95% CI) by negative-control practice within each tissue group; numbers above bars are study counts. (B) Contaminant share by publication year: individual studies, the pooled proportion per year (years with at least three studies) and a descriptive logistic trend with 95% CI. (C) Percentage of studies in each tissue group reporting each strict-list contaminant genus.

**Table 1.** Characteristics of eligible (n = 475) and usable (n = 398) studies.

**Table 2.** Pre-specified model estimates for control practice, decontamination, publication year and sequencing method (odds ratios with 95% CI).

## Supplementary material

**Supplementary Figure S1.** Study selection flow diagram.
**Supplementary File S2.** Full search strategies and record counts.
**Supplementary File S3.** Contaminant reference lists with source evidence; S3b, genus-name adjudication.
**Supplementary File S4.** Study-level (S4a) and genus-level (S4b) data.
**Supplementary File S5.** All model, robustness and sensitivity estimates and hypothesis decisions.
**Supplementary File S6.** Protocol with dated amendments.

---

## References

1. Aagaard K, Ma J, Antony KM, Ganu R, Petrosino J, Versalovic J. The placenta harbors a unique microbiome. Sci Transl Med. 2014;6(237):237ra65. doi:10.1126/scitranslmed.3008599
2. Nejman D, Livyatan I, Fuks G, Gavert N, Zwang Y, Geller LT, et al. The human tumor microbiome is composed of tumor type-specific intracellular bacteria. Science. 2020;368(6494):973–980. doi:10.1126/science.aay9189
3. Riquelme E, Zhang Y, Zhang L, Montiel M, Zoltan M, Dong W, et al. Tumor microbiome diversity and composition influence pancreatic cancer outcomes. Cell. 2019;178(4):795–806.e12. doi:10.1016/j.cell.2019.07.008
4. Urbaniak C, Gloor GB, Brackstone M, Scott L, Tangney M, Reid G. The microbiota of breast tissue and its association with breast cancer. Appl Environ Microbiol. 2016;82(16):5039–5048. doi:10.1128/AEM.01235-16
5. Salter SJ, Cox MJ, Turek EM, Calus ST, Cookson WO, Moffatt MF, et al. Reagent and laboratory contamination can critically impact sequence-based microbiome analyses. BMC Biol. 2014;12:87. doi:10.1186/s12915-014-0087-z
6. Glassing A, Dowd SE, Galandiuk S, Davis B, Chiodini RJ. Inherent bacterial DNA contamination of extraction and sequencing reagents may affect interpretation of microbiota in low bacterial biomass samples. Gut Pathog. 2016;8:24. doi:10.1186/s13099-016-0103-7
7. Weyrich LS, Farrer AG, Eisenhofer R, Arriola LA, Young J, Selway CA, et al. Laboratory contamination over time during low-biomass sample analysis. Mol Ecol Resour. 2019;19(4):982–996. doi:10.1111/1755-0998.13011
8. Lauder AP, Roche AM, Sherrill-Mix S, Bailey A, Laughlin AL, Bittinger K, et al. Comparison of placenta samples with contamination controls does not provide evidence for a distinct placenta microbiota. Microbiome. 2016;4:29. doi:10.1186/s40168-016-0172-3
9. de Goffau MC, Lager S, Sovio U, Gaccioli F, Cook E, Peacock SJ, et al. Human placenta has no microbiome but can contain potential pathogens. Nature. 2019;572(7769):329–334. doi:10.1038/s41586-019-1451-5
10. Panzer JJ, Romero R, Greenberg JM, Winters AD, Galaz J, Gomez-Lopez N, et al. Is there a placental microbiota? A critical review and re-analysis of published placental microbiota datasets. BMC Microbiol. 2023;23:76. doi:10.1186/s12866-023-02764-6
11. Kennedy KM, de Goffau MC, Perez-Muñoz ME, Arrieta MC, Bäckhed F, Bork P, et al. Questioning the fetal microbiome illustrates pitfalls of low-biomass microbial studies. Nature. 2023;613(7945):639–649. doi:10.1038/s41586-022-05546-8
12. Poore GD, Kopylova E, Zhu Q, Carpenter C, Fraraccio S, Wandro S, et al. Microbiome analyses of blood and tissues suggest cancer diagnostic approach. Nature. 2020;579(7800):567–574. doi:10.1038/s41586-020-2095-1. Retraction in: Nature. 2024;631:694. doi:10.1038/s41586-024-07656-x
13. Gihawi A, Ge Y, Lu J, Puiu D, Xu A, Cooper CS, et al. Major data analysis errors invalidate cancer microbiome findings. mBio. 2023;14(5):e0160723. doi:10.1128/mbio.01607-23
14. Tan CCS, Ko KKK, Chen H, Liu J, Loh M, SG10K_Health Consortium, et al. No evidence for a common blood microbiome based on a population study of 9,770 healthy humans. Nat Microbiol. 2023;8(5):973–985. doi:10.1038/s41564-023-01350-w
15. Eisenhofer R, Minich JJ, Marotz C, Cooper A, Knight R, Weyrich LS. Contamination in low microbial biomass microbiome studies: issues and recommendations. Trends Microbiol. 2019;27(2):105–117. doi:10.1016/j.tim.2018.11.003
16. Fierer N, Leung PM, Lappan R, Eisenhofer R, Ricci F, Holland SI, et al. Guidelines for preventing and reporting contamination in low-biomass microbiome studies. Nat Microbiol. 2025;10:1570–1580. doi:10.1038/s41564-025-02035-2
17. Zakis DR, Paulissen E, Kornete L, Kaan AMM, Nicu EA, Zaura E. The evidence for placental microbiome and its composition in healthy pregnancies: a systematic review. J Reprod Immunol. 2022;149:103455. doi:10.1016/j.jri.2021.103455
18. Williamson EM, Hammer TJ, Hogendoorn K, Eisenhofer R. Blanking on blanks: few insect microbiota studies control for contaminants. mBio. 2025;16:e0265824. doi:10.1128/mbio.02658-24
19. Davis NM, Proctor DM, Holmes SP, Relman DA, Callahan BJ. Simple statistical identification and removal of contaminant sequences in marker-gene and metagenomics data. Microbiome. 2018;6:226. doi:10.1186/s40168-018-0605-2
20. Austin GI, Park H, Meydan Y, Seeram D, Sezin T, Lou YC, et al. Contamination source modeling with SCRuB improves cancer phenotype prediction from microbiome data. Nat Biotechnol. 2023;41:1820–1828. doi:10.1038/s41587-023-01696-w

*All references were checked against Europe PMC on 23 Nov 2026 (`manuscript/references_verified.json`). Page/issue details for Fierer 2025, Williamson 2025 and Austin 2023 should be confirmed against the journal's style at submission.*
