# Seed 17, Y-PPE development validation: completed two-expert paired inference

**Date:** 2026-10-17. **Status:** Complete for one seed / one development split; NOT held-out test, external deployment, router success, energy measurement or Q1-ready outcome.

## Verified assets and protocol

- 356 Y-PPE-h9-v2 **validation-only** images and 356 annotation files, immutable frozen manifest SHA-256
  \`82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8\`.
- Exact original \`last.pt\` checkpoints, locally re-hashed:
  - Y_YOLO_s17 \`b5c54704553a6bbc900b8ac37735ee1040025a3c685dcd3717c4490d107bbee5\`
  - C_YOLO_s17 \`daef1d3841af76e0d3c801f8fd7a41d4713e465617b09b2e18d5fe67e5eb46c4\`.
- CPU inference, Ultralytics \`8.4.156\`, resolution 640, export confidence 0.001, individual-model NMS IoU 0.70, batch size 1, repeated non-benchmark 16-image chunks.
- Exactly **23 verified chunks and 356 frame records per model**; no skipped frame or missing detections miscounted as negative. At export cutoff 0.001, zero-detection frame counts were 11 (Y) and 35 (C).
- Each complete chunk’s CSV SHA-256 rechecked against its own private manifest. Model and dataset hashes, ontology and inference settings verified. No images, filenames, individual detections or GT labels uploaded to GitHub.
- Fixed evaluation cutoff confidence >=0.25. Safety classes \`no_helmet, no_gloves, no_boots\`. One-to-one class-aware maximum-cardinality GT matching with IoU >=0.50. Joint NMS on aggregated detections is class-aware IoU 0.70. Raw concatenation is used **only as a recall upper-bound oracle**.
- Independent NetworkX maximum bipartite cardinality check agreed in **1,424/1,424** image-by-policy evaluations (356 images x four policies), validating the local augmenting-path matcher’s TP counts.

## Development-only measured outcomes

Validation safety GT: **345 objects on 126 images**.
Per-class GT: 40 \`no_helmet\`, 251 \`no_gloves\`, 54 \`no_boots\`.

| Policy | Matched TP / 345 | FN | FP | Safety detections | Recall | Precision |
|---|---:|---:|---:|---:|---:|---:|
| Y-PPE primary expert | 106 | 239 | 35 | 141 | 30.72% | 75.18% |
| Construction-PPE secondary expert | 1 | 344 | 2 | 3 | 0.29% | 33.33% |
| Joint class-aware NMS | 106 | 239 | 37 | 143 | 30.72% | 74.13% |
| Raw concatenation oracle | 106 | 239 | n/a | 144 | 30.72% | n/a |

Per-class matched Y-expert TPs: 15/40 \`no_helmet\`, 71/251 \`no_gloves\`, 20/54 \`no_boots\`.
Construction-expert TPs: 0/40, 1/251, 0/54 respectively.
Raw concat and joint NMS TPs equal Y alone on **every one of the 356 validation images** under the fixed operating protocol: no observed complementarity in this domain/seed.

## Cross-domain development-only interpretation

The previously archived seed17 Construction validation analysis recorded 98 GT
safety objects: Y expert 7/98, Construction expert 8/98, joint NMS 13/98,
concat oracle 14/98. On Y validation, the same seed exhibits zero marginal
safety recall gain from adding Construction and slightly worse precision.

This is **asymmetric complementarity on two development splits**, not
evidence that selective routing works, nor a stable population-wide effect.
The in-domain Y recall of 30.72% is itself far too low to claim operational
safety adequacy. Confidence-only routing also underperformed on the seed17
Construction development pilot and has not passed a safety non-inferiority gate.

## Strict blockers

- Must replicate across seeds 42 and 2026 and both validation domains;
- no held-out test used in these development computations;
- do not silently select domain/seed or thresholds based on favorable results;
- must predefine minimum acceptable absolute safety recall and false-alarm
  tradeoff in addition to a non-inferiority margin against a potentially
  inadequate always-run-both reference;
- only after development-only policy freeze should independent held-out
  testing, grouping-aware uncertainty and local power/memory/latency
  measurement take place. Expert invocation count != joules/image.

**Interpretation:** Do not claim a benefit from automatically activating two
experts. The null improvement in 356/356 per-image comparisons requires any
future router to learn when secondary inference has genuine expected value,
not merely when primary confidence is low.
