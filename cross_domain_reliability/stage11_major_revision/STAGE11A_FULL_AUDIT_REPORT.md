# Stage 11A — Full Train/Test Dependence Audit

**Status: COMPLETE (audit); sensitivity re-evaluation pending GPU execution.**

## Scope
The audit distinguishes exact duplication, transformed near-duplication, and scene-level dependence. Similarity alone is not treated as leakage. No image was deleted from the frozen datasets.

## Results
- Total frozen images audited: **3,094**.
- Exact SHA-256 cross-split duplicate pairs: **0** in both datasets.
- Perceptual-hash candidates: **16** for Y-PPE-h9-v2 and **91** for Construction-PPE-h9-v2.
- Under the original strict image-wide pHash/SSIM confirmation rule, confirmed near-duplicate pairs: **0**. This rule is intentionally conservative and can miss transformed/cropped derivatives.
- Geometric feature matching identified high-confidence train/validation-to-test scene dependence for **6/186 Y-PPE test images (3.2%)** and **25/138 Construction-PPE test images (18.1%)** when train and validation links are combined.
- Restricting to direct **train→test** dependence gives **6/186 (3.2%)** for Y-PPE and **23/138 (16.7%)** for Construction-PPE.

## Evidence classification
Manual review of the high-confidence test-linked candidates produced the following conservative classification:

- **Y-PPE-h9-v2:** 4 near-duplicate test derivatives and 2 related-scene test images.
- **Construction-PPE-h9-v2:** 25 related-scene test images; **0 confirmed near-duplicates** under the evidence available.

The Construction-PPE cases are dominated by sequential/same-scene captures of the same workers and backgrounds. They are therefore treated as **scene-level dependence**, not automatically as data leakage.

## Sensitivity subsets frozen before re-evaluation

### A. Strict near-duplicate exclusion
- Y-PPE test: remove 4 visually confirmed near-duplicate derivatives → **182 images remain**.
- Construction-PPE test: remove 0 confirmed near-duplicates → **138 images remain**.

### B. Conservative train-scene independence
- Y-PPE test: remove all 6 high-confidence train-related test images → **180 images remain**.
- Construction-PPE test: remove all 23 high-confidence train-related test images → **115 images remain**.

These subsets are for **evaluation-only sensitivity analysis**. The six trained checkpoints, confidence threshold, NMS IoU, match IoU, and image size remain unchanged.

## Interpretation boundary
This audit does **not** establish that the original paper suffered confirmed dataset leakage. It establishes that a small number of Y-PPE test images are transformed near-duplicate derivatives and that scene-level dependence exists in both datasets, especially Construction-PPE. The material question is whether removing these cases materially changes the reported in-domain performance or cross-domain gap.
