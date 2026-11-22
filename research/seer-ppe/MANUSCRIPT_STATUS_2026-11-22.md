# SEER-PPE manuscript status — 22 November 2026

**Current main manuscript:** v0.43  
**Current supplementary material:** v0.43  
**Research branch:** `research/v30-progressive-xai-2026-11-22`  
**Repository:** https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR

## Research and editorial status

- V26: full original-source Validation detection evaluation on 459 images — complete.
- V27–V30: target perturbation, deletion/insertion, timing and progressive black-box XAI — complete as archived experiments.
- V33-A/V33-B: same-target reanalysis and 4×4 grid-resolution experiment — complete.
- V34-A: spatial map alignment and rank correlation — complete.
- V34-B: one summary figure plus ten paired target maps — generated and numerically reproduced.
- V35-A: numerical audit — passed, with the V27 timestamp warning retained.
- V35-B: figure integration — complete.
- V35-C: focused literature and editorial audit — complete, 17 working references.
- V35-D: editable Word export and automated QA — complete.
- V35-E: representative visual layout QA and main/supplement packaging — in progress.

## Current scientific headline values

- M0 Validation: 459 images; 3,471 author reference objects; TP=3,297; FP=806; FN=174; micro-F1=0.870610.
- Progressive XAI: 1,068 hosted calls in the frozen V30 run.
- Spatial agreement across ten target maps: mean Spearman ρ=0.5416; mean Kendall τ-b=0.4239; mean top-four overlap=65%.
- Grid-resolution comparison is target-dependent; one target has zero top-four overlap.
- The 11 figure assets are separated into one main-text summary figure and ten supplementary paired maps.

## Data/model integrity constraints

- No retraining.
- No Test-split access.
- No new detector inference calls during V33-A, V34-A, V34-B, V35 or editorial/export work.
- No source-image, annotation, split or original-model mutation.
- Local checkpoint/gradient/model-parameter access is not claimed.
- Worker-level compliance, Person–PPE association accuracy, task mandates, human-review efficacy, external generalization, causal explanation faithfulness and physical energy are outside the measured endpoints.

## Author/journal gates still requiring confirmation

1. Ethics approval or exemption and the applicable consent/privacy basis for worker imagery.
2. Funding statement.
3. Competing-interest statement.
4. Author-contribution statement.
5. Official IEEE metadata/author-order confirmation for the two eSmarTA 2026 publications.
6. Target journal and its word, figure, reference and supplementary-material rules.
7. Final choice of main-text versus supplementary tables/appendices after the journal is selected.

## Technical audit warnings retained

- V27 start/end chronology warning remains unresolved unless the original execution log is recovered; no timestamp was guessed.
- V34-B contains a nested duplicate PDF with a different file hash; the manifest-selected outer directory remains canonical pending archive reconciliation.
- The two eSmarTA 2026 author lists are not yet confirmed against official IEEE metadata.

## Version history

- v0.38: complete research-dossier Word export; 96 pages, 16 tables, 11 figures.
- v0.39–v0.40: intermediate table-width experiments; not publication-approved.
- v0.41: native Pandoc Word template fixed heading/paragraph flow and removed the empty TOC.
- v0.42: split wide V26 cohort/class tables; 18 tables, one main summary figure and ten supplementary map figures.
- v0.43: clean article front matter and abstract, scientific scope statement, separation of non-scoring legacy contracts and audit appendices into supplementary material, and figure numbering split between main and supplement.
