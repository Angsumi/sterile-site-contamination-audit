# C6 pilot report (22 Nov 2026)

Protocol section 9. Extraction by an AI agent (Claude); **first pass, not yet checked by a person.** Files: `extraction_entries.py` (all decisions, with evidence IDs and quotes), `extractions/`, `pilot_results.csv`, `pilot_genera.csv`, `pilot_summary.json`, `pilot_projection.json`.

## Sample

- 4 papers per block, the first eligible ones in the fixed random order (seed 6) of the v2 screening sample (`screening/screening_log_v2.csv`).
- "Other sterile" had only 3 eligible "other" papers in its v2 sample; the 4th (normal breast tissue, PMC9239270) and a replacement for a rat paper (intraocular, PMC7943566) came from the v1 sample.
- 21 full texts read; all downloaded as OA JATS XML (NCBI PMC E-utilities, Europe PMC as fallback).

## Go / no-go

| Rule (protocol section 9) | Threshold | Pilot | Pass |
|---|---|---|---|
| 1. Usable genus list (≥ 3 genera in text/tables/captions) | ≥ 60% of eligible | **16 / 19 (84%)** | yes |
| 2. Control practice classifiable | ≥ 80% | **19 / 19 (100%)** | yes |
| 3. Automatic source checks pass | ≥ 95% | **279 / 279 (100%)** | yes |
| 4. Projected usable OA studies | ≥ 150, with ≥ 15 in ≥ 3 categories | **≈ 240**; tumour 102, blood 72, other 38, placenta 24, brain 4 | yes |

Projection = v2 OA records × title/abstract include rate (30-record sample) × full-text eligibility (19/21) × usable rate (16/19).

**Verdict: GO.**

## What the pilot found

- **Full-text exclusions (2/21):** one metaproteomics study (placenta) and one rat study (follicular fluid) that passed title/abstract screening.
- **No usable list (3/19):** one brain study reports phyla/classes/orders only; one placenta study presents all placental genera as contaminants (1 genus left); one intraocular metagenome shows genera only in figures.
- **Control practice (19 eligible):** sequenced 8, included but not sequenced (PCR gel or Ct check only) 4, none mentioned 7. All 4 host-sequencing mining studies (TCGA-style re-use of RNA-seq/WGS) have no controls.
- **Decontamination:** none 9, tool 4 (decontam, SCRuB, binomial test, batch correction), removed control taxa 2, abundance filter only 2, literature list 1, unclear 1.
- **Methods:** 16S 11, host-sequencing mining 4, 2bRAD-M 2, shotgun 1, 16S + shotgun 1. So shotgun-type studies are about a third; at the projected volume (~240) the "≥ 30 shotgun" rule in section 8.2 would likely be met.
- **Contaminant share (primary list, 16 usable studies, descriptive only):** median 0.18 (range 0–0.64); 14 of 16 studies report at least one primary-list genus. Strict list median 0.16. The broad list matches a median 0.76 of genera and cannot separate studies (amendment 0.3 makes it descriptive only).
- **Most frequent primary-list genera:** *Sphingomonas* (6 studies), *Bradyrhizobium* (4), *Burkholderia*, *Ralstonia*, *Rhodococcus* (3 each). *Bradyrhizobium* survived decontamination in two studies with sequenced controls (brain, breast).
- **Highest share:** cerebral thrombi, 0.64 (14 of 22 genera; top five *Acinetobacter, Burkholderia, Sphingomonas, Pedobacter, Serratia*), with blanks checked only by PCR gel.
- **By control practice** (n = 5 / 4 / 7; far too few to test): medians 0.22 sequenced, 0.27 included-not-sequenced, 0.18 none. Not interpretable at this size; the "none" group is mostly host-sequencing mining.

## Problems found and fixed in amendment 0.3

1. New decontamination categories (`literature_list`, `unclear`).
2. Many papers name only genera that differ between groups → new `list_type` field and a full-profile sensitivity analysis.
3. Counting rules for SILVA composite names, fungi/viruses and author-flagged genera.
4. Host-sequencing mining confounds "no controls" with method → H1 also tested without them.
5. Brain/CSF too small → merged into "other sterile" for models.
6. Broad list uninformative → descriptive only.

## Limits of the pilot

- Not yet checked by a person (protocol: all pilot papers are checked before analysis).
- Genera in figures cannot be read from XML (4/19 papers have figure-only or partly figure-only profiles). OA supplementary tables were not opened in the pilot.
- The share depends on how many genera a paper names; differential-only lists bias it in unknown directions.
