# Stage 9 — Evidence and Administrative Audit

**Status:** evidence consolidation complete; a small number of administrative confirmations remain before submission.

## A. Dataset identity and provenance

### Y-PPE source corpus

Evidence from the master's thesis and published project materials establishes the original Y-PPE corpus as:

- 2,327 original annotated images;
- 16,520 annotated instances;
- 17 original classes;
- raw split: 1,625 train / 468 validation / 234 test;
- localized construction/development-project imagery from Yemen, supplemented by a limited number of vetted open-access images for rare/contextual categories.

The thesis states that the primary raw image corpus was obtained through formal coordination with the Social Fund for Development (SFD) and partner civil-society organizations, using routine field documentation captured by site engineers and safety supervisors. It also states that some supplementary images were sourced from open-access repositories.

The public Roboflow Universe project currently declares **CC BY 4.0** for the ALTAYYAR/Y-PPE dataset and exposes the 2,327-image, 17-class project.

**Submission caution:** the public CC BY 4.0 declaration documents the current dataset-level license on Roboflow, but the manuscript should still retain a clear statement describing the original field-image permissions/organizational authorization and the handling of any externally sourced images. A public platform license should not be treated as a substitute for documenting underlying image provenance.

### Construction-PPE source corpus

Official Ultralytics documentation establishes:

- dataset version: 1.0.0;
- 1,416 images;
- 1,132 train / 143 validation / 141 test;
- 11 original classes;
- object-detection annotations in Ultralytics YOLO format;
- license: **AGPL-3.0**;
- canonical source: Ultralytics Construction-PPE.

The study's source record pins the official YAML metadata and class order before harmonization.

## B. Final harmonized datasets used in the paper

The paper does **not** train on the original Y-PPE 17-class corpus or the original Construction-PPE 11-class corpus directly.

The final Stage 4.5 conservative derivatives are:

### Y-PPE-h9-v2
- train: 1,236 images
- validation: 356 images
- test: 186 images
- retained shared-class instances: 9,471
- fingerprint: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`

### Construction-PPE-h9-v2
- train: 1,046 images
- validation: 132 images
- test: 138 images
- retained shared-class instances: 9,514
- fingerprint: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`

The exact shared class order is:

`person, helmet, gloves, vest, boots, goggles, no_helmet, no_gloves, no_boots`

The conservative filter excluded images that would become empty after harmonization or contained critical unmatched source annotations under the frozen structural rule. No model predictions were used for dataset membership and held-out test pixels were not opened during adjudication.

## C. Semantic harmonization evidence

The nine-class ontology was frozen before the final baseline training.

Key mappings include:

- Y-PPE `Persons` ↔ Construction-PPE `Person` → `person`
- `Hard Hat` ↔ `helmet` → `helmet`
- `Safety Boots` ↔ `boots` → `boots`
- `No Hard Hat` ↔ `no_helmet` → `no_helmet`
- `No Gloves` ↔ `no_gloves` → `no_gloves`
- `No Safety Boots` ↔ `no_boots` → `no_boots`

Y-PPE `No Safety Vest` was excluded because Construction-PPE has no direct `no_vest` class. Construction-PPE `no_goggle` and `none` were excluded because no strict Y-PPE semantic counterpart was established.

The ontology explicitly guards against interpreting dataset-defined negative-state labels as proof that a particular PPE item was normatively required in every scene.

## D. Stage 5 training settings for the CURRENT paper

These settings must not be confused with the older Roboflow-managed thesis benchmark.

The current cross-domain paper uses the frozen Stage 5 local YOLO11m protocol:

- architecture: YOLO11m
- initialization: `yolo11m.pt` pretrained checkpoint
- epochs: 100 exactly
- input size: 640 × 640
- seeds: 17, 42, 2026
- physical batch size: 8
- workers: 2
- mixed precision: CUDA AMP enabled
- stochastic online augmentation: disabled
- early stopping: disabled (`patience=0`, verified under the pinned Ultralytics version)
- primary checkpoint: final-epoch `last.pt`, not validation-selected `best.pt`
- GPU: Tesla T4
- Python: 3.13.15
- PyTorch: 2.11.0+cu128
- CUDA runtime: 12.8
- Ultralytics: 8.4.156
- optimizer policy: Ultralytics `optimizer=auto`; recorded training logs resolve this to AdamW
- representative frozen logs record AdamW with learning rate 0.000769, momentum 0.9, and decay 0.0005 for decayed weight groups.

The six completed runs differ only in source dataset and random seed under the frozen YOLO execution policy.

## E. Historical-thesis settings that MUST NOT be imported into this paper

The master's thesis/published benchmark describes a different Roboflow-managed experiment, including a YOLOv11m run with 300 epochs and platform-managed/auto-tuned optimization. Those settings belong to the historical 17-class thesis benchmark.

They are **not** the settings of the current nine-class cross-domain paper.

This distinction must remain explicit in the Methods section to avoid a reproducibility error.

## F. Held-out integrity

Stage 6 was frozen before held-out testing:

- no fine-tuning or adaptation on test data;
- no checkpoint reselection after test exposure;
- no test-informed confidence tuning;
- final-epoch checkpoints only;
- exactly 12 held-out evaluation cells (6 completed models × 2 test domains).

## G. Administrative items still requiring explicit author confirmation

The following cannot be truthfully inferred from the available files and should remain unresolved until the author confirms them:

1. exact funding statement for this new paper;
2. exact competing-interests statement;
3. final CRediT author-contribution statement;
4. exact institutional/organizational wording for permission to use and publicly redistribute the field images;
5. whether a formal ethics/IRB waiver, approval, or institutional determination exists for the image dataset;
6. the final archival repository/DOI or immutable release identifier for code and derived data.

Until confirmed, the manuscript should use placeholders rather than invented declarations.
