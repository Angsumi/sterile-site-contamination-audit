# C6 full-text extraction instructions (protocol v0.5, sections 3, 6 and amendments 0.3–0.5)

You are an AI extraction agent doing a **first-pass** extraction for a systematic audit of contaminant
genera reported in human "sterile-site" (low-biomass) microbiome studies. A person will check a sample
later. Work only from the paper's own open-access full text. Never guess: if something is not stated,
use the "not stated" value defined below.

Working directory: `projects/sterile-site-contamination-audit/` (all paths below are relative to it).
Use the project Python: `.venv/bin/python`.

## Inputs per paper

- `papers/<PMCID>/packet.md` — reading aid: abstract, keyword windows of methods/controls passages,
  every NCBI bacterial genus name found in the paper with the evidence IDs and sections where it occurs,
  figure/table captions, list of supplements. **Start here.**
- Full evidence elements (paragraphs, captions, table rows), each with a stable ID `E0001…`:
  `.venv/bin/python workflow/show_el.py <PMCID> E0012 E0013` (prints full text; `MAX=4000` env for long ones).
  To search the whole paper: `.venv/bin/python workflow/stage4/grep_el.py <PMCID> "<regex>"`.
- Supplements converted to Markdown (only some papers): `papers/<PMCID>/supp_md/S<k>.md`.
  **Use a supplement only if the main text gives fewer than 3 genera** (rule 4, amendment 0.4).
  Supplement evidence locator = `S<k>:L<line>` (1-based line number in that .md file; `grep -n` gives it).

## Output

Write one JSON file per paper: `extraction/json/<PMCID>.json`, then run
`.venv/bin/python workflow/stage4/check_one.py <PMCID>` and fix every `FAIL` (quotes must be copied
**verbatim** from the cited element; a genus must appear in its cited element). `WARN` lines are information.

```json
{
 "pmcid": "PMC123",
 "tissue_category": "tumour | placenta_fetal | blood | brain_csf | other_sterile",
 "sub_site": "e.g. breast tumour; placenta; plasma; aqueous humour",
 "year": 2023,
 "country": "where samples were collected, or ''",
 "eligible_fulltext": true,
 "exclusion_reason": "",
 "data_source": {"value": "own_samples | public_reuse", "dataset": "e.g. TCGA (Poore 2020 Kraken data)", "evidence": [{"id": "E0010", "quote": "..."}]},
 "method": {"value": "16S | shotgun | metatranscriptomic | host_seq_mining | 2bRAD-M | 16S+shotgun | other", "region": "V3-V4 or ''", "evidence": [...]},
 "controls": {"value": "sequenced | included_not_sequenced | none_mentioned", "types": "extraction blank; PCR NTC; sampling blank; ...", "n_sequenced": null, "evidence": [...]},
 "decontamination": {"value": "none | removed_control_taxa | tool | literature_list | abundance_filter_only | unclear", "tool": "decontam / SCRuB / SourceTracker / microDecon / ...", "evidence": [...]},
 "biomass_qpcr": {"value": "yes | no", "evidence": [...]},
 "n_target_samples": 40,
 "list_type": "full_profile | differential_only | mixed",
 "genera": [{"name": "Ralstonia", "evidence_id": "E0021", "flagged_contaminant": false}],
 "top5": ["Ralstonia", "..."],
 "figures_only": "no | partial | yes",
 "authors_conclusion": "claimed | not_claimed | unclear",
 "notes": "short notes on anything unusual",
 "extractor": "AI agent (Claude, sub-agent batch NN)",
 "date": "2026-11-23"
}
```

Evidence objects are `{"id": "<evidence ID>", "quote": "<verbatim substring of that element, 8–250 chars>"}`.

## Rules

### 1. Full-text eligibility (protocol section 3; check every paper)
Eligible only if ALL hold:
- **Human** samples from a target site: internal tumours not open to a mucosal surface (breast, pancreas,
  liver, bile duct tissue, kidney, prostate, ovary, endometrium, thyroid, brain, bone, soft tissue, lung
  parenchyma/lung tumour tissue, melanoma tissue, lymphoma tissue, adrenal, thymus, lacrimal gland);
  placenta / fetal membranes / amniotic fluid / cord blood / fetal tissue; blood (whole blood, plasma,
  serum, buffy coat, serum/plasma EVs) in people **without suspected bloodstream infection**; brain
  tissue / CSF profiling; other sterile tissue (adipose, liver, kidney, heart valve without infective
  endocarditis, atherosclerotic plaque, thrombus, aneurysm wall, synovial fluid/tissue, intraocular fluid,
  follicular fluid, non-tumour breast or lung tissue, skeletal muscle).
- Microbial **community profiling by sequencing** (16S/other amplicon, shotgun, metatranscriptomics,
  2bRAD-M, or mining of host RNA-seq/WGS/WES for microbial reads, including re-analysis of TCGA/GEO data).
- Aim is to describe the microbes in that site.
Exclude (set `eligible_fulltext: false`, give `exclusion_reason`, fill only pmcid/tissue_category/year): animal or in-vitro
only; diagnostic mNGS for suspected infection (sepsis, meningitis, endocarditis, PJI, endophthalmitis);
culture/qPCR/FISH/ddPCR-only; reviews/protocols; only mucosal or high-biomass samples (stool, oral, vaginal,
airway/BAL/sputum, urine, bile only, colorectal/gastric/oesophageal/oral/head-neck/cervical/bladder tumours);
virome-only or fungi-only. Papers with several sample types are eligible if at least one target site is
profiled — then extract **only the target-site samples** (e.g. lung tumour tissue, not BALF; blood, not stool).
Pan-cancer re-analyses: eligible if they report genera for at least one eligible tumour type; extract only
the eligible tumour types and say which in `sub_site`.

`tissue_category`: the target site you extract. If several target sites, choose the one with the most
samples and note the others.

### 2. data_source
`public_reuse` when the microbial profiles come from data generated by others (TCGA, GEO, SRA, cBioPortal,
TCMA, "Kraken-TCGA", Poore et al. data, ORIEN); name the dataset. Otherwise `own_samples`.

### 3. method
`host_seq_mining` = microbial reads mined from host RNA-seq/WGS/WES (TCGA-style) or single-cell RNA-seq.
`shotgun` = shotgun metagenomics of extracted DNA (incl. plasma cfDNA metagenomics, mNGS used for profiling).
`metatranscriptomic` = RNA-based microbial profiling designed as such. `16S+shotgun` if both produce genus results.
`other` = anything else (e.g. ITS+16S is still 16S if bacterial genera come from 16S).

### 4. controls (the key variable — read the methods carefully)
- `sequenced`: negative controls (extraction blanks, no-template PCR controls, sampling/air/reagent blanks)
  were **sequenced** alongside samples (stated, or their sequencing results/reads reported).
- `included_not_sequenced`: negative controls mentioned but only checked by PCR/gel/qPCR, or it is not
  stated that they were sequenced.
- `none_mentioned`: no negative control mentioned (typical for TCGA re-analyses). Evidence may be empty.
Positive controls/mock communities do NOT count as negative controls.

### 5. decontamination
- `removed_control_taxa`: taxa found in the paper's own controls removed (manually or by rule).
- `tool`: decontam, SCRuB, SourceTracker, microDecon, MicrobIEM, or similar statistical tool; also
  batch-/plate-based contaminant removal (Poore-style); give the tool name.
- `literature_list`: taxa removed because they are on a published contaminant list, without own controls.
- `abundance_filter_only`: only prevalence/abundance thresholds.
- `none`: nothing stated. `unclear`: something done but not interpretable.
If several apply, choose in this order: removed_control_taxa or tool (pick the main one) > literature_list > abundance_filter_only.

### 6. biomass_qpcr
`yes` if bacterial load was measured (16S qPCR/ddPCR, total bacterial DNA quantification) in target samples.

### 7. genera (counting rules — protocol 6.1 and amendment 0.3)
Record **every genus the paper presents as detected in the target samples** after the authors' own
filtering, from Results text, tables, figure captions (and supplements only under the < 3 rule):
- one entry per genus (first good evidence ID, preferably Results/table/caption);
- species names count as their genus (*Cutibacterium acnes* → `Cutibacterium`); write the genus name
  exactly as spelled in the paper; SILVA composites count once as written (e.g. `Burkholderia-Caballeronia-Paraburkholderia`,
  `Escherichia-Shigella`) — the script maps them;
- family-, order- or phylum-only names are NOT genera; fungal, viral, archaeal names are not recorded;
- do NOT record genera that are only mentioned in the Introduction/Discussion as literature, only in
  methods (e.g. mock community, positive control strains, culture standards), or only detected in
  stool/oral/other non-target samples or in negative controls;
- genera that the authors identified as contaminants: if **removed**, record with `"flagged_contaminant": true`;
  if they remain in the reported profile but the authors interpret them as contamination, also set
  `true` (amendment 0.3 rule 3);
- include genera that differ between groups AND genera described as dominant/most abundant/core.
`list_type`: `full_profile` if the paper lists all or the top-N genera of the target samples;
`differential_only` if it only names genera that differ between groups; `mixed` otherwise.
`top5`: the five most abundant genera in the target samples, only if the paper ranks them (else `[]`).
`figures_only`: `yes` if the genus-level profile is shown only in figures (no names in text/tables), `partial`
if the text names only some of the genera shown in figures, `no` otherwise.

### 8. authors_conclusion
`claimed` = authors conclude a resident/true microbiome or microbial signal exists in the site;
`not_claimed` = they conclude it is absent or indistinguishable from contamination; `unclear` otherwise.

## Pace and quality
- Typical paper: read packet, open 3–8 key elements with show_el.py, write JSON, run check_one.py.
- Prefer completeness of the genus list over speed; do not invent quotes.
- When finished with your batch, run `check_one.py` on all your PMCIDs and report: PMCIDs done, how many
  eligible, any paper you could not resolve and why (one line each).
