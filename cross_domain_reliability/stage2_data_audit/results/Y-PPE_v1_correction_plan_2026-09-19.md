# Y-PPE v1 — Stage 2 Correction Plan

**Date:** 2026-09-19  
**Status:** correction manifest prepared; dataset has not been modified.  
**Rule:** keep the current test identities locked wherever a confirmed source group spans multiple splits; do not start harmonized experiments until the corrected export passes Stage 2 again.

## Confirmed corrections from visual leakage adjudication

The 38 dHash candidates were previously adjudicated as 21 leakage, 7 not-leakage, and 10 uncertain. Confirmed leakage pairs were consolidated into 19 connected source components. Using split priority `test > valid > train`, the pair-level plan marks **20 files for exclusion** and **19 higher-priority counterpart files for retention**.

## Additional source-group leakage found from explicit video filenames

A source-group pass over the run-3 image manifest found **3 explicit video groups** whose frames occur in more than one split:

- `43_MOV`: test=1, valid=1 (total 2)
- `RPReplay_Final1667001201_MP4`: test=1, train=9 (total 10)
- `Sapi-7_mp4`: test=2, train=15, valid=4 (total 21)

Because frames from the same video are not independent samples, each entire video group must be assigned to one split. With the locked-test rule, the combined file-level correction manifest currently marks **47 exported images for exclusion from their current split** and **21 images as retained references**. Some exclusions overlap the 21 visually confirmed near-duplicate decisions.

## Annotation cleanup

The run-3 provenance audit showed **316 raw exact duplicate bbox rows** in training labels. Each duplicate group occurs twice. The deterministic cleanup plan retains the first occurrence and removes the extra occurrence. No polygon-normalization collision was responsible for these 316 duplicates.

## Items still unresolved

1. **10 uncertain source-family/product-variant pairs** remain unresolved. They must be resolved by source provenance or a conservative grouping rule before split freeze.
2. **8 near-identical same-class bbox pairs (IoU ≥ 0.995)** still require image overlays and manual object-level adjudication.
3. The current Roboflow Version 1 training export is augmentation-expanded (4,875 images), so this cleanup does not replace the need to recover/freeze the original 1,625-image source training split for the strongest leakage statement.
4. Semantic geometry review is still required for `No Hard Hat`, `No Gloves`, and `No Safety Boots` before the 9-class ontology is frozen.

## Correction order

1. Preserve locked test items/source groups.
2. Remove or reassign lower-priority copies from confirmed visual-leakage components.
3. Apply **whole-video grouping** for all explicit cross-split video groups listed above.
4. Resolve the 10 uncertain source-family cases.
5. Deduplicate the 316 exact bbox rows.
6. Adjudicate the 8 near-identical bbox pairs with overlays.
7. Re-export a new frozen Y-PPE version and rerun Stage 2.
8. Only after the audit passes, freeze the harmonized ontology and begin baseline training.
