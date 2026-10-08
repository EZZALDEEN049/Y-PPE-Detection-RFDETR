# Stage 11E2 — Image-Cluster Bootstrap for mAP50:95 Domain Gaps

**Status: FROZEN BEFORE EXECUTION**

## Objective
Add 95% image-cluster bootstrap confidence intervals for the mean mAP50:95 domain-generalization gap without treating object instances within one image as independent.

## Why a new inference archive is required
The original Stage 6 outputs retained aggregate metrics but not the per-image ranked prediction statistics required to recompute AP under bootstrap resampling. Therefore AP uncertainty cannot be reconstructed validly from TP/FP/FN totals alone.

## Frozen procedure
1. Re-run the six primary **last.pt** checkpoints on the two unchanged frozen test sets under the exact Stage 6 AP settings:
   - imgsz=640
   - confidence floor=0.001
   - NMS IoU=0.70
   - no TTA
2. Use Ultralytics 8.4.156's own DetectionValidator matching procedure and retain, for every test image:
   - IoU-threshold TP matrix (0.50:0.95);
   - prediction confidence;
   - predicted class;
   - target class.
3. Verify that each reconstructed archive reproduces the corresponding validator mAP50:95 before any bootstrap result is accepted.
4. Perform **2,000** nonparametric bootstrap replicates with deterministic RNG seed **20261009**.
5. Resample **images**, not objects, with replacement. All objects and predictions belonging to a sampled image move together.
6. The same resampled image indices are applied to all three seed models for a given test domain, preserving the shared-test-set dependence across seeds.
7. Y-PPE and Construction-PPE test images are resampled independently.
8. For every replicate, recompute Ultralytics AP from the resampled ranked prediction statistics for each seed, then calculate:
   - mean in-domain mAP50:95 across the three seeds;
   - mean cross-domain mAP50:95 across the same three seeds;
   - gap = in-domain mean − cross-domain mean.
9. Replicates in which resampling removes every target instance of any originally represented canonical class are redrawn so the nine-class mAP estimand remains fixed.

## Interpretation
The resulting percentile 95% intervals quantify test-image sampling uncertainty conditional on the six trained YOLO11m realizations. They are not site-level population confidence intervals and do not convert the two source datasets into independent samples of all construction environments.

## Scientific safeguards
- inference only;
- no retraining;
- no fine-tuning;
- no checkpoint reselection;
- no threshold tuning;
- no change to the primary Stage 6 point estimates;
- primary checkpoint remains last.pt.
