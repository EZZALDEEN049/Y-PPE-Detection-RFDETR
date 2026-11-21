# SEER-PPE V20 — execute frozen historical INTERNAL Valid object detection analysis

**21 November 2026.** This request triggers the readonly GitHub Actions metadata/numeric aggregation after [the internal protocol was frozen before outcomes](VALID_HISTORICAL_INTERNAL_OBJECT_EVAL_PROTOCOL_FROZEN_V20.md).

- **Actual identity:** 468/468 historical Eval image IDs match the original Valid Source IDs; exactly 459 are the corrected Clean17 Valid cohort, nine historical originals excluded.
- **Original author labels:** fetched existing saved Source annotation envelopes for **459/459 Valid images** without image review, with **3,471 current annotation boxes**, including **729 model-assisted provenance markers**. Twenty-five-image request batches were used solely for read-only annotation queries.
- **Historical fixed model:** reuse **existing Roboflow 2025 version-2 Eval** `KyzP9neuyNTN5eQpGCAY` saved per-Valid-image TP/FP/FN at confidence **0.20**; do not run a new model, open any Test, or assert original Eval box geometry remains available.
- **Known mismatch:** historical Eval uses **3,455 reference objects** versus **3,471 current Source annotations**; 446/459 image counts agree, **13** image counts disagree by **16** objects in total. This is a reference-version reconciliation issue; do not say the historic metrics were recalculated on all current labels.
- **Before-outcome fixed cohorts:** M0 459, M1 448, M2 367 by metadata-only source risk flags, no human re-review or independent-source assertions.
- **Action:** run self tests and source-ID/row integrity checks, calculate **historical micro TP/FP/FN and P/R/F1** by each cohort, report mismatched source IDs in an audit ledger and retain explicit caveats. Persist only derived numeric JSON.
- **Never:** re-train model, change images/annotations/splits, run Test/Valid inference, manufacture author signatures, infer worker PPE violation, or claim SEER safety/XAI/energy benefit.

Reproducible script: [V20 historical valid scorer](tools/compile_historical_valid_internal_metrics_v20.mjs). The strict worker-compliance independent-source scoring gate remains `scoring_ready=false`.
