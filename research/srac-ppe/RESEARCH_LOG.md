# SRAC-PPE research log

Append-only dated record. Each entry must distinguish actual verification, inherited project history, and unresolved claims. Do not backfill missing experiment outcomes.

## 2026-10-29 — Public GitHub progress synchronization
- Confirmed target existing repository is **public** and write access is available.
- Opened and inspected the project-held manuscript v3 DOCX locally; it contains drafted methods and an explicitly unfilled Results shell.
- Re-ran tests from the SRAC-PPE frozen-model integration starter package using `python -m unittest discover -s tests -v`: **14 tests / 14 pass**.
- Re-inspected the available harmonized nine-class Y-PPE ZIP: 1,236 train + 356 validation + 186 test images, corresponding annotation files, and `no_helmet` annotation counts 113/40/14.
- Confirmed that the above are **software/data checks only**: no real independent RF-DETR test inference or new calibration outcome is claimed.
- Initialized the public-safe, centralized [PROJECT.md](PROJECT.md), [MANUSCRIPT_PROGRESS.md](MANUSCRIPT_PROGRESS.md), and [SYNC_PROTOCOL.md](SYNC_PROTOCOL.md); linked the hub from the repository root README; read back all five hub files from GitHub.
- Created and enabled a daily conditional ChatGPT automation for evidence-gated GitHub synchronization. Future execution and access are not yet independently verified.

## 2026-10-28 — Previous project session (historical log)
- Updated an unpublished research draft to v3 with a frozen-model interface.
- Project-session image review reported possible related-scene overlap and uncertainty in interpreting `no_helmet` as an actual safety-policy violation; replicate the acquisition-level audit before relying on it.
- Tested prototype with synthetic/unit scenarios; this is **not** independent detector validation.

## Historical author research (not this paper's results)
- Repository documents prior harmonized datasets and a related YOLO11m cross-domain reliability study.
- The earlier results may motivate hypotheses and supply methods/provenance, but cannot be represented as original SRAC-PPE experiment outputs.

## 2026-10-29 — Independent archive, math, code and novelty audit
- Rechecked the `Y-PPE-h9-v2_RFDETR_Roboflow.zip` image/label records (1,778 paired files), index SHA-256 and all per-file hashes; 0 exact-byte image cross-split duplicates, 1 within-training duplicate group. Reported object-label support and an explicitly limited 64-bit dHash screen. See [data audit](DATA_AUDIT_2026-10-29.md).
- Analyzed ground-truth **box-center** association feasibility for no-helmet objects: train 107 unique / 4 unmatched / 2 ambiguous; valid 39/1/0; test 13/0/1. This is *not* inference performance.
- Verified exact binomial case counts for k={0,1,2,3,5,10} using SciPy beta quantiles, and authored a generic [risk sample calculator](tools/risk_budget.py).
- Found and reproduced a `auto_clear_coverage` reporting bug (200% coverage with indeterminate GT included in numerator); patched an **unpublished local working copy** and added regression test: 15/15 unit tests passed. Canonical v2 ZIP remains untouched. See [code audit](CODE_AUDIT_2026-10-29.md).
- Verified foundational and overlapping 2024–2026 papers at publishers; documented novelty collisions rather than asserting a novel risk theorem. See [novelty audit](NOVELTY_AUDIT.md).
- Drafted [experiment protocol v0.2](EXPERIMENT_PROTOCOL.md) with frozen-model, label-meaning, independent-site, threshold selection and fair-baseline requirements.
- Defined [annotation codebook v0.1](ANNOTATION_CODEBOOK.md) for context-dependent helmet mandates, head visibility, all GT workers and two-blind-annotator adjudication. **No actual field annotations performed.**
- **Still not done:** independent RF-DETR inference, ground-truth PPE-required adjudication, calibrated worker scores, site-specific empirical risk bounds, main method/baseline experiments or final-result tables.

## 2026-10-29 — Second-pass pHash overlap, fail-closed split guard and extended tests
- Computed 64-bit pHash for **all 1,778** decoded JPEGs of the nine-class ZIP, screened all cross-split pairs at Hamming <=4/6/8/10/12, and visually reviewed all 10 pairs at <=8. Confirmed **4 same-scene/same-product-image train-test pairs affecting 3 distinct test images**, plus **2 train-validation pairs affecting 2 distinct validation images**. Other lookalike product images were rejected as leakage claims. See [scene audit](SCENE_LEAKAGE_AUDIT_2026-10-29.md) and [quarantine candidates](QUARANTINE_CANDIDATES_2026-10-29.csv).
- Three quarantined test image labels contain **zero `no_helmet` object annotations**; the total 14 test `no_helmet` annotations does not therefore change from excluding these three images, but remains unsuitable for worker-level risk guarantees.
- Added [pHash screening script](tools/phash_overlap_audit.py) and [source-group overlap gate](tools/group_independence_gate.py), with **8 additional local unit tests** against intentionally overlapping/faulty manifests. Source-group metadata for the actual ZIP are still incomplete; a PASS based only on hashes would be unscientific.
- Repaired coverage denominator in the **local working integration package** and added 5 regression tests: now **19/19 local package tests pass** (previously 14). Committed an [applyable patch](software/patches/0001-fix-coverage-denominator.patch); it is **not yet applied to the originally supplied ZIP**.
- Added a privacy-safe GitHub Actions [quality-gates workflow](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/blob/main/.github/workflows/srac-ppe-static-checks.yml); **remote CI completion has not been verified**.
- Unchanged blockers: no frozen-model inference on independent site data; no independent worker-level mandated-PPE labels; no final paper results.

## 2026-10-29 — Anti-leakage policy schema finding
- Reviewed original `srac_ppe/risk.py` and confirmed the same `ppe_required` field feeds inference policy logic and offline risk-denominator selection. Identified this as a **potential policy/GT label-leakage channel**, unless provenance proves the field was prospectively available.
- Amended [EXPERIMENT_PROTOCOL.md](EXPERIMENT_PROTOCOL.md) with separated runtime policy and independent offline truth fields. No claim that the original risk software interface is now corrected.

## 2026-10-29 — Corrected research-only runtime policy prototype
- Added a second sequential [research patch](software/patches/0002-separate-runtime-policy-and-ground-truth.patch) to split deployable site safety rule `policy_helmet_requirement` (REQUIRED / NOT_REQUIRED / UNKNOWN), its `policy_source_id` and offline-only `gt_ppe_required` truth.
- Found a further safety-measure blind spot: a **NOT_REQUIRED** decision on a truly violating worker would not be counted by the old UC definition. Expanded `UC` to count CLEAR, UNDETECTED and erroneous NOT_REQUIRED, while keeping FC as CLEAR only.
- Added five local interface/regression tests: **24/24 tests of the research-only patched v2 integration prototype passed**. The original ZIP is unchanged; patch application was checked locally but not deployed into a production codebase.
- Updated [experiment protocol](EXPERIMENT_PROTOCOL.md), [software notes](software/README.md) and manuscript section status. **No new real RF-DETR inference, calibrated worker probability, independent site labels or final risk result**.

## Next entry
Record the next independently verified milestone, its reproducible command or provider experiment reference, dataset identity, date, and what remains unverified. Do not update the status simply because time has passed.
