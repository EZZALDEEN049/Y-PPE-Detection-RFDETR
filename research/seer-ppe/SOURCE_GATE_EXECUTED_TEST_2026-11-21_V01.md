# SEER-PPE — Executed Node source-integrity gate test and live-data logic check (21 Nov 2026)

## Verified executable artifact

- **Target file:** [`tools/source_integrity_readiness_gate.mjs`](tools/source_integrity_readiness_gate.mjs).
- **GitHub blob SHA-1:** `db6714be6280d35959ef5859fba7994ebbcd4e7c`.
- **Local replay bytes:** 4,075 bytes, and Git object digest of the replayed source **exactly matched** the current GitHub blob SHA. This is stronger than matching just the filename or copied output.
- **Local runtime:** Node.js `v22.16.0`.
- **Exact script run:** `node source_integrity_readiness_gate.mjs --self-test` → **`SOURCE_INTEGRITY_READINESS_GATE_SELF_TEST_PASS`**. This is an **actually executed** Node self-test, not a theoretical test plan.
- **Additional runtime tests:** imported exported `summarize()` after enabling its built-in self-test CLI branch; one valid synthetic case passed with `scoring_ready=false`; four invalid cases threw errors as expected: null manifest, repeated image IDs, missing named-site hold row, and unsupported visual-hold ID. **4/4 deliberately invalid scenarios rejected**.
- **Live repository-data gate logic cross-check:** separately re-applied the exact hold/group conditions in the connected JavaScript environment to the existing GitHub JSON manifests, yielding 3 named-site Valid holds + 2 visually suspicious Valid holds = **5** distinct held IDs; **26** additional filename-only Valid candidates; **468** Valid Source IDs; the updated cross-split review queue has **83** unique Valid IDs. These checks read the actual GitHub manifests but do **not** constitute execution of the Node CLI's default real-data branch.
- **GitHub Actions CI:** a [workflow has been committed](../../.github/workflows/seer-ppe-source-reference-gates.yml) to run these checks in future pushes, but the **remote execution outcome was not confirmed** in this session. Do not claim a passing GitHub Actions job without verified run logs.

## Boundaries and blockers

This verifies deterministic program logic only. The gate always returns `model_metric_scoring_ready:false` and has not been promoted to a scientific eligibility gate. The full original 2,093 Train/Valid images have not been obtained inside the execution container, so there are no real complete SHA-256 / decoded-pixel hash / dHash measurements. No newly accessed Test images, no model inference or retraining, no Roboflow data mutation, and no new human Person–PPE ground truth.

This is a **research engineering test** result, not evidence that photo family independence, PPE compliance, scientific effectiveness, mAP, F1 or energy metrics have been established.

## Output status

`NODE_SELF_TEST_EXECUTED_PASS`  
`FOUR_NEGATIVE_CASES_REJECTED_PASS`  
`LIVE_MANIFEST_LOGIC_CHECK_PASS`  
`GITHUB_ACTIONS_EXECUTION_UNVERIFIED`  
`ORIGINAL_PIXEL_HASH_AUDIT_INCOMPLETE`  
`SCORING_READY_FALSE`
