# YOLOv11 vs RF-DETR Comparison Protocol

## Purpose

This document defines the minimum evidence required before reporting a direct performance comparison between the two Roboflow-trained Y-PPE model tracks.

## Experiment A — YOLOv11 Medium

- Roboflow project: `master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh`
- Model ID: `altayyar-0oflt-lafos-qqauz-ty5nh/1`
- Dataset version: `1`
- Architecture: YOLOv11 Object Detection (Medium)
- Public platform metrics: mAP@50 = 92.2%, Precision = 95.3%, Recall = 87.2%

## Experiment B — RF-DETR Small

- Roboflow project: `softyyemen/altayyar-0oflt-lafos-qqauz`
- Model ID: `altayyar-0oflt-lafos-qqauz/2`
- Dataset version: `2`
- Architecture: RF-DETR (Small)
- Public platform metrics: mAP@50 = 94.0%, Precision = 94.4%, Recall = 88.0%

## Publicly Verified Dataset Configuration

The public Roboflow dataset pages report the same configuration for both model-linked versions:

- Total generated images: 5,577
- Train: 4,875 images (88%)
- Validation: 468 images (8%)
- Test: 234 images (4%)
- Preprocessing: Auto-Orient applied
- Resize: Stretch to 640 × 640
- Augmentation outputs per training example: 3
- Mosaic augmentation: applied
- Classes: 17

## What Is Not Yet Proven

Matching counts and preprocessing settings do not prove that the exact same source images belong to the train, validation, and test partitions in the two projects. Before treating the metrics as a controlled head-to-head experiment, verify split membership directly using exported file lists, image identifiers, or hashes.

## Required Split Identity Check

For each exported dataset version:

1. Record every image filename in `train`, `valid`, and `test`.
2. Preferably compute SHA-256 hashes for original image files.
3. Compare the sets between the YOLOv11-linked and RF-DETR-linked exports.
4. Report:
   - train intersection and mismatch count;
   - validation intersection and mismatch count;
   - test intersection and mismatch count.
5. A strict controlled comparison requires zero split-membership mismatches, or a documented re-evaluation of both models on one common held-out test set.

## Evaluation Controls

For the final paper comparison, use a common evaluation protocol whenever possible:

- same held-out test images;
- same class mapping;
- same IoU definition;
- same confidence handling;
- same mAP convention (including mAP@50 and, preferably, mAP@50:95);
- same per-class evaluation procedure;
- same hardware and timing method for latency/FPS comparisons.

## RF-DETR Metric Discrepancy

The RF-DETR Universe overview currently reports mAP@50 = 94.0%, while the free-text project description states 96.2% mAP@50 on an "independent test set." The 96.2% value must not be used as the principal comparison result unless its test set, evaluation procedure, and source artifact are documented. Until then, treat 94.0% as the platform-reported public metric and flag 96.2% as an unverified project-description claim.

## Current Methodological Status

The two model tracks are highly comparable in their publicly reported dataset size, split counts, preprocessing, augmentation, and class count. However, exact split identity has not yet been verified from the public pages. Therefore the current Roboflow metrics may be presented descriptively as platform-reported results, but a strong causal statement that one architecture outperforms the other should wait until the split identity/common-test-set check is complete.
