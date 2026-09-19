# Y-PPE v1 — Stage 2 Correction Plan

**Date:** 2026-09-19  
**Status:** correction manifest prepared; run-4 box adjudication completed; dataset has not been modified.  
**Rule:** keep the current test identities locked wherever a confirmed source group spans multiple splits; do not start harmonized experiments until the corrected export passes Stage 2 again.

## Confirmed corrections from visual leakage adjudication

The 38 dHash candidates were adjudicated as **21 leakage**, **7 not-leakage**, and **10 uncertain**. Confirmed leakage pairs were consolidated into connected source components. Using split priority `test > valid > train`, the current file-level plan preserves the higher-priority evaluation copy and excludes/reassigns lower-priority counterparts.

## Confirmed source-group leakage from explicit video filenames

Run #4 independently reproduced **3 explicit video groups** whose frames occur in more than one split:

- `43_MOV`: test=1, valid=1 (total 2)
- `RPReplay_Final1667001201_MP4`: test=1, train=9 (total 10)
- `Sapi-7_mp4`: test=2, train=15, valid=4 (total 21)

Frames from the same video are not independent samples. Each entire video source group must therefore be assigned to one split. With the locked-test rule, the combined file-level correction manifest currently marks **47 exported images for exclusion from their current split** and **21 images as retained references**. Some exclusions overlap visually confirmed near-duplicate components.

## Annotation cleanup — now fully adjudicated

Two separate annotation problems are confirmed:

1. **316 raw exact duplicate bbox rows** in training labels. Each duplicate group occurs twice. Retain one copy and remove the extra copy.
2. **8 near-identical same-class bbox pairs (IoU >= 0.995)**. Stage 2 run #4 produced overlays for all eight; visual adjudication confirms that every pair annotates the same object/region rather than two distinct objects. Retain row A and remove row B for each case.

Therefore the confirmed annotation cleanup is **324 row removals in total**. The eight near-identical cases do not overlap the 316 exact-duplicate groups identified earlier.

## Items still unresolved

1. **10 uncertain source-family/product-variant pairs** remain unresolved. They are mainly helmet product/color variants with related templates. They require provenance evidence or a predeclared conservative grouping rule before split freeze.
2. The current Roboflow Version 1 training export is augmentation-expanded (**4,875 images**). This cleanup does not by itself recover the original **1,625-image** training source split. The strongest source-level leakage statement should be based on the original source identities or a documented reconstruction of those identities.
3. Semantic geometry review is still required for `No Hard Hat`, `No Gloves`, and `No Safety Boots` before the 9-class ontology is frozen.

## Correction order

1. Preserve locked test items/source groups.
2. Remove or reassign lower-priority copies from confirmed visual-leakage components.
3. Apply **whole-video grouping** for all three explicit cross-split video groups.
4. Resolve the 10 uncertain source-family cases by provenance; if provenance cannot be established, document and apply a conservative grouping rule before test evaluation.
5. Remove the **316 exact duplicate bbox rows**.
6. Remove row B from each of the **8 visually confirmed near-identical duplicate-object pairs**.
7. Recover/reconstruct the original pre-augmentation training source identities and perform source-level leakage checking on them.
8. Complete semantic geometry auditing for the three primary missing-PPE classes.
9. Re-export a corrected, frozen Y-PPE version and rerun Stage 2.
10. Only after the corrected audit passes, freeze the harmonized ontology and begin baseline training.
