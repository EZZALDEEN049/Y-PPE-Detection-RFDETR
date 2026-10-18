# EcoSafe — best.pt checkpoint-policy sensitivity on Y-PPE validation

**Executed:** 2026-10-18 (UTC execution 2026-10-17). **Scientific classification: checkpoint-policy sensitivity on DEVELOPMENT ONLY.** The original `last.pt` primary analysis remains unchanged. No retraining or held-out test used.

## Immutable provenance and quality control

- All six immutable `best.pt` checkpoint binaries originally from the linked Stage5_Baselines Drive folders were independently hashed. See the exact source SHA-256 and sizes in `scripts/11_export_best_validation_chunks.py` and `BEST_PT_CONSTRUCTION_THREE_SEEDS_VALIDATION_2026-10-18.md`.
- The original **Y-PPE-h9-v2** validation split has 356 images, 126 safety-positive images and **345 safety ground-truth objects**: 40 no_helmet, 251 no_gloves, 54 no_boots. Manifest SHA-256: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`.
- PyTorch 2.10.0+cpu, Ultralytics 8.4.156, resolution 640, per-model NMS IoU 0.70, raw export confidence >=0.001; 16-image inference chunks, batch size 1. Exactly **23 verified chunks per each of six checkpoints**, complete 356-frame coverage, including zero-detection images. All private frames/prediction CSV were checksum verified before aggregation.
- Safety fixed-point confidence 0.25, one-to-one class-aware maximum-cardinality GT matching at IoU>=0.50; class-aware joint operational NMS 0.70; evaluation-only raw concatenation oracle separately computed.
- Independent NetworkX maximum-bipartite cardinalities reproduced **8,544 / 8,544** per-image policy outcomes (356 images × 3 seeds × 4 policies × 2 diagnostic confidence thresholds 0.05 and 0.25). Construction best.pt verification previously reproduced **3,168 / 3,168**; **11,712 / 11,712** independent checks overall. No per-image identities, names, images or weights have been committed.

## Main operating-confidence results: 345 Y-PPE critical objects

| Seed | last.pt joint TP / FP | best.pt Y expert TP / FP | best.pt Construction expert TP / FP | best.pt joint NMS TP / FP | best.pt raw-concat oracle TP |
|---|---|---|---|---|---:|
| 17 | 106 / 37 | 111 / 50 | 5 / 4 | **113 / 54** | 113 |
| 42 | 103 / 33 | 119 / 58 | 14 / 13 | **122 / 74** | 122 |
| 2026 | 94 / 33 | 133 / 93 | 8 / 13 | **134 / 108** | 134 |

Joint best.pt safety recall across seeds: **32.75%, 35.36%, 38.84%** (each denominator 345); joint precision: **67.66%, 62.24%, 55.37%**. These are fixed-point count ratios, **not** COCO mAP. Compared with the stronger Y expert in each seed, the operational fused model recovers only **+2, +3, +1** extra safety objects at the chosen cutoff, but adds **+4, +16, +15** false detections.

Class-wise **joint** best.pt safety TPs by seed, out of fixed class support:
- no_helmet (40): **14, 19, 19**;
- no_gloves (251): **77, 78, 87**;
- no_boots (54): **22, 25, 28**.

These figures show persistent substantial per-class misses despite increased overall recall. The primary `last.pt` Y-domain joint baseline recovered **106, 103 and 94** safety objects and had **37, 33 and 33** FP, respectively. It must not be replaced or hidden.

## Exploratory cutoff sensitivity — no final threshold selected

| Confidence cutoff | Seed17 joint TP / FP | Seed42 joint TP / FP | Seed2026 joint TP / FP |
|---|---|---|---|
| 0.05 | 146 / 237 | 150 / 200 | 166 / 287 |
| 0.25 | 113 / 54 | 122 / 74 | 134 / 108 |

Confidence 0.05 yields up to 166/345 (48.12%) Y-domain GT matches among examined settings, but 287 FPs for seed2026; other cutoff choices also need to report missed violations and their error burden. These confidence checks are **retrospective developmental diagnostics** and no cutoff will be selected based on held-out test results.

## Confidence-only escalation, best.pt — exploratory, not a trained router

Primary-only uncertainty `1-max(primary_safety_class_confidence)` at score cutoff 0.50 triggers genuine second expert invocation with class-aware joint NMS on escalation, not prediction switching.

| Seed | Primary | Invoked secondary / 356 | Selective TP / 345 | Always-joint TP / 345 |
|---|---|---:|---:|---:|
| 17 | Y | 279 | 112 | 113 |
| 42 | Y | 281 | 120 | 122 |
| 2026 | Y | 270 | 133 | 134 |
| 17 | Construction | 355 | 110 | 113 |
| 42 | Construction | 351 | 116 | 122 |
| 2026 | Construction | 350 | 125 | 134 |

The Y-primary router spends extra expert invocations on **76–79% of frames** to recover **0–1** more matched violations above Y alone in these runs. The reverse direction escalates almost every frame. None establishes a useful primary-only safety/computation frontier; even the always-joint reference has too many missed violations. Expert-call counts are NOT energy, carbon, memory or matched-hardware latency measurements.

## Selection bias, scope and decision

**In-domain `best.pt` checkpoint-selection optimism:** the Y-trained expert was originally chosen using source-domain validation feedback. These same Y-PPE development frames therefore cannot serve as an unbiased independent confirmation of its improved performance. The cross-domain Construction expert was selected under its own original development policy, and its transfer to Y-PPE has a different selection relationship. The fused ensemble partly inherits the in-domain bias.

**Research gate:** `best.pt` restores **limited object-level expert complementarity** on Y-PPE that was absent for `last.pt` at confidence 0.25. The marginal extra TP is tiny compared with increases in FP and expert calls, and absolute violation recall remains too low for a field-safety adequacy claim. This sensitivity strengthens the need to treat checkpoint policy as an experimental factor, not to claim successful EcoSafe energy/safety noninferiority.

The full two-domain `best.pt` development experiment is complete. No held-out test has been accessed and no hardware joules/image, CO2e, local matched latency, independent site grouping or operational safety target has been established. **Current GO/NO-GO remains NO-GO for deployable safety or sustainable-inference superiority claims** until an independently justified changed hypothesis is frozen and tested once on appropriate independent evidence.
