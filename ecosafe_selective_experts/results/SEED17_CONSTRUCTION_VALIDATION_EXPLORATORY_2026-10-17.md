# Exploratory EcoSafe validation experiment — Seed 17 / Construction-PPE

**Date:** 2026-10-17. **Status:** development-only exploratory result; NOT a held-out test, complete EcoSafe experiment, calibrated power benchmark, or Q1 submission result.

## Provenance and data lock

- Exact Y-PPE-expert checkpoint: Y_YOLO_s17 last.pt; SHA-256:
  b5c54704553a6bbc900b8ac37735ee1040025a3c685dcd3717c4490d107bbee5.
- Exact Construction-expert checkpoint: C_YOLO_s17 last.pt; SHA-256:
  daef1d3841af76e0d3c801f8fd7a41d4713e465617b09b2e18d5fe67e5eb46c4.
- Both individual 40 MB checkpoint bytes were retrieved from the connected
  Stage5_Baselines storage and **re-hashed locally**.
- Frozen validation-only data artifact: GitHub Actions run 38826721499,
  artifact 12015950029, ZIP SHA-256:
  5337fb80a7e74bbb56ebed497d56f129d5020efff1c36540d74095f2823ae1d7.
- Construction-PPE-h9-v2 manifest SHA-256:
  59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14.
- Y-PPE-h9-v2 manifest SHA-256 independently checked:
  82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8.
- Only the **132 Construction-PPE validation images** and labels were analyzed.
  The Y-PPE validation domain, alternate seeds and both held-out test splits
  have **not** been evaluated in this pilot.
- Environment: CPU-only PyTorch 2.10.0+cpu, Ultralytics 8.4.156 (versioned
  offline wheel from GitHub Actions run 38819888174). Model resolution 640,
  prediction-export confidence 0.001, model-internal NMS IoU 0.70.
- Inference in local chunks of 16 frames, batch size 1. One Construction
  expert frame produced no detections even at confidence 0.001; rerun of that
  single validation frame confirmed the zero count. No model retraining.
- Operating-confidence cutoff 0.25 and GT matching IoU >= 0.50 follow the
  existing EcoSafe development-builder defaults. This is NOT a COCO mAP
  evaluation; it is fixed-operating-point safety-object matching.

## Observed development-set safety outcomes

Safety classes: no_helmet (43 GT objects), no_gloves (51), no_boots (4).
Overall: 98 safety-positive objects on 27 positive validation frames.

| Policy | Matched safety objects (TP / 98) | FN | Safety detections | FP (object-matching convention) | Recall | Precision |
|---|---:|---:|---:|---:|---:|---:|
| Y expert alone | 7 | 91 | 66 | 59 | 7.14% | 10.61% |
| Construction expert alone | 8 | 90 | 16 | 8 | 8.16% | 50.00% |
| Joint class-aware greedy NMS at IoU 0.70 | 13 | 85 | 80 | 67 | 13.27% | 16.25% |
| Raw concatenation oracle (upper bound ONLY) | 14 | 84 | 82 | not evaluated | 14.29% | not evaluated |

One-to-one class-aware maximum-cardinality GT/detection matching, IoU >= 0.50,
was used for fixed-threshold TP/FN/FP counts. These precision/recall numbers are
not COCO mAP or confidence-integrated AP. Fusion NMS uses combined predictions
without ground-truth access; oracle matching uses GT only for retrospective
upper-bound evaluation, never for prediction selection.

### By critical class (matched TP counts)

| Class | Ground-truth boxes | Y expert TP | Construction expert TP | Raw concat oracle TP |
|---|---:|---:|---:|---:|
| no_helmet | 43 | 0 | 6 | 6 |
| no_gloves | 51 | 6 | 2 | 7 |
| no_boots | 4 | 1 | 0 | 1 |

- Raw concatenation oracle additionally matches **7** GT objects over Y
  alone and **6** over Construction alone, in this development split.
- The old per-frame difference-of-FN-counts proxy yields **6** and **5**,
  respectively; it misses one true improvement frame in each direction.
- Joint class-aware NMS gives more recall than either detector separately,
  **but poorer precision than Construction alone** due to additional FPs.
  Thus no conclusion of operational safety superiority can be drawn.
- No-bootstrap class-level claims should be made from four no_boots objects.
- The primary paper has a documented near-floor Construction negative-state
  issue; this pilot aligns qualitatively but does not re-evaluate that paper.

## Independent verification and explicit blockers

Per-frame matched TP cardinalities for all 132 validation images x three
policies (Y, Construction, raw concatenation oracle) were independently
cross-checked using NetworkX maximum bipartite matching. **396/396**
cardinalities agreed with the local augmenting-path matching implementation.

**Scientific gate: still NOT passed for a deployable selective routing claim.**
These values are from a SINGLE seed and SINGLE development domain. Actual
router thresholds are not yet frozen, no out-of-fold router was fitted, no
held-out test data were consulted, and no power, joules/image, carbon, cost or
robust local latency comparison has been measured. An operating fusion policy
and uncertainty analysis must be frozen and replicated on all seeds/domains
before test exposure.

The raw private per-image CSV, image files, labels and checkpoint binaries
are intentionally excluded from GitHub. The next deliverable is a
strictly validated, reproducible paired-prediction aggregation script wired
to 08_export_validation_chunks.py; subsequent runs must include zero-detection
frame records, full partition coverage, stable class ordering, and the
checksum-locked validation manifests.
