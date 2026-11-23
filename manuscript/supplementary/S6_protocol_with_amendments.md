# C6 protocol: Contamination audit of "sterile-site" human microbiome studies

*Version 0.8, 23 Nov 2026. Version 0.1 (commit daa04ef) was committed before any study results were extracted. Amendment 0.2 (commit d11b64e) was made after title/abstract screening of the v1 sample and before any full-text extraction. Amendment 0.3 was made after the pilot (section 9) and before full screening and extraction. Amendment 0.4 was committed on 23 Nov 2026 before full screening, before any non-pilot extraction and before any model was run. Amendment 0.5 was committed on 23 Nov 2026 after screening and full-text download, before any non-pilot extraction or model.*

**Amendment 0.8 (23 Nov 2026): genus-name review, H4 model and human-check result, made after extraction and the human check and before any model was run.**

1. **Genus-name review.** 51 extracted names were not NCBI Bacteria/Archaea genus names (`data/check_summary.json`). Each was adjudicated once, on taxonomic grounds only, in `reference/genus_name_review.csv` (41 rows): obvious misspellings are counted as the intended genus (e.g. *Norcadioides* → *Nocardioides*, *Lodobacter* → *Iodobacter*); validly named or *Candidatus* bacterial genera missing from current NCBI genus nodes are counted as written (e.g. *Bosea*, which NCBI now files as *Allobosea*; the name is kept so that it matches the fixed contaminant list); non-genus names are not counted (*Myxobacterium*, *Candidatus* Adlerbacteria). Composite names separated by "/" count as their first genus, as for hyphens (amendments 0.3 and 0.6). After review, 5 names are not counted (2 archaeal, 3 non-genus).
2. **H4.** The main analysis is the shotgun-class model (amendment 0.4 rule 7: 94 usable shotgun-class studies ≥ 30), which has no method term. H4 (16S vs shotgun) is therefore decided in the pooled model with a method term (model C), with its own four robustness analyses on the pooled data.
3. **Human check.** The project owner checked all 84 human-check packets (46 random eligible non-pilot papers, 21 pilot papers, 17 priority cases) and 175 screening decisions and reported 100% agreement, no corrections (`human_check/HUMAN_CHECK_RESULT.md`). The first-pass handling of the retracted record PMC9130323 (no usable genus list, so outside the models), the exclusion of PMC12922273 and the cohort-link decisions were accepted as recorded.
4. The analysis script `analysis/run_models.py` is frozen in the commit that adds this amendment (SHA-256 in `analysis/FROZEN.txt`), before its first run.

**Amendment 0.6 (23 Nov 2026): composite-name normalization, before rebuilding the full extraction dataset or running models.** A review of a new extraction showed that SILVA composite genus labels can use typographic dash characters (e.g. en dash), while the counting code split only ASCII hyphens. The extractor keeps the paper's exact spelling and evidence quote; dataset normalization treats Unicode hyphen/dash/minus characters as separators and counts the first genus, as already specified by amendment 0.3 rule 3. No eligibility, extraction, contaminant-list, or model rule changes.

**Amendment 0.7 (23 Nov 2026): case-insensitive taxonomic matching, before rebuilding the full extraction dataset or running models.** The same extraction audit found lowercase genus spellings in source text that were being excluded by an exact-case lookup. Extraction JSON and evidence retain the paper's spelling; dataset counting matches a genus to the canonical NCBI bacterial genus name case-insensitively. This affects name matching only and does not broaden genus eligibility.

**Amendment 0.5 (23 Nov 2026): extraction set-up, fixed after screening and full-text download and before any non-pilot extraction.** Screening result: 3,462 records; 423 include, 101 unclear (`screening/screening_counts.json`); OA XML obtained for 523/524 (`data/fulltext_download_log.csv`). No study data had been extracted when this was written.

1. **Extraction by parallel AI agents.** First-pass extraction is done by several Claude sub-agents in parallel, each working through a batch of papers with the same written instructions (`workflow/stage4/EXTRACTION_INSTRUCTIONS.md`) and the same per-paper packets (`workflow/stage4/build_packets.py`). The coordinating agent runs the automatic source checks (section 6.4) on every output and re-extracts or sets fields to "not reported" where checks fail. All outputs are provisional until the human check (amendment 0.4 rule 9). Pilot extractions are kept (amendment 0.4 rule 6) and receive the new fields below.
2. **Supplementary files and markitdown.** Supplements are taken from the PMC Open Access dataset on AWS (`pmc-oa-opendata`), because direct PMC/Europe PMC links failed. Accepted formats are widened to `.xlsx .xls .csv .tsv .txt .docx .doc .pdf` (≤ 25 MB) and every file is converted to Markdown with Microsoft **markitdown** (v0.1.9; `workflow/stage4/fetch_supplements.py`). The use rule of amendment 0.4 rule 4 is unchanged (supplements only when the main text gives fewer than 3 genera). Supplement evidence locator: `S<k>:L<line>` = line in `papers/<PMCID>/supp_md/S<k>.md`; the automatic check requires the genus name on that line.
3. **Re-use of public data (e.g. TCGA).** New field `data_source`: `own_samples` or `public_reuse` (with the dataset named, e.g. "TCGA via Poore 2020 / Kraken-TCGA"). Each paper stays the unit of analysis, because the audit asks what each paper reports after its own processing; the overlap rule of amendment 0.4 rule 3 (same group and cohort) is unchanged. **Pre-specified sensitivity analysis:** all section 8 main/H1 models re-run excluding `public_reuse` papers.
4. **Further new fields:** `list_type` (amendment 0.3), `figures_only` (`no` / `partial` / `yes`), `n_target_samples`, `eligible_fulltext` with reason, and `country` where stated.
5. **Genus dictionary:** NCBI Taxonomy new_taxdump downloaded 23 Nov 2026 (SHA-256 61710d80…090ea); Bacteria and Archaea genus names and synonyms in `reference/ncbi_genera.tsv` (`workflow/stage4/build_genus_dictionary.py`). Archaeal genera are logged but not counted (bacterial genera only, amendment 0.3 rule 3).

**Amendment 0.4 (23 Nov 2026): procedures for the full review, fixed before full screening, extraction and analysis.** No new study result had been seen when this was written (only the pilot, already reported).

1. **Search re-run (section 4).** The v1 and v2 searches were re-run unchanged on 23 Nov 2026 (`workflow/stage4/rerun_searches.py`, `search/rerun_2026-11-23/`). The OA record lists were identical to 22 Nov (3,380 and 782). Merged and de-duplicated by PMCID, then DOI and PMID: **3,462 unique records** (2,680 v1 only, 82 v2 only, 700 both; 3 without a PMCID, which have no PMC OA full text and are excluded). Script `workflow/stage4/merge_records.py`; counts `data/merge_counts.json`.
2. **Screening at scale.** A keyword pre-sort (`workflow/stage4/presort.py`) only *suggests* a reason (non-primary, animal/environment title, mucosal/high-biomass title, diagnostic/infection title, no sequencing terms). The AI agent reads every title, and reads the abstract whenever the title alone does not settle the decision (always for records without a suggested reason). It logs decision (`include` / `unclear` / `exclude`), tissue category and a reason for every record (`screening/screening_log_full.csv`). The 300 decisions from the 22 Nov screening samples are carried over unchanged and labelled as such. Unclear records go to full text. If a record matches several tissue blocks, the category is set from the sampled site.
3. **Full text.** OA JATS XML for all `include` and `unclear` records (`workflow/epmc.py`). The full-text eligibility check (section 3) is mandatory and logged with a reason. **Overlapping samples:** when two eligible papers report the same samples (same group and same cohort, stated or obvious), the one with the longer genus list is kept and the link is recorded.
4. **Supplementary tables.** OA supplementary files listed in the XML with extension `.csv`, `.tsv`, `.txt`, `.xlsx` or `.xls` (≤ 25 MB each) are downloaded from PMC to the local-only `papers/<PMCID>/supp/` with URL, size and SHA-256. They are **used only for eligible papers whose main text yields fewer than 3 genera** (otherwise unusable): the agent may then take the genus list from a supplementary table that gives the genera detected in the target samples. Evidence IDs for supplements are `S<file#>:<sheet>:R<row>`, checked automatically like main-text IDs. Sensitivity analysis: excluding supplement-derived lists.
5. **Genus validation.** Each extracted genus is checked automatically against the NCBI Taxonomy genus names (public `taxdump`, downloaded once, date and SHA-256 logged). Names that are not NCBI genera of superkingdom Bacteria are not counted (amendment 0.3 rule 3); archaeal, fungal and viral genera are logged but not counted. Renamed genera are mapped with the fixed synonym table of `workflow/build_contaminant_list.py` (e.g. *Cutibacterium* → *Propionibacterium*); new renames needed for list matching are added only if listed in that table's source logic, otherwise names are kept as written.
6. **Pilot papers** are part of the full data set. Their extractions are kept, with `list_type` added (amendment 0.3).
7. **Coding for the models (section 8.2), fixed now:**
   - *Control practice:* reference level `sequenced`; levels `included_not_sequenced`, `none_mentioned`.
   - *Decontamination yes* = `removed_control_taxa`, `tool` or `literature_list`; *no* = `none`, `abundance_filter_only`, `unclear`.
   - *Tissue:* tumour (reference), placenta/fetal, blood, other (other sterile + brain/CSF, amendment 0.3). In any model data set, a tissue level with fewer than 5 studies is merged into "other" for that model.
   - *Method class:* `16S` = bacterial 16S amplicon (any region); `shotgun` = shotgun metagenomics, metatranscriptomics and host-sequencing mining; `other` = 2bRAD-M, other reduced-representation or multi-method designs (e.g. 16S + shotgun). The section 8.2 rule counts usable `shotgun` studies; if ≥ 30, the **main analysis** is the shotgun-class model (control practice + decontamination + tissue + year), and the 16S model is secondary.
   - *Year:* per 5 years, centred at 2020.
   - Quasi-binomial GLM fitted with Pearson-χ² scale and HC1 robust SEs (statsmodels); 95% Wald CIs.
   - If a control-practice level has fewer than 3 studies in a model's data set, that contrast is reported as not estimable (no merging).
8. **Pre-specified analyses, in order** (all with the primary list unless stated): (a) main model (per rule above); (b) H1 co-primary sensitivity: main model excluding host-sequencing mining studies; (c) pooled model with method term (all usable studies), with and without mining studies; (d) 16S model (secondary); (e) the four robustness analyses of section 8.4 as amended in 0.3 (strict list; primary + 14 human-associated Salter genera; ≥ 10 genera; unweighted linear model on logit share with 0.5 added); (f) leave-one-tissue-out; `full_profile` only; excluding papers with partly figure-only profiles; excluding supplement-derived lists; (g) secondary outcome: any primary-list genus in the top 5 (logistic, same covariates, studies that rank genera). The analysis script is frozen (committed, SHA-256 recorded) before it is first run on the full data. Any later change is a new dated amendment made before the changed run.
9. **Human-check packet.** A random 10% of eligible extracted papers (seed 6, excluding pilot papers) plus all 21 pilot papers, and a random 5% of screening decisions (seed 6, stratified by decision), are put in `human_check/` with the cited evidence. Agreement is reported after a person has checked them, before stage 6. Until then all screening and extraction data are labelled **provisional (AI first pass)**.
10. **Data-volume gate (stage 4):** the go/no-go rule 4 of section 9 applied to the real data: ≥ 150 usable studies, with ≥ 15 in at least 3 tissue categories. If it is not met, the review stops and reports before analysis.

**Amendment 0.3 (22 Nov 2026): changes from the pilot.** Pilot results: `pilot/pilot_report.md`. None of these changes uses the pilot's contaminant shares.

1. **Decontamination categories:** add `literature_list` (removal of taxa on a published contaminant list, without own controls) and `unclear`. For H2, "decontamination = yes" means `removed_control_taxa`, `tool` or `literature_list`.
2. **New field `list_type`:** `full_profile` (all or top-N genera of the target samples), `differential_only` (only genera that differ between groups) or `mixed`. Sensitivity analysis: `full_profile` studies only. In the pilot several papers named only differential genera.
3. **Counting rules:** SILVA composite names count as their first genus (e.g. *Burkholderia–Caballeronia–Paraburkholderia* → *Burkholderia*). Only bacterial genera are counted (fungal and viral names are not). Species names count as their genus. Genera the authors interpret as contamination are recorded as flagged even if not removed (e.g. a paper concluding there is no placental microbiome).
4. **Host-sequencing mining studies** (TCGA and similar re-mined RNA-seq/WGS) never have negative controls, so control practice and method are confounded. H1 is also tested **excluding host-sequencing mining studies**; this is a pre-specified co-primary sensitivity analysis.
5. **Brain / CSF is merged into "other sterile"** for the models (pilot projection: about 4 usable OA studies); it is still reported descriptively.
6. **Broad list is descriptive only.** In the pilot the broad list matched a median 76% of reported genera, because Glassing 2016's kit lists contain many gut and oral genera; it cannot separate studies. Sensitivity analyses use the primary and strict lists; sensitivity analysis 2 (section 8.4) is replaced by "primary list plus the 14 human-associated Salter genera" (i.e. full Salter 2014 list).
7. **Full-text eligibility check stays mandatory:** 1 of 20 title/abstract inclusions was a rat study and 1 was metaproteomics.

**Amendment 0.2 (22 Nov 2026): tighter search (v2), before the pilot.**

1. **Why:** screening of the fixed v1 sample (30 OA records per block, seed 6; `screening/screening_log_v1.csv`) found eligible records in tumour 7/30 (+1 unclear), placenta/fetal 0/30 (+1), blood 17/30, brain/CSF 0/30 and other 3/30 (+1). The placenta and brain blocks mostly caught animal, infant-gut, meconium and diagnostic CSF mNGS papers; 22/30 tumour records were mucosal (mostly colorectal) tumours.
2. **v2 search** (`workflow/run_search_v2.py`, `search/search_log_v2.json`): narrower tissue phrases (e.g. "placental microbiome", "brain tissue"); a human word required in the abstract; title exclusions for animals, diagnostic/case-report terms and, per block, off-target sites (mucosal tumours; meconium/infant/vaginal; gut). Brain and other blocks use a stricter microbiome block without "metagenomic" (which mainly caught diagnostic mNGS).
3. **v2 counts (22 Nov 2026):**

   | Block | PubMed | Europe PMC | Europe PMC OA full text (kept, non-preprint) |
   |---|---|---|---|
   | Tumour | 580 | 436 | 252 |
   | Placenta / fetal | 118 | 109 | 62 |
   | Blood | 279 | 244 | 157 |
   | Brain / CSF | 72 | 78 | 40 |
   | Other sterile | 714 | 599 | 298 |
   | **Unique OA records** | | | **782** |

4. **Screening sample and pilot** are now drawn from `search/epmc_oa_records_v2.csv` (same seed 6, 30 per block). The go/no-go projection (section 9, rule 4) uses v2 counts. The v1 screening log is kept as the record.
5. For the full review, the v1 and v2 searches will be combined and de-duplicated, so recall is not lost; the v2 search is used for the feasibility estimate because its precision can be measured cheaply.

**Rule:** secondary data only (published papers). Open-access full texts only. No lab work, no cloud use. Copyrighted full texts stay local (`sterile-site-contamination-audit/papers/`, local only: linked from `data_local/`).

**What exists at version 0.1:** the search (counts in section 5), the reference contaminant list (section 7), and the scripts. No study has been screened or extracted.

---

## 1. Question

Many papers report microbes in body sites that are normally sterile or nearly so: internal tumours, placenta, blood, brain. These samples hold very little microbial DNA, so DNA from extraction kits, reagents and the lab ("kitome") can make up most of the signal (Salter et al. 2014). Some high-profile findings have been withdrawn or contested for this reason (placenta: de Goffau et al. 2019; tumours: Poore et al. 2020, retracted 2024, after Gihawi et al. 2023).

**Across published human low-biomass microbiome studies, what share of the genera they report are known laboratory contaminants? Do studies without sequenced negative controls, or without decontamination, report more of them?**

### Pre-specified hypotheses

| ID | Hypothesis | Direction |
|---|---|---|
| **H1** | The contaminant share is higher in studies that did **not** sequence negative controls than in studies that did | one direction (higher without) |
| **H2** | The contaminant share is lower in studies that applied a decontamination step (removing taxa found in controls, or a tool such as decontam, SourceTracker, microDecon, SCRuB) | lower with decontamination |
| **H3** | The contaminant share falls with publication year (field awareness grew after Salter 2014 and Eisenhofer 2019) | falls |
| **H4** | The contaminant share differs between 16S amplicon and shotgun studies | two-sided (16S has more PCR reagent DNA; shotgun has more database misassignment) |
| **H5** (descriptive) | Share and control practice differ by tissue | none set |

**Also reported regardless of H1–H4:** the share of studies in each tissue and period that sequenced negative controls, applied decontamination, and measured biomass (qPCR).

---

## 2. Novelty check (stage 2)

Searched 22 Nov 2026: web search, Europe PMC and PubMed (queries and hits in `search/novelty_check_epmc.json`).

| Closest work | What it shows | Gap C6 fills |
|---|---|---|
| Fierer et al. 2025, *Nat Microbiol* 10:1570 (consensus guidelines) | How to prevent and report contamination in low-biomass studies | Guidance, not a measurement of the literature |
| "Blanking on blanks", *mBio* 2025 (PMC11980574) | Few insect microbiota studies use or sequence controls | Insects, not humans; counts control use, not contaminant taxa reported |
| Phyllosphere systematic review (plants) | Contamination controls rarely used | Plants; no taxon-level audit |
| Zakis et al. 2022 (placenta systematic review, 57 studies); Panzer et al. 2023 *BMC Microbiol* (re-analysis of 15 placenta 16S datasets); placenta/preterm review with 16S re-analysis (2026, PMID 42104576) | Placental genera overlap with contaminants; signal often indistinguishable from controls | One tissue; mostly narrative; no meta-regression on control practice |
| Oesophagogastric cancer microbiome review with quality assessment (2023, PMC10216300) | Reporting quality of one tumour type | One tumour type, mucosal (high-biomass) site |
| Gihawi et al. 2023 *mBio*; Poore et al. 2020 (retracted); Nejman et al. 2020 | Contamination and database errors in one large tumour dataset | One dataset, not a cross-study audit |
| Salter 2014; Glassing 2016; Weyrich 2019; Eisenhofer 2019 | Lists of contaminant genera found in blanks | The reference lists C6 uses; they do not audit published studies |

**Verdict: passes.** No quantitative cross-study, cross-tissue audit of reported contaminant genera in human low-biomass studies was found.

---

## 3. Eligibility

**Unit:** one paper (study). Papers re-using the same samples are linked; the most complete one is used.

### Include

1. Human samples from a target site (section 3.1).
2. Microbial community profiled by **sequencing**: 16S/18S/ITS amplicon, shotgun metagenomics or metatranscriptomics, or mining of host sequencing data (e.g. tumour WGS/RNA-seq) for microbial reads.
3. The paper aims to describe the microbes in that site (a "microbiome" or "microbial signature").
4. Peer-reviewed; published 2012–2026; English; **open-access full text** in Europe PMC / PMC.

### Exclude

- Diagnostic mNGS for a suspected infection (sepsis, meningitis, prosthetic joint infection). These belong to idea C1.
- Culture-only, qPCR-only, FISH or imaging-only studies.
- Animal, in-vitro, environmental studies; reviews, editorials, conference abstracts, preprints.
- Studies of high-biomass or mucosal sites only (stool, oral, vaginal, skin, airway swabs, colorectal/gastric/oesophageal/oral/cervical/bladder tumours).

### 3.1 Target sites (tissue categories)

| Category | Includes | Excludes |
|---|---|---|
| **Tumour** | Tumours of internal organs not open to a high-biomass mucosal surface: breast, pancreas, liver, bile duct, kidney, prostate, ovary, endometrium, thyroid, brain, bone, soft tissue, lung parenchyma, melanoma tissue | Colorectal, gastric, oesophageal, oral/head and neck, cervical, bladder tumours |
| **Placenta / fetal** | Placenta, membranes, amniotic fluid, cord blood, fetal tissue | Meconium, vaginal swabs |
| **Blood** | Whole blood, plasma, serum, buffy coat, blood cells in people without suspected bloodstream infection | Sepsis diagnostics |
| **Brain / CSF** | Brain tissue, CSF profiling studies | Diagnostic CSF mNGS for meningitis/encephalitis |
| **Other sterile** | Adipose, liver, kidney, heart valve, atherosclerotic plaque, thrombus, synovial fluid, intraocular fluid, follicular fluid, non-tumour breast and lung tissue | Bronchoalveolar lavage, sputum, urine |

---

## 4. Information sources

PubMed (E-utilities) and Europe PMC (REST API). Publication years 2012–2026. Searches for feasibility ran on 22 Nov 2026 and will be re-run at the start of full screening.

---

## 5. Search

Exact queries are in `search/search_log.json` (script `workflow/run_search.py`). Structure: **microbiome/sequencing block AND tissue block**, human, no reviews.

- PubMed: method block `(microbiome OR microbiota OR "16S rRNA" OR "16S rDNA" OR metagenom* OR "bacterial DNA" OR "microbial DNA")[tiab] AND (sequencing OR 16S OR metagenom*)[tiab]`, plus the tissue block, `NOT (animals[mh] NOT humans[mh])`, reviews/comments/editorials excluded, 2012–2026.
- Europe PMC: the same blocks in the abstract field, `NOT PUB_TYPE:"review"`, 2012–2026; the open-access subset adds `OPEN_ACCESS:Y AND HAS_FT:Y`. Preprints are dropped from the record list.

**Feasibility counts (22 Nov 2026):**

| Tissue block | PubMed | Europe PMC | Europe PMC open-access with full text |
|---|---|---|---|
| Tumour | 663 | 1,320 | 764 |
| Placenta / fetal | 598 | 1,550 | 822 |
| Blood | 274 | 353 | 231 |
| Brain / CSF | 829 | 1,356 | 778 |
| Other sterile | 815 | 1,692 | 880 |
| **Unique open-access records** | | | **3,380** |

The blocks are broad on purpose (e.g. "fetal" and "cerebrospinal fluid" catch many ineligible papers); screening removes them. The OA records are in `search/epmc_oa_records.csv`.

---

## 6. Screening and extraction (AI agent, as in R2)

1. **Title/abstract screening:** an AI agent (Claude) applies section 3 to each record and logs a decision, the tissue category and a one-line reason (`screening/screening_log.csv`). Unclear records go to full text.
2. **Full text:** the OA JATS XML is downloaded from Europe PMC (fallback: PMC E-utilities), with URL, date, size and SHA-256 logged (`workflow/epmc.py`). The text is split into numbered evidence elements (paragraphs, captions, table rows: `E0001`…).
3. **Extraction:** the agent fills the fields in section 6.1. Every field cites evidence ID(s) and a short verbatim quote.
4. **Automatic source checks** (`workflow/check_extraction.py`): each quote must appear in its cited element (whitespace- and case-normalised); each reported genus must appear in its cited element. Failures are fixed or the field is set to "not reported".
5. Contaminant matching is done by **script** against the fixed list, never by the agent. The agent records every genus the paper presents as detected in the target samples, not a selection.
6. All AI outputs are first passes. A person checks a random 10% (and all pilot papers) before analysis; agreement is reported.

### 6.1 Extraction fields

| Level | Field | Values |
|---|---|---|
| Study | id, PMCID, DOI, year, journal, country | |
| | tissue category, sub-site, disease/condition, n target samples | section 3.1 |
| | method | 16S (region) / shotgun / metatranscriptomic / host-sequencing mining / several |
| | DNA extraction kit; sequencing platform | free text |
| | **negative controls** | `none_mentioned` / `included_not_sequenced` (or sequencing not stated) / `sequenced` |
| | control types | extraction blank, PCR no-template, sampling/field blank, other |
| | n controls sequenced; control results reported (yes/no) | |
| | **decontamination** | `none` / `removed_control_taxa` (manual) / `tool` (name) / `abundance_filter_only` |
| | biomass measured (qPCR or similar) | yes/no |
| | positive control / mock community | yes/no |
| | authors' conclusion | resident microbiome claimed / not claimed / unclear |
| Genus | genus name (as written), location (text / table / caption), rank or abundance if given | one row per genus reported as detected in target samples, after the authors' own filtering |
| | flagged by authors as contaminant | yes/no (flagged genera that the authors removed are **not** counted as reported) |

**"Reported genera"** = genera named in the Results text, tables, figure captions or open-access supplementary tables as detected in the target samples. Genera that appear only inside figure images cannot be read from the XML; the number of papers affected is recorded. Names below genus are mapped to their genus; family-only names are not counted. Renamed genera are mapped (e.g. *Cutibacterium* → *Propionibacterium*; *Escherichia–Shigella* → *Escherichia*).

---

## 7. Reference contaminant list (fixed before extraction)

Built by `workflow/build_contaminant_list.py` from the open-access full texts of three sources; each genus links to an evidence ID in the source. Output: `reference/contaminant_genera.csv` (185 genera in the union).

| Source | What | Genera |
|---|---|---|
| Salter et al. 2014, *BMC Biol* 12:87, Table 1 | Genera in sequenced blank controls, 3 labs, 4 years | 92 |
| Glassing et al. 2016, *Gut Pathog* 8:24, Tables 1–2 | Genera in blood and soil DNA extraction kits | 113 |
| Weyrich et al. 2019, *Mol Ecol Resour* 19:982, Table 1 | Dominant genera in extraction blanks and no-template controls | 40 |

Eisenhofer et al. 2019 (*Trends Microbiol*) and de Goffau et al. 2019 (*Nature*) are not used as list sources: the first is not open access and the second gives its contaminant list only in supplementary figures.

**Three lists:**

- **Primary ("environmental"), 78 genera:** Salter 2014 genera, minus 14 genera that are dominant human gut/oral/skin/vaginal members or major pathogens (*Abiotrophia, Acinetobacter, Brevibacterium, Corynebacterium, Enterobacter, Escherichia, Facklamia, Kingella, Kocuria, Micrococcus, Propionibacterium, Pseudomonas, Stenotrophomonas, Streptococcus*). A hit on these is weak evidence of contamination in a human tissue.
- **Strict, 30 genera:** primary genera also found in Glassing 2016 or Weyrich 2019 (e.g. *Ralstonia, Bradyrhizobium, Burkholderia, Methylobacterium, Sphingomonas, Afipia, Cupriavidus, Novosphingobium, Pelomonas*).
- **Broad, 185 genera:** every genus in any source, including human-associated ones (sensitivity analysis only; Glassing's kit lists contain many gut genera).

The human-associated exclusion set is written in the script and was fixed on 22 Nov 2026 before extraction.

---

## 8. Analysis

### 8.1 Outcome

**Study-level contaminant share** = reported genera on the primary list ÷ all reported genera (genus-level names).

Secondary outcomes: the same share with the strict and broad lists; **any primary-list genus among the 5 most abundant reported genera** (yes/no; only for studies that rank genera).

### 8.2 Models

- **Primary model:** binomial GLM (logit), successes = contaminant genera, trials = reported genera, scale estimated from Pearson χ² (quasi-binomial), robust (HC1) standard errors:
  `share ~ control practice (none_mentioned / included_not_sequenced / sequenced) + decontamination (yes/no) + tissue + method (16S / shotgun / other) + year (per 5 years)`.
- **Method rule (main vs secondary):** if **≥ 30** eligible shotgun (or host-sequencing) studies have a usable genus list, the shotgun studies form the **main analysis** and 16S studies the secondary one (same model without the method term). If fewer than 30, the pooled model above is the main analysis and shotgun results are descriptive.
- Studies with fewer than 3 reported genera are excluded from the share models (counted in the flow diagram).

### 8.3 Decision rules (fixed)

| Hypothesis | Supported if |
|---|---|
| H1 | Odds ratio, `none_mentioned` vs `sequenced`, > 1 with 95% CI excluding 1 in the main model |
| H2 | Odds ratio for decontamination < 1 with 95% CI excluding 1 |
| H3 | Year coefficient < 0 with 95% CI excluding 0 |
| H4 | Method term (16S vs shotgun) 95% CI excludes 1, either direction |

An effect counts as **robust** if its direction holds and its CI excludes the null in at least 3 of the 4 sensitivity analyses below.

### 8.4 Sensitivity analyses

1. Strict list; 2. Broad list; 3. Only studies reporting ≥ 10 genera; 4. Unweighted linear model on logit share (0.5 added to counts).
Also: leave-one-tissue-out; excluding host-sequencing mining studies; excluding studies whose genera are in figures only for part of the profile.

### 8.5 Main figure

Panel A: contaminant share (mean and 95% CI) by control practice within each tissue. Panel B: share by publication year with the fitted trend. Panel C: heatmap of how often each strict-list genus is reported, by tissue.

---

## 9. Pilot and go / no-go

**Pilot:** 20 open-access papers, 4 per tissue category, taken in a fixed random order (seed 6) from `search/epmc_oa_records.csv` and screened until 4 eligible papers per category are found. Before the pilot, a random 30 records per category are title/abstract screened to estimate eligibility rates.

**GO if all hold:**

1. ≥ 60% of eligible pilot papers give a usable genus list (≥ 3 genera from text/tables/captions).
2. Control practice can be classified in ≥ 80% of pilot papers.
3. ≥ 95% of extracted quotes pass the automatic source check.
4. Projected eligible OA studies ≥ 150 in total, with ≥ 15 in at least 3 tissue categories (projection = category OA count × screened eligibility rate × pilot usable rate).

**NO-GO** if 1 or 4 fails. If only 2 or 3 fails, revise the extraction instructions and repeat the pilot once.

---

## 10. Risks

| Risk | Mitigation |
|---|---|
| Many studies show genera only in figures or report only the top few genera | Count affected papers; secondary binary outcome uses the top 5 only; sensitivity with ≥ 10 genera |
| Denominators differ (top-10 vs full lists) | Binomial weighting; ≥ 10-genera sensitivity |
| Some list genera can be real (e.g. *Methylobacterium* in tissue) | The share is a contamination **risk** marker, not proof; three lists |
| The list comes from 3 labs and specific kits | Strict list needs ≥ 2 sources; kitome varies by kit and lot (stated as a limitation) |
| Confounding: newer studies use controls and also better kits | Year in the model; descriptive tables by period |
| Many studies are 16S | Method rule in 8.2 |
| Open-access only | Compare the OA share by tissue with all records; state as a limitation |
| AI extraction errors | Evidence IDs, automatic source checks, human check of 10% |

---

## 11. Files

| Path | What |
|---|---|
| `workflow/epmc.py` | Search, full-text download, evidence index |
| `workflow/run_search.py` | Feasibility search; writes `search/search_log.json`, `search/epmc_oa_records.csv` |
| `workflow/build_contaminant_list.py` | Builds `reference/contaminant_genera.csv` |
| `workflow/check_extraction.py` | Automatic source checks and contaminant matching (written for the pilot) |
| `screening/`, `pilot/` | Screening log and pilot extractions |
| `papers/` | OA full texts (local only, local only: linked from `data_local/`) |
