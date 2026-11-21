# SEER-PPE V26 — actual complete original Valid current author-label geometry scoring (459/459)

**21 November 2026.** Current master manuscript: **v0.26**. The numerical original RF-DETR object-detection benchmark on current author-curated **original Source Valid labels** has now been executed, fully scored and reproducibly verified. It is **not** a new scientific demonstration of safety-constrained A5 policy improvement, target-faithful XAI, reduced electricity use or independent acquisition-source generalization.

## What was actually executed and checked

1. A [frozen exact original Source/Valid scientific protocol](V26_FROZEN_FULL_CURRENT_SOURCE_VALID_BBOX_PROTOCOL_2026-11-21.md) identified precisely **459** Source images retained in Clean17 Valid from **468 original source Valid** images, with predetermined source-risk groups M0=459, M1=448 and M2=367, and a prespecified 13 historical/current annotation-count mismatch Source-ID sensitivity.
2. A [separate pre-score execution-method addendum](V26_FROZEN_VECTOR_BATCH_INFERENCE_ADDENDUM_2026-11-21.md) fixed a side-effect-free vectorized Roboflow workflow with original unchanged 17-class `altayyar-0oflt-lafos-qqauz/2`, hosted confidence **0.20**, overlap **0.50**, disabled active learning, exact original Source image identity and native pixel dimensions. The five V23 previously used Valid images were **newly re-inferred**, not merged from prior per-image model outputs. Some earlier single-image and workflow outputs vary slightly, even with identical resolved original model ID; this is disclosed.
3. The same original author reviewed boxes in native Roboflow (read-only annotation retrieval) were checked for exact Source ID, original filename, dimension, annotation group version, object-class count and model-assisted provenance against saved V20 Source count snapshots. Some automatically assisted label records lacked native per-box IDs; they received **local numeric audit IDs only**, without changing the original data. No second reviewer or image reinspection.
4. Actual source images, labels and model predictions were archived as **12 numeric-only shards**, `V26_ORIGINAL_VALID_GEOMETRY_SHARD_00_OF_12.json` through `..._11_OF_12.json` (459 successful source+reference+inference pairs, **zero failed**). Source image bytes, private signed URLs, API tokens and Test data were not committed.
5. The [deterministic V26 scorer](tools/score_original_valid_current_boxes_v26.mjs) computed exact-class, one-to-one greedy **IoU≥0.50** matches with original-image bounded rectangles and complete TP/FP/FN conservation. [Successful GitHub CI 44947700353](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44947700353) ran its negative controls and verified all **459** identities and class/source strata.
6. [V26 full current GT-vs-model audit](ACTUAL_CURRENT_SOURCE_ORIGINAL_VALID_459_CLASS_BBOX_METRICS_V26.json) is large, so [V26 compact structured 17-class scores](V26_VALID_CURRENT_SOURCE_459_NUMERIC_SUMMARY.json) and [reader-friendly full results](V26_VALID_CURRENT_SOURCE_459_RESULTS_REPORT.md) were generated deterministically from it by [the independent report renderer](tools/render_v26_current_valid_report.mjs), without any new inference.

## Real V26 new current-reference object-detection scores

| Preexisting technical source-risk cohort | Original Valid Source images scored | Current saved author boxes | Fresh model boxes | TP | FP | FN | Precision | Recall | F1 |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| M0, all matched current original Source Valid | **459** | **3,471** | **4,103** | **3,297** | **806** | **174** | **0.803558** | **0.949870** | **0.870610** |
| M1, excludes historic holds and high-overlap quarantines | **448** | **3,433** | **4,063** | **3,261** | **802** | **172** | **0.802609** | **0.949898** | **0.870064** |
| M2, technically unflagged, but **source independence NOT proven** | **367** | **3,049** | **3,618** | **2,894** | **724** | **155** | **0.799889** | **0.949164** | **0.868157** |

Original fixed **17-class** TP/FP/FN/P/R/F1 are all available in the compact JSON and main Results §4.20. Examples in M0 include `Hard Hat` GT388/TP377/FP39/FN11 (F1 **93.78%**) and `No Safety Boots` GT93/TP85/FP41/FN8 (F1 **77.63%**), which are **object-class detection** values, not violation or worker PPE mandate accuracy. Original author boxes include **729 assisted-provenance markers** (3,471 GT boxes).

**Prespecified descriptive sensitivity**:
- Exclude the **13 IDs with legacy-provider/current-label count differences**: 446 images, **3,152** current reference boxes, F1 **0.884660** (88.47%). **This drops 319 entire-image annotations**, not only the net 16 current-vs-historical count discrepancies, so attributing the F1 change to 16 labels is invalid.
- Exclude the **five previously V23-used Valid Source IDs** from M0: 454 images, **3,448** current boxes, F1 **0.870085**.
- Exclude the same five from M2: 362 images, **3,026** current boxes, F1 **0.867543**.

## Separate, not directly comparable historical model/provider result

The historical **2025** Roboflow model-v2 Valid provider Eval ID `KyzP9neuyNTN5eQpGCAY`, reaggregated in V20, had M0/M1/M2 F1 **0.885018 / 0.884642 / 0.880754**, but its GT geometry cannot be rebuilt from the current original saved annotation boxes, which now differ in **13 Source image counts, by 16 boxes overall**. The V26 model inference method is also vectorized rather than the prior provider Eval execution. There is **no controlled claim of a performance improvement/degradation** between 2025 and V26, and neither set establishes independent source acquisition or SEER system safety superiority.

## New manuscript and uncompleted primary SEER experiment

The [master research manuscript v0.26](MANUSCRIPT_MASTER.md) now integrates all M0/M1/M2 results, all 17 class scores, prior-version and prior-pilot sensitivities in the Abstract, Methods **§3.20**, Results **§4.20**, Discussion **§5.8**, strengthened limitations/Section 7 and new **Appendix R**.

**Completed:** source, inference, current reference pairing, all Valid current-bbox detection metrics, technically defined sensitivity testing and reproducible documentation. The originally requested expanded original-source Valid detection evaluation is no longer pending.

**Still fundamentally unmeasured:** actually executed target-matched occlusion/deletion/insertion XAI fidelity; **strong** uncertainty-gated selective PPE verification matched to A5 and actual compute/review budgets; verified worker-to-equipment/required-task safety states when claimed; worker false-safe-clearance/correct-violation endpoints; user-independent acquisition and deployment generalization; metered physical Joules or honest latency/memory evidence; journal-level figure, bibliographic and final analysis cleanup. Previous V25 policy routing on 74 real saved detector boxes made only **undispatched** suggestions. The original Test is development-exposed historically and **was not accessed in V26**; no model retraining or data edits.

**Next execution:** freeze and run **V27 real target-matched XAI fidelity and computational time** on predeclared original images under an actual strong matched selective comparator, using the unchanged model and source geometry; if worker mandate evidence is absent, keep occupational safety endpoint **NOT_ESTIMABLE** rather than inventing labels. The strict independent-source/worker-safety gate remains **`NOT_FROZEN`/`scoring_ready=false`**. Author's completed image review is accepted; no second reviewer or repeated general inspection is necessary.
