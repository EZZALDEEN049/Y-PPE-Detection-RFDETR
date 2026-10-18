# EcoSafe — best.pt checkpoint-policy sensitivity on Construction validation

**Executed:** 2026-10-18 (UTC execution 2026-10-17). **Research status:** Development-only, pre-test diagnostic. This analysis does **NOT** overwrite the original `last.pt` primary evidence.

## Independent source and execution verification

All SIX original `best.pt` checkpoint binaries were privately retrieved from Stage5_Baselines Google Drive and locally SHA-256 verified. Model / SHA-256:

| Frozen model | best.pt SHA-256 |
|---|---|
| Y_YOLO_s17 | `ba9ce25e398cc901cef1d999cc3d2805097f3f40240038da7daf79a313254c8a` |
| C_YOLO_s17 | `b2ee85bc5fe0c512a9cdebbfed2b2b316e612bcb8e07a58872b6bde036ddd0b7` |
| Y_YOLO_s42 | `6b77e3ccb474e0886a8e53ff6c05e7375749c522f78cbaea2ab355a82f4de3d1` |
| C_YOLO_s42 | `3a48e71fe175961f881bbfc94202c94343d17fd6c5054e2fd2110f81f8fc0bb2` |
| Y_YOLO_s2026 | `9ed35e976b6e5d0179f13d78b69de0bff0318978f977970abead7cf4d0605e98` |
| C_YOLO_s2026 | `c3dd35b7c1cfef528c023952fc00786270067f175d8bfebbbe84d75e0cd1a264` |

- Same immutable Construction-PPE-h9-v2 **validation** partition: 132 images, 98 GT critical objects on 27 images; manifest SHA-256 `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`.
- Safety class support: 43 `no_helmet`, 51 `no_gloves`, 4 `no_boots`.
- CPU execution, PyTorch `2.10.0+cpu`, Ultralytics `8.4.156`, input 640, original per-expert NMS IoU 0.70, low-confidence export 0.001, batch size 1. 9 verified, nonoverlapping chunks per checkpoint covering all **132 frames** each; raw per-image predictions and image names remained private.
- Protocol: fixed evaluation confidence 0.25, class-aware GT one-to-one maximum-cardinality matching IoU >= 0.50, operational candidate joint class-aware NMS IoU 0.70. Raw concatenation oracle is nonoperational and evaluated ONLY as an upper bound on matched GT at this confidence.
- Independent NetworkX bipartite matching matched **3,168/3,168** per-image/policy cardinalities, using 132 images × 3 seeds × 4 policies × 2 operating-confidence settings (0.05 and 0.25). Private CSVs were re-hashed and checked against per-chunk metadata before aggregation. No detector training or final held-out test access.

## Fixed operating-point results

Each TP is matched critical ground-truth boxes out of 98 (not COCO mAP). FP counts use one-to-one class-aware matching at the same fixed point.

| Seed | last.pt joint TP / FP | best.pt Y TP / FP | best.pt C TP / FP | best.pt joint TP / FP | best.pt raw concat oracle TP |
|---|---|---|---|---|---:|
| 17 | 13 / 67 | 8 / 88 | 13 / 22 | **20 / 110** | 20 |
| 42 | 13 / 68 | 10 / 79 | 40 / 79 | **47 / 157** | 48 |
| 2026 | 14 / 74 | 10 / 113 | 21 / 36 | **27 / 148** | 27 |

Joint best.pt fixed-point recall across seeds: **20.41%, 47.96%, 27.55%**, respectively. Joint fixed-point precision: **15.38%, 23.04%, 15.43%**. Checkpoint choice materially shifts recall, but the seed-to-seed dispersion is large and alert counts can exceed GT safety objects.

Joint best.pt matched TPs by class:
- Seed 17: no_helmet 10/43, no_gloves 10/51, no_boots 0/4.
- Seed 42: no_helmet 30/43, no_gloves 16/51, no_boots 1/4. The C model individually matches **31 helmets**, versus 30 after joint NMS: fusion can suppress a true match.
- Seed 2026: no_helmet 10/43, no_gloves 16/51, no_boots 1/4.

The earlier last.pt baseline remains unchanged and scientifically primary. No conclusion of universally improved safety follows from `best.pt` performance on the validation images that were involved in checkpoint selection.

## Diagnostic confidence sensitivity, not test-threshold selection

| Confidence | Seed 17 joint TP / FP | Seed 42 joint TP / FP | Seed 2026 joint TP / FP |
|---|---|---|---|
| 0.05 | 56 / 575 | 60 / 559 | 49 / 458 |
| 0.10 | 43 / 278 | 56 / 340 | 43 / 294 |
| 0.25 | 20 / 110 | 47 / 157 | 27 / 148 |
| 0.50 | 8 / 65 | 25 / 59 | 17 / 88 |

The grid is retrospective and explores the recall / false-alarm frontier. For example, seed 42 joint recovers 60 of 98 violations at confidence 0.05, with **559** false detections. This is not an operationally acceptable alert policy by itself, and no threshold is frozen from these observations.

## Critical bias and interpretation

**Checkpoint-selection leakage/optimism:** `best.pt` was originally selected using validation feedback in the training process. Re-evaluating its performance on the same development validation subset is a **checkpoint-selection-biased diagnostic**; it cannot be interpreted as an independent validation improvement or a confirmatory benefit over the preregistered final-epoch policy. It is reported alongside `last.pt`, not swapped in without disclosure.

**Scientific decision:** The sensitivity shows that checkpoint choice is a major driver of safety-positive detection, but even this retrospective favorable choice does not demonstrate sufficiently low miss/false-alarm rates on Construction-PPE. The present evidence is **NO-GO for operational safety and measured sustainability claims**, not a negative judgment on all selective-inference research.

**Next gate:** Repeat `best.pt` sensitivity on the *Y-PPE validation* domain with all three paired seeds; then integrate both development domains, select a defensible revised study question and assess whether a single independently locked test is scientifically justified. No direct wattage, calibrated joules/image, CO2e, deployment latency or site-cluster generalization has been assessed.
