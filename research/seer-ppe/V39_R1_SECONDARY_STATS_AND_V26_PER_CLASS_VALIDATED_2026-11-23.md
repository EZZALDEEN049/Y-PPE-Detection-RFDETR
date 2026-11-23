# V39-R1 — Verified secondary statistics and V26 per-class detection evidence

**Source:** V38-B immutable audited per-target JSON (48 rows), and original V26 compact 459-image current-author reference summary (`M0.per_class`), both read from frozen research branch. **New hosted model calls:** 0. These statistics derive from the original stored results; the primary analysis is not rerun or changed.

## New descriptive statistics and cluster sensitivity

| Statistic | Computed value | Denominator |
|:--|--:|:--|
| Prespecified target detections | 48 | 24 source images |
| Estimable rho | 45 | 3 maps ambiguous |
| Spearman median | 0.687270 | 45 valid targets |
| Spearman interquartile range | 0.514706–0.811765 | 25th–75th percentile, linear interpolation |
| Spearman minimum–maximum | -0.017647 to 0.926471 | 45 valid targets |
| Target rho <0.50 | 11/45 | Descriptive illustrative threshold, not a prespecified acceptance criterion |
| Target rho ≥0.70 | 20/45 | Descriptive illustrative threshold |
| Leave-one-image-out mean rho range | 0.640997–0.664868 | 24 iterations, remove BOTH targets of one image |
| Gray vs blur paired rho difference median | -0.176471 | 14 available targets, 8 images |
| Leave-one-image-out paired mean blur − gray range | -0.248039 to -0.178659 | 8 image-cluster iterations |

The interval from dropping one image is a **descriptive image-level influence range**, not an externally independent sampling confidence interval. All 45 rankable targets are development-exposed. This test must not be misrepresented as generalization to unseen locations.

## Complete per-class historical V26 current-reference detection

**Parameters:** Confidence floor 0.20; hosted overlap 0.50; class-exact box IoU≥0.50; Validation original source images 459, single-curator current GT; checkpoint `altayyar-0oflt-lafos-qqauz/2`. The 17 classes were taken from the **unchanged original compact V26 summary**. The "No X" classes are object-annotation categories, **not** verified worker compliance states.

| Annotation class | GT | Predictions | TP | FP | FN | Precision | Recall | F1 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| Animal | 66 | 75 | 66 | 9 | 0 | 0.8800 | 1.0000 | 0.9362 |
| Child | 31 | 37 | 29 | 8 | 2 | 0.7838 | 0.9355 | 0.8529 |
| Face Masks | 80 | 101 | 74 | 27 | 6 | 0.7327 | 0.9250 | 0.8177 |
| No Hard Hat | 56 | 64 | 55 | 9 | 1 | 0.8594 | 0.9821 | 0.9167 |
| No Safety Boots | 93 | 126 | 85 | 41 | 8 | 0.6746 | 0.9140 | 0.7763 |
| Soft Hat | 60 | 69 | 57 | 12 | 3 | 0.8261 | 0.9500 | 0.8837 |
| Hard Hat | 388 | 416 | 377 | 39 | 11 | 0.9063 | 0.9716 | 0.9378 |
| No Safety Vest | 160 | 198 | 156 | 42 | 4 | 0.7879 | 0.9750 | 0.8715 |
| Pants | 207 | 263 | 201 | 62 | 6 | 0.7643 | 0.9710 | 0.8553 |
| No Face Mask | 280 | 320 | 269 | 51 | 11 | 0.8406 | 0.9607 | 0.8967 |
| No Safety Attire | 87 | 105 | 80 | 25 | 7 | 0.7619 | 0.9195 | 0.8333 |
| No Gloves | 328 | 423 | 308 | 115 | 20 | 0.7281 | 0.9390 | 0.8202 |
| Gloves | 278 | 330 | 250 | 80 | 28 | 0.7576 | 0.8993 | 0.8224 |
| Safety Boots | 365 | 442 | 337 | 105 | 28 | 0.7624 | 0.9233 | 0.8352 |
| Safety Vests | 315 | 342 | 297 | 45 | 18 | 0.8684 | 0.9429 | 0.9041 |
| Goggles | 189 | 216 | 183 | 33 | 6 | 0.8472 | 0.9683 | 0.9037 |
| Persons | 488 | 576 | 473 | 103 | 15 | 0.8212 | 0.9693 | 0.8891 |

Micro aggregate (archived): GT=3,471; predictions=4,103; TP=3,297; FP=806; FN=174; precision **0.803558**, recall **0.949870**, F1 **0.870610**.

**Limits:** Single-author labels and development-exposed Validation; class-exact evaluator matching depends on annotation definitions and frozen 0.20 threshold. Metrics for negative equipment categories cannot be equated to person-specific noncompliance accuracy. No confidence calibration, inter-annotator agreement or external field-site validation was carried out.

## Reproduction recipe

For rankable target set `T`, median and IQR use all 45 non-null `rho` values. Let `I` denote the 24 original source-image IDs; for each `i∈I`, compute `mean(rho_t: t∈T and image(t) != i)`. Report min and max across these 24 means. For operator subset `O` of 14 paired valid targets, compute each `blur_rho − gray_rho`; calculate median and drop all records of each of eight original-image IDs before recomputing the paired mean.

**No new random seeds, inference calls, image/target reselection, imputation or investigator-chosen omission.**
