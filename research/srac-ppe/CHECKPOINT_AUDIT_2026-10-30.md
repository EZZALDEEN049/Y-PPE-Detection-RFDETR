# Checkpoint provenance audit — 2026-10-30

**Status:** VERIFIED METADATA, NOT A VALIDATED NEW SRAC-PPE EXPERIMENT.

## Newly located private checkpoint
The researcher's connected Google Drive contains `Y_RFDETR_s17/train/checkpoint_best_ema.pth` and larger training-state checkpoints. The lightweight EMA checkpoint was fetched into a temporary controlled runtime and loaded with `torch.load(..., map_location="cpu", weights_only=True)`.

**Verified safe-read metadata:**
- File SHA-256: `398b8444a71391990ca54922d8a112b2f27dfcea226e1e7e4a6575d2ee10235d`.
- Model class: `RFDETRSmall`; recorded package: `rfdetr 1.10.1`.
- Head/class configuration: **9 dataset classes** (10 class-head output slots, including no-object/background as configured by that model architecture).
- Training data recorded by `run_manifest_pre.json`: `Y-PPE-h9-v2`, seed 17, image resolution 640, planned 100 epochs.
- Best EMA checkpoint records zero-indexed epoch 13. A separate trainer metrics file contains validation entries through epoch 49. **Do not assume a full 100-epoch training run**.
- `run_manifest_pre.json` explicitly states `test_evaluation_performed=false`.

## Identity distinction: CRITICAL
This is **NOT** the same proven checkpoint as the publicly hosted Roboflow model `altayyar-0oflt-lafos-qqauz/2`, which is a distinct **17-original-class** track. Do not substitute the nine-class checkpoint for the named 17-class frozen deployment model, even though both use an RF-DETR Small architecture.

## Inference status
No actual model predictions have been extracted or benchmarked using this checkpoint during this audit. The execution environment has a CPU-only PyTorch installation but lacks the matching `rfdetr` package, and outbound package installation was unavailable. Inference is therefore **BLOCKED**, not validated. The file is present in restricted storage; **no model weights or private images are committed**.

## Next verified gate
For a secondary (not primary) baseline, reconstruct the exact RF-DETR 1.10.1 environment using authorized controlled compute, load this 9-class checkpoint explicitly, record class map/resolution/checkpoint hash, run a *source-group-clean* evaluation set, then compare only with other models on the same supported ontology and test images. The primary 17-class model requires separate authorized inference.

Official model loading documentation: https://rfdetr.roboflow.com/latest/learn/train/
