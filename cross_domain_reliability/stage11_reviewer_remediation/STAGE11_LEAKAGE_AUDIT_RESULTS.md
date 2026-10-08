# Stage 11 — Cross-Split Duplicate / Near-Duplicate Leakage Audit

**Status:** SUBMISSION HOLD — high-confidence same-scene cross-split leakage candidates detected.

This audit was triggered by the external reviewer request for an explicit duplicate / near-duplicate check before submission.

## 1. Audit scope

The frozen Stage 4.5 derivatives were audited:

- Y-PPE-h9-v2: 1,236 train / 356 validation / 186 test images.
- Construction-PPE-h9-v2: 1,046 train / 132 validation / 138 test images.

Cross-split comparisons were performed for train↔validation, train↔test, and validation↔test.

## 2. Audit methods

The audit deliberately used multiple increasingly tolerant checks.

### Exact duplicates
SHA-256 hashes were computed from every encoded image file. Any identical hash appearing in more than one split was treated as an exact duplicate.

### Perceptual candidates
A 64-bit DCT perceptual hash (pHash) and a 64-bit difference hash (dHash) were computed for each image. A pair became a candidate when either Hamming distance was <= 6.

### Geometric same-scene confirmation
Candidate pairs were compared with ORB keypoints and RANSAC homography. To define a conservative **high-confidence same-scene near-duplicate candidate**, the final exclusion audit uses all of the following:

- at least 100 RANSAC inlier matches;
- inlier ratio >= 0.50;
- source-keypoint spatial coverage >= 0.05 of image area.

These are image-similarity criteria only. No model prediction, class score, test metric, or manuscript result was used.

## 3. Exact duplicate result

**No exact SHA-256 cross-split duplicate pairs were found in either dataset.**

This is reassuring but does not rule out consecutive frames, transformed copies, or closely related views.

## 4. High-confidence same-scene findings

Using the conservative ORB/RANSAC criterion above, the audit found 74 high-confidence cross-split same-scene pairs.

### Construction-PPE-h9-v2

- train↔validation: 19 pairs, involving 14 unique validation images;
- train↔test: 33 pairs, involving 23 unique test images;
- validation↔test: 7 pairs, involving 7 unique test images;
- unique test images linked to train and/or validation: **25 / 138 (18.1%)**.

A visually verified example is the worker sequence in which train image912.jpg and test image913.jpg depict essentially the same scene and subject with only a small pose/frame change.

### Y-PPE-h9-v2

- train↔validation: 7 pairs, involving 6 unique validation images;
- train↔test: 7 pairs, involving 6 unique test images;
- validation↔test: 1 pair, involving 1 test image;
- unique test images linked to train and/or validation: **6 / 186 (3.2%)**.

Visually verified examples include transformed/adjacent footwear images appearing across train/test or validation/test.

## 5. Interpretation

The earlier structural statement of “0 source/video cross-split groups” is not sufficient as a modern near-duplicate audit. The stricter pixel/feature audit detects related same-scene images that are not byte-identical.

This finding does **not** prove that all original Stage 6 results are invalid. It does mean that in-domain performance may be optimistic because a subset of held-out images has strong same-scene similarity to train/validation content. Cross-domain models do not receive the target-domain train split, so the inflation can be asymmetric and can make the apparent domain gap larger.

Therefore, the current manuscript must not be submitted until a leakage-safe sensitivity evaluation is completed.

## 6. Leakage-safe sensitivity population

To minimize false-positive exclusions, only the high-confidence threshold above is used.

- Y-PPE leakage-safe test: **180 images** (6 excluded).
- Construction-PPE leakage-safe test: **113 images** (25 excluded).

The exclusion is post-hoc and based only on visual similarity. It is therefore reported as a **leakage-corrected sensitivity analysis**, not as a preregistered replacement of the original frozen Stage 6 protocol.

## 7. Required next evaluation

On the same leakage-safe test images, evaluate:

1. all six `last.pt` checkpoints;
2. all six `best.pt` checkpoints;
3. both target domains for every checkpoint;
4. the same AP and fixed operating-point thresholds as Stage 6;
5. safety-class recall and three-seed consensus false negatives.

This produces 24 leakage-safe evaluation cells and simultaneously addresses the reviewer’s best-vs-last checkpoint sensitivity concern.

No retraining is required for this sensitivity analysis.
