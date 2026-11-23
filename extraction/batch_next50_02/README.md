# C6 second 50-paper batch — 23 Nov 2026

50 further downloaded include records reviewed in one agent using Markdown and native source verification. Convenience selection continues by shortest available reading copies; this is not representative sampling.

- 47 records added to canonical extraction, including two study exclusions (protocol; qPCR-only) and one same-cohort duplicate exclusion.
- 39 additional usable studies with ≥3 counted bacterial genera.
- Three records held outside canonical data: PMC5610236 (diagnostic intra-amniotic infection scope), PMC12072589 (TCGA-CESC blood-versus-tumour source), and PMC12922273 (unidentified microbial sequencing/database provenance).
- All merged records pass the existing source checker. For the cohort duplicate, the complete eligible extraction was checked before exclusion, so exclusion did not bypass initial quote/genus checking.
- PMC8971327 explicitly follows the same 33-woman cohort in PMC4971513, using a 27-slide-review subset. PMC4971513 has the longer named-genus list and is retained under the protocol overlap rule.
- Other overlap leads remain explicit in `cohort_review.json`; shared assays or sample size alone were not used to exclude studies.
- Available supplements were downloaded and converted using installed markitdown. Several supply only read counts, clinical information, primer lists, or higher-rank plots. No unsupported figure transcription was inserted into the source-checked genus lists.
- The main-text review distinguishes human from mouse results, target blood/tissue from gut/airway results, and post-filter bacterial profiles from control-only, culture-only, viral and archaeal labels. The early-pregnancy placental pilot PMC9892641 was confirmed to contain actual results despite present-tense methods.

Five eligible records still have fewer than three recovered genera. Some additional image-only profile labels require visual review. Missing genus names are not biological nondetection. Some specimen counts and compartment attribution remain flagged; no count was inferred by doubling a participant total without source support.

Dataset after rebuild: 319 extracted, 303 eligible, 256 usable; zero automatic source failures. 204 downloaded papers remain outside canonical extraction, including held records. Human checks and final overlap resolution remain outstanding. No models were run.

Files: `selection.json`, `batch_summary.csv`, `batch_report.json`, `cohort_review.json`, `supplement_retrieval_log.json`, and per-paper JSON snapshots. Canonical records are in `extraction/json/`.
