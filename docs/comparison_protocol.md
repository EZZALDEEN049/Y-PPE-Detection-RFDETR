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


---

## Verified status addendum — 22 November 2026 (Q15 Option C)

The public Roboflow records were rechecked read-only.

### Model and version metadata

- YOLOv11m: public project master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh, model altayyar-0oflt-lafos-qqauz-ty5nh/1, version 1; the version record identifies architecture yolov11m and training status finished.
- RF-DETR Small: public project softyyemen/altayyar-0oflt-lafos-qqauz, model altayyar-0oflt-lafos-qqauz/2, version 2; the connected-workspace training record identifies rfdetr-small and status finished.
- Both raw project records report 2,327 images, 17 classes, and 1,625/468/234 train/valid/test images.
- Both model-linked generated versions report 5,577 images and 4,875/468/234 train/valid/test counts. Both report Auto-Orient, stretch resize to 640×640, three image versions, and Mosaic.
- Both YOLOv8 dataset export requests returned ready=true. The archives have **not** been downloaded or hash-compared.

### Interpretation limits

Matching raw counts, generated counts, class names, and preprocessing/augmentation metadata do **not** prove identical image identities in the three splits. Exact filename/ID/hash comparison remains mandatory. Generated training augmentation copies must be separated from the 2,327-image original source roster.

The YOLO project belongs to the public master-fylfq workspace, while the connected Roboflow credential belongs to softyyemen. Public version reads and export succeeded, but workspace-scoped model-list/training-detail requests for YOLO were denied by the workspace boundary. This is an access limitation, not evidence that the model is absent. No raw checkpoint binary was downloaded, and no new YOLO inference was run.

The RF-DETR v2 training summary reports mAP50 93.97%, precision 94.36%, and recall 88.0%. A separate platform evaluation record reports mAP 0.9622053873, precision 0.952, recall 0.934, and F1 0.942. These are source-of-results records, not independent recomputations; do not mix them with YOLO figures as though a common evaluator and operating point had been used.

### SEER-PPE evidence reuse

SEER-PPE source-integrity and RF-DETR V26 outputs can be reused only within their recorded scope. The 459-row Validation crosswalk is provisional, and the SEER V26 summary records source independence as unverified. The stored V26 predictions support an RF-only retrospective Validation diagnostic, not a new paired model comparison or a fresh held-out Test result.

### Current gate

Q15 Option C is approved and partially executed. E1 and E2 remain **NOT PASSED**. Before a direct comparison, obtain both exports in controlled storage, hash and compare exact split membership, authenticate the 459-image crosswalk, resolve class/box conventions, verify checkpoint exposure, and produce both models' predictions on the same eligible roster. Then select thresholds on eligible Validation data only and evaluate once on an admissible held-out set.

Detailed public-safe evidence is recorded in [the Q1 progress checkpoint](../research/y-ppe-q1/PROGRESS_CHECKPOINT_2026-11-22.md) and [the Roboflow/SEER evidence audit](../research/y-ppe-q1/ROBOFLOW_SEER_EVIDENCE_AUDIT_2026-11-22.md).
