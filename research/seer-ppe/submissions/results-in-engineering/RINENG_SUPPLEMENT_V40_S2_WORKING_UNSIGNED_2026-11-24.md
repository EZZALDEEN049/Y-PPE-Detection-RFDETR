# Supplementary File S2 — V38-B enlarged target-matched perturbation study

**Article:** Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection

**Target journal:** Results in Engineering.

## S2.1. Fixed study and reproducibility

The separate, prospectively specified V38-B extension evaluated **48 exact detections in 24 original Validation images**, covering **11 PPE classes**, using frozen RF-DETR Small (model ID altayyar-0oflt-lafos-qqauz/2). The images are development-exposed, not an acquisition-independent field sample. The frozen candidate record screened 459 historical Validation images, yielding 225 eligible images before the balanced 24-image selection. The selected archived V26 confidences were 0.5959–0.9325 (median 0.8463); class-exact reference IoUs were 0.5267–0.9464 (median 0.7889). These descriptors are conditional on the eligibility filters, not representative of all detector outcomes. Models, ground-truth annotations, and Test images were not changed or used. All extension images were transmitted as JPEG quality 95 with 4:4:4 chroma after EXIF orientation correction. This differs from the historical ten-target PNG-based setup and prevents meaningful pooling of raw cohorts as if paired.

The one-time run completed **4,984 real model-image calls, all successful**, and all 24 images. An append-only journal confirms 4,984 contiguous ATTEMPT_RESERVED entries and 4,984 corresponding ATTEMPT_SUCCEEDED entries, with no failed attempts. The budget was at most 6,000 attempted calls. Original run: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45085935253

Full raw output and call-ledger files remain immutable in the research branch, and the numerical independent audit is at https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45088345895 . Tables below use T01–T48 in archive order to minimize source-image identifier disclosure in the journal text.

## S2.2. Prespecified primary cross-resolution results

| Endpoint | Value | Denominator |
|:--|--:|:--|
| Frozen source images | 24 | All retained |
| Fixed targets | 48 | All retained |
| Estimable rho, tau and top-four overlap | 45 | 3 undefined from ambiguous matching |
| Spearman rho target mean | 0.6490 | 45 |
| Spearman rho image-balanced mean | 0.6508 | 24 image groups |
| Descriptive image-bootstrap range (2.5%–97.5%) | 0.5950–0.7044 | 5,000 deterministic resamples |
| Kendall tau-b target mean | 0.5197 | 45 |
| Mean top-four overlap | 66.6667% | 45 |
| Targets with zero top-four overlap | 0 | Within 45 estimable values |

The image-bootstrap percentiles are **descriptive uncertainty summaries**, not independently validated source-population confidence intervals; images were purposively selected, and multiple targets share source images.

## S2.3. Individual outcomes including the three missing values

The archived gray-fill maps contain 45 LOST outcomes out of 3,072 fine-grid target-cell records and 52 out of 768 coarse-grid target-cell records; ambiguous outcomes numbered 7 and 6. LOST is an operational zero under fixed output and IoU thresholds, not zero internal response; ambiguous scores remain undefined. Counts are descriptive and do not identify the reason for a non-match. Random-order curves are internal diagnostics, not independent explanation ground truth or published-method comparisons.

| Target | PPE category | Paired-map status | Spearman rho | Kendall tau-b | Top-four overlap | Ambiguous fine cells | Ambiguous coarse cells | Progressive curves |
|:--|:--|:--|--:|--:|--:|--:|--:|:--|
| T01 | Hard Hat | AVAILABLE | 0.2765 | 0.1833 | 0.2500 | 0 | 0 | EXECUTED |
| T02 | No Gloves | AVAILABLE | 0.7882 | 0.6333 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T03 | Safety Vests | AVAILABLE | 0.6971 | 0.5833 | 0.7500 | 0 | 0 | EXECUTED |
| T04 | No Face Mask | AVAILABLE | 0.6873 | 0.5272 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T05 | No Safety Vest | AMBIGUOUS_REGION | NA | NA | NA | 1 | 0 | NOT_RUN |
| T06 | Goggles | AVAILABLE | 0.8559 | 0.7000 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T07 | Safety Boots | AVAILABLE | 0.8235 | 0.7333 | 0.7500 | 0 | 0 | EXECUTED |
| T08 | No Safety Boots | AVAILABLE | 0.8147 | 0.6500 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T09 | No Hard Hat | AVAILABLE | 0.7647 | 0.6000 | 0.7500 | 0 | 0 | EXECUTED |
| T10 | Gloves | AVAILABLE | 0.6971 | 0.5333 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T11 | No Face Mask | AVAILABLE | 0.6471 | 0.4500 | 0.7500 | 0 | 0 | EXECUTED |
| T12 | Face Masks | AVAILABLE | 0.4971 | 0.3667 | 0.2500 | 0 | 0 | NOT_SELECTED |
| T13 | No Gloves | AVAILABLE | 0.7000 | 0.5167 | 0.5000 | 0 | 0 | EXECUTED |
| T14 | Goggles | AVAILABLE | 0.6647 | 0.5167 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T15 | Hard Hat | AVAILABLE | 0.8235 | 0.6667 | 0.7500 | 0 | 0 | EXECUTED |
| T16 | No Safety Vest | AVAILABLE | 0.8059 | 0.6667 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T17 | No Hard Hat | AVAILABLE | 0.5147 | 0.4000 | 0.7500 | 0 | 0 | EXECUTED |
| T18 | Safety Vests | AVAILABLE | 0.4971 | 0.3667 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T19 | No Safety Boots | AVAILABLE | 0.4941 | 0.4000 | 0.5000 | 0 | 0 | EXECUTED |
| T20 | Safety Boots | AVAILABLE | 0.6206 | 0.4500 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T21 | Gloves | AVAILABLE | 0.4735 | 0.3500 | 0.7500 | 0 | 0 | EXECUTED |
| T22 | Face Masks | AVAILABLE | 0.8471 | 0.6667 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T23 | Goggles | AVAILABLE | 0.5941 | 0.4667 | 0.7500 | 0 | 0 | EXECUTED |
| T24 | No Face Mask | AVAILABLE | 0.7324 | 0.6667 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T25 | Safety Boots | AVAILABLE | 0.2912 | 0.1833 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T26 | No Gloves | AVAILABLE | 0.8941 | 0.7833 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T27 | Hard Hat | AVAILABLE | 0.6324 | 0.4833 | 1.0000 | 0 | 0 | NOT_SELECTED |
| T28 | No Safety Vest | AVAILABLE | -0.0176 | -0.0167 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T29 | No Safety Boots | AVAILABLE | 0.4412 | 0.3333 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T30 | Safety Vests | AMBIGUOUS_REGION | NA | NA | NA | 4 | 4 | NOT_SELECTED |
| T31 | No Hard Hat | AVAILABLE | 0.8118 | 0.6333 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T32 | Face Masks | AVAILABLE | 0.4500 | 0.4000 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T33 | Gloves | AVAILABLE | 0.8765 | 0.7500 | 1.0000 | 0 | 0 | NOT_SELECTED |
| T34 | No Face Mask | AVAILABLE | 0.4941 | 0.4167 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T35 | Goggles | AVAILABLE | 0.8412 | 0.7000 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T36 | No Gloves | AVAILABLE | 0.8000 | 0.6500 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T37 | Hard Hat | AVAILABLE | 0.6059 | 0.5333 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T38 | No Safety Vest | AVAILABLE | 0.3294 | 0.1833 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T39 | No Hard Hat | AVAILABLE | 0.9265 | 0.7833 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T40 | Safety Boots | AVAILABLE | 0.6500 | 0.5500 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T41 | Safety Vests | AVAILABLE | 0.8824 | 0.7500 | 1.0000 | 0 | 0 | NOT_SELECTED |
| T42 | No Safety Boots | AVAILABLE | 0.5559 | 0.4500 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T43 | Gloves | AVAILABLE | 0.5294 | 0.4500 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T44 | Face Masks | AVAILABLE | 0.6382 | 0.4833 | 0.5000 | 0 | 0 | NOT_SELECTED |
| T45 | Goggles | AVAILABLE | 0.7000 | 0.5167 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T46 | No Face Mask | AVAILABLE | 0.8197 | 0.6778 | 0.7500 | 0 | 0 | NOT_SELECTED |
| T47 | Hard Hat | AMBIGUOUS_REGION | NA | NA | NA | 2 | 2 | NOT_SELECTED |
| T48 | No Gloves | AVAILABLE | 0.7353 | 0.6000 | 0.7500 | 0 | 0 | NOT_SELECTED |

The original numeric ledger retains all 48 target IDs, confidence values, scores and masks; undefined coefficients are **NA** and never converted to zero or silently discarded.

## S2.4. Exactly three ambiguous target maps

| Target | PPE category | Ambiguous 8×8 response cells | Ambiguous 4×4 response cells | Curves |
|:--|:--|--:|--:|:--|
| T05 | No Safety Vest | 1 | 0 | NOT_RUN |
| T30 | Safety Vests | 4 | 4 | NOT_SELECTED |
| T47 | Hard Hat | 2 | 2 | NOT_SELECTED |

These ambiguities arise from *same-class detection identity matching after image modification* under the frozen match threshold and tie margin. The records alone do not prove whether a different same-class object was selected, a detection disappeared, or an arbitrary detector error occurred. The unscorable curve target belonged to **No Safety Vest** and was blocked because of INVALID_GRID_8; no substitute target was selected.

## S2.5. Descriptive consistency by PPE label

| PPE class | Selected targets | Estimable Spearman | Mean rho | Mean top-four overlap | Ambiguous per-cell trials |
|:--|--:|--:|--:|--:|--:|
| Face Masks | 4 | 4 | 0.6081 | 50.0000% | 0 |
| Gloves | 4 | 4 | 0.6441 | 81.2500% | 0 |
| Goggles | 5 | 5 | 0.7312 | 65.0000% | 0 |
| Hard Hat | 5 | 4 | 0.5846 | 68.7500% | 4 |
| No Face Mask | 5 | 5 | 0.6761 | 70.0000% | 0 |
| No Gloves | 5 | 5 | 0.7835 | 65.0000% | 0 |
| No Hard Hat | 4 | 4 | 0.7544 | 75.0000% | 0 |
| No Safety Boots | 4 | 4 | 0.5765 | 62.5000% | 0 |
| No Safety Vest | 4 | 3 | 0.3725 | 50.0000% | 1 |
| Safety Boots | 4 | 4 | 0.5963 | 62.5000% | 0 |
| Safety Vests | 4 | 3 | 0.6922 | 83.3333% | 8 |

Per-label denominators of three to five are too small for independent class-effect claims. No target or regional cell is treated as an independent source site.

## S2.6. Eight-image operator control (16 targets)

Gaussian-blur-fill cross-resolution rho was estimable for 15 targets; **14** also had an estimable gray-fill value, forming the paired sample. These fourteen gave mean gray rho **0.6943**, mean blur rho **0.4811**, and mean paired difference blur minus gray **-0.2132**. Blur produced lower rho in **10/14** and higher rho in **4/14**.

The separate, **unpaired** fifteen-target blur-fill mean rho was 0.5088. It must never be subtracted from the entire 45-target gray-fill mean as if paired. Changing the image replacement operator changes the response being measured; spatial normalization does not cancel interaction/nonlinearity.

## S2.7. Eleven targets with ten seeded-random comparator orders

Twelve targets were prespecified for progressive deletion/insertion. One was blocked by ambiguous 8×8 matching; **eleven** produced **264 numerically valid** eleven-point AUC curves (24 curves per target), compared to the **mean of ten seeded random 8×8 rankings per target**:

| Target | Direction | 8×8 saliency AUC | Valid random orders | 8×8 mean random AUC | Saliency − random mean | 4×4 saliency AUC |
|:--|:--|--:|--:|--:|--:|--:|
| T01 | deletion | 0.0469 | 10 | 0.4270 | -0.3801 | 0.0625 |
| T01 | insertion | 0.7557 | 10 | 0.5531 | 0.2026 | 0.9087 |
| T03 | deletion | 0.0469 | 10 | 0.5914 | -0.5445 | 0.0627 |
| T03 | insertion | 0.9531 | 10 | 0.5701 | 0.3830 | 0.9370 |
| T07 | deletion | 0.0468 | 10 | 0.5119 | -0.4650 | 0.0625 |
| T07 | insertion | 0.9532 | 10 | 0.5006 | 0.4526 | 0.9372 |
| T09 | deletion | 0.0468 | 10 | 0.5235 | -0.4766 | 0.0624 |
| T09 | insertion | 0.9500 | 10 | 0.4417 | 0.5083 | 0.9339 |
| T11 | deletion | 0.0469 | 10 | 0.4875 | -0.4406 | 0.0625 |
| T11 | insertion | 0.9526 | 10 | 0.5091 | 0.4435 | 0.9375 |
| T13 | deletion | 0.0469 | 10 | 0.4672 | -0.4203 | 0.0625 |
| T13 | insertion | 0.9527 | 10 | 0.5269 | 0.4258 | 0.9307 |
| T15 | deletion | 0.0469 | 10 | 0.5013 | -0.4544 | 0.0625 |
| T15 | insertion | 0.9428 | 10 | 0.4883 | 0.4545 | 0.9371 |
| T17 | deletion | 0.0469 | 10 | 0.3720 | -0.3252 | 0.0625 |
| T17 | insertion | 0.9531 | 10 | 0.6320 | 0.3211 | 0.9373 |
| T19 | deletion | 0.0469 | 10 | 0.4266 | -0.3797 | 0.0625 |
| T19 | insertion | 0.9531 | 10 | 0.5479 | 0.4052 | 0.9375 |
| T21 | deletion | 0.0470 | 10 | 0.4987 | -0.4518 | 0.0625 |
| T21 | insertion | 0.9255 | 10 | 0.4802 | 0.4453 | 0.9196 |
| T23 | deletion | 0.7552 | 10 | 0.9093 | -0.1541 | 0.8303 |
| T23 | insertion | 0.9830 | 10 | 0.9334 | 0.0496 | 0.9700 |

Mean saliency-minus-random AUC difference among the eleven was **−0.4084 for deletion** (lower favorable) and **+0.3720 for insertion** (higher favorable), and **11/11** targets were favorable in each direction against their own ten-random average. The saliency ranking and its response test rely on the same detector perturbations: these are **within-protocol responses**, not independent causal attribution truth, an unbiased superiority experiment, or a direct D-RISE/D-MFPP benchmark.

## S2.8. Figures, code and limitations

Separate Figure 2 and Figure 3 should be treated as descriptive quantitative results: one records 45 rankable vs three ambiguous target outcomes; the other shows the 14-case paired operator change and the eleven-target AUC differences. They contain no identifiable worker photos. Historical Figure 1 and Supplementary Figures S1–S10 are unchanged.

Reproducible sources and original artifacts in GitHub: the one-time V38-B result JSON, the full write-ahead JSONL model-attempt ledger, the independently audited numeric summary, and the V38-C plotting and editorial scripts. No raw-photo publication permission, ethical approval, independent-site representativeness, worker-level PPE compliance assessment, causal saliency correctness or safety-outcome effect is claimed. These remain separate author/editorial release requirements.

## S2.9. V39-R1 secondary rank-distribution and image-influence checks

The original forty-eight selected targets remain unchanged. Among 45 available Spearman coefficients, the median was **0.687270**, Q1–Q3 were **0.514706–0.811765**, and the full observed range was **−0.017647 to 0.926471**. Exactly **11/45** coefficients were <0.5, and **20/45** were ≥0.7. These thresholds describe the sampled variation and were not preregistered pass/fail criteria.

A leave-one-original-image-out diagnostic, excluding *all* detections from one image at a time before recomputing the target-weighted mean rho, yielded **0.640997–0.664868** across 24 leave-one-image deletions. This is influence analysis of selected development-exposed images, *not* an independent-site population confidence interval.

The Gaussian-blur minus neutral-gray rho difference was defined only on the **14 paired valid targets from eight images**. Its median was **−0.176471**. Recomputing its mean after deleting one of the eight images and all target observations from it yielded **−0.248039 to −0.178659**. It would be inappropriate to use 14 targets as 14 independent construction-site observations.

Three primary targets remained undefined because of same-class target-identity matching ambiguity. The missingness may correlate with crowding and visual complexity; no zero imputation or replacement target was used. Figure 2 in the main article displays individual valid cases and undefined marks.

## S2.10. Original-source Validation class-by-class detection performance (V26)

The following values are copied without retraining or re-running RF-DETR from the original V26 source-reference metric summary's **M0/per_class** records (459 original Validation images, 3,471 GT boxes, 4,103 model detections; confidence floor 0.20, overlap 0.50; class-exact matching at IoU≥0.50). They are an *internal single-curator annotation reference*, not an independent site validation. PPE "No" labels are dataset annotation classes, not assertions that a person is non-compliant with a task-specific PPE policy.

| Class | GT | Predictions | TP | FP | FN | Precision | Recall | F1 |
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

Total: **TP=3297, FP=806, FN=174**, micro precision **0.803558**, recall **0.949870**, F1 **0.870610**. Class F1 ranges from **0.776256 (No Safety Boots)** to **0.937811 (Hard Hat)**. These metrics describe frozen detections against the current single-curator author labels and cannot establish worker-level PPE compliance accuracy.

**Source integrity:** Calculated only from archived V38-B audited numeric rows and V26 \`M0.per_class\`. The exact analytic record, \`research/seer-ppe/V39_R1_SECONDARY_STATS_AND_V26_PER_CLASS_VALIDATED_2026-11-23.md\`, is version-controlled. No new hosted inference was required.
