# Stage 5 Colab Runtime Path Correction — 2026-09-21

## Status

**Pre-training software correction; no completed model run and no held-out test evaluation occurred before this correction.**

The first attempted Stage 5 run (`Y_YOLO_s17`) stopped during YOLO trainer initialization after approximately 10.5 seconds with exit code 1. `run_manifest_pre.json` and the Ultralytics run directory were created, but no checkpoint was produced and the orchestrator recorded zero completed runs.

## Root cause

The Stage 4.5 frozen derivatives intentionally contain a portable `data.yaml` with:

```yaml
path: .
train: images/train
val: images/val
test: images/test
```

Ultralytics resolves an explicit relative `path` against its configured global datasets directory rather than the YAML file's own directory. In the transient Google Colab runtime, `path: .` therefore does not reliably identify the verified frozen derivative root even though the YAML file itself is supplied by absolute path.

## Correction

`train_yolo11m_baseline.py` now creates a run-local runtime YAML before training. The runtime YAML is copied from the frozen YAML and changes only:

- `path: .` → the absolute, fingerprint-verified Stage 4.5 dataset root in the active runtime.

The following remain unchanged:

- Stage 4.5 manifest bytes and SHA256 fingerprint;
- image bytes and label bytes;
- class order and class IDs;
- train/validation/test split membership;
- split-relative paths (`images/train`, `images/val`, `images/test`);
- all training hyperparameters and seeds;
- the held-out test gate.

The frozen YAML SHA256 and the runtime adapter flag are recorded in every YOLO run manifest.

## Scientific interpretation

This is a transport/path-resolution correction only, not a dataset, protocol, or hyperparameter change. Because the first attempt produced no completed training run, no model metrics existed to influence this correction. The resource freeze must be regenerated after pulling the corrected repository SHA before retrying the training orchestrator.
