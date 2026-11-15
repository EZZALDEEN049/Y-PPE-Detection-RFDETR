# SRAC-PPE — Canonical project status

**Last checked:** 2026-11-15 (Asia/Aden)  
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
| Frozen detector | Roboflow model ID `altayyar-0oflt-lafos-qqauz/2`; RF-DETR Small, 17 original classes; 48-image public cross-dataset hosted-inference probe completed. | Inference pathway verified; worker-level and site-level risk evaluation still pending |
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
- A synthetic end-to-end v3 CLI smoke test also succeeded (120 fabricated calibration violations and one fabricated test policy disagreement); the revised UC measure captured the erroneous NOT_REQUIRED. **No target worker-level labels, frozen RF-DETR inference or empirical risk-control results have been produced.**

## 2C. Open deployment-knowledge issue
- The originally distributed v2 prototype uses a shared `ppe_required` Boolean for runtime decisions and offline risk truth. This is **potential leakage if derived from retrospective GT**. The study requires [strict policy/GT separation](EXPERIMENT_PROTOCOL.md#b2-strict-anti-leakage-interface-contract-critical-prerequisite). A [research-only patch](software/patches/0002-separate-runtime-policy-and-ground-truth.patch) and revised local tests now demonstrate this separation; **24 local unit tests pass, but archived v2 ZIP and data producers have not been migrated**, so the end-to-end gate remains OPEN.
- Unknown policy requirement routes to REVIEW for detected workers, not silently to `False`. Erroneous `NOT_REQUIRED` on a true violation contributes to revised UC risk. The interface is locally prototyped and tested; full provenance and downstream compatibility remain **OPEN**.

## 2D. Public cross-dataset image-level inference probe (2026-11-15; exploratory only)

- The frozen 17-class RF-DETR Small model was run through hosted inference on **48 images** from the test split of the public [Construction-PPE dataset](https://universe.roboflow.com/disitech-0pg5l/construction-ppe-unha4-5njlk): 1,416 total images (1,132 train / 143 validation / 141 test).
- Sample construction: all 24 test images with GT metadata `Person + no_helmet`; plus 24 of 103 `Person + helmet` images without a `no_helmet` tag, selected by ascending FNV-1a 32-bit hash of `SRAC20261110:` plus provider image ID. All 48 inference requests returned results.
- Model `altayyar-0oflt-lafos-qqauz/2`; hosted inference confidence 0.25, overlap 0.50. GT `no_helmet` was compared with predicted `No Hard Hat` at image level.
- At the 0.25 cutoff, 22/24 positive-stratum images contained at least one predicted `No Hard Hat` box (91.7%; nominal two-sided exact 95% CI 73.0–99.0%). One of 24 comparison images also contained a predicted `No Hard Hat` box (4.2%; nominal exact CI 0.1–21.1%). This is **label discordance**, not a validated false-positive rate.
- Post-hoc filtering of the original 0.25 predictions at 0.50 and 0.75 retained 20/24 and 15/24 positive-stratum images, respectively; the comparison stratum remained 1/24 at both. These are descriptive sensitivity checks, not prospective threshold selection.
- Machine-assisted visual review suggested two positive-stratum images were non-construction scenes (soccer child; stage performer with casual cap), while the discordant comparison image appeared to include a second bareheaded person omitted from the absence-class labels. This is not qualified human adjudication.
- A three-image predicted-box geometry screen examined 10 head-equipment boxes: 9 had a unique predicted-person candidate, 1 was ambiguous between two candidates, and none was unmatched using a top-40%-of-person-box containment heuristic. This is not validated worker association.
- This is **cross-dataset image-level feasibility only**. Model training-source overlap, true site independence, worker identity, helmet mandate, all-worker GT, and source-cluster independence are unresolved. No calibration, FC/UC risk estimation, R_AC estimation, baseline comparison, or cross-site claim follows.

See [the full public-safe progress report](PROGRESS_UPDATE_2026-11-15.md) and [aggregate probe summary](EXTERNAL_IMAGE_LEVEL_PROBE_SUMMARY_2026-11-15.csv).

## 3. Scientific definitions and guardrails
- **FC risk:** `P(CLEAR | true violation requiring PPE)`.
- **Accepted-CLEAR violation proportion (R_AC):** `P(true violation requiring PPE | decision = CLEAR)`. This is not controlled by an FC bound and requires a representative all-worker test sample; a stratified case-control image sample cannot estimate it.
- **UC risk (revised after policy/GT separation):** `P(CLEAR or UNDETECTED or erroneous NOT_REQUIRED | true violation requiring PPE)`.
- **Risk-controlled decision:** fixed detector, score mapper, evidence gate and a pre-specified finite threshold grid; conservative upper confidence bounds on a separate target-domain risk-calibration set.
- **Assumptions:** suitable independent acquisition units, accurate worker-level labels, correct PPE-required context, no calibration/test reuse and well-defined target population.
- **No guarantee across sites** from a bound calibrated at one site. Two dataset sources do not automatically constitute verified independent construction sites.
- **Risk targets in the draft are illustrative research parameters**, not validated legal safety thresholds.

## 4. Current critical path
1. **Freeze the genuine target evaluation population:** identify independent construction-site/camera/acquisition groups and permission to use field images.
2. **Freeze inference provenance and audit source overlap:** preserve the authorized hosted-inference path for the frozen 17-class RF-DETR, verify detector training-source overlap against the external test images, and never publish secret API tokens.
3. **Create worker-level ground truth:** complete worker inventory (including people not detected), helmet present/worn status, visual observability, person–helmet association and whether a helmet is required.
4. **Check leakage and sample support** before assigning target score-calibration, risk-calibration and final-test groups.
5. **Run frozen inference** and retain prediction provenance, class map and thresholds; separately map 17-class outputs to the intended worker-level task.
6. **Evaluate baselines before the proposed method:** detector-only, fixed-confidence, score calibration, selective human review and ablations.
7. **Calibrate site-specific risk**, report when no feasible threshold can be supported; do not hide abstention or missed workers.
8. **Independent final test:** report FC/UC risk, violation recall, automation coverage/review burden, ECE/Brier as appropriate, risk–coverage, latency, uncertainty intervals, failure cases and site-specific breakdowns.
9. **Novelty audit vs related published risk/calibration/PPE systems**; update manuscript only when grounded results exist.

## 5. Items expressly NOT completed
- A 48-image public cross-dataset image-level probe is now available; it is not an independent worker-level, risk-calibration, or verified cross-site evaluation.
- No finalized worker-level regulatory/context ground truth.
- No actual target-site risk-calibration results or validated 5% guarantee.
- No SRAC-PPE improvement established vs competitive baselines.
- No independent multi-site test established.
- No submission-ready Q1 manuscript.

## 6. Requests that would unblock the critical path
- A permissioned independent construction-site collection with site/camera/acquisition-group provenance and a documented overlap audit against the detector's training sources.
- A reproducible independent image dataset with documented collection/site groups and true worker-level safety context.
- Expert adjudication of helmet requirement and ambiguous/occluded workers.

**Update policy:** change this file only when a new step is actually verified; include date, source, method, and limitations. See [SYNC_PROTOCOL.md](SYNC_PROTOCOL.md). The 15 November public-safe evidence snapshot is [here](PROGRESS_UPDATE_2026-11-15.md).
