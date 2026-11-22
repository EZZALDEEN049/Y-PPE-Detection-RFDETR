# V38-A — Exploratory image-cluster sensitivity on frozen V34A results

**Date:** 23 November 2026  
**Purpose:** Strengthen the statistical description of the already archived XAI measurements without using the hosted detector, retrieving images, changing annotations, rerunning the model or opening Test.  
**Author-approved manuscript title:** Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection.  
**Status:** **COMPLETED offline deterministic descriptive analysis**, not a new prospective confirmation.

## 1. Original source

`research/seer-ppe/V34A_SPATIAL_MAP_ALIGNMENT_RANK_CORRELATION_2026-11-22.json`; status `PASSED`; use **exact full-precision per-target entries**, not rounded supplementary table cells.

Population in the archived analysis is a **purposively selected** set of 10 target detections within **8 distinct, development-exposed source images**, including two images with two targets each. Target-level observations are not necessarily independent; multiple images are not independently acquired field sites.

## 2. Fixed descriptive method

- Target-weighted mean: average across all 10 archived target entries.
- Equal-image mean: first average scores among all targets per original image, then average the 8 image means.
- Leave-one-image-out (LOIO): remove **all targets sharing one `image_key`** and recompute the target-weighted mean across remaining 8–9 targets, repeated once per image.
- Report minimum–maximum over these eight recomputed means. **These are sensitivity ranges, not 95% confidence intervals, p-values, or evidence of independent generalization.**
- Do not treat the 16 aligned regions per target as independent sampled subjects. Signed sensitivity ranks/ties and original missing-value rules are unchanged.

## 3. Newly computed descriptive results

| Endpoint | Original target-weighted mean | Equal-image-weight mean | Eight LOIO mean range |
|:--|--:|--:|--:|
| Spearman rho, signed area-normalized | 0.541566 | 0.545951 | **0.512987–0.578916** |
| Kendall tau-b | 0.423876 | 0.432248 | **0.406929–0.457567** |
| Four-region overlap fraction | **0.650000** | **0.671875** | **0.625000–0.718750** |

The mean rho stays positive and moderate upon the removal of any **one image**; the mean top-four overlap remains 62.5%–71.875% over these exclusions. This suggests the original descriptive central tendency is not a single-image artifact under this narrow check, **but the sample is too small and not independently representative to infer population robustness**. The single zero-overlap target remains a scientifically important observed limitation; retaining/discarding the full corresponding image is a sensitivity test, not a reason to remove this result.

## 4. Reproducibility

Executable, standard-library-only exact source calculation: `tools/v38_offline_image_cluster_sensitivity.py`. Running it against the committed JSON recomputes the table and prints the per-omission means. All original numerical records remain frozen.

## 5. What this does NOT fix

1. Does not expand sample size (10 targets / 8 images).
2. Does not provide independent construction-project source evaluation or a new human reference.
3. Does not test algorithm superiority, calibrated explanation faithfulness, model generalization, PPE worker compliance, or safety intervention benefits.
4. Does not replace stronger comparator controls, multiple independent seeded random orderings, blur/grayscale operator ablations, prospective target-selection protocol and optional new legally usable independent photographs.
5. The eight exclusion cases are highly dependent on the same observed data, so neither LOIO range nor a naive cell-level statistical test should be promoted as statistical significance.

**Editorial positioning:** may be added to Supplementary Material as a small descriptive robustness note, attributed to the original, development-exposed ten-target cohort. Main findings and every frozen original detection/model record remain intact.
