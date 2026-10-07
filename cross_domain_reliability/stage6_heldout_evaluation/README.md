# Stage 6 — Frozen Held-Out Evaluation

This folder implements the evaluation-only phase of the cross-domain PPE reliability study.

Primary rule: **no new training**. Only the six completed YOLO11m Stage 5 `last.pt` checkpoints are evaluated.

## Run

```bash
python cross_domain_reliability/stage6_heldout_evaluation/evaluate_yolo_cross_domain.py \
  --stage5-root /content/drive/MyDrive/Stage5_Baselines \
  --y-data /path/to/Y-PPE-h9-v2/data.yaml \
  --c-data /path/to/Construction-PPE-h9-v2/data.yaml \
  --out /content/drive/MyDrive/Stage6_Heldout_Evaluation \
  --device 0
```

The script produces exactly 12 cells (6 completed models × 2 held-out test domains), with one JSON result per cell plus a consolidated CSV and JSON.

Read `STAGE6_PROTOCOL_FROZEN.md` before execution.
