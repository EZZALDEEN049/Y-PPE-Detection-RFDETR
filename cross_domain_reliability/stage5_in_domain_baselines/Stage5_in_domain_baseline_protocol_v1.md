# Stage 5 — Harmonized In-Domain Baseline Protocol v1

**Status:** pre-execution protocol; Stage 4.5 label-completeness/background-policy gate is closed. No Stage 5 model result exists yet.

## Scientific prerequisite — Stage 4.5 (CLOSED)

The original Stage 4 nine-class derivatives retained cleaned source images while dropping non-shared annotation rows. Stage 4.5 tested whether that policy could silently convert visible retained-class objects into false background.

Stage 4.5 workflow run `35485667262` completed successfully. Its evidence artifact was `stage4-5-label-completeness-evidence` (`10597440734`, digest `sha256:086489f617e19c6483b3da5e7deb3f53acffb3701f279ffd835883fecf3b44ab`). Train/validation visual contact sheets were reviewed; held-out test image pixels were not opened for adjudication.

A deterministic annotation-only whole-image correction policy was then frozen in `Stage4_5_adjudication_and_policy_2026-09-20.md`. The corrected harmonized derivatives were rebuilt automatically in workflow run `35486021600`, which completed successfully. Evidence artifact: `stage4-5-corrected-h9-freeze-evidence` (`10598145018`, digest `sha256:e10b77a262490550014808b38644e433529f4547884552af33b7be97a88c8e3f`).

The correction changes dataset membership but does not relabel or infer annotations. Test membership is decided from annotation metadata only; no test visual adjudication or model output is used.

## Scientific objective

Establish controlled in-domain reference performance for the corrected nine-class derivatives before any zero-shot cross-domain claim is made.

Primary matrix:

- Y-PPE-h9-v2 train/val -> Y-PPE-h9-v2 held-out test
- Construction-PPE-h9-v2 train/val -> Construction-PPE-h9-v2 held-out test
- Architecture A: Ultralytics YOLO11m
- Architecture B: RF-DETR Small
- Seeds: 17, 42, 2026

This creates 12 independent training runs (2 datasets x 2 architectures x 3 seeds).

## Frozen dataset identity

### Y-PPE-h9-v2

Fingerprint:

`82669459c4c8b53535ee765321fa22277a1ef8d43695409ebb0d212764eb8b89`

Image counts:

- train: 1,340
- validation: 385
- test: 204

Retained shared-class instances: 9,471.

The Stage 4.5 policy removes 255/74/30 images from train/validation/test relative to the pre-Stage-4.5 clean source. Animal-only harmonized-empty images are retained as explicit negative images; other unsafe harmonized-empty images and images with critical unmatched excluded-class content are removed before harmonization.

### Construction-PPE-h9-v2

Fingerprint:

`59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`

Image counts:

- train: 1,046
- validation: 132
- test: 138

Retained shared-class instances: 9,514.

The Stage 4.5 policy removes 31/2/3 images from train/validation/test where unmatched `none` content or harmonized-empty membership could create false background.

Every Stage 5 run record must contain these corrected fingerprints. If a reconstructed derivative does not reproduce its expected fingerprint, training must stop.

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
- Primary reported checkpoint for architecture-to-architecture comparison: **final-epoch EMA checkpoint** after the fixed 100 epochs. This avoids validation-selected "best checkpoint" bias while using the final EMA representation produced natively by both training frameworks.
- Framework best-validation checkpoints may be retained as clearly labelled sensitivity results, but they must not replace the fixed-epoch primary comparison.
- No offline image augmentation is permitted. The corrected harmonized image membership must be preserved.
- Stochastic online augmentation is disabled in the primary controlled comparison.
- Held-out test metrics are computed only after the complete training run has finished and only with the frozen common evaluator.

### YOLO11m primary settings

- pretrained checkpoint: `yolo11m.pt`
- `imgsz=640`
- `epochs=100`
- `patience=0`; Stage 5 preflight run `35486220628` verified against Ultralytics 8.4.156 that this maps to infinite patience and therefore disables early stopping
- deterministic mode enabled
- all configurable color/geometric/mix augmentations set to zero
- no custom Albumentations augmentation stack
- optimizer: framework training recipe, recorded verbatim in run metadata
- primary fixed-epoch weights: final `last.pt`; Ultralytics checkpoints are serialized from the trainer EMA weights

### RF-DETR Small primary settings

- model class: `RFDETRSmall`
- pretrained RF-DETR Small checkpoint
- `resolution=640`
- `epochs=100`
- `early_stopping=False`
- `aug_config={}`
- `scale_jitter=False`
- `use_ema=True`
- primary fixed-epoch weights: final EMA checkpoint `last_ema.pth`
- optimizer and scheduler: RF-DETR native fine-tuning recipe, recorded verbatim in run metadata

The RF-DETR final-weight policy is frozen before the first full run. RF-DETR 1.10.1 explicitly writes `last_ema.pth` at fit end when EMA tracking is enabled, mirroring `last.pth` for the live model. This final-epoch EMA checkpoint is used rather than `checkpoint_best_total.pth`, because the latter is validation-selected and would violate the fixed-epoch primary comparison.

RF-DETR Small uses a detection block size of 32 (patch size 16 x two windows), so 640 is a valid controlled resolution.

## Framework layout compatibility without scientific data change

The corrected harmonized derivatives use an Ultralytics-style layout (`images/train`, `labels/train`, etc.). RF-DETR's YOLO loader expects a split-directory view such as `train/images`, `valid/images`, and `test/images`.

Stage 5 therefore uses `make_rfdetr_yolo_view.py` to create a deterministic **layout-only compatibility view** for RF-DETR. The adapter:

- preserves every image byte and label byte;
- preserves split membership and class IDs;
- copies the harmonized `manifest.jsonl` byte-for-byte;
- requires the expected corrected fingerprint before adapting;
- requires the same fingerprint after adapting;
- changes no annotation geometry or dataset content.

This is an implementation compatibility layer, not a new dataset version and not a preprocessing transformation.

`prepare_stage5_frozen_datasets.py` has been updated to reconstruct the corrected Stage 4.5 derivatives, enforce the two fingerprints above, and create RF-DETR compatibility views. It must still complete end-to-end on the actual Colab execution environment before the first full training run. Raw datasets remain outside Git and the Roboflow API key is read only from the environment.

## Hardware-dependent parameters not yet frozen

Physical batch size, gradient accumulation, worker count, AMP dtype, and exact GPU model are execution parameters. They must be chosen only after the actual Colab GPU preflight, then frozen per architecture before the first full run. They may not be changed between Y-PPE and Construction-PPE because of performance outcomes.

The run manifest must record:

- GPU model and VRAM
- CUDA version
- PyTorch version
- Ultralytics and RF-DETR package versions
- physical batch size
- gradient accumulation
- effective batch size
- mixed-precision mode
- final EMA checkpoint policy
- seed
- wall-clock training time

The corrected Stage 5 software/API preflight run `35486220628` passed. It verified the corrected dataset identities, the 12-run matrix, RF-DETR 640-pixel structural compatibility, RF-DETR layout adapter compatibility, and YOLO no-early-stop semantics. Exact application package versions are to be pinned for Colab; the Colab-compatible PyTorch/CUDA pair must be recorded from the actual GPU runtime rather than forced from the CPU-only GitHub runner.

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

## Remaining gate before full Stage 5 training

Stage 4.5 is closed, the corrected fingerprints are frozen, YOLO early-stopping semantics are verified, and the RF-DETR final EMA policy is frozen. Full training may begin only after:

1. `prepare_stage5_frozen_datasets.py` completes end-to-end on the actual Colab environment and reproduces both corrected fingerprints;
2. the actual Colab GPU hardware/software preflight is recorded;
3. physical batch size, RF-DETR gradient accumulation, worker count, and mixed-precision mode are frozen from a training-only resource preflight;
4. Colab application package versions are pinned and recorded.

Held-out test evaluation remains separately gated on freezing the common evaluator.

## Gate to Stage 6

Zero-shot cross-domain evaluation must not begin until:

1. all four in-domain model/dataset cells have completed the prespecified seed runs or a documented compute limitation is declared before inspecting target-test results;
2. run manifests are complete;
3. checkpoint provenance is preserved;
4. the common evaluator is frozen.
