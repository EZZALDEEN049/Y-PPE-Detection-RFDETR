# Verified Asset Inventory

## Completed detector runs

Six YOLO11m runs are available and marked training-complete:

| Domain | Seed | Run ID | Primary checkpoint |
|---|---:|---|---|
| Y-PPE-h9-v2 | 17 | Y_YOLO_s17 | last.pt |
| Y-PPE-h9-v2 | 42 | Y_YOLO_s42 | last.pt |
| Y-PPE-h9-v2 | 2026 | Y_YOLO_s2026 | last.pt |
| Construction-PPE-h9-v2 | 17 | C_YOLO_s17 | last.pt |
| Construction-PPE-h9-v2 | 42 | C_YOLO_s42 | last.pt |
| Construction-PPE-h9-v2 | 2026 | C_YOLO_s2026 | last.pt |

Each completed run also contains a validation-selected `best.pt` checkpoint. The prior held-out study used `last.pt` as its primary checkpoint policy; `best.pt` is retained for sensitivity analysis.

## Frozen training environment recorded by run manifests

- model family: YOLO11m
- epochs: 100
- image size: 640
- batch size: 8
- workers: 2
- AMP: enabled
- early stopping: disabled
- stochastic online augmentation: disabled
- GPU: NVIDIA Tesla T4
- Python: 3.13.15
- PyTorch: 2.11.0+cu128
- CUDA runtime: 12.8
- Ultralytics: 8.4.156

The Y-PPE seed-2026 run was resumed from its own checkpoint and completed the planned 100-epoch run. This provenance must remain visible in any final reproducibility statement.

## Dataset fingerprints

- Y-PPE-h9-v2: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`
- Construction-PPE-h9-v2: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`

Shared class order:

`person, helmet, gloves, vest, boots, goggles, no_helmet, no_gloves, no_boots`

## Held-out evaluation already available

Stage 6 is marked complete with:
- six eligible YOLO11m models;
- two test domains;
- 12 evaluation cells;
- final-epoch `last.pt` checkpoint policy;
- no new training during held-out evaluation.

Aggregate metrics are already archived, but the Stage 6 output folders contain metrics summaries rather than reusable per-image detection tables. Therefore the new EcoSafe extension requires a deterministic prediction export pass from the existing checkpoints.

## Storage policy

Do not copy large checkpoint files into the public Git repository. Keep weights and raw/frozen datasets in external storage and version only:
- path conventions;
- hashes/fingerprints where available;
- scripts;
- configuration;
- derived lightweight tables;
- manuscript evidence.
