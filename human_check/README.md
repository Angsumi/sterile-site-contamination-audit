# C6 independent human checks — pending

First-pass extraction is complete for all 523 downloaded full articles. An additional conference abstract is excluded in the 524-candidate disposition ledger. Current provisional totals: 475 eligible and 398 usable papers.

The seed-6 protocol extraction sample contains **46 randomly selected eligible nonpilot papers plus all 21 pilot papers**, 67 unique papers. There are **84 packet files** after adding explicit uncertainty priorities. Extra priorities are separate from the random sample and must not be used to claim unbiased agreement estimates.

The screening sample contains **175 decisions**, selected with seed 6 and 5% rounded up within each decision stratum. Exact IDs, denominators and selection methods are in `manifest.json`.

Review source full texts and supplements independently; record corrections and reviewer/date in the blank human columns of `review_form.tsv` and `screening_review.json`. For each genus, verify detection in the target compartment, source spelling, contaminant flag and sample-cohort attribution. Complete missing sample units, country and assay-region metadata where stated. For excluded records, verify the exclusion against the source.

Both manual figure transcriptions (PMC7355471 and PMC6109274) require visual comparison to the retained source PDF/rendering. The automatic checker can match the derived text, but cannot independently validate the figure reading. Review the retracted reporting record, unverifiable sequencing provenance and cohort links before analysis.

**No human reviews or agreement measurements have been completed. No models have been run.** After review, reconcile corrections, resolve cohort/taxonomy issues, rebuild the dataset, reassess the gate, and only then use the frozen model code. Baseline dataset and model hashes are recorded without executing the models.
