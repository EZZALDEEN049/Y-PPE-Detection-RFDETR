# SRAC-PPE — Canonical project status

**Last checked:** 2026-10-29 (Asia/Aden)  
**Lifecycle:** experimental validation preparation; **NOT submission-ready**  
**Research owner:** Ezzaldeen Nabil Ghaleb Obadi Al-Tayar, Taiz University  
**Research title:** *Trustworthy and Risk-Aware Vision Transformers for PPE Compliance Monitoring Under Domain Shift and Limited Data*.

## 1. Research objective
Develop and independently evaluate a worker-level, selective PPE decision policy built on an existing frozen RF-DETR Small detector. Candidate decisions: **CLEAR (visual evidence supports compliance), ALERT, REVIEW**, with **UNDETECTED** accounted for during ground-truth-based evaluation. The key endpoint is wrongly clearing a worker who is actually noncompliant in a context where the PPE is required.

Do not conflate (a) no visible hard hat with (b) an adjudicated occupational-safety violation. A no-helmet label alone does not prove a site-level helmet mandate.

## 2. What is verified as of this update

| Item | Evidence and scope | State |
|---|---|---|
| Proposal and v3 English manuscript | A draft v3 DOCX was inspected locally in the project session: Introduction, Related Work, formal risk objective, proposed methodology, experimental plan, structured *empty* Results section, limitations and references. | Draft prepared; **not** empirical paper |
| Frozen detector | Roboflow model ID `altayyar-0oflt-lafos-qqauz/2` is identified; RF-DETR Small with 17 original classes. | Identified; no new independent inference performed here |
| SRAC-PPE prototype | Python risk module, Roboflow parsing/association bridge, CLI and tests exist in the project starter package (v2). | Software prototype |
| Prototype tests | On 2026-10-29, the package's `python -m unittest discover -s tests -v` ran **14 tests, all passing**. | Verified on synthetic/unit scenarios, **not model accuracy** |
| Y-PPE harmonized archive | ZIP inspected locally on 2026-10-29: **1,236 train, 356 validation, 186 test** images, each matched by a label file; total **1,778 images**. | Archive accessible; structural counts confirmed |
| No-helmet support | 113 train, 40 validation, **14 test** `no_helmet` object annotations. | Verified *object* annotations; not independent, adjudicated worker violations |
| Existing related baseline | The prior project repository documents earlier YOLO11m and harmonized cross-domain studies. | Prior work; not new SRAC-PPE evidence |

The 14 test no-helmet annotations are insufficient for a strong 5% worker-level false-clearance risk claim, even ignoring within-image dependence and the need for context-specific ground truth.

### Prior audit caveat
Earlier project-session visual inspection reported some cross-split related scenes and contextually ambiguous no-helmet images. Those observations should be independently reproduced, logged by acquisition group, and adjudicated before accepting this archive as an independent evaluation benchmark. Hash-unique images can still depict the same scene.

## 2A. Newly verified audit and methodological readiness (2026-10-29)
- [Dataset evidence audit](DATA_AUDIT_2026-10-29.md): full ZIP/manifest integrity checks passed for **1,778** image–label records; no exact-byte cross-split duplicates, **one within-training exact duplicate**, and two *unadjudicated* dHash<=4 train–validation candidate pairs. These checks do **not** prove source-scene independence.
- Nine-class Y-PPE test has **14 no-helmet object annotations in 12 images**; this is not an independent-worker violation sample.
- [Experimental protocol v0.2](EXPERIMENT_PROTOCOL.md): frozen decision ontology, independent sampling, fair matched-review baselines and risk endpoints are drafted **but not preregistered or empirically validated**.
- [Annotation codebook v0.1](ANNOTATION_CODEBOOK.md): specifies context-verified worker/helmet-required labels, blind double annotation and explicit indeterminate states; **no independent human labels have been completed**.
- [Finite-sample planning](tools/risk_budget.py): exact one-sided Clopper–Pearson / 2M Bonferroni feasibility requires **115** independent violations for zero FC errors at 5%, or **159** for one error, under the candidate protocol.
- [Prototype software audit](CODE_AUDIT_2026-10-29.md): corrected a reproduced CLEAR-coverage denominator error in a **local working copy** and passed **15/15** tests; originally distributed ZIP is **not yet patched**.
- [Related-work collision audit](NOVELTY_AUDIT.md): identified direct 2024–2026 overlaps in uncertainty-aware PPE worker review, context-sensitive rules, detection calibration, cross-site generalization and general risk-control theory. Novelty requires strong empirical proof, not naming components.

## 2B. New independently checked gates (2026-10-29, second-pass)
- [Cross-split pHash + visual audit](SCENE_LEAKAGE_AUDIT_2026-10-29.md): 4 related train–test pairs, **3 unique test images**; 2 related train–valid pairs, **2 unique validation images**. The test/validation files are now listed in [quarantine candidate manifest](QUARANTINE_CANDIDATES_2026-10-29.csv) pending source-family adjudication; original ZIP must remain immutable. Candidate pHash pairs alone are not proof; these six were visually reviewed. This **reopens** the independence gate for the 1,778-image nine-class ZIP, without retroactively invalidating a separately frozen cleaned corpus.
- [Group independence gate](tools/group_independence_gate.py) rejects cross-split acquisition group overlap, SHA-256 overlap and unknown provenance; **8 local synthetic tests passed**. A [GitHub Actions quality-gate workflow](../../.github/workflows/srac-ppe-static-checks.yml) was added (the actual remote run result has not yet been verified).
- [Local risk code regression](CODE_AUDIT_2026-10-29.md): the corrected local v2 package now passes **19/19** unit tests. An [applyable patch](software/patches/0001-fix-coverage-denominator.patch) is committed, **but the original distributed ZIP remains unchanged**.
- No target worker-level labels, frozen RF-DETR inference or empirical risk-control results have been produced.

## 3. Scientific definitions and guardrails
- **FC risk:** `P(CLEAR | true violation requiring PPE)`.
- **UC risk:** `P(CLEAR or UNDETECTED | true violation requiring PPE)`.
- **Risk-controlled decision:** fixed detector, score mapper, evidence gate and a pre-specified finite threshold grid; conservative upper confidence bounds on a separate target-domain risk-calibration set.
- **Assumptions:** suitable independent acquisition units, accurate worker-level labels, correct PPE-required context, no calibration/test reuse and well-defined target population.
- **No guarantee across sites** from a bound calibrated at one site. Two dataset sources do not automatically constitute verified independent construction sites.
- **Risk targets in the draft are illustrative research parameters**, not validated legal safety thresholds.

## 4. Current critical path
1. **Freeze the genuine target evaluation population:** identify independent construction-site/camera/acquisition groups and permission to use field images.
2. **Obtain an executable inference pathway** for the frozen 17-class RF-DETR: authorized Roboflow inference on permitted images or separately available verified weights; never publish secret API tokens.
3. **Create worker-level ground truth:** complete worker inventory (including people not detected), helmet present/worn status, visual observability, person–helmet association and whether a helmet is required.
4. **Check leakage and sample support** before assigning target score-calibration, risk-calibration and final-test groups.
5. **Run frozen inference** and retain prediction provenance, class map and thresholds; separately map 17-class outputs to the intended worker-level task.
6. **Evaluate baselines before the proposed method:** detector-only, fixed-confidence, score calibration, selective human review and ablations.
7. **Calibrate site-specific risk**, report when no feasible threshold can be supported; do not hide abstention or missed workers.
8. **Independent final test:** report FC/UC risk, violation recall, automation coverage/review burden, ECE/Brier as appropriate, risk–coverage, latency, uncertainty intervals, failure cases and site-specific breakdowns.
9. **Novelty audit vs related published risk/calibration/PPE systems**; update manuscript only when grounded results exist.

## 5. Items expressly NOT completed
- No new frozen RF-DETR inference results on independent images in this repository update.
- No finalized worker-level regulatory/context ground truth.
- No actual target-site risk-calibration results or validated 5% guarantee.
- No SRAC-PPE improvement established vs competitive baselines.
- No independent multi-site test established.
- No submission-ready Q1 manuscript.

## 6. Requests that would unblock the critical path
- Access to **authorized model predictions** on an independent, permitted collection, or executable weights/inference access **without sharing a secret in GitHub or chat**.
- A reproducible independent image dataset with documented collection/site groups and true worker-level safety context.
- Expert adjudication of helmet requirement and ambiguous/occluded workers.

**Update policy:** change this file only when a new step is actually verified; include date, source, method, and limitations. See [SYNC_PROTOCOL.md](SYNC_PROTOCOL.md).
