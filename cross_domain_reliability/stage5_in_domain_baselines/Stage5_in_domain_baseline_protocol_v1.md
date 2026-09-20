# Stage 5 — Harmonized In-Domain Baseline Protocol v1

**Status:** pre-execution protocol. Stage 4.5 label-completeness/background-policy gate is closed. No Stage 5 model result exists yet.

## Scientific prerequisite — Stage 4.5 (CLOSED)

The original Stage 4 derivatives retained all cleaned source images while dropping nonshared annotations, creating a potential false-background/missing-ground-truth risk. Stage 4.5 audited this risk and froze a model-independent conservative whole-image policy.

Final freeze evidence:

- Workflow: `Stage 4.5 Conservative Harmonized v2 Freeze`
- Run ID: `35536050231`
- Head SHA: `eb87aa14dab07d7546e713c2d5eb68ef583f2d5a`
- Artifact: `stage4-5-conservative-harmonized-v2-evidence`
- Artifact ID: `10612876023`
- Digest: `sha256:24b5851f8eef044e17d6804272db2965fed9737098718ed229d0e5a57028786f`

The frozen rule excludes any image that either becomes empty after nine-class harmonization or contains at least one critical unmatched source annotation under IoU >= 0.50 OR excluded-box containment >= 0.80. Membership uses source annotation metadata/geometry only. No model prediction was used, and held-out test image pixels were not opened for adjudication. Both final derivatives contain zero harmonized-empty images.

## Scientific objective

Establish controlled in-domain reference performance on the final structurally harmonizable nine-class subsets before any zero-shot cross-domain claim.

Primary matrix: 2 datasets x 2 architectures x 3 seeds = 12 independent training runs.

- datasets: `Y-PPE-h9-v2`, `Construction-PPE-h9-v2`
- architectures: Ultralytics YOLO11m, RF-DETR Small
- seeds: 17, 42, 2026

## Frozen dataset identity

### Y-PPE-h9-v2

- fingerprint: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`
- train: 1,236
- validation: 356
- test: 186
- retained shared-class instances: 9,471
- Stage 4.5 exclusions: 359/103/48 images from train/validation/test

### Construction-PPE-h9-v2

- fingerprint: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`
- train: 1,046
- validation: 132
- test: 138
- retained shared-class instances: 9,514
- Stage 4.5 exclusions: 31/2/3 images from train/validation/test

Every Stage 5 run must carry the exact relevant fingerprint. Any mismatch stops execution.

## Frozen class order

0. person
1. helmet
2. gloves
3. vest
4. boots
5. goggles
6. no_helmet
7. no_gloves
8. no_boots

## Controlled training design

Shared controls:

- COCO-pretrained initialization for both architectures.
- square input resolution 640 x 640.
- exactly 100 epochs.
- seeds 17, 42, 2026.
- no held-out test use for hyperparameter selection, stopping, threshold selection, or checkpoint selection.
- validation may be used for training monitoring only.
- primary checkpoint is the final-epoch EMA representation, not a validation-selected best checkpoint.
- no offline augmentation and stochastic online augmentation disabled for the primary controlled comparison.

### YOLO11m

- checkpoint: `yolo11m.pt`
- `imgsz=640`, `epochs=100`, deterministic mode enabled.
- `patience=0`; pinned Ultralytics 8.4.156 preflight verifies this maps to infinite patience and disables early stopping.
- configurable color/geometric/mix augmentations set to zero; no custom Albumentations stack.
- optimizer: framework-native recipe, recorded verbatim.
- primary weights: final `last.pt`, serialized from trainer EMA weights.

### RF-DETR Small

- `RFDETRSmall`, pretrained initialization.
- `resolution=640`, `epochs=100`, `early_stopping=False`.
- `aug_config={}`, `scale_jitter=False`, `use_ema=True`.
- primary final weights: `last_ema.pth`, not validation-selected `checkpoint_best_total.pth`.
- optimizer/scheduler: framework-native fine-tuning recipe, recorded verbatim.
- 640 is valid for the 32-pixel RF-DETR Small block size.

## Layout compatibility

The final harmonized derivatives use `images/train`, `labels/train`, etc. `make_rfdetr_yolo_view.py` creates a layout-only RF-DETR view while preserving image bytes, label bytes, split membership, class IDs, and `manifest.jsonl`; the same dataset fingerprint must hold before and after adaptation.

`prepare_stage5_frozen_datasets.py` reproduces the successful conservative Stage 4.5 policy, enforces the final fingerprints/counts, verifies zero empty labels, and creates the RF-DETR compatibility views. It must complete end-to-end in the actual Colab runtime before full training.

## Hardware-dependent parameters still to freeze

Before the first full run, the actual Colab environment must record and freeze per architecture:

- GPU model and VRAM
- NVIDIA driver/CUDA runtime
- PyTorch version
- Ultralytics/RF-DETR/Roboflow/PyYAML versions
- physical batch size
- RF-DETR gradient accumulation and effective batch size
- worker count
- mixed-precision mode

The same architecture-specific execution policy must be used on both datasets and may not be changed in response to performance.

## Evaluation policy

Training scripts do not evaluate held-out test data. Framework validation metrics are diagnostic only. Paper-level held-out test comparison uses a single common evaluator frozen before any held-out test metric is computed.

Required Stage 5 final metrics include mAP50:95, mAP50, precision, recall, F1, per-class AP, macro summaries, and violation-focused false-negative metrics for `no_helmet`, `no_gloves`, and `no_boots`.

Calibration/reliability/safety-loss/LRP-style error and adaptation belong to later stages and must not be inferred from Stage 5 alone.

## Statistical policy

Report all three seed-level results per dataset/model cell plus mean and dispersion. Seeds are not independent images. Later architecture comparisons on the same held-out test images require paired image-level resampling; seed variability is reported separately.

## Remaining gate before full Stage 5 training

Full training may begin only after:

1. final dataset materialization succeeds end-to-end in Colab and reproduces both frozen fingerprints/counts;
2. Colab GPU/software preflight is archived;
3. batch size, RF-DETR gradient accumulation, worker count, and mixed precision are frozen from a training-only resource preflight;
4. application package versions are pinned/recorded.

Held-out test evaluation remains separately blocked until the common evaluator is frozen.
