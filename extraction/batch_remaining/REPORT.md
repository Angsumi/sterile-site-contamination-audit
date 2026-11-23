# C6 remaining corpus — provisional first-pass completion

23 Nov 2026. No subagents used. Existing MarkItDown full texts were read with native JATS evidence mapping; supplements used where needed.

**105 remaining downloaded papers processed and merged: 77 eligible and 28 excluded, adding 53 usable genus lists.** All 523 downloaded full articles now have canonical first-pass records. The 524th candidate, PMC7776645, is a conference/journal-supplement abstract (Europe PMC publication type `Abstract`) and is excluded separately in the complete candidate-disposition ledger.

Current totals: **523 extracted; 475 eligible; 398 usable; zero automatic source-check failures.** All counts remain provisional.

## Cohorts and scope

- PMC6586825 explicitly reused the asthma/control plasma samples in PMC6345098; the earlier, longer genus list is retained.
- PMC13243561 reused 46 breast tumours from PMC8052771 as Cohort A. Its new record contains only independent Cohort B (314 tumours; only Staphylococcus named for that cohort).
- PMC9609265 has a new stage-II lung cohort; old Peters validation data are not pooled into its genus list.
- Other possible links remain in `cohort_links.json` and the human-check priorities. Different recruitment locations/counts alone do not prove overlap.
- PMC12922273 is provisionally excluded because the bacterial sequence dataset and profiling assay cannot be verified; the available validation experiments are qPCR/FISH. This exclusion needs human adjudication.
- PMC9130323 is explicitly retracted. The protocol has no automatic retraction exclusion, so it is retained as a clearly flagged reporting record with no usable genus list, requiring human handling before analysis.

## Evidence and limitations

Supplemental genus tables were used for PMC7709364, PMC8326911, PMC12282056 and PMC13185545. For PMC13185545, positive species-abundance entries were matched to eligible cancer types using the same supplement patient metadata; the row-level mapping is preserved in its support manifest. Pooled taxa without eligible-site attribution were not guessed.

PMC7355471 has a provisional genus list transcribed from supplementary Figure S3 (page 2), restricted to light-grey lung-tissue columns. Its source PDF, rendering and transcription are hashed and retained. Like the prior batch’s PMC6109274 transcription, this needs independent visual verification. Automatic source checks match the labelled derived transcription; they do not independently validate image interpretation.

Several eligible papers remain below three securely attributable genera because the report is at family/phylum level, has no named taxa, or only has unresolved site-specific figure labels. Eligibility review is complete at first pass; this does not assert that every possible figure label has been adjudicated. Country, sample-unit details, regions and control provenance that remain incomplete need human completion.

The numerical gate is met in four tissue categories. Human checking, taxonomy adjudication, final cohort resolution and retraction sensitivity handling must precede models. No models have been run.

## Paper outcomes

| Paper | Outcome | Counted genera | Tissue |
|---|---|---:|---|
| PMC13478868 | eligible below genus threshold | 0 | tumour |
| PMC4419820 | eligible below genus threshold | 2 | placenta_fetal |
| PMC8904948 | eligible usable | 4 | tumour |
| PMC7355471 | eligible usable | 16 | other_sterile |
| PMC3587628 | eligible usable | 8 | blood |
| PMC5610236 | excluded | 0 | placenta_fetal |
| PMC12072589 | excluded | 0 | tumour |
| PMC12922273 | excluded | 0 | tumour |
| PMC3577789 | excluded | 0 | placenta_fetal |
| PMC9602924 | eligible usable | 9 | tumour |
| PMC11748541 | eligible usable | 6 | brain_csf |
| PMC13378360 | eligible below genus threshold | 0 | tumour |
| PMC10966708 | eligible usable | 9 | placenta_fetal |
| PMC6586825 | excluded | 0 | blood |
| PMC8004470 | eligible below genus threshold | 0 | brain_csf |
| PMC12490247 | eligible usable | 3 | tumour |
| PMC8929612 | eligible usable | 20 | placenta_fetal |
| PMC6697540 | eligible below genus threshold | 2 | placenta_fetal |
| PMC7291729 | eligible below genus threshold | 0 | placenta_fetal |
| PMC8110246 | eligible below genus threshold | 0 | placenta_fetal |
| PMC13243561 | eligible below genus threshold | 1 | tumour |
| PMC12649041 | eligible usable | 24 | tumour |
| PMC12388318 | eligible usable | 16 | blood |
| PMC12269162 | eligible usable | 19 | blood |
| PMC12780107 | eligible usable | 5 | tumour |
| PMC9609265 | eligible usable | 6 | tumour |
| PMC13233812 | eligible usable | 5 | tumour |
| PMC12866835 | eligible usable | 9 | other_sterile |
| PMC13343675 | eligible usable | 7 | brain_csf |
| PMC12931691 | eligible below genus threshold | 0 | other_sterile |
| PMC12277338 | excluded | 0 | tumour |
| PMC13784061 | eligible usable | 5 | tumour |
| PMC8240556 | eligible usable | 12 | placenta_fetal |
| PMC12688851 | excluded | 0 | tumour |
| PMC11863458 | eligible below genus threshold | 0 | blood |
| PMC11811456 | excluded | 0 | tumour |
| PMC12245331 | eligible usable | 25 | other_sterile |
| PMC11434507 | excluded | 0 | placenta_fetal |
| PMC5420800 | eligible usable | 8 | other_sterile |
| PMC12029928 | eligible usable | 8 | brain_csf |
| PMC6652165 | excluded | 0 | other_sterile |
| PMC9000115 | eligible usable | 17 | blood |
| PMC10031003 | eligible below genus threshold | 0 | tumour |
| PMC7530676 | excluded | 0 | other_sterile |
| PMC12450707 | excluded | 0 | tumour |
| PMC13774904 | eligible below genus threshold | 2 | tumour |
| PMC11569570 | excluded | 0 | other_sterile |
| PMC13097533 | eligible usable | 9 | tumour |
| PMC11780891 | eligible usable | 22 | tumour |
| PMC11020926 | eligible usable | 9 | tumour |
| PMC3555817 | excluded | 0 | blood |
| PMC9357631 | eligible usable | 14 | tumour |
| PMC8495218 | excluded | 0 | tumour |
| PMC7709364 | eligible usable | 55 | blood |
| PMC11754412 | excluded | 0 | tumour |
| PMC12502792 | eligible usable | 14 | tumour |
| PMC12798661 | excluded | 0 | other_sterile |
| PMC5193428 | eligible usable | 5 | other_sterile |
| PMC11309925 | eligible below genus threshold | 1 | blood |
| PMC11841003 | eligible below genus threshold | 0 | tumour |
| PMC11720077 | eligible usable | 8 | other_sterile |
| PMC13126416 | eligible usable | 9 | tumour |
| PMC4671185 | eligible below genus threshold | 2 | placenta_fetal |
| PMC12845112 | eligible below genus threshold | 0 | blood |
| PMC12393667 | eligible usable | 11 | tumour |
| PMC13141833 | excluded | 0 | tumour |
| PMC11786307 | eligible below genus threshold | 1 | blood |
| PMC13209569 | eligible below genus threshold | 1 | tumour |
| PMC12358694 | eligible below genus threshold | 0 | tumour |
| PMC8326911 | eligible usable | 229 | tumour |
| PMC9705781 | excluded | 0 | other_sterile |
| PMC6284549 | eligible below genus threshold | 0 | blood |
| PMC13207979 | eligible usable | 9 | other_sterile |
| PMC12325116 | excluded | 0 | tumour |
| PMC12282056 | eligible usable | 71 | tumour |
| PMC13746512 | eligible usable | 3 | tumour |
| PMC13255227 | eligible usable | 13 | placenta_fetal |
| PMC13492822 | eligible usable | 4 | tumour |
| PMC8978520 | excluded | 0 | tumour |
| PMC13423660 | eligible usable | 9 | placenta_fetal |
| PMC11757874 | eligible usable | 6 | tumour |
| PMC8375156 | excluded | 0 | blood |
| PMC11651096 | eligible usable | 3 | tumour |
| PMC12692072 | eligible usable | 16 | tumour |
| PMC13743254 | eligible usable | 6 | tumour |
| PMC13529793 | eligible usable | 4 | tumour |
| PMC13708057 | excluded | 0 | blood |
| PMC12542631 | eligible usable | 4 | tumour |
| PMC13681576 | eligible usable | 6 | tumour |
| PMC13561942 | eligible usable | 3 | tumour |
| PMC7109368 | eligible usable | 3 | tumour |
| PMC13720141 | eligible below genus threshold | 0 | tumour |
| PMC12077203 | eligible usable | 5 | tumour |
| PMC4636327 | excluded | 0 | other_sterile |
| PMC12354738 | excluded | 0 | tumour |
| PMC13185545 | eligible usable | 119 | tumour |
| PMC12162974 | eligible below genus threshold | 2 | tumour |
| PMC11876501 | eligible usable | 37 | tumour |
| PMC12539271 | excluded | 0 | other_sterile |
| PMC12054239 | excluded | 0 | placenta_fetal |
| PMC9130323 | eligible below genus threshold | 0 | tumour |
| PMC12823436 | excluded | 0 | other_sterile |
| PMC9037597 | eligible usable | 44 | tumour |
| PMC13116083 | eligible below genus threshold | 1 | brain_csf |
| PMC12892072 | eligible usable | 5 | tumour |
