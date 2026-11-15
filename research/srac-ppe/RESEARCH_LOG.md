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

## 2026-10-29 — Synthetic, end-to-end risk CLI integration check
- Executed `python -m srac_ppe.cli` from the locally patched v3 prototype with an **independent synthetic** calibration/test CSV and frozen protocol config. Exit code **0**; a JSON report was parsed and its assertions passed.
- Synthetic calibration: 120 independent violation clusters, with zero false CLEAR / missed cases, selected threshold 0.02 (under example config). Test: 1 true required-helmet violation but erroneous policy `NOT_REQUIRED`. Correct result: `false_clearance_count=0`, `uncontained_violation_count=1`, `n_policy_gt_requirement_disagreements=1`.
- This confirms **interface integration on fabricated test fixtures only**. It is not a model measurement, not a validated 5% field-risk guarantee, and not an inference or deployment experiment.

## 2026-11-15 — Public cross-dataset inference probe and manuscript-state synchronization

- Queried the public [Construction-PPE Roboflow Universe dataset](https://universe.roboflow.com/disitech-0pg5l/construction-ppe-unha4-5njlk): 1,416 images (1,132 train / 143 validation / 141 test). The test partition contained 24 images with `Person + no_helmet`, and 103 images with `Person + helmet` but no `no_helmet` tag.
- Ran the frozen author model `altayyar-0oflt-lafos-qqauz/2` (RF-DETR Small, original 17 classes) on all 24 positive-stratum images and 24 deterministic comparison images selected by ascending FNV-1a 32-bit hash of `SRAC20261110:` plus provider image ID. All 48 hosted inference calls returned predictions at confidence 0.25 / overlap 0.50.
- Image-level outcome: predicted `No Hard Hat` present in 22/24 positive-stratum images (91.7%; nominal exact 95% CI 73.0–99.0%) and 1/24 comparison images (4.2%; nominal exact CI 0.1–21.1%). This is image-level class presence / label discordance only, not worker-level recall or false-positive rate.
- Post-hoc filtering of the original 0.25 detections at 0.50 and 0.75 retained 20/24 and 15/24 positive-stratum images; comparison images remained 1/24 at each. These are descriptive sensitivity checks, not separate hosted inference calls or threshold selection.
- Machine-assisted visual review suggested two positive-stratum examples were non-construction scenes (soccer child; stage performer with casual cap), and the comparison discordance may involve an unannotated bareheaded second person. This review is not qualified human adjudication.
- A geometry-only screen of three crowded images considered 10 predicted head-equipment boxes: 9 had exactly one predicted-person candidate and 1 was ambiguous between two candidates; none were unmatched by a top-40%-person-region containment heuristic. This is not validated identity association or accuracy.
- Explicitly retained limits: detector training-source overlap and true site independence not checked; no independent worker inventory, helmet-rule adjudication, score fitting, probability calibration, risk calibration, final test, baseline comparison, or injury/deployment claim. The stratified image sample cannot estimate population precision, `R_AC`, or `R_FC`.
- Clarified the separate estimands `R_FC = P(CLEAR | true violation)`, `R_UC = P(CLEAR or UNDETECTED or erroneous NOT_REQUIRED | true violation)`, and `R_AC = P(true violation | CLEAR)`; an `R_FC` bound does not bound `R_AC`. The latter requires a representative all-worker sample.
- The committed candidate sample calculator still records 115 independent violations for zero FC errors and 159 for one FC error under the fixed two-risk/nine-threshold procedure. A separate 661-case scenario mentioned in chat was not reproduced from the committed calculator and is not adopted.
- Manuscript artifact inspection: local filename/metadata identify v5, visible title page labels v4.0; status text mentions six smoke tests while Section 6.1 reports the 48-image probe. Full unpublished DOCX was not uploaded to the public repo.
- The repo's previous 24/24 research-only prototype test record remains the canonical reproducible record; a later 25/25 conversational count was not independently rerun from source during this synchronization.
- Added [public progress report](PROGRESS_UPDATE_2026-11-15.md) and [aggregate probe CSV](EXTERNAL_IMAGE_LEVEL_PROBE_SUMMARY_2026-11-15.csv); updated canonical project status, manuscript checklist, experimental estimands and progress hub. No images, image IDs, credentials, weights, or full manuscript were committed.

## Next entry
Record the next independently verified milestone, its reproducible command or provider experiment reference, dataset identity, date, and what remains unverified. Do not update the status simply because time has passed.
