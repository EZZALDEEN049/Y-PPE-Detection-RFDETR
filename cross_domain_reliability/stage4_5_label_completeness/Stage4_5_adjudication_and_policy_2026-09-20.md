# Stage 4.5 adjudication and correction policy — 2026-09-20

**Status:** correction policy frozen before Stage 5 training.

## Evidence reviewed

Stage 4.5 workflow run `35485667262` completed successfully at commit `fa9fbd140a960a0866f7c6bfef2aa2d48cb4817c`.

Artifact: `stage4-5-label-completeness-evidence` (`10597440734`), digest `sha256:086489f617e19c6483b3da5e7deb3f53acffb3701f279ffd835883fecf3b44ab`.

The audit used annotation metadata for all splits and opened image pixels only for train/validation visual review. Held-out test image pixels were not opened.

Structural findings before correction:

- **Y-PPE:** 462 train/validation images required visual review, 341 images across all splits contained at least one critical unmatched excluded-class box, and 48 test images were structurally flagged. The harmonized derivative contained 198/53/31 empty labels in train/val/test.
- **Construction-PPE:** 33 train/validation images required visual review, 36 images across all splits contained at least one critical unmatched `none` box, and 3 test images were structurally flagged.

All generated train/validation contact sheets were visually inspected during adjudication. The review confirmed that the structural alerts represent a mixture of (a) safe negative animal-only Y-PPE images and (b) images in which excluded labels can correspond to human/person or PPE-state content that must not silently become background after harmonization. No test pixels were inspected during this decision.

## Frozen correction rule

A deterministic annotation-only image-membership rule is used so the same rule can be applied to train, validation, and test without looking at test pixels or model predictions.

### Y-PPE

Exclude a whole image when either condition is true:

1. `risk_reasons` contains any `critical_unmatched:*` alert (`Child`, `No Safety Attire`, or `Soft Hat` under the frozen Stage 4.5 audit); or
2. the image is `harmonized_empty` **unless** its excluded annotation set is exactly `Animal`.

Rationale:

- `Child` and `No Safety Attire` can represent human instances that would otherwise become unlabeled background for the retained `person` class.
- `Soft Hat` can create an unresolved helmet-state/background ambiguity after dropping the native class.
- Y-PPE animal-only empty images are visually valid negative images for the shared nine-class ontology and are retained.
- Other harmonized-empty compositions are conservatively excluded rather than treated as negative background.

Expected image removals from the successful Stage 4.5 evidence are:

- train: 255 -> 1,340 images remain
- validation: 74 -> 385 images remain
- test: 30 -> 204 images remain

### Construction-PPE

Exclude a whole image when either condition is true:

1. `risk_reasons` contains `critical_unmatched:none`; or
2. the image is `harmonized_empty`.

The `none` class is nonshared. Images in which a `none` box does not satisfy the predeclared structural person-match rule are conservatively removed so the dropped annotation cannot become a false background target.

Expected image removals are:

- train: 31 -> 1,046 images remain
- validation: 2 -> 132 images remain
- test: 3 -> 138 images remain

## Scientific safeguards

- The rule is frozen before Stage 5 training and before held-out test performance is observed.
- Test decisions use annotation metadata only; test image pixels remain unopened for adjudication.
- No model prediction, score, loss, or test metric contributes to image removal.
- No annotation is relabeled or inferred. Problematic images are removed as whole samples rather than inventing replacement ground truth.
- Because membership changes, the previous Stage 4 fingerprints are retired for new experiments. A new harmonized derivative and new SHA256 fingerprints must be generated before Stage 5.
- The same frozen rule must be applied to every reconstruction of the corrected derivative.

## Stage 5 gate

Stage 5 full training remains **HOLD** until the corrected nine-class derivatives are rebuilt, audited, assigned new fingerprints, and those fingerprints replace the original Stage 4 identities in the Stage 5 experiment matrix/protocol.
