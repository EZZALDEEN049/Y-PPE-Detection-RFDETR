# SEER-PPE V14 — pre-freeze research design and Validation eligibility rules

**Status: PREREGISTRATION DRAFT / NOT FROZEN / NO SCIENTIFIC SCORING.** Model `altayyar-0oflt-lafos-qqauz/2` remains fixed and unchanged. The current historical Test has prior development exposure and is not treated as a fully independent unseen source-family Test. No Test images may be opened for further design.

## Unit and cohort

The unit of source-independence screening is the **original Source image with a human-evidenced acquisition/site/session family**; the selection cohort may contain only actually matched original→Clean17 Valid Source images and individually source-family-signed records that do not intersect Train source/site families. The original→Clean17 technical match is supported for all 459 exported Valid files, but the present independent-source **scoring population is zero**. Five old research holds and six additional technical strong-overlap sources are excluded from any candidate independent scientific scoring until a documented adjudication protocol explicitly resolves the conflict. Eighty-one more flagged source-lineage sources remain pending. Three hundred sixty-seven unflagged sources remain uncertified, not automatic controls. No original Train/Valid splits or labels are to be altered to implement these research controls.

## Fixed-model paired evaluation design

A future pre-specified cohort will use the same fixed RF-DETR predictions as input to **baseline** (raw model evidence without SEER-PPE policy) and **SEER overlay** (uncertainty, person–item association, abstention and prioritized review), with no original model retraining. The exact predictor version/weights provenance, thresholds, person/gear matching policy, confidence calibration, inference hardware and input preprocessing will be frozen by commit and signed approval before Validation evaluation. Do not fit thresholds from the Validation outcomes later used to report performance; training-only development probes may be used and must be labeled exploratory.

The reference unit for visible PPE is `(source_id, person_id, ppe_type)` with `PRESENT`, `ABSENT`, `UNKNOWN`. Prediction `UNKNOWN`/abstention is never conflated with absence. Approved visible reference states and item-owner links are researcher-specific evidence and separate from task-specific site PPE mandates. Person–item association scoring requires reviewed person and item correspondence; it must not be described as whole-detector mAP. Person coverage, including detector misses and human-signed zero-person scenes, is mandatory.

## Outcomes and analysis

Pre-specify: (1) known visual PPE coverage, retained-accuracy and PRESENT precision/recall per PPE type, including explicit human-unknown and predictor-abstention counts; (2) association pair precision/recall/F1 after independently verified correspondence; (3) false-safe/false-clearance only when an applicable task PPE mandate and actual human-certified violation reference are both evidenced, otherwise `NOT_ESTIMABLE`; (4) explanations only after pre-specified faithfulness checks with real perturbations on permitted data; (5) energy only from measured hardware power/energy instrumentation, never wall time multiplied by guessed TDP. Report all zero denominators as undefined, not zero.

For uncertainty estimates, avoid treating near-duplicate or same-site frames as independent replicates; group resampling by human-verified site/acquisition families when the independent evaluation population and group counts permit. Do not claim confidence intervals or generalization from the current exploratory Train A/B/C/D controls. Comparison of policy variants must be paired on identical frozen image/person cohorts and use an error taxonomy distinguishing false negatives from principled abstentions.

## Required proof before freeze

1. Signed source-family decisions for each chosen Valid Source ID, with Train-family crosscheck, acquisition/session evidence, and handling of the five prior holds and six technical overlap quarantines.
2. Original-to-Clean17 correspondence from [V13 photo content evidence](ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json), with no Test image bytes accessed.
3. Independently reviewed Validation human Person–PPE reference, complete worker coverage, unknown/occlusion states and task mandates. The saved Train-only pilot still lacks four B visual cells and D zero-person human signoff.
4. Fixed baseline and SEER policy, thresholds, matching, metrics and energy/XAI acquisition instructions; signed freeze file with Source IDs, protocol commit and reviewer details.
5. A read-only CI gate reporting `scoring_ready=true` only after evidence is fully verified, and a separate explicit research approval before any real Validation scoring.

[Current signed freeze (NOT_FROZEN)](VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json) · [V14 quarantine register](VALIDATION_TECHNICAL_QUARANTINE_V14.json) · [six prioritized source-review handoffs](VALIDATION_P0_HIGH_OVERLAP_HUMAN_REVIEW_V14.json) · [V11 executable Person–PPE scorer](PERSON_PPE_EXECUTABLE_EVALUATION_PROTOCOL_2026-11-21_V11.md).
