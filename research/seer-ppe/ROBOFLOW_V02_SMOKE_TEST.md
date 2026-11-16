# SEER-PPE Roboflow conservative review cues v0.2 — implementation and Train smoke test

**Date:** 2026-11-17 | **Status:** `PASS` for schema validation + single-Train-image execution; `NOT_RUN` for calibrated validation, worker adjudication, old Test and scientific claims.

## Provenance and non-mutation contract

- Roboflow workspace: `softyyemen`.
- New, separate unpublished research Workflow: **SEER-PPE Conservative Review Cues v0.2**, ID `61llCTFuQ4Aq4goQ9HiP`, slug `seer-ppe-conservative-review-cues-v02-1794873200805`.
- Roboflow reference URL: https://app.roboflow.com/jKwqROZgEDNWeNDWEgqAnytu2ZC3/solutions/chat?workflowUrl=seer-ppe-conservative-review-cues-v02-1794873200805
- Frozen original trained 17-class model: `altayyar-0oflt-lafos-qqauz/2`; detector `roboflow_object_detection_model@v3`, confidence_mode=`custom`, custom_confidence=`0.20`, iou_threshold=`0.30`, disable_active_learning=`true`.
- Band threshold `0.60` is a provisional **engineering** choice; **not calibrated**. v0.1, original ALTAYYAR Base Workflow, dataset/splits/labels, trained weights and deployments were not modified.
- Independently fetched saved Workflow specification and validated it with `workflow_specs_validate` (`status:ok`). Audited **21 native blocks**; none was a dataset-upload, sink, webhook, persistent tracking, training, external provider or other data-writing step.

## What v0.2 computes

1. Retains all raw detections with class/confidence/box identities and model/inference provenance.
2. Separates high score (`>=0.60`) from low band (`[0.20,0.60)`) without assuming low scores signify absence.
3. Separates `Persons`, PPE/absence-like combined candidates, positive-class candidates and explicit negative/absence-marker *detections*.
4. Computes geometric center overlaps with persons; also emits `overlap_analysis@v1` pairwise geometry using minimum-overlap `0.10` between PPE candidates and detected persons.
5. Computes the count of detected persons and low-score detections. Conditional expressions produce image-level `PERSON_COVERAGE_UNKNOWN` when no person box was detected, otherwise `PERSON_CANDIDATES_DETECTED_COVERAGE_UNVERIFIED`; and `LOW_CONFIDENCE_NEEDS_REVIEW` when a low-score candidate exists, otherwise `NO_LOW_SCORE_CANDIDATES_RETURNED`.
6. Emits always-conservative `ASSOCIATION_UNKNOWN` and `POLICY_UNKNOWN` **constant** metadata. These are not visually inferred or independently reviewed status predictions.
7. Returns two annotated views, all intermediate detection groups, candidate pairwise geometry, image-level counts/review codes and provenance.

**Explicit non-capabilities:** No defensible unique per-worker PPE assignment; no PPE-specific head/torso/hand/foot association, no top-two assignment margin or computed `AMBIGUOUS`, no verified unmatched-item set, no exhaustive person coverage, no completed human queue, no known task/site PPE mandate, no per-worker `PRESENT/ABSENT/UNKNOWN` visual reference, no `COMPLIANT/VIOLATION` assessment, no XAI faithfulness and no electrical Joules. The pairwise geometric list **must not be interpreted as correct wearer assignment**; absence-marker *class detections* are not proof of true physical absence or of policy violation.

## Actual Roboflow-only engineering smoke test

- Source: existing **Train** image `Kathiah Gets a Chance03.jpg`, workspace image ID `0jGu9euJp1MbvkLtfBcs`, in project `softyyemen/altayyar-0oflt-lafos-qqauz`.
- Execution: `workflow_specs_run` with the saved read-back specification and source-image URL; the built-in model and native workflow ran remotely within Roboflow. Inference ID: `48d1a139-86cc-4612-85a8-e16a65dba10a`.
- Input dimensions: **2048 x 1365**.

| Engineering output | Observed |
| --- | ---: |
| Raw model detections at 0.20 | 29 |
| Persons detections | 4 |
| High-score detections >=0.60 | 26 |
| Low-score review candidates <0.60 | 3 |
| PPE/absence-like category boxes | 25 |
| Positive PPE/clothing-category boxes | 14 |
| Absence-marker-category detections | 11 |
| Boxes in center-overlap candidates | 24 |
| Pairwise geometric candidate records | 26 |

Actual returned codes: `person_coverage_review_code=PERSON_CANDIDATES_DETECTED_COVERAGE_UNVERIFIED`; `confidence_review_code=LOW_CONFIDENCE_NEEDS_REVIEW`; `association_status_constant=ASSOCIATION_UNKNOWN`; `policy_status_constant=POLICY_UNKNOWN`. Both annotated-image outputs were produced. No source-image pixel contents were added to this repository.

These are **raw detector and routing outputs**, not ground truth or verified worker-safety scores. The 26 pair records are not 26 uniquely confirmed person-PPE matches; the two geometric methods can have different multiplicities. The above is **one development-exposed Train image**, not a Validation calibration or independent Test result.

## Next preregistered gates

1. On Train, design a researcher reference for **all visible people**, including missed/occluded people, and a separate per-worker-per-PPE `PRESENT / ABSENT / UNKNOWN` visual status with association justification.
2. Record source/rights/identity-group status, site/task eligibility and documented mandate `REQUIRED / NOT_REQUIRED / POLICY_UNKNOWN`; only a truly verified mandate and confirmed absence can support a violation reference. A single researcher reviewer is not independent multi-rater consensus.
3. Evaluate unique association algorithms with normalized PPE-specific regions and pairwise margin on Train; unresolved ties remain `ASSOCIATION_UNKNOWN` / `AMBIGUOUS`. Do not artificially mark unreturned detections as absent.
4. Choose and freeze review thresholds on Validation only, subject to adequate support and false-clearance/review-burden analysis; retain old Test solely for a one-time clearly qualified internal evaluation after freeze.
5. If Roboflow native components cannot execute reliable per-worker matching or model-specific explanation fidelity, record the capability gap rather than fabricating the feature. No energy saving in Joules until physically metered.

**Research interpretation:** This passes a narrow software-platform execution milestone and explicitly does not pass any SEER-PPE risk-control, attribution-fidelity, worker-coverage, energy or publication-readiness gate.
