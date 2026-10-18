# EcoSafe — Y-PPE validation: all three frozen seeds (2026-10-18)

**Status:** Real completed experiment on **development / validation data only**. NOT the independent held-out test, a router benchmark, proof of field safety, or energy measurement.

## Checkpoint and data provenance

The existing frozen original Stage5_Baselines **last.pt** files were used with NO retraining, substitution, extra fine-tuning or test exposure.

- Dataset: **Y-PPE-h9-v2**; exactly **356 validation images and 356 corresponding labels**, with **345 safety ground-truth objects on 126 positive frames**: `no_helmet`=40, `no_gloves`=251, `no_boots`=54.
- Manifest SHA-256: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`; checksum independently confirmed from the archive.
- Validation-only ZIP from GitHub Actions run `38826721499`, artifact `12015950029`, ZIP SHA-256 `5337fb80a7e74bbb56ebed497d56f129d5020efff1c36540d74095f2823ae1d7`. Raw images and image names **not** copied to public GitHub.
- Model hashes independently rechecked bytewise before running:
  - Y_YOLO_s42 `3ec0b396ae344361a9e000683891aa88dd92ef9a6edff07829243f95bf6eaf64`
  - C_YOLO_s42 `868b533722848a6885909391daabf52d7bd189cca4fc1e8d82fbe0f4c03869a1`
  - Y_YOLO_s2026 `c1ab6209e26aa461ef2833889c85d8edb8ffac6de70348117b0923b80939c23e`
  - C_YOLO_s2026 `f1f160d2f1e84b8641872adb01d10b6c9d3b736a53b7ec5775333eef30f88bb1`
  - Seed17 checkpoint provenance and completed 356-image comparison were archived separately in `SEED17_Y_PPE_VALIDATION_PAIRED_INFERENCE_2026-10-17.md`.
- CPU PyTorch `2.10.0+cpu`, Ultralytics `8.4.156`, four CPU Torch threads, input 640, export conf 0.001, individual NMS IoU 0.70, batch size 1; **NOT a controlled latency or energy measurement**.
- Each of four newly run expert/domain cells contains **23 nonoverlapping 16-frame chunks covering 356/356 validation images**. All private prediction CSV and frame-coverage CSV SHA-256 hashes and checkpoint/dataset-lock manifests were re-verified; zero-detection frames retained explicitly.
- Safety evaluation: class-aware one-to-one **maximum-cardinality** GT match, IoU >=0.50; confidence >=0.25, combined class-wise NMS IoU 0.70. Raw concatenation is an **evaluation-only oracle ceiling** for the given exported predictions, not an operational ensemble. Matching is fixed-confidence safety object counting, **not COCO mAP**.
- Independent NetworkX bipartite matching agreed with **2,848/2,848** per-frame-policy cardinalities (356 images × 4 policies × 2 new seeds). The earlier seed17 Y domain verification independently agreed for 1,424/1,424, thus the three-seed Y-domain checks cover **4,272 comparisons** in all.

## Results: 356 Y-PPE validation images, same 345 annotated safety objects

| Seed | Y expert TP | Y expert FP | Construction expert TP | Construction expert FP | Joint NMS TP | Joint NMS FP | Raw union oracle TP |
|---|---:|---:|---:|---:|---:|---:|---:|
| 17 | 106 | 35 | 1 | 2 | 106 | 37 | 106 |
| 42 | 103 | 31 | 2 | 1 | 103 | 33 | 103 |
| 2026 | 94 | 33 | 2 | 0 | 94 | 33 | 94 |

Joint-NMS recall = **30.72%, 29.86%, 27.25%** across seeds 17, 42, 2026; descriptive three-seed mean = **29.28%** on the same development images. Joint-NMS precision = **74.13%, 75.74%, 74.02%**, respectively.

**At this particular fixed operating point, adding the Construction expert does not increase matched GT safety objects on Y validation in ANY of three seeds.** The concatenation oracle also adds no GT match: the limitation is not merely NMS suppression. Seed17 and 42 fusion each add two false detections; seed2026 fusion adds none. No population-level universality or all-threshold impossibility is inferred.

The matched Y-expert critical-class TPs for seeds 17, 42, 2026:
- `no_helmet` (40 GT): 15, 18, 15.
- `no_gloves` (251 GT): 71, 66, 63.
- `no_boots` (54 GT): 20, 19, 16.

Construction expert by class: seed17 (0 helmet / 1 gloves / 0 boots); seed42 (1 / 1 / 0); seed2026 (0 / 2 / 0). Class counts and domain denominators are critically different from Construction validation, where boots GT support is only 4.

## Two-domain, three-seed development comparison

On **Construction-PPE validation** (132 images, 98 safety GT), original archived data:
| Seed | Y-alone safety TP | C-alone safety TP | Joint-NMS safety TP | Joint-NMS FP |
|---|---:|---:|---:|---:|
| 17 | 7 | 8 | 13 | 67 |
| 42 | 9 | 5 | 13 | 68 |
| 2026 | 8 | 7 | 14 | 74 |

The small Construction-domain gain of 4–6 safety objects compared with the **best single expert** per seed is coupled with high false-positive burden and low joint absolute recall (~13–14%). In contrast, across all Y-domain seeds, the gain is **exactly 0** at confidence 0.25. These are asymmetric development observations; do not infer that the same holds on unseen sites or independent held-out test images.

## Exploratory threshold sensitivity (NOT frozen)

Using the very same low-confidence predictions from seeds 42/2026, without inference or training:
- At confidence 0.05, seed42 Y alone=115 TP/46 FP and joint=115 TP/50 FP; seed2026 Y alone=111 TP/58 FP and joint=113 TP/58 FP.
- At confidence 0.50, seed42 Y alone=94 TP/23 FP versus joint=95 TP/24 FP; seed2026 Y alone=85 TP/25 FP versus joint=85 TP/25 FP.

**Therefore the no-gain result is expressly limited to the 0.25 operating point; a few additional matches occur at other thresholds.** No threshold is selected for held-out test based on these post hoc observations, and even favorable sensitivity rows retain many missed violations.

## Descriptive confidence-only routing (NOT training or selection)

Development-only score: `risk=1-max(primary safety detection confidence)`, risk=1 without any safety detection. Escalate at threshold 0.50, then merge via operational joint NMS:
- Seed42, Y-primary: secondary invoked **287/356 = 80.62%** of frames; **103/345** safety TP, no change vs Y alone, hence dominated on this development split.
- Seed2026, Y-primary: secondary invoked **289/356 = 81.18%** of frames; **94/345** safety TP, also no change vs Y alone.
- Seed42 C-primary: invokes Y on **353/356** images yet achieves **97/345** TPs (below always-both's 103).
- Seed2026 C-primary: invokes Y on **355/356** images yet achieves **93/345** TPs (below always-both's 94).

These invocation figures are **inference-call proxies**, not measured Joules, carbon, throughput, or latency. No learned router fitted.

## Uncertainty and source-dependence limitation

A **5,000-resample paired image-level bootstrap** (fixed seed 20261018+training seed) yields exactly zero retrospective joint-minus-Y recall on both new seeds, with 0.0–0.0 frame-percentile interval, because no frame's observed fixed-threshold TP count improves. This is purely a conditional description of 356 development frames, **NOT a valid site-cluster confidence interval** nor a proof of no future improvement.

The frozen manifest fields are `image, image_sha256, label, label_sha256, retained_instances, split`; it does **not** encode verified independent site/sequence/source-group IDs. Source independence and dependence-aware uncertainty are thus unresolved.

## GO / MODIFY / NO-GO

**NO-GO** for claims of operationally safe, sustainable, *universally beneficial* selective dual-expert PPE monitoring with these fixed `last.pt` experts at this evaluation policy. The fused reference is too weak in absolute safety recall on BOTH development domains and can add false alerts while failing to add safety TPs in Y. A relative non-inferiority claim against this weak fused reference would not be meaningful safety validation.

**MODIFY, without silent data/model switching**: if pursuing the research, first declare a separately analyzed frozen validation-selected `best.pt` sensitivity (previous study already identified checkpoint-policy sensitivity) or a substantially revised safety evaluation question, then choose a real absolute operational target, lock all decision/fusion thresholds on development only, and perform a single independent held-out test if the validation gate is met. Assess model invocation, router overhead and calibrated per-image energy separately.

**No held-out test exposure, new detector training, raw model uploads, power/CO2 claims or public private-frame CSVs occurred in this evaluation.**
