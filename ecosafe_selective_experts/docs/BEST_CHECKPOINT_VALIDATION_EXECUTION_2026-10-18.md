# Reproducible EcoSafe best.pt sensitivity (separate from primary last.pt)

**Scope:** Six existing validation-selected `best.pt` weights, both frozen nine-class **validation-only** splits, seeds 17 / 42 / 2026, two original domain-specific YOLO11m experts per seed. **No retraining or held-out test exposure.** Results may be optimistically biased because original best.pt checkpoint choice depended on validation performance.

Original primary evidence remains checkpoint-policy `last.pt` and is not modified. `best.pt` validation outputs have a **separate checkpoint SHA-256 registry** and `__BEST_VAL_` output prefix so they cannot silently collide with the primary protocol.

## Offline/private execution

Use PyTorch, Ultralytics **8.4.156**, and the exact validation-only archive from GitHub Actions run `38826721499`. Preserve the two source manifests:
- Y-PPE-h9-v2: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`.
- Construction-PPE-h9-v2: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`.

Model weights: six **original** `Stage5_Baselines/{Y,C}_YOLO_s{17,42,2026}/train/weights/best.pt` files in **private authorized storage**. Their expected byte counts and SHA-256 checks are pinned in `scripts/11_export_best_validation_chunks.py`; stop on any mismatch.

Example private CPU command, repeated for each seed, expert, domain and chunk:

```bash
python ecosafe_selective_experts/scripts/11_export_best_validation_chunks.py \
  --validation-root /private/FROZEN_VALIDATION \
  --checkpoint /private/Stage5_Baselines/C_YOLO_s17/train/weights/best.pt \
  --model-id C_YOLO_s17 --domain c \
  --chunk-index 0 --chunk-size 16 \
  --out-dir /private/EcoSafe_BestPt_Validation --device cpu --cpu-threads 4
```

For Construction `c`, repeat chunk indices 0–8 (132 images); for Y-PPE `y`, indices 0–22 (356 images). Complete **both** experts for any requested seed/domain pair. The exporter fails closed if checkpoint or manifest provenance is wrong, frames are skipped, image labels missing, boxes malformed, or a chunk already exists.

After full checksum-consistent coverage of both experts:

```bash
python ecosafe_selective_experts/scripts/12_best_validation_fusion_report.py \
  --validation-root /private/FROZEN_VALIDATION \
  --private-chunks /private/EcoSafe_BestPt_Validation \
  --domain c --seed 17 \
  --out /private/aggregate_reports/c_best_seed17.json
```

The report rejects invalid version, name, ontology, model fingerprint, split provenance, chunk metadata or incomplete frame coverage. Only aggregate reports may be publicly shared. **Do not commit checkpoint binaries, private per-frame predictions, raw labels, image filenames, worker images or API keys.**

## Audit interpretation

- Primary comparison: model operating-confidence >=0.25; fixed class-aware GT IoU >=0.50; merged class-wise NMS IoU=0.70.
- Models exported at confidence=0.001 to permit **development-only** sensitivity at confidence cutoffs 0.05/0.10/0.25/0.50. These are not an independently locked post-development operating policy.
- Report TP, FP, FN, precision and recall **per safety class** and both domains. Raw concatenation matching is an oracle ceiling, **not** an operational ensemble.
- Maintain a frozen `last.pt` comparator; do not swap the `best.pt` variant in the main table or select favorable seeds post hoc.
- Site or video-group IDs are not established in the frozen export; image-level resampling does not yield source-group independent inference.
- Evaluation here measures **neither energy nor deployable safety**. Higher recall accompanied by unacceptable false alarms or rare-class failures is not a safety success.
- Finish a two-domain, three-seed report, then make an explicit revised study/no-go decision before considering held-out test access.
