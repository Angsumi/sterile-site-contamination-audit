# C6 final analysis report (stage 5): contaminant genera in human "sterile-site" microbiome studies

*23 Nov 2026. Protocol v0.8 (`C6_protocol.md`). Analysis script frozen before its first run on the full data
(`analysis/FROZEN.txt`, commit 9a3c032). Every number below is traceable to the file named in brackets.*

## 1. Data flow

| Step | Count | Source |
|---|---:|---|
| Unique Europe PMC open-access records (v1 + v2 searches, re-run 23 Nov 2026) | 3,462 | `data/merge_counts.json` |
| Title/abstract: include / unclear / exclude | 423 / 101 / 2,938 | `screening/screening_counts.json` |
| OA full texts obtained | 523 of 524 | `data/fulltext_download_log.csv` |
| Eligible on full text | 475 | `data/check_summary.json` |
| Usable (≥ 3 counted bacterial genera) — analysis set | **398** | `data/studies.csv` (`usable`) |
| Automatic source-check failures | 0 | `data/check_summary.json` |
| Human check (84 extraction packets, 175 screening decisions) | 100% agreement | `human_check/HUMAN_CHECK_RESULT.md` |

Usable studies by tissue: tumour 206, blood 85, placenta/fetal 50, other sterile 46, brain/CSF 11 (merged into
"other" for models). Data-volume gate (≥ 150 usable, ≥ 15 in ≥ 3 tissues) met. [`results/table1_characteristics.csv`]

## 2. What the literature does (eligible studies, n = 475) [`results/table1_characteristics.csv`, `results/descriptives.json`]

- **Negative controls:** sequenced 167 (35%), included but not sequenced 69 (15%), **none mentioned 239 (50%)**.
  Of the 75 public-data re-analyses (mostly TCGA-style host-sequencing mining), 71 mention no controls; among the
  400 studies of own samples, 168 (42%) mention none (`data/studies.csv`, crosstab of `data_source` × `controls`).
- **Decontamination:** none 267 (56%); a tool 87; removal of control taxa 62; literature list 8; abundance filter only 27; unclear 24.
- **Biomass measured (qPCR or similar):** 75 (16%).
- **Method:** 16S 338; host-sequencing mining 76; shotgun 34; 2bRAD-M 14; other/mixed 13.
- **Reporting:** in 406 of 475 the text names only part of a profile that is shown in figures (`figures_only = partial`);
  86 give a full or top-N profile; 60 name only genera that differ between groups.
- **Over time** the share of studies sequencing controls did not rise: 2012–16 6/15, 2017–20 26/70, 2021–23 62/152,
  2024–26 73/238 (`controls_by_period`).

## 3. How often contaminant genera are reported (usable studies, n = 398) [`results/descriptives.json`]

| List | Median share of reported genera (IQR) | Studies with ≥ 1 listed genus |
|---|---|---:|
| Primary (78 environmental kit/reagent genera) | **0.19 (0.06–0.29)** | **77%** |
| Strict (30 genera in ≥ 2 sources) | 0.11 (0.00–0.22) | 68% |
| Full Salter 2014 list (92) | 0.40 (0.25–0.57) | 93% |
| Broad (185; descriptive only) | 0.71 (0.57–0.88) | 99% |

Pooled across all studies, 19.8% of reported genera are primary-list contaminant genera (`pooled_proportion_primary`).
Most often reported primary-list genera (number of usable studies): *Sphingomonas* 97, *Bacillus* 79, *Ralstonia* 70,
*Methylobacterium* 52, *Burkholderia* 50, *Brevundimonas* 46, *Bradyrhizobium* 44, *Rhodococcus* 38, *Comamonas* 35,
*Delftia* 35 (`top_primary_genera`). The same few genera recur in every tissue (Figure 1C; `results/table3_strict_genera_by_tissue.csv`).

## 4. Pre-specified models [`results/models.csv`, `results/hypotheses.json`, `results/model_log.txt`]

Main analysis (rule 8.2): 94 usable shotgun-class studies (≥ 30), so the **main model is the shotgun-class model**
(75 of 94 have no controls; 68 are host-sequencing mining). Quasi-binomial GLM, HC1 robust SE; odds ratios (OR) per
contaminant-genus-in-list.

| Hypothesis | Main model estimate (95% CI) | Verdict | Robustness (of 4) |
|---|---|---|---|
| **H1** no controls vs sequenced → higher share | OR 0.64 (0.37–1.09), n = 94 | **Not supported** | 0 |
| H1 co-primary, excluding mining studies | OR 0.85 (0.45–1.60), n = 26 | Not supported | – |
| **H2** decontamination → lower share | OR 0.66 (0.39–1.09) | **Not supported** | 1 |
| **H3** share falls with year (per 5 y) | OR 0.74 (0.51–1.09) | **Not supported** | 2 |
| **H4** 16S vs shotgun differ (pooled model, n = 398) | shotgun vs 16S OR 0.77 (0.59–1.00) | **Not supported** | 0 |

**The direction of H1 is reversed in the larger models.** In the pooled model (n = 398) studies that mention no
negative controls report a *lower* contaminant share than studies that sequence them: OR 0.63 (0.48–0.83), and the
same in all four pooled robustness analyses (strict list 0.67; full Salter list 0.57; ≥ 10 genera 0.59; unweighted
logit-share β −0.48, all CIs excluding the null), excluding mining studies (0.69, 0.50–0.94), excluding public
re-analyses (0.66, 0.48–0.91) and among 16S studies only (0.65, 0.45–0.93). Decontamination: pooled OR 0.74 (0.55–0.99),
not robust (CI excludes 1 in only 2 of 4 pooled robustness analyses). [`results/table2_key_estimates.csv`]

Dispersion < 1 in all GLMs (Pearson χ²/df ≈ 0.13–0.28). Sensitivity: `full_profile`-only main model skipped (< 10
studies); top-5 secondary outcome estimable only in the pooled set (27 ranked studies, with complete separation for
the "other" method level — not interpretable). [`results/model_log.txt`]

## 5. Main figure [`results/figure1.png`, `results/figure1.pdf`; code `analysis/make_figure.py`]

A: mean primary-list share by control practice within tissue (no gradient favouring controlled studies).
B: share by year, essentially flat (descriptive trend ≈ 0.18 → 0.20). C: % of usable studies reporting each
strict-list genus by tissue.

## 6. Interpretation for the manuscript (to be written in stage 6)

1. About one in five genera reported from human low-biomass sites belongs to a fixed set of environmental
   kit/reagent contaminant genera, and three quarters of studies report at least one; the same genera recur
   across tumour, blood, placenta and other tissues.
2. Half of the studies mention no negative controls and only about a third sequence them, with no improvement
   in recent years; decontamination and biomass measurement are uncommon.
3. H1 is not supported; the association runs the other way. Plausible, testable explanations: sequencing controls
   reveals contaminant genera that authors then report (or report as removed); studies without controls are dominated
   by TCGA-style mining with database-driven taxa and differential-only lists. The share is a contamination *risk*
   marker, not proof (protocol section 10).

## 7. Limitations to carry forward

Open-access subset only; first-pass extraction by AI checked by one reviewer on a 10% sample plus pilot papers
(100% reported agreement, attested); most papers show genus profiles only partly in text; differential-only lists;
paper (not cohort) is the unit — unconfirmed cohort overlaps kept separate; contaminant lists from three labs/kits;
reversed H1 is an observational association.

## 8. Reproduce

```
.venv/bin/python workflow/stage4/build_dataset.py   # data/studies.csv, data/genera.csv
.venv/bin/python analysis/run_models.py              # frozen; results/models.csv, hypotheses.json, descriptives.json
.venv/bin/python analysis/make_figure.py             # figure 1, tables 1-3
```
