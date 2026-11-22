# V38-B — Pre-registered XAI replication, control comparisons and hard inference budget

**Recorded 23 November 2026**. **Target journal:** *Results in Engineering*.  
**Author-approved exact manuscript title:** Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection.  
**Status:** **DATA-ONLY DESIGN / CANDIDATE FREEZE; ZERO new hosted inference, zero model training, no Test access**. The model, V26–V35 raw numerical ledgers, original dataset, labels, splits and previously published results remain untouched.

## 1. Scientific question and primary endpoint

**Question:** In a larger, fully frozen but development-exposed Validation sample, how consistent are *target-matched* signed occlusion-response rankings when the grid resolution changes from 8×8 to 4×4?

- Primary endpoint: image-balanced mean target-level Spearman rho over 16 spatially registered 4×4 regions, comparing independently occluded coarse regions against pixel-area-weighted pooling of four corresponding fine 8×8 signed sensitivity-density cells. All 48 selected target detections in 24 unique original images contribute, with both target scores per image averaged first; report target-weighted mean and distribution as secondary.
- Secondary descriptive endpoints: target-level Kendall tau-b, region-top-four overlap (0–4), proportion of zero-overlap targets, per-class response and consistency, failure/ambiguous match rates, and area-normalized nonlinear coarse-minus-pooled-fine response difference.
- Diagnostic supplementary endpoint: deletion and insertion AUC under a fixed Gaussian baseline and 11 cumulative points for one frozen target per image on a 12-image subset, with 10 distinct pre-seeded random-ranking controls at 8×8 and matched saliency ordering at 4×4.
- Operator ablation: repeat single-cell **Gaussian-blur fill** rather than neutral RGB(127,127,127) for both grids on a predeclared eight-image subset. This tests sensitivity to the choice of occlusion operator, not explanation ground truth.

The preexisting historical 10-target/8-image V34A numbers **must remain a separate development result** and should not be pooled with the 48-target extension without declared overlap/exposure assumptions. Current project/site-family independence is not established; do not label the new sample an external independent test.

## 2. Prospective candidate pool and transparent selection

**Read-only source:** 12 frozen V26 geometry/prediction shards containing exactly 459 original Validation image entries, model-id \`altayyar-0oflt-lafos-qqauz/2\`, original confidence floor 0.20 and overlap 0.50. Prior V30 source manifest supplies four Valid image exclusions; V23 pilot source exposures are excluded when flagged.

**Eligibility:** archived successful image, width≥320 and height≥240; target must have one of 11 occupational PPE-relevant labels, historical model confidence≥0.55, original target box width and height≥16 px, area≥0.03% of original image, and an existing same-class current-author box with IoU≥0.50. Eligible image requires ≥2 distinct represented PPE label classes. These are candidate-selection gates only: confidence and IoU from earlier V26 outcomes are not newly earned independent validation, and author-curated annotations may have model assistance.

**Deterministic algorithm:** seed \`SEER-PPE|V38-B|2026-11-23|preregistered-v1\`; select one target per class per image by FNV-1a32 hash of frozen prediction ID, then run balanced greedy pair selection across image-class pairs: class-count below 3 has priority; then favor underrepresented classes and modestly favor one presence/one absence label; hash ties by sorted target IDs and image source ID. Do not inspect new XAI maps in selection. **Actual frozen output: 24 images, 48 unique targets, 11 classes with four or five targets per class.** All future source/target changes must be versioned as a prospective amendment and must not erase missing results.

Reproduction entry point: \`tools/v38b_freeze_sample_and_budget.py\`. Its output manifest is \`research/seer-ppe/V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json\`. Use the exact target IDs, image IDs, classes and bounding-box geometry from that file; the new acquisition stage must reverify source image identity/hashes rather than assume saved V26 response IDs guarantee identical pixels.

## 3. Inference rules and quality gates

1. **No new inference under this protocol alone.** Separate author approval of the exact 6,000-call maximum, successful read-only source availability/hash preflight and budget-enforced execution script are required before any Roboflow call. All 6,000 attempted calls, including retries, must be logged. Model \`altayyar-0oflt-lafos-qqauz/2\` locked at confidence 0.20 and overlap 0.50. No model weights, GT, class map, source split, Test or annotator changes.
2. For each of the 24 images, one rechecked unperturbed baseline and one shared fully Gaussian-blurred baseline. Match both frozen targets by the original class/bbox at IoU≥0.50 and reject ambiguous two-candidate matches when the competing best IoUs differ by ≤0.03. Baseline class/position must reproduce; baseline confidence drift >0.08 from frozen V26 is an explicit fail, not a reason to relax a threshold.
3. For 24 images, 8×8 (64 cells) and 4×4 (16 cells) separately replace a single cell with gray RGB(127,127,127) in full original-image coordinates. Shared image inferences score both frozen target detections; derive signed baseline-confidence minus matched response score. LOST=0 by frozen convention; AMBIGUOUS=null and flagged. Do not zero negative sensitivities, conceal null or label ambiguity as an ordinary response.
4. Spatial mapping: floor-derived pixel bounds, direct 4×4 per-cell call vs average of four independently occluded 8×8 responses after normalizing by exact cell pixel area, tie-aware Spearman/Kendall and row-major top-four ties. **Note nonlinear/multi-cell interaction**: coarse occlusion is not causally equivalent to summing individual fine occlusions; report their difference rather than implying geometry normalization removes interaction.
5. For **one target in each of the first 12 frozen images**, produce 8×8 11-point progressive Gaussian-baseline deletion and insertion for (a) observed saliency order, (b) **10 distinct, reproducibly SHA256-seeded target-specific random permutations**, with reuse of original/blurred endpoints. Nine intermediate points/order/direction; actual area fractions on x-axis, target confidence divided by frozen verified baseline and clipped to [0,1]. Add 4×4 saliency deletion/insertion for same 12 targets with nine intermediate calls per direction. If mapping invalid or ambiguous, retain null rather than sample replacements; calls are *up to* budgets.
6. For the **first 8 frozen images**, repeat 8×8 and 4×4 single-cell maps under a fixed Gaussian-blur-fill operator (same image-level radius for all cells). Reference blur: Gaussian sigma=max(3 px, round(0.01×min(image width,image height), 3)); use one rendered blurred baseline per image shared across grids. The exact image decoder, Gaussian implementation, fill color, clipping and blur source must be checksum-tested before inference. This planned V38 implementation should not silently mix slightly different V30/V33 historical blur-rounding conventions.
7. The 48-target sample and all invalid/missing rows remain visible; do not substitute easier targets after observing new responses, do not run Test for method selection, and do not claim worker–PPE ownership, verified safety compliance, explanation causal truth, inference energy or site-level generalization.

## 4. Exact worst-case model-call budget (all phases count, no free replays)

| Phase | Formula | Max calls |
|:--|:--|--:|
| Main 8×8 and 4×4 gray single-cell maps | 24 images × (64+16) | **1,920** |
| Original-image and shared Gaussian-baseline endpoints | 24 images × 2 | **48** |
| Ten seeded-random + saliency 8×8 progressive curves | 12 targets × 11 orders × 2 directions × 9 intermediates | **2,376** |
| Saliency 4×4 progressive curves | 12 targets × 2 directions × 9 intermediates | **216** |
| Blur-fill two-grid map ablation | 8 images × (64+16) | **640** |
| **Maximum intended experimental calls** | | **5,200** |
| Technical retry reserve, no additional research arms | Maximum | **800** |
| **HARD CAP: all new hosted model calls including failed attempts** | | **6,000** |

Hard-stop implementation must reject a call whose cumulative attempted count would exceed 6,000. A technical retry is allowed only for transient transport/provider error, with no more than one retry per image/mask and no target exclusions or protocol changes. If a preflight fails, **stop before spending**; do not use the reserve for a new D-RISE/D-MFPP arm or for extra targets. Hosted API credits/monetary charges per call require inspection in the author's account; **6,000 is a model request-count cap, not an agreed price**.

## 5. Model-agnostic comparison and published-method positioning

A fair head-to-head **D-RISE / D-MFPP** runtime comparison is *not included in 6,000 calls*. Such explainers require separate mask generation, target-scoring conventions, and a sufficiently large, equal-call budget to be meaningful. Do **not** manufacture an algorithm winner from unsupported proxy scores.

Literature and reproducibility comparators to document now:
- Andrés, A., Martínez-Seras, A., Laña, I. & Del Ser, J. (2024), “On the black-box explainability of object detection models for safe and trustworthy industrial applications”, *Results in Engineering*, 24, 103498, https://doi.org/10.1016/j.rineng.2024.103498. Discuss D-MFPP and D-Deletion, especially multiple same-class target handling, differing generated masks, and metric conventions.
- Petsiuk, V., et al. (2021), “Black-Box Explanation of Object Detectors via Saliency Maps”, CVPR, pp. 11443–11452, https://openaccess.thecvf.com/content/CVPR2021/html/Petsiuk_Black-Box_Explanation_of_Object_Detectors_via_Saliency_Maps_CVPR_2021_paper.html. Distinguish D-RISE random input masks from the current deterministic signed occlusion-response grids.

Study contribution remains **direct within-instance, two-grid empirical spatial alignment** under frozen detector and masks; neither new detector architecture nor calibrated explanation ground truth is claimed.

## 6. Statistical reporting and release

- **Primary statistic:** equal-image mean Spearman rho, 24 image-level averages of two target-level rho values. Report uncertainty from nonparametric bootstrap resampling images (e.g., 5,000 fixed-seed replicates), alongside 24 per-image points. Descriptive 95% bootstrap intervals are **not population-generalization intervals** because source images were not independently probability sampled.
- **Secondary:** per-target median/range, Kendall tau-b, top-four intersection, full class strata (4–5 targets each; flag any low stratum n), image-level leave-one-out analysis, signed coarse–fine differences, variability by operator, predeclared missing target counts and full random AUC distributions. No target/cell/curve-point independence tests as if those were sites.
- Avoid a formal proof of "stable" based on one fixed threshold; report the actual variation, failure cases and available intervals. Report any zero-overlap or sign reversals rather than omitting outliers.
- Frozen V30/V33/V34 findings remain archival; this extension is **a registered, development-exposed supplemental experiment**. If legally available genuinely independent field sites are later added, analyze separately with new consent/license review rather than relabeling these archived Valid images.
- Publication release remains gated by V37 authorship/ethics/CRediT/funding/COI/AI use/figures and real journal rules. No submission authorization is inferred from approval of experimental design.

**Status check:** planning / selection / budget freeze only. There are **no new V38-B model predictions, maps, AUCs, effect sizes or p-values** until a separately approved execution returns verifiable evidence.
