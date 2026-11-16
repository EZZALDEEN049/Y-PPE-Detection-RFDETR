# SEER-PPE — experimental master protocol v0.7 (author decisions through Q39)

**Revised:** 17 November 2026 (Q40 data ownership addendum). **Status:** working, *not preregistered*, hypotheses and operational methods only. Historical Y-PPE Test was exposed during earlier dataset/model refinement. No newly independent holdout, new safety superiority result, XAI faithfulness result or joules measurement is claimed.

## Research question and objective

Can **SEER-PPE**, a safety-constrained and uncertainty-aware post-detection policy, achieve lower **incremental** explanation compute cost than a strong **preselected matched-budget selective XAI competitor**, while satisfying prespecified worker-level false-clearance, uncontained-violation, review-load and explanation-faithfulness requirements?

A joule endpoint is permissible only if physically metered electrical energy and device/sensor scope are documented; otherwise preregister an explicit computational efficiency endpoint before final assessment (e.g. additional predictor/XAI calls per eligible worker), with latency and memory as secondary indicators. Never translate model-call reduction or FLOPs into claimed measured electrical saving.

## Fixed source and checkpoint boundaries

- Use existing **17-class Y-PPE** images only. Historical raw: 2,327 images, 16,520 labels, train/valid/test 1,625/468/234. Roboflow augmented version 2: 5,577 images 4,875/468/234; finished original **RF-DETR Small** model ID `softyyemen/altayyar-0oflt-lafos-qqauz/2` (historic mAP@50 96.22%, **prior work only**). Version 3 is the unaugmented source, not assumed a separately trained model.
- **Clean17** frozen derivative: 2,288 images, 16,300 labels, splits 1,595/459/234; private ZIP SHA256 `d47d9676b785a847ef1bcb8a871574815b0b67b967f9107680fb0b85b1a52d61`. Full archive extraction verified, not a new acquisition-independent dataset.
- `Y_RFDETR_s17` (seed 17) checkpoint is **9-class h9**, not 17-class original. Roboflow connector issued short-lived authorized original-version weights URL; raw weight download, exact checkpoint SHA/class-head inspection, local inference and gradient access remain OPEN.
- Hosted original-model predictions in Roboflow and locally loaded original checkpoint predictions in Colab will be checked on permitted Train images; hosted network/API time must not be interpreted as local energy.

## Source independence and split control

- Use Train for implementation and exploratory work; validation examples not already used for SEER tuning for calibration; lock all routing weights, selection decisions, comparator, analysis scripts, fallback endpoint and budget before **one post-freeze historical-Test internal assessment**.
- Historical Test was repeatedly viewed/used in earlier Y-PPE development, and three historical smoke inputs were SEER-development exposed. Do **not** call it untouched, independent, external, blinded or acquisition-independent. Do not tune against its final results; report prior exposure.
- No per-image source ledger exists. Preserve the frozen underlying image files, splits and annotations. Maintain a new **separate** audit manifest: `image_id, split, sha256, provenance_family_if_supported, possible_scene_group, SOURCE_UNKNOWN, review_basis, suspected_leakage`. Existing stage-2 exact duplicates and known video/source grouping conflicts were corrected. Seven small-dHash cross-split pairs were visually judged different objects/images by a single analyst, not independently verified acquisition. Flag, inspect and group justified suspected same scenes. Report overlap-excluded sensitivity analysis; never claim complete source independence.

## Reference construction and status semantics

- Reuse the completed 30-image context pilot (14 work-plausible, 14 negative/non-work controls, 2 uncertain) for sampling-plan feasibility only. Choose a random core sample plus distinctly reported hard/rare-case enrichment. Determine final target number using eligible workers, verified violations and risk-interval precision; predefine selection, enrichment and stopping rules. Unknown task/site policy is never inferred solely from Y-PPE class labels.
- Researcher is the current **single curator and single reviewer**; not independent A/B safety reviewers. Label **all visible persons**, including persons missed by detector. For each worker/equipment item capture visually `PRESENT, ABSENT, UNKNOWN`; model detection `DETECTED, NOT_DETECTED`; association `MATCHED, ASSOCIATION_UNKNOWN`; worker eligibility and task/site mandate `REQUIRED, NOT_REQUIRED, POLICY_UNKNOWN` with source/justification. Only when confirmed **required** and confirmed **absent** label a real occupational violation. Hypothetical site policies are simulated scenarios only.
- Unknown state must not be silently mapped to compliant or violation. Count review-needed, missing worker and uncontained true violation separately. Reference-review uncertainty and unknown site mandate must be disclosed as construct validity limits.

## Evidence routing and safety invariants

- Route `BASIC` for sufficient detector evidence, `EXPLAIN` for selected target-specific XAI, and `REVIEW` to abstain/request human review. Routing inputs can include detected boxes/class/score, visibility, association margin, hazard severity/priority, risk/uncertainty, known task mandates, elapsed compute and budget; **never** adjudicated reference/test labels.
- Rules fixed before calibration: no confirmed violation from a bare `No Hard Hat` detection without known mandate; no `COMPLIANT` for unresolved visual evidence, source/worker coverage, association or policy; no unsupported clearance due to exhausted XAI or review budget. Precautionary alerts for potentially severe hazards are logged apart from verified violations.
- Person–equipment association uses geometric containment, PPE-specific body region, overlap, confidence and top-two candidate margin. Unresolved ties `ASSOCIATION_UNKNOWN` route for explanation/review. Missing person detection is not repaired by heatmaps on existing objects. Optional budgeted repeat detector or secondary person detector is included only if executable, matched across eligible baselines and fully costed. Explicitly inspect an evaluation sample of **zero-person-prediction frames**.
- Adaptive compute budget and review cap have prespecified values chosen from feasible development/calibration evidence. Overflow remains `UNKNOWN`/`PENDING_REVIEW`, not `COMPLIANT`; log queue size, pending duration and completed assessments. `REVIEW_REQUESTED` is not `REVIEW_COMPLETED` or `ACTION_CONFIRMED`. Simulated queue time is labeled simulation, not observed real operations.

## Target-specific faithfulness

- Use original target class/box identity, model-agnostic Occlusion, controlled deletion/insertion perturbations, evidence/worker/PPE localization and non-target control regions. Re-predict on each perturbed image; match same-class boxes using a predeclared same-instance IoU/spatial rule. Log `MATCHED`, `LOST` and `AMBIGUOUS` distinctly, without assigning a different target or imputing zero score for vanished predictions.
- Use more than one perturbation/masking scheme; report robustness and artifact limitations. Gradient explanation may be compared only if the **exact audited original 17-class** checkpoint has a compatible differentiable loader and suitable gradients. Hosted inference JSON alone does not yield gradient access.

## Experimental arms, comparator and ablations

- A0 detector only; A1 Explain-All eligible targets; A2 Confidence-Only; A3 Budget-Only; A4 unsafe safety-guard-off **diagnostic** comparator (separate, not deployment option); A5 full SEER-PPE.
- Preselect a **strong selective primary comparator** on Validation before inspecting final SEER Test results. For fair main contrasts hold same basic safety guardrails, detector, input images, site policies and GPU. Constrain review capacity equally and report a second matched-compute/XAI-call budget analysis. Avoid cheap 'wins' obtained by dumping more cases into review.
- Four core ablations remove risk, uncertainty, association-specific evidence or adaptive compute budgeting individually while preserving nonnegotiable safety rules. Optionally test predeclared risk×uncertainty and association×uncertainty interactions. Recalibrate each on Validation; avoid post-test selection.

## Calibration, gate ordering and inference

**Gate 1: worker safety and explainability feasibility.** Fix worker-level false-clearance and uncontained-confirmed-violation denominators; severity/mandate requirement; allowed review/overflow; explanation target-match/fidelity lower bounds; confidence level and noninferiority margin (if feasible) before final analysis. These values have **not yet been established** and will be feasible only if confirmed sample sizes support their interval widths. A queue request does not constitute mitigation.

**Gate 2: efficiency after Gate 1.** Among gate-passing policies compare measured incremental XAI cost vs preregistered selective comparator, with Explain-All secondary. If sensor gate passes, use integrated real power trace under specified detector/XAI scope and report Joules; otherwise use a **predeclared computational outcome** and explicitly mark Joules/energy savings as unmeasured. Include base detector and optional secondary detector in total cost. Log human review separately.

Detector score calibration, worker-level correctness and risk-controlled/conformal statistics are separate. Check prerequisites, verified event counts, calibration leakage and acquisition exchangeability rather than asserting distribution-free guarantees.

## Paired statistics and repeatability

- Same-image/worker observations across arms; paired contrasts and uncertainty intervals; workers nested within frames; known source families clustered where supported. `SOURCE_UNKNOWN` groups cannot be assumed independent; conduct exclusions/sensitivity.
- Repeat timing/memory/energy measurement after warm-up with balanced order and fixed hardware, preprocessing, software/driver, batch size, randomization and sensor scope. Hardware repeats are **not independent workers**; do not inflate sample size.
- Preregister primary contrast, primary endpoint/fallback, margin and multiplicity strategy, number of hardware repeats, missing/ambiguous handling, one-time Test freeze. Rare-label support prevents broad unconditional claims.

## Audit trail, privacy and responsible release

Per-case log with pseudonymous IDs, frozen-split/source-group/sha pointers, exact weight/config/environment versions, boxes/classes/confidence, wearer/equipment states, association candidates and margin, task-policy provenance, risk/uncertainty/review/XAI routing reasons, target perturbations and `LOST/AMBIGUOUS`, alerts/abstentions, queue completion status, costs, measured-or-simulated tags, and raw energy provenance if present. Keep image files, identity/provenance maps, ground-truth adjudication and runtime logs in separate permission-controlled stores; never feed post-hoc labels into routing. **Author's Q40 declaration (17 November 2026):** The researcher affirms full ownership and disposition rights over the **primary Y-PPE research data**. Record this as author self-attestation, not independently verified chain of title. Original author-created images/annotations may be slated for public release at their discretion, subject to identifiable-person privacy requirements; distinguish any externally sourced or provenance-unknown photos before broader redistribution. The fine-tuned/original RF-DETR checkpoint and Roboflow service artifacts may carry platform-specific distribution conditions separate from image-data ownership. **Q41 selected a comprehensive, reproducible research package (option D):** rights-cleared Y-PPE data and annotations, source code, frozen configuration/environment requirements, SHA-256 data/model manifests, access-controlled or pseudonymized audit and experiment logs, automated tests, Colab notebooks, and scripts to regenerate tables/figures from genuine results. Maintain a public/restricted manifest and publication checklist. Exact model weights may be redistributed only where license/hosting terms allow; otherwise document authorized retrieval. Data export, checkpoint access, real evaluation, energy measurement and release status must each be verified separately. No public release has yet occurred. **No dataset, image or weight release has been performed by this protocol edit.**

## Evidence and open gates (15 November 2026)

**Verified:** Clean17 archive checksum and extraction; earlier fixed split integrity, explicit candidate source triage; 30-image analyst-only pilot; 56 synthetic code tests; original Roboflow 17-class model project/version/training metadata; issuance of authorized temporary original weights download URL.

**Open:** Local bytes/loader/17-class weight inspection; real model-specific explanations; usable worker/task-policy reference; feasible rare-event risk bounds; source-family uncertainty quantification; actual metered electrical power; locked settings/comparator; executed full matched baseline and ablation evaluation. No XAI/risk/energy superiority result is available.

Related manuscript: `research/seer-ppe/MANUSCRIPT_MASTER.md`. Original dataset integrity report: `cross_domain_reliability/stage2_data_audit/results/Y-PPE_v2_clean_stage2_closure_2026-09-20.md`.
