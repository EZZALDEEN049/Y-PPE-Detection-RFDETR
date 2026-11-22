# SEER-PPE — experimental master protocol v0.8 (V32 image-level detection/XAI scope amendment)

**Revised:** 22 November 2026 (V32 scope amendment). **Status:** working, *not preregistered*, evidence-bounded protocol. Historical Y-PPE Test was exposed during earlier dataset/model refinement. No newly independent holdout, worker-safety superiority result, externally validated explanation-faithfulness result or joules measurement is claimed.

**V32 scope amendment — 22 November 2026 (supersedes conflicting worker-safety requirements below):** The current thesis paper is limited to image-level PPE object detection, target-specific black-box perturbation analysis, and selective explanation/inspection prioritization. Person–PPE gold, worker/task mandates, compliance/violation labels, worker false-clearance, actual review efficacy, acquisition-independent generalization, and physical Joules are **outside the current endpoint and are not completion blockers**. Historical worker-level procedures and pilot artifacts remain in the protocol for traceability/future work only. Current XAI outputs establish perturbation sensitivity, not externally validated causal faithfulness. See [V32 scope decision](V32_IMAGE_LEVEL_DETECTION_XAI_SCOPE_DECISION_2026-11-22.md).

## Research question and objective

Can the unchanged 17-class RF-DETR Small detector be evaluated reproducibly on the author-curated Y-PPE image corpus, and can target-specific black-box perturbation and selective explanation routing characterize how selected PPE detections respond to removal or isolation of their visual regions under a fixed XAI-call budget?

**Primary endpoints:** exact-class image-level precision/recall/F1; class-wise support; target detection retention and confidence response under occlusion/deletion/insertion; progressive deletion/insertion AUC; and selected-target overlap/call counts for A5/A6-style policies.

**Scope exclusions:** this study does not estimate worker-level compliance, person-to-PPE ownership, task/site PPE mandates, confirmed violations, false-clearance risk, actual human-review efficacy, external/acquisition-independent generalization or electrical energy. Review is a request/priority state only. Hosted request round-trip is not pure model latency; call counts are not Joules.

## Fixed source and checkpoint boundaries

- Use existing **17-class Y-PPE** images only. Historical raw: 2,327 images, 16,520 labels, train/valid/test 1,625/468/234. Roboflow augmented version 2: 5,577 images 4,875/468/234; finished original **RF-DETR Small** model ID `softyyemen/altayyar-0oflt-lafos-qqauz/2` (historic mAP@50 96.22%, **prior work only**). Version 3 is the unaugmented source, not assumed a separately trained model.
- **Clean17** frozen derivative: 2,288 images, 16,300 labels, splits 1,595/459/234; private ZIP SHA256 `d47d9676b785a847ef1bcb8a871574815b0b67b967f9107680fb0b85b1a52d61`. Full archive extraction verified, not a new acquisition-independent dataset.
- `Y_RFDETR_s17` (seed 17) checkpoint is **9-class h9**, not 17-class original. Roboflow connector issued short-lived authorized original-version weights URL; raw weight download, exact checkpoint SHA/class-head inspection, local inference and gradient access remain OPEN.
- **Roboflow-only operational constraint (author update, 17 Nov 2026):** reuse the finished original hosted RF-DETR Small 17-class model without retraining, with direct Roboflow prediction on permitted Train images and frozen server-side parameters. Compare repeated Roboflow outputs as a hosted reproducibility check; a Colab run or local checkpoint is **not** a prerequisite. Hosted network/API time must not be represented as electrical joules.

## Source independence and split control

- Use Train for implementation and exploratory work; validation examples not already used for SEER tuning for calibration; lock all routing weights, selection decisions, comparator, analysis scripts, fallback endpoint and budget before **one post-freeze historical-Test internal assessment**.
- Historical Test was repeatedly viewed/used in earlier Y-PPE development, and three historical smoke inputs were SEER-development exposed. Do **not** call it untouched, independent, external, blinded or acquisition-independent. Do not tune against its final results; report prior exposure.
- The author describes the corpus as a **multi-project, multi-location Yemeni field-image collection** assembled in the context of civil-society organization projects; the original image selection/review and dataset curation were completed during preparation. A named worksite/project ID for every image is **not required** for the internal image-level detection question and must not be invented. Preserve frozen files, splits and annotations; do not repeat full-corpus review merely to populate site names. The absence of a complete per-image site/session register must be disclosed, and `SOURCE_UNKNOWN` must not be relabelled independent. The author-curated multi-project corpus is not a documented probability sample of Yemeni worksites; do not estimate national prevalence or claim independent site-level generalization from project diversity alone.
- Maintain a separate leakage audit manifest only for source evidence that is supported: `image_id, split, sha256, provenance_family_if_supported, possible_scene_group, SOURCE_UNKNOWN, review_basis, suspected_leakage`. Existing stage-2 exact duplicates and known video/source grouping conflicts were corrected. Seven small-dHash cross-split pairs were visually judged different objects/images by a single analyst, not independently verified acquisition. Continue to hold credible exact duplicates, derivatives, shared scenes or shared sites across splits. Report M0/M1/M2 overlap-risk sensitivity; never claim complete acquisition-independent source families or site-independent generalization.

## Reference construction and status semantics

- Use the existing author-curated object-class and bounding-box annotations as the single-curator reference for the image-level detection endpoint, with exact Source-ID joins and a frozen same-class IoU matching rule.
- Report image-level TP/FP/FN, precision, recall and F1, plus class-wise support and source-overlap sensitivity cohorts M0/M1/M2. Keep model-assisted annotation provenance and known label discrepancies disclosed.
- For XAI targets, freeze the original detection identity, class, box and baseline confidence. Preserve `MATCHED`, `LOST` and `AMBIGUOUS` as distinct outcomes after perturbation; never infer a missing worker state from a detector miss.
- The archived Person–PPE pilot is exploratory only. It is not completed into worker-level gold, and no task/site policy is inferred. No compliance or violation label is produced under this protocol.

## V18 owner-approved single-curator annotation reference policy (21 November 2026)

The original image collector/selector/classifier has explicitly confirmed that all images were reviewed and checked before/during/after dataset creation. **Accept original author-curated image/object annotations as the primary reference**, and **do not impose another human annotator, duplicate manual relabeling or repeated visual reinspection as an automatic prerequisite**. See [V18 author-curator policy](AUTHOR_CURATOR_REFERENCE_POLICY_2026-11-21_V18.md).

**Endpoint-specific evidence:** original annotated class/box labels may be used for scoped *historical internal object-detection evaluation*, if truly aligned with exact source image IDs and fixed model predictions. Individual Person–PPE states/owner links already recorded remain valid single-curator evidence; missing cells are **NOT_RECORDED**, not automatically absent/present/unknown. Occupational compliance violations require independently sourced applicable PPE task mandates and verified visual states. External-source independence, independent reviewer agreement and unbiased unseen-Test claims are not implied by this author statement. Site-family unknowns and historical test exposure remain explicitly disclosed, and strict independent-source worker-safety scoring remains blocked until its distinct conditions are met.

For the internal detection endpoint **a second reviewer and a newly signed person-level overlay for every image are not absolute requirements**. The strict V15 gate pertains to claims of fully verified worker-level safety and certified acquisition independence, not to ordinary reproduction of the author's original object-detection labels. The data owner must not be asked to redo the previously completed general image review.

## Evidence routing and image-level invariants

- Route `BASIC` for a retained detector output, `EXPLAIN` for a selected detection requiring perturbation-based analysis, and `REVIEW` for a request to visually inspect an uncertain or priority image region.
- Routing inputs may include detector confidence, predicted class, box area/visibility, uncertainty proxies and remaining XAI-call budget. Do not use reference/test labels, worker compliance assumptions or task/site mandates as routing inputs.
- A review request is not a completed review, confirmed violation, safety clearance or protective intervention. The system must not emit worker-level `COMPLIANT` or `VIOLATION` conclusions.
- Preserve detector identity, original image/split and model parameters; report missed/ambiguous target matches explicitly. No retraining, source-label edits or protected-Test tuning.

## Target-specific perturbation sensitivity

- Use original target class/box identity and predeclared black-box perturbations: Gaussian occlusion, black-fill deletion, target-only insertion and progressive grid-based deletion/insertion.
- Re-predict on each perturbed image and match the same class/instance using the frozen spatial/IoU rule. Log `MATCHED`, `LOST` and `AMBIGUOUS` separately.
- Include random and inverse-saliency controls where supported. Report deletion/insertion curves and trapezoidal AUC, but interpret them as perturbation sensitivity only.
- Test robustness to grid resolution, mask/background fill, blur choices and target selection. An externally grounded explanation reference is required before claiming causal explanation faithfulness.
- Gradient methods remain outside the current hosted-only evidence unless the exact original checkpoint and differentiable implementation are independently verified.

## Experimental arms, comparator and ablations

- Compare A0 detector-only, A1 Explain-All, A2 confidence-only, A3 budget-only, A5 and A6 selective explanation/target-prioritization policies.
- Match target and XAI-call budgets where feasible; report selected-target overlap, unmatched slots, detection correctness where reference matching exists, and actual model-call counts.
- Current A5/A6 evidence is small, development-exposed and has shared target slots. It is descriptive; do not claim statistical superiority or worker-safety benefit.
- A4 safety-guard-off remains historical design documentation and is not a current study arm.

## Calibration and inference

Freeze image/target selection, confidence thresholds, perturbation settings, AUC computation and comparator policy before each planned evaluation. Use Validation/development material only for selection and sensitivity checks; disclose historical exposure and source overlap. Do not access protected Test for tuning. No worker-level safety gate, false-clearance threshold or task-policy calibration is part of the V32 endpoint.

Efficiency is reported as actual XAI/model-call counts and hosted request round-trip where available. Do not infer Joules, memory use, internal detector latency or financial cost from request timing or call counts.

## Paired statistics and repeatability

- Use paired same-image/target contrasts where policies share eligible targets; report target overlap and the effective number of unique images/targets.
- Cluster curve/target observations by source image where appropriate; avoid treating multiple grid cells or perturbation points as independent images.
- Report descriptive values and uncertainty transparently; do not overstate A5/A6 differences from small overlapping samples.
- Maintain M0/M1/M2 source-overlap sensitivity and disclose that unflagged sources are not thereby proven independent.
- Hosted timing repeats characterize request round-trip only, not detector-only latency or energy.

## Audit trail, privacy and responsible release

Per-case log with pseudonymous IDs, frozen-split/source-group/sha pointers, exact weight/config/environment versions, boxes/classes/confidence, wearer/equipment states, association candidates and margin, task-policy provenance, risk/uncertainty/review/XAI routing reasons, target perturbations and `LOST/AMBIGUOUS`, alerts/abstentions, queue completion status, costs, measured-or-simulated tags, and raw energy provenance if present. Keep image files, identity/provenance maps, ground-truth adjudication and runtime logs in separate permission-controlled stores; never feed post-hoc labels into routing. **Author's Q40 declaration (17 November 2026):** The researcher affirms full ownership and disposition rights over the **primary Y-PPE research data**. Record this as author self-attestation, not independently verified chain of title. Original author-created images/annotations may be slated for public release at their discretion, subject to identifiable-person privacy requirements; distinguish any externally sourced or provenance-unknown photos before broader redistribution. The fine-tuned/original RF-DETR checkpoint and Roboflow service artifacts may carry platform-specific distribution conditions separate from image-data ownership. **Q41 selected a comprehensive, reproducible research package (option D):** rights-cleared Y-PPE data and annotations, source code, frozen configuration/environment requirements, SHA-256 data/model manifests, access-controlled or pseudonymized audit and experiment logs, automated tests, Colab notebooks, and scripts to regenerate tables/figures from genuine results. Maintain a public/restricted manifest and publication checklist. Exact model weights may be redistributed only where license/hosting terms allow; otherwise document authorized retrieval. Data export, checkpoint access, real evaluation, energy measurement and release status must each be verified separately. No public release has yet occurred. **No dataset, image or weight release has been performed by this protocol edit.**

## Evidence and open gates — V32 scope

**Verified:** Clean17 integrity and source mapping; current original-source 459-image detection evaluation; V27–V29 actual perturbation and hosted timing; V30 progressive black-box curves, 60 AUCs and independent numeric/source-hash audit; aggregate multi-project provenance decision.

**Open within scope:** explanation-perturbation robustness; a stronger and better-powered matched-budget A5/A6 target-selection comparison; final table/figure reconciliation; complete literature/DOI verification; editable manuscript export.

**Outside scope and not blocking:** worker-level Person–PPE gold, task/site mandates, compliance/violation labels, actual human-review efficacy, independent acquisition cohort, local gradient access, process memory and physical Joule measurement. The current paper must not imply these were measured.

Related manuscript: `research/seer-ppe/MANUSCRIPT_MASTER.md`.

## Q42 — Staged reproducibility verification (author-approved; not yet executed)

The author selected option D, subsequently amended to **Roboflow-only execution**. Require: (R1) frozen Roboflow project/version/model ID, data/split metadata, any available server-side version fingerprints and recorded parameters (weights SHA only if independently accessible without an unwanted local run); (R2) versioned checks on output schema and saved prediction/annotation identity, with software tests where supported; (R3) repeat hosted `models_infer` on preselected Train cases and compare class/box/score within fixed tolerances, logging response engine/model details; (R4) repeat genuinely executable Roboflow-native Workflow/Evals/target perturbation/baseline components **only after permission and capability checks**, record call counts and response times but not electrical joules; (R5) regenerate manuscript tables and figures only from genuine exported or logged results and verify all summaries. Each gate logs `PASS`, `FAIL` or `NOT_RUN` plus an explicit artifact/version/environment and reproducibility failure reason. GPU numerical outputs may vary within stated bounds; runtime, energy and queue simulation require their own validity and statistical criteria, not an inappropriate exact equality check. Never claim scientific replication from synthetic unit tests alone or report successful reproduction of unexecuted research experiments. Q43 will specify how Python, PyTorch, RF-DETR, CUDA/driver, Colab image, seeds and deterministic settings will be captured and restored.


## Binding execution constraint — owner instruction, 17 November 2026

The owner states the existing Y-PPE/RF-DETR training took approximately three months and **must be preserved; no retraining from scratch, new training, Colab requirement or alternate simulation platform is authorized**. SEER-PPE is strictly a post-training research layer over original, already trained `altayyar-0oflt-lafos-qqauz/2`; all planned computation/simulation uses **Roboflow itself**, where actually supported. Older references in this draft to a mandatory Colab local load or independent original checkpoint should be read as superseded for the current execution plan. Do not require the owner to upload weights/dataset just to repeat preexisting results.

**Live platform capability audit:** model hosted inference and dataset/annotation read checks PASS; existing Workflow catalog includes `detections_filter`, `per_class_confidence_filter`, `overlap`, `continue_if`, `switch_case`, blur visualization, bbox/heatmap visualizations, trackers and aggregator/event blocks. The `heatmap_visualization` block depicts detection density, not verified Grad-CAM or an instance-faithful saliency map. Person–PPE overlap is a *candidate heuristic*, not certified person-to-PPE assignment; compute explicit ambiguity states. All XAI Occlusion/Deletion/Insertion, automated safe multi-image perturbations and paired baseline experiments are **capability/permissions contingent**; validation and trial must precede any efficacy assertion. RF-DETR gradient internal access and genuine power/joule readings are **not confirmed by hosted inference APIs** and remain unavailable claims under the strict platform-only constraint unless Roboflow provides a verified native alternative. Record network and hosted timings as hosted response times, not electrical usage.

**Permissions:** connected Roboflow account currently lacks `Manage Workflows` for new workflow authoring and `view_workflow_evals` for Eval tools; annotation-board listing and deployment inspection also failed access checks. Existing Base Workflow has a `roboflow_dataset_upload@v2` Active Learning side-effect and therefore must NOT be run for read-only experiments. Use direct `models_infer` until a separate write-free research Workflow can be created with appropriate workspace rights. Do not alter weights, source annotations, splits, versioned datasets, Workflows, deployment or Active Learning without explicit authorization. If a method cannot be scientifically executed inside Roboflow, disclose the limitation and seek a user decision on *method scope*, not an automatic switch of platform.


## Authenticated safe baseline Workflow — actual execution 17 November 2026

Owner-linked Roboflow Admin reconnection restored access: `workflow_evals_capabilities` reported read/write/run/export true. A new validated and independently read-back, separate, write-free Workflow `SEER-PPE Research Safe Inference` (ID `9ioiyoi0xE7JNAVjd2pf`, slug `seer-ppe-research-safe-inference-1794871166931`) uses the exact original 17-class RF-DETR `altayyar-0oflt-lafos-qqauz/2`, disables active learning and only adds box/label visualization. A server-side Workflow run on one permitted Train image `image_604.jpg`, confidence .4 and IoU .3, returned the same five predicted classes as prior original model hosted inference, along with raw boxes/scores, model ID, inference ID and an annotated image. This is a **verified technical baseline execution**, not SEER routing, validated XAI, measured safety benefit or Test result. No original dataset, annotation, weights, training or earlier Workflow changed. Current experimental plan remains platform-only, no retraining.


## SEER-PPE Routing Prototype v0.1 — native implementation and boundaries (17 November 2026)

Roboflow access was restored through the owner's Admin account. In a **new separate read-only draft Workflow**, the native detector `altayyar-0oflt-lafos-qqauz/2` emits all *post-detector-threshold* predictions at 0.20 confidence with 0.30 IoU and `disable_active_learning:true`; confidence filters isolate `>=0.60` and `[0.20,0.60)` categories; dedicated filters expose `Persons`, PPE-category boxes and their union; `roboflow_core/overlap@v1` with `Center Overlap` identifies geometrically overlapping PPE-category candidates; annotation-only visualizations expose raw and overlap pictures. Original project/baseline and other resources are unchanged. Workflow `QYzcGMCrJ9uwLmkAfsfF`, slug `seer-ppe-routing-prototype-v01-1794871362276`, editor https://app.roboflow.com/softyyemen/workflows/edit/seer-ppe-routing-prototype-v01-1794871362276 .

On one **Train engineering smoke case** `Kathiah Gets a Chance03.jpg`, the exact saved specification executed using Roboflow hosted inference. Observed model predictions: raw=29, high-confidence=26, lower-confidence=3, persons=4, PPE-category=25, person-center-overlap PPE-category=24. These data are not compliance ground truth, model generalization estimates or calibrated risk. No independent worker assignment is established, no uniquely unassociated set or automated review reason codes are implemented, and no actual review transaction occurred. A person box missed by the detector is not covered by overlap logic. Next gates: build human-reviewed worker reference, validate policy-unknown and ambiguous states, predeclare robust person-instance matching rules, compare constrained alternatives and calibrate thresholds ONLY on Validation; use historical development-exposed Test once postfreeze as internal sensitivity evaluation. XAI, reviews, Joules and safety gains remain **not tested**. A detection heatmap is not gradient explanation.


## V33-A evidence-bounded numeric amendment — 22 November 2026

V33-A reanalyzes the **already executed** V30 eight-image/ten-target 8×8 experiment. It recomputes all 60 original modified-pixel-area AUCs; calculates saliency-versus-random full and early-30%-area contrasts; checks nominal-vs-actual area differences, blurred-baseline response ratios and inverse-saliency complementary identities; and decomposes A5/A6 selection into six shared and four nonshared targets. The six balanced reallocations of the four unique targets are **conditional post-hoc descriptive checks**, not randomized-trial hypothesis tests. Only a single seeded random order per target exists in V30. A real 4×4 perturbation experiment has not yet run; [V33-B prospective protocol](V33_B_GRID4_PROSPECTIVE_PROTOCOL_2026-11-22.md) bounds it at 496 additional hosted inference calls and requires separate explicit authorization. No worker-level compliance or energy endpoint is introduced. Canonical [manuscript v0.33](MANUSCRIPT_MASTER.md) and [V33-A report](V33_A5_A6_NUMERIC_ROBUSTNESS_REPORT_2026-11-22.md) are the current references.
