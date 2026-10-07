# Stage 6 — Frozen Held-Out Cross-Domain Evaluation Protocol

Status: **FROZEN before any held-out test evaluation**

## Scope
Stage 6 is evaluation-only. No training, fine-tuning, adaptation, checkpoint selection, threshold tuning, or test-informed model modification is permitted.

## Eligible models
Only the six completed YOLO11m Stage 5 runs are eligible:

- Y_YOLO_s17
- Y_YOLO_s42
- Y_YOLO_s2026
- C_YOLO_s17
- C_YOLO_s42
- C_YOLO_s2026

The primary checkpoint is the final-epoch checkpoint `last.pt` for every run. `best.pt` is not used for primary results.

## Frozen datasets
- Y-PPE-h9-v2 — fingerprint: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`
- Construction-PPE-h9-v2 — fingerprint: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`

Class order (9 classes):
`person, helmet, gloves, vest, boots, goggles, no_helmet, no_gloves, no_boots`

## Evaluation matrix
Each of the six models is evaluated on both frozen held-out test sets, giving exactly 12 evaluation cells:

- Y-trained models on Y-PPE test = in-domain
- Y-trained models on Construction-PPE test = cross-domain
- Construction-trained models on Construction-PPE test = in-domain
- Construction-trained models on Y-PPE test = cross-domain

## Frozen evaluation settings
- Input resolution: 640
- No test-time augmentation
- AP sweep confidence floor: 0.001
- Prediction NMS IoU: 0.70
- Primary AP metrics: mAP50:95, mAP50, mAP75
- Fixed operating point for P/R/F1 and safety FN analysis:
  - confidence = 0.25
  - class-matched detection IoU = 0.50
  - prediction NMS IoU = 0.70
- No threshold is selected after viewing test results.

## Reported outputs
For every evaluation cell:
- mAP50:95, mAP50, mAP75
- per-class AP50:95
- fixed-threshold micro Precision, Recall, F1
- fixed-threshold per-class TP, FP, FN, Precision, Recall, F1
- violation-focused FN for `no_helmet`, `no_gloves`, `no_boots`
- inference timing reported as descriptive only

Across the three seeds:
- mean
- standard deviation
- seed-level values

## Domain generalization gap
For each training domain and metric:

`Domain Gap = In-domain performance - Cross-domain performance`

Positive values indicate performance degradation under domain shift.

## Integrity rules
1. Held-out test labels must not be used for model selection.
2. No checkpoint may be changed after inspecting Stage 6 outcomes.
3. No confidence threshold may be tuned on either held-out test set.
4. Any failed evaluation cell must be rerun with identical frozen settings.
5. Partial or interrupted RF-DETR runs are excluded from Stage 6 primary results.
