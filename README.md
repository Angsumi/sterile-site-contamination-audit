# Sterile-site contamination audit

Manuscript, data, and analysis for a review of contaminant-associated genera and contamination-control practices in human low-biomass microbiome studies.

- `manuscript/manuscript_v2.md` is the current manuscript; `manuscript/supplementary/` contains its supplementary files.
- `C6_protocol.md` records the protocol and amendments.
- `data/`, `reference/`, `search/`, `screening/`, `extraction/`, `pilot/`, and `human_check/` contain the study data, search and screening records, extraction evidence, and review records.
- `analysis/` contains the frozen models and scripts for the figure and supplement; `results/` contains their reported outputs. `workflow/` contains the search, preparation, and checking scripts.

## Reproduce the reported analyses

From the repository root, create a Python environment and install `requirements.txt`, then run:

```sh
python analysis/run_models.py
python analysis/make_figure.py
python analysis/make_supplement.py
```

These commands overwrite generated files in `results/` and `manuscript/supplementary/`. `analysis/FROZEN.txt` records hashes of the frozen analysis and inputs. Rebuilding the extraction and checking source quotations also requires the locally stored full-text corpus, which is not included in this repository; the original `papers/` link was local to the author. The source records and extraction data are retained here. The manuscript and protocol describe the screening and extraction methods and their limitations.

The manuscript and review records require author verification before submission.
