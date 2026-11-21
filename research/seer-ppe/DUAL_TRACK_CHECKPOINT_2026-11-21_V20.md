# SEER-PPE V20 checkpoint — frozen internal historical Valid detection analysis and original-label count audit

**21 November 2026. Status: stored historical 2025 Roboflow model Eval Valid-only counters aggregated by prespecified source-risk cohorts; NOT a new held-out or SEER-PPE safety-effectiveness result.**

## What was executed

- [The V20 internal-only protocol](VALID_HISTORICAL_INTERNAL_OBJECT_EVAL_PROTOCOL_FROZEN_V20.md) was committed **before** V20's first historical per-Valid-image outcome page was read. It fixes Model `altayyar-0oflt-lafos-qqauz/2`, preexisting Roboflow Eval `KyzP9neuyNTN5eQpGCAY`, version `2`, split `valid` exclusively, confidence `0.20`, exact original Valid Source ID join, micro P/R/F1 formula and the preselected M0/M1/M2 source-risk cohorts.
- The preexisting model Eval's **468** original Valid per-image records (generated September 2025) were read at confidence 20%. Their `imageId` field exactly equals **468/468** original Valid Source IDs. Exactly **459** align with corrected Clean17 retained Valid; the **9** previously excluded originals were not included in any scored descriptive cohort. No Test outcomes were read.
- The author's already-curated current Source object annotations were inspected **numerically only** via Roboflow's read-only annotation API for the **459 original Valid images**: **3,471 current object-label boxes**, including **729 marked as model-assisted annotations**. No second reviewer, reinspection, box editing or source mutation was required.
- **Critical version reconciliation:** The historical platform Eval's reference denominator covers **3,455** objects for those 459 images, while the current Source annotation count is **3,471**. The per-image counts agree in **446/459** images; **13/459** show differences of **16 objects** total. Therefore V20 is explicitly a **historical Version-2 Eval counter analysis**, not a recomputation of current Source box-level detection quality. Legacy Eval geometry returns `unavailable` and cannot establish identical box-level labels today.
- Deterministic read-only compilation was tested in [successful V20 GitHub Actions run 44856892166](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44856892166). It verifies IDs, source cohort sizes, TP+FP/FN arithmetic, mismatch trace and forbids fake independent source, Test injection, source GT fabrication and wrong model/evaluation identity.

## Valid only — historical fixed-model detection counters by preselected risk scenario

| Historical Valid cohort | Images | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| M0: all corrected mapped original Valid | 459 | 3252 | 642 | 203 | 0.835131 | 0.941245 | **0.885018** |
| M1: minus 5 old holds and 6 high-overlap technical quarantines | 448 | 3217 | 639 | 200 | 0.834284 | 0.941469 | **0.884642** |
| M2: also minus 81 other risk-flagged possible source families | 367 | 2851 | 589 | 183 | 0.828779 | 0.939684 | **0.880754** |

F1 differences from M0 are **−0.0376** and **−0.4264 percentage points** for M1 and M2. This is **subset sensitivity**, not evidence of an independently generalizable performance advantage or an SEER intervention. All M0/M1/M2 image acquisition-family independence assertions remain unproven; source-risk is technically screened only.

## Preserved limits

This is **one preexisting historical RF-DETR evaluation**, not paired A0-versus-A5 SEER scoring. The historical platform summary cannot be treated as current-label ground-truth precision/recall in the 13 differing images. Do not call these metrics externally validated, unbiased held-out, XAI, measured energy or worker-violation metrics. Label geometry, present PPE, task mandate and human-review completion are distinct constructs. V20 ran **zero new model inferences**, never used Test, did not alter original source labels or splits, did not create any new human signatures, and did not require a second reviewer.

The original single-curator image selection/review is accepted as previously completed. The strict verified occupational safety/independently certified source freeze remains **`NOT_FROZEN`**, `scoring_ready=false`. The narrow **historical descriptive Valid object-detection metric aggregation** is complete with explicit source-label-version caveats.

## Saved evidence

[Original Valid annotation counts (part 1)](V20_VALID_SOURCE_ANNOTATION_COUNTS_PART1_PRIVATE_WORKING.json) · [part 2](V20_VALID_SOURCE_ANNOTATION_COUNTS_PART2_PRIVATE_WORKING.json) · [historical 468 Valid-only TP/FP/FN by exact Source ID](HISTORICAL_V2_VALID_PER_IMAGE_COUNTERS_V20.json) · [derived V20 459/448/367 metrics and 13 mismatches](HISTORICAL_VALID_INTERNAL_METRICS_V20.json) · [deterministic compiler](tools/compile_historical_valid_internal_metrics_v20.mjs).

**Next research step:** If claiming quality against the **current** 459-image source annotation geometry, obtain new original-model `valid` predictions at frozen settings, compare per-class boxes with the current saved author labels and report 13 legacy-vs-current reference differences; do not overwrite historical evaluator counters. A SEER-versus-strong-selective comparison remains a separate, not-yet-executed experiment.
