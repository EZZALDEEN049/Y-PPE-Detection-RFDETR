# V38-B — Final executable-runner technical signoff, zero paid model calls

**Date:** 23 November 2026 (Asia/Aden).  
**Paper title:** Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection.  
**Repository branch:** `research/v30-progressive-xai-2026-11-22`.

## Latest passing independent GitHub Actions verification

- **Run:** https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/45085319928 — all steps `success`, no Roboflow API key, no inference SDK, **zero hosted model calls**.
- **Frozen selection:** 24 Validation source images, 48 exact V26 detection targets, 11 PPE classes, identities and geometries unchanged, exclusion of prior V23 pilot and four previously V30-exposed Valid IDs.
- **Images:** All 24 fetched only to ephemeral CI storage; original source raw SHA-256 and canonical EXIF-corrected RGB SHA-256 checked against `V38_B_CURRENT_SOURCE_EXIF_AWARE_SHA256_PREFLIGHT_2026-11-23.json`. One EXIF orientation=6 image handled without resizing; original bytes not committed or uploaded.
- **Scientific mock:** Full 2-target/1-image synthetic execution: 8×8/4×4 single-cell gray perturbation and Gaussian blur-fill maps; target-match baseline; 8×8 saliency plus 10 SHA256 seeded random rankings and 4×4 saliency 11-point deletion/insertion curves. Total **378 mocked calls**, **24 curves**, complete mock response results and deterministic repeatable checks.
- **Transport:** Single raw HTTPS model-image POST per attempt with standard serverless endpoint, fixed confidence 20%, overlap 50%, no application or SDK automatic retries, redirects forbidden, API key remains secret. Mock HTTP 503 and mock HTTP 200 each generated exactly one transport attempt. Ledger writes `ATTEMPT_RESERVED` with disk `fsync` **before** request; records success/failure; refuses duplicate-run log, tests fail-safe call cap and authorization refusal.
- **Wire encoding prospective amendment:** Every image and perturbation is encoded as JPEG quality=95, chroma 4:4:4, `optimize=False`; original-image benchmark max **9,183,493 bytes / 24 images**, versus original lossless PNG max **26,239,500 bytes** (1/24 over runner's 15 MiB cap). Lossy compression acknowledged as methodological caveat; future any-perturbation payload >15 MiB aborts and is logged instead of resizing or changing encoding.
- **Budget:** 5,200 intended model-image requests, 800 unspent contingency budget slots, absolute `MAX_CALLS=6000` app-transport attempted requests, no auto-retries. All settings frozen and numeric evidence from historical V26–V37 unaffected.
- **Author screenshot funding:** monthly included Research Plan 50 credits; 2.49 credits used; 47.51 credits arithmetic headroom as of provided snapshot. Estimated 6,000 requests ≈1.125 credits based on earlier public standard model-specific rate, **not** metering guarantee; no credit purchase, no paid experimental inference.

## Guardrails / not-yet-executed items

- `research/seer-ppe/tools/run_v38b_xai.py` has opt-in live `--execute` mode, but refuses without a **separately author-approved, one-time, exact-manifest-SHA-bound authorization JSON** AND the CLI `--confirm-authorized-max-attempts 6000`. It also must see 24 matching current oriented image SHA-256 values and must refuse reuse of a prior result/checkpoint/attempt-ledger file.
- The CI never supplied a credential; its successful run proves offline flow, source checks, mock transport, and refusals. It does **not** prove that the real model returns valid baseline scores for all targets with new JPEG wire encoding, or that no transient provider failure happens. Those outcomes must be recorded faithfully in a later authorized run.
- No paid trigger or automatically executing GitHub workflow has been set up. A future single-run supervised workflow/CLI execution and numeric evidence archive should be created **only after author approval**; do not implicitly authorize paid inference because credits are available.
- The study is a **development-exposed diagnosis**, not an external source-independent evaluation, not an objective ground-truth explanation test, and not a worker-level safety-compliance result.
- This report is internal research engineering signoff, not submission to *Results in Engineering*.

**TECHNICAL READINESS:** PASSED (offline and read-only). **AUTHOR EXECUTION APPROVAL:** NOT YET GIVEN. **NEW V38-B HOSTED MODEL CALLS:** ZERO.
