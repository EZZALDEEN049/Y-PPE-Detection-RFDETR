# Stage 5 — Harmonized In-Domain Baseline Protocol v1

**Status:** pre-execution protocol; full training is on scientific HOLD until Stage 4.5 label-completeness/background-policy closure. No Stage 5 model result exists yet.

## Scientific prerequisite — Stage 4.5

The frozen Stage 4 nine-class derivatives retain cleaned source images while dropping non-shared annotation rows. Before any full Stage 5 training, the Stage 4.5 label-completeness/background-policy audit must be closed. That audit checks whether excluded native annotations can leave visible retained-class objects unlabeled and therefore convert valid objects into false background.

Stage 4.5 closure requires structural annotation analysis, train/validation-only visual adjudication, a predeclared annotation-only test policy without opening test pixels, and—if any membership or annotation changes are required—a new harmonized derivative and new fingerprints. The Stage 4 fingerprints below remain provisional Stage 5 inputs until that gate is closed.

## Scientific objective

Establish controlled in-domain reference performance for the accepted nine-class derivatives before any zero-shot cross-domain claim is made.

Primary matrix:

- Y-PPE-h9 train/val -> Y-PPE-h9 held-out test
- Construction-PPE-h9 train/val -> Construction-PPE-h9 held-out test
- Architecture A: Ultralytics YOLO11m
- Architecture B: RF-DETR Small
- Seeds: 17, 42, 2026

This creates 12 independent training runs (2 datasets x 2 architectures x 3 seeds).

## Frozen dataset identity

Current Stage 4 Y-PPE-h9 fingerprint:

`db49295a0ef2c9eec73b14c620966ed00bf12dac253866b65bab9b50af9db896`

Current Stage 4 Construction-PPE-h9 fingerprint:

`bd706ae34aa77507f119a9a4d5cd443d4cb84ee6cd2020b9b8ee6e086350880e`

Every Stage 5 run record must contain the final accepted fingerprints after Stage 4.5 closure. If Stage 4.5 produces a corrected derivative, these fingerprints must be superseded rather than silently reused. If a reconstructed derivative does not reproduce its expected fingerprint, training must stop.

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

### Shared controls

- COCO-pretrained initialization for both architectures.
- Square input resolution: **640 x 640** for the controlled primary comparison.
- Fixed maximum training duration: **100 epochs**.
- Fixed seeds: **17, 42, 2026**.
- No test image is used for hyperparameter selection, stopping, threshold selection, or checkpoint selection.
- Validation data may be used for training monitoring only.
- Primary reported checkpoint for architecture-to-architecture comparison: **final epoch checkpoint** after the fixed 100 epochs. This avoids framework-specific differences in "best checkpoint" selection rules.
- Framework best-validation checkpoint may be retained as a clearly labelled sensitivity result, but it must not replace the fixed-epoch primary comparison.
- No offline image augmentation is permitted. The final accepted harmonized image membership must be preserved.
- Stochastic online augmentation is disabled in the primary controlled comparison.
- Held-out test metrics are computed only after the complete training run has finished and only with the frozen common evaluator.

### YOLO11m primary settings

- pretrained checkpoint: `yolo11m.pt`
- `imgsz=640`
- `epochs=100`
- `patience=0` in the current implementation candidate; exact no-early-stop behavior must be verified against the pinned Ultralytics version before the first full run
- deterministic mode enabled
- all configurable color/geometric/mix augmentations set to zero
- no custom Albumentations augmentation stack
- optimizer: framework training recipe, recorded verbatim in run metadata

### RF-DETR Small primary settings

- model class: `RFDETRSmall`
- pretrained RF-DETR Small checkpoint
- `resolution=640`
- `epochs=100`
- `early_stopping=False`
- `aug_config={}`
- `scale_jitter=False`
- `use_ema=True` may remain enabled for training-state tracking, but the fixed-epoch primary result must explicitly state whether final raw or final EMA weights are evaluated; this choice must be locked before the first full training run and then held constant across both datasets and all seeds.
- optimizer and scheduler: RF-DETR native fine-tuning recipe, recorded verbatim in run metadata

RF-DETR Small uses a detection block size of 32 (patch size 16 x two windows), so 640 is a valid controlled resolution.

## Framework layout compatibility without scientific data change

The Stage 4 harmonized derivatives use an Ultralytics-style layout (`images/train`, `labels/train`, etc.). RF-DETR's YOLO loader expects a split-directory view such as `train/images`, `valid/images`, and `test/images`.

Stage 5 therefore uses `make_rfdetr_yolo_view.py` to create a deterministic **layout-only compatibility view** for RF-DETR. The adapter:

- preserves every image byte and label byte;
- preserves split membership and class IDs;
- copies the harmonized `manifest.jsonl` byte-for-byte;
- requires the expected harmonized fingerprint before adapting;
- requires the same fingerprint after adapting;
- changes no annotation geometry or dataset content.

This is an implementation compatibility layer, not a new dataset version and not a preprocessing transformation.

`prepare_stage5_frozen_datasets.py` is an execution candidate for reconstructing the harmonized derivatives from audited sources and correction manifests, checking fingerprints, and creating RF-DETR compatibility views. Its end-to-end reconstruction must itself pass on the actual execution environment before it is used for full training. Raw datasets remain outside Git and the Roboflow API key is read only from the environment.

## Hardware-dependent parameters not yet frozen

Physical batch size, gradient accumulation, worker count, AMP dtype, exact GPU model, and final RF-DETR raw-vs-EMA weight policy are execution parameters. They must be chosen only after GPU preflight, then frozen per architecture before the first full run. They may not be changed between Y-PPE and Construction-PPE because of performance outcomes.

The run manifest must record:

- GPU model and VRAM
- CUDA version
- PyTorch version
- Ultralytics and RF-DETR package versions
- physical batch size
- gradient accumulation
- effective batch size
- mixed-precision mode
- RF-DETR final raw-vs-EMA weight policy
- seed
- wall-clock training time

The Stage 5 CI preflight discovers and records the currently installed software versions. Exact package versions must then be pinned before the first full GPU training run; no training should start against floating package versions.

## Evaluation policy

Framework validation metrics may be used for training diagnostics only. The paper's held-out test comparison will use one common post-training evaluator applied to predictions from both architectures. The common evaluator must be frozen **before any held-out test metric is computed**, not merely before Stage 6.

Required final metrics include at least:

- mAP50:95
- mAP50
- precision
- recall
- F1
- per-class AP
- macro summaries
- violation-focused false-negative metrics for no_helmet, no_gloves, and no_boots

Calibration, reliability, safety loss, LRP-style localization error, and target-domain adaptation belong to later stages and must not be inferred from Stage 5 alone.

## Statistical policy

For each dataset/model cell, report the three seed-level results and mean with dispersion. Do not treat the seeds as independent images. Later model-to-model significance comparisons on the same held-out test images must use paired image-level resampling; seed variability is reported separately.

## Gate to Stage 6

Zero-shot cross-domain evaluation must not begin until:

1. Stage 4.5 is closed and the final accepted harmonized fingerprints are frozen;
2. all four in-domain model/dataset cells have completed the prespecified seed runs or a documented compute limitation is declared before inspecting target-test results;
3. run manifests are complete;
4. checkpoint provenance is preserved;
5. the common evaluator is frozen.
