# EcoSafe validation execution: immutable six-model paired inference

**Version:** 2026-10-17. **Status:** implementation and synthetic CI checks complete.
A local single-seed/Construction validation pilot is documented separately,
not an independent held-out result. NO new detector training is authorized.

## Frozen materials

- Stage5_Baselines/Y_YOLO_s{17,42,2026}/train/weights/last.pt
- Stage5_Baselines/C_YOLO_s{17,42,2026}/train/weights/last.pt
- Immutable frozen validation-only archive reconstructed by GitHub Actions
  run 38826721499, artifact "ecosafe-frozen-validation-splits"; SHA-256
  5337fb80a7e74bbb56ebed497d56f129d5020efff1c36540d74095f2823ae1d7
- Frozen manifests:
  Y-PPE-h9-v2:
  82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8
  Construction-PPE-h9-v2:
  59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14

**The artifacts contain identifiable construction imagery; keep images and
per-frame detections in private, authorized storage, not public GitHub.**
Labels in validation are known. Never inspect frozen test labels for router
training/threshold selection, nor borrow any result from a different 17-class
dataset experiment as a substitute for nine-class Stage 5 models.

## Local environment and preflight

Use the project's exact Ultralytics v8.4.156 (wheel archived in GitHub
Actions run 38819888174), a working PyTorch CPU/GPU installation and matching
runtime dependencies. Record OS, Torch/device, Ultralytics version, available
RAM and original model file hashes. Absolute resource timings from different
machines are NOT directly comparable.

Unpack only the "ecosafe-frozen-validation-splits" archive into:

    PRIVATE_VALIDATION/
      Y-PPE-h9-v2/images/val/
      Y-PPE-h9-v2/labels/val/
      Y-PPE-h9-v2/manifest.jsonl
      Construction-PPE-h9-v2/images/val/
      Construction-PPE-h9-v2/labels/val/
      Construction-PPE-h9-v2/manifest.jsonl

For EACH model and EACH validation domain, process every chunk; last.pt and
both manifests are SHA-locked by the executable. Examples:

    python ecosafe_selective_experts/scripts/08_export_validation_chunks.py \
      --validation-root /private/PRIVATE_VALIDATION \
      --checkpoint /private/Stage5_Baselines/Y_YOLO_s17/train/weights/last.pt \
      --model-id Y_YOLO_s17 --domain c \
      --chunk-index 0 --chunk-size 16 \
      --out-dir /private/EcoSafePredictions --device cpu --cpu-threads 2

Repeat with model ID C_YOLO_s17 (its own checkpoint) for the same domain.
For 132 Construction validation images, indices are 0..8; for 356 Y-PPE
validation images indices are 0..22. Then repeat for seeds 42 and 2026.
Each chunk writes a manifest, a per-frame coverage CSV (including
zero-detection frames), and a separate detection CSV. Incomplete chunks
must be re-run in a *new private output directory* after root cause review,
not silently patched, overwritten or counted as zero-detection frames.

**Strict aggregation only after complete per-model paired chunk coverage:**

    python ecosafe_selective_experts/scripts/09_validation_fusion_report.py \
      --validation-root /private/PRIVATE_VALIDATION \
      --private-chunks /private/EcoSafePredictions \
      --domain c --seed 17 \
      --out /private/reports/seed17_construction_development_aggregate.json

Run the same for domain y and seeds 42/2026. The script fails closed if
frames, metadata, counts, checkpoint hashes or frozen manifest provenance
are incomplete/mismatched. It computes three *distinct* policies: single
experts, class-aware joint NMS and raw-concatenation object-recall oracle.
Only aggregate summary may be shared; individual CSVs stay private.

## Scientific gates

1. Validate the study has BOTH model directions, BOTH development domains,
   and ALL three precommitted random seeds (6 models x 2 domains).
2. Report per-class TP, FP, FN, denominators and uncertainty. With only
   four no_boots validation objects in Construction, avoid any sweeping claims.
3. Evaluate a family of proposed routing policies *on development only*,
   with out-of-fold router fitting. Choose/lock the safety loss delta and
   reference explicitly; "replace primary with secondary" is NOT a fusion policy.
4. Do not claim reduced energy from fewer second-expert calls. Include
   actual router overhead, wakeup/loading cost, model-conditional latency and
   instrumented J/image on one hardware platform before an energy/CO2 claim.
5. Frozen test sets remain untouched until the whole model/threshold protocol
   is recorded. Publication needs an independent held-out evaluation and
   appropriate source-group/near-duplicate leakage sensitivity.

## Pre-execution warning

The documented seed17 Construction validation pilot found 98 safety GT
objects, with 7/98 and 8/98 found by individual models, and only 13/98
by a joint NMS candidate; raw concatenation upper bound 14/98. These
figures do NOT establish safety adequacy or a generalizable router benefit.
A safety non-inferiority margin relative to such a weak baseline must NOT be
mistaken for a minimum acceptable operational safety-recall requirement.
