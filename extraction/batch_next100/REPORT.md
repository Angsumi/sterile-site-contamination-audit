# C6 next 100 papers — provisional extraction

23 Nov 2026. Single-agent continuation; no subagents used. Main texts were read from the existing MarkItDown Markdown conversion, with native JATS evidence IDs retained.

**100 papers processed: 99 merged, 1 held.** The merged records comprise 95 eligible and 4 excluded papers, adding 89 usable genus lists. Overall: **418 extracted, 398 eligible, 345 usable; zero automatic source-check failures.**

The four exclusions are PMC9749999 (target sites qPCR-only), PMC13125019 (qPCR panel only), PMC13097710 (virome-only), and PMC13562036 (febrile-neutropenia systemic-infection cohort). PMC3577789 remains held for the diagnostic intra-amniotic infection / early-onset sepsis scope decision.

Supplemental files were retrieved for 10 papers. Supplemental genus evidence was used for PMC12711707, PMC5675698, PMC7813997, and PMC6109274; PMC8824227 also required supplementary control/method evidence. Other inspected supplements did not justify target-genus expansion.

PMC6109274 was resolved using a direct visual review of supplemental PDF Figure S6A (page 9), with S5A/B corroboration. `S990.md` is explicitly labelled as a manual figure transcription, with the source PDF/render/transcription hashes in its figure manifest. Automatic matching of that transcription is not independent visual validation; prioritize it for human checking.

Source spellings that do not resolve to the existing bacterial taxonomy dictionary remain uncounted; see `validation.json` and record review flags. No taxonomy dictionary, protocol, model code or previous extraction record was changed in this batch.

The control and decontamination classifications, cohort links and missing design metadata remain provisional AI extraction. `cohort_links.json` logs five relevant links, including explicit public reuse and possible unresolved primary-cohort overlap. Convenience selection by short Markdown files is not representative. Models have not been run.

105 downloaded papers remain outside canonical extraction, including held records.

## Outcomes

| Paper | Outcome | Counted genera | Target |
|---|---|---:|---|
| PMC13069727 | eligible usable | 10 | tumour |
| PMC11781185 | eligible usable | 8 | tumour |
| PMC9705848 | eligible usable | 12 | tumour |
| PMC9749999 | excluded | 0 | other_sterile |
| PMC8494912 | eligible usable | 8 | blood |
| PMC12617009 | eligible usable | 3 | placenta_fetal |
| PMC13125019 | excluded | 0 | other_sterile |
| PMC13123245 | eligible usable | 12 | tumour |
| PMC4968547 | eligible usable | 8 | tumour |
| PMC12940155 | eligible usable | 19 | blood |
| PMC7524391 | eligible usable | 8 | placenta_fetal |
| PMC5669892 | eligible usable | 15 | placenta_fetal |
| PMC13485531 | eligible usable | 3 | tumour |
| PMC6029081 | eligible usable | 20 | placenta_fetal |
| PMC12922691 | eligible usable | 5 | blood |
| PMC8080813 | eligible usable | 26 | blood |
| PMC9808057 | eligible usable | 8 | placenta_fetal |
| PMC9046152 | eligible below genus threshold | 0 | placenta_fetal |
| PMC6945248 | eligible usable | 4 | placenta_fetal |
| PMC12717426 | eligible usable | 26 | tumour |
| PMC5063344 | eligible usable | 12 | other_sterile |
| PMC4964003 | eligible usable | 8 | other_sterile |
| PMC5593928 | eligible usable | 4 | placenta_fetal |
| PMC5592210 | eligible usable | 14 | placenta_fetal |
| PMC11903660 | eligible usable | 5 | tumour |
| PMC8824227 | eligible usable | 27 | blood |
| PMC12580212 | eligible usable | 12 | blood |
| PMC10986513 | eligible usable | 14 | tumour |
| PMC6345098 | eligible usable | 10 | blood |
| PMC13446152 | eligible usable | 14 | placenta_fetal |
| PMC7353057 | eligible usable | 20 | tumour |
| PMC8821101 | eligible usable | 14 | tumour |
| PMC7416914 | eligible below genus threshold | 0 | placenta_fetal |
| PMC11708301 | eligible usable | 8 | tumour |
| PMC9294280 | eligible usable | 29 | tumour |
| PMC13555953 | eligible usable | 15 | tumour |
| PMC6871869 | eligible usable | 6 | other_sterile |
| PMC7352186 | eligible usable | 7 | tumour |
| PMC11839906 | eligible usable | 7 | blood |
| PMC9880005 | eligible usable | 21 | tumour |
| PMC13474856 | eligible usable | 16 | tumour |
| PMC12222121 | eligible usable | 18 | blood |
| PMC9176212 | eligible usable | 10 | blood |
| PMC11850547 | eligible usable | 7 | blood |
| PMC13483239 | eligible usable | 8 | tumour |
| PMC13381187 | eligible usable | 7 | tumour |
| PMC6987042 | eligible usable | 19 | blood |
| PMC7562954 | eligible below genus threshold | 0 | other_sterile |
| PMC12711707 | eligible usable | 74 | blood |
| PMC12183207 | eligible usable | 8 | tumour |
| PMC8064568 | eligible usable | 10 | tumour |
| PMC11981758 | eligible usable | 12 | tumour |
| PMC13097710 | excluded | 0 | placenta_fetal |
| PMC7107015 | eligible usable | 10 | placenta_fetal |
| PMC13141924 | eligible usable | 29 | tumour |
| PMC9116393 | eligible usable | 9 | tumour |
| PMC6109274 | eligible usable | 16 | placenta_fetal |
| PMC11746125 | eligible usable | 16 | other_sterile |
| PMC13079188 | eligible usable | 3 | other_sterile |
| PMC7952451 | eligible below genus threshold | 0 | blood |
| PMC8396677 | eligible usable | 40 | tumour |
| PMC10964645 | eligible usable | 18 | placenta_fetal |
| PMC13022639 | eligible usable | 18 | blood |
| PMC12314883 | eligible usable | 31 | blood |
| PMC5675698 | eligible usable | 43 | tumour |
| PMC12914011 | eligible below genus threshold | 2 | blood |
| PMC13326317 | eligible usable | 10 | tumour |
| PMC12275360 | eligible usable | 7 | placenta_fetal |
| PMC8744134 | eligible usable | 8 | tumour |
| PMC12271595 | eligible usable | 8 | tumour |
| PMC11702424 | eligible usable | 22 | tumour |
| PMC12605661 | eligible usable | 10 | tumour |
| PMC7564876 | eligible usable | 28 | tumour |
| PMC9794006 | eligible usable | 16 | tumour |
| PMC13088536 | eligible usable | 22 | tumour |
| PMC13680605 | eligible below genus threshold | 1 | other_sterile |
| PMC13739529 | eligible usable | 7 | brain_csf |
| PMC12095603 | eligible usable | 5 | tumour |
| PMC8408135 | eligible usable | 4 | tumour |
| PMC5507499 | eligible usable | 10 | placenta_fetal |
| PMC10989844 | eligible usable | 6 | tumour |
| PMC13562036 | excluded | 0 | blood |
| PMC12008866 | eligible usable | 21 | blood |
| PMC8052771 | eligible usable | 50 | tumour |
| PMC5759273 | eligible usable | 14 | other_sterile |
| PMC12187763 | eligible usable | 9 | tumour |
| PMC9600380 | eligible usable | 26 | placenta_fetal |
| PMC9577097 | eligible usable | 14 | blood |
| PMC7813997 | eligible usable | 189 | blood |
| PMC6109311 | eligible usable | 16 | tumour |
| PMC12846730 | eligible usable | 14 | tumour |
| PMC3577789 | held | held | placenta_fetal |
| PMC13166237 | eligible usable | 16 | other_sterile |
| PMC13720179 | eligible usable | 5 | tumour |
| PMC12550791 | eligible usable | 6 | tumour |
| PMC12363524 | eligible usable | 10 | tumour |
| PMC12797839 | eligible usable | 7 | tumour |
| PMC9885577 | eligible usable | 27 | other_sterile |
| PMC9793878 | eligible usable | 19 | tumour |
| PMC12856059 | eligible usable | 18 | other_sterile |
