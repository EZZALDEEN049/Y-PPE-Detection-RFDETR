# Stage 11D — Validation-Selected Checkpoint Sensitivity Protocol

**Status: FROZEN BEFORE EVALUATION**

## Reviewer concern
The primary study uses final-epoch `last.pt` checkpoints and a deliberately controlled no-online-augmentation recipe. A reviewer could argue that the observed domain gap partly reflects checkpoint policy rather than domain shift.

## Objective
Test whether the principal aggregate cross-domain degradation persists when the **validation-selected `best.pt` checkpoint** is used instead of `last.pt`.

This is a sensitivity analysis only. It does not replace the frozen primary Stage 6 analysis.

## Frozen design
- architecture: YOLO11m
- datasets: Y-PPE-h9-v2 and Construction-PPE-h9-v2
- seeds: 17, 42, 2026
- six already-completed Stage 5 runs
- checkpoint for this sensitivity analysis: `best.pt`
- no retraining
- no fine-tuning
- no target-domain adaptation
- no new threshold selection
- no test-informed checkpoint selection beyond the pre-existing validation-selected `best.pt`
- evaluation settings identical to Stage 6:
  - imgsz=640
  - AP confidence floor=0.001
  - fixed operating confidence=0.25
  - NMS IoU=0.70
  - class-matched IoU=0.50
  - no test-time augmentation

## Evaluation matrix
Exactly 12 cells:
- each of the six `best.pt` checkpoints
- evaluated on Y-PPE test and Construction-PPE test

## Primary comparison
For each source domain:
1. `last.pt` in-domain mean mAP50:95 vs `best.pt` in-domain mean;
2. `last.pt` cross-domain mean vs `best.pt` cross-domain mean;
3. domain gap under `last.pt` vs domain gap under `best.pt`;
4. fixed-operating recall/F1;
5. safety-class recall.

## Interpretation rule
If a substantial domain gap persists under `best.pt`, the conclusion becomes less dependent on the final-epoch checkpoint policy.

If `best.pt` materially improves in-domain and cross-domain performance but eliminates the domain gap, the manuscript must narrow the domain-shift claim.

No manuscript claim will be changed until all 12 sensitivity cells are complete.
