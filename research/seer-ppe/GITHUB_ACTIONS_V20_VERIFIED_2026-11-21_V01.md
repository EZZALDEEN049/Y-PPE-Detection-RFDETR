# V20 — successful GitHub Actions: historical original model Valid-only counters and single-curator source label reconciliation

**2026-11-21.** [V20 execution run 44856892166](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44856892166) completed with all substantive numeric and source-identity steps **success**, including synthetic fail-closed tests, deterministic output generation and archival.

The **read-only historical 2025 version 2 Roboflow Eval** `KyzP9neuyNTN5eQpGCAY`, model `altayyar-0oflt-lafos-qqauz/2`, provided 468 original **Valid-only** image counters at confidence 0.20. Native image IDs match original Source IDs 468/468, of which 459 are retained in corrected Clean17. Current author-curated 459 Source annotation envelopes contribute 3,471 saved boxes (729 previously marked model-assisted); historic Eval reference counts total 3,455. **446 sources agree, 13 disagree by 16 objects**. Historical Eval geometry is unavailable for independent box-level re-evaluation.

Actual predeclared M0=459: TP3252 FP642 FN203, P0.835131 R0.941245 F10.885018. M1=448: TP3217 FP639 FN200, P0.834284 R0.941469 F10.884642. M2=367: TP2851 FP589 FN183, P0.828779 R0.939684 F10.880754. These results are **historical provider-evaluator counter aggregates**, not recalculated current-annotation metrics, not independent acquisition test, not a full mAP, and not SEER policy safety benefit.

The dedicated compiler checks wrong split/model/eval identity, forged independent-source cohort, duplicate IDs, current-source version mismatch and non-numeric counts. No original model inference, Test data use, user reinspection, second reviewer, weights/data edits, XAI, Joules or task-specific worker safety claims. Strict `scoring_ready=false` remains intact.

[Input historic Valid counters](HISTORICAL_V2_VALID_PER_IMAGE_COUNTERS_V20.json) · [derived outcome ledger](HISTORICAL_VALID_INTERNAL_METRICS_V20.json) · [protocol frozen before outcome retrieval](VALID_HISTORICAL_INTERNAL_OBJECT_EVAL_PROTOCOL_FROZEN_V20.md) · [script](tools/compile_historical_valid_internal_metrics_v20.mjs).
