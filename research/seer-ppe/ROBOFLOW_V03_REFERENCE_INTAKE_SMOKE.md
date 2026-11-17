# SEER-PPE Roboflow Train reference intake and conservative routing smoke test — v0.3 staging
**Date:** 2026-11-17 (Asia/Aden)  
**Status:** `PASS` for separate Eval Dataset creation, four incomplete cases and v0.2 engineering runs; `NOT_RUN` for human adjudication, dynamic `MATCHED`/`AMBIGUOUS`, Validation calibration and scientific metrics.

## Platform state, provenance and side effects
- Roboflow workspace `softyyemen`; frozen original 17-class model `altayyar-0oflt-lafos-qqauz/2` and 21-block `SEER-PPE Conservative Review Cues v0.2`, ID `61llCTFuQ4Aq4goQ9HiP`, unchanged.
- New **separate** Eval Dataset `SEER-PPE worker association reference — Train pilot v0.1`, ID `9c2679df-f2b9-4e25-b88d-9c6ac9033a95`, URL slug `seer-ppe-worker-association-reference-train-pilot-v0-1`. Input `image: InferenceImage`; ground truth contracts: persons, ppe_items, worker_ppe_states, associations, task_mandates arrays and source_review label.
- Created 4 **Train** Eval Cases using existing Roboflow workspace source images. **Every case remains `groundTruthState=incomplete` with `groundTruth={}`.** This means no human labels or measured association accuracy exist.
- The saved v0.2 Workflow was independently re-read and validated `status=ok` before running. Block-type audit: detection, filtering, geometric overlap/analysis, length, expression, visualizations only. No training, dataset uploader, webhook, sink, external provider or annotation-writing block. Tests executed by `workflow_specs_run` directly on the saved specification, not the original Base Workflow with an Active Learning uploader.
- Existing project source images, original annotations, splits, trained weights and baseline Workflows were **not modified**. No Eval Runs, Validation images or Test images were used.

## New / expanded Train engineering observations
| Image | Workspace ID | Annotated Persons in original geometry | Returned persons | Raw detector boxes | PPE/absence-like candidates | Geometric pair records | Low-score routing | Inference ID |
|---|---|---:|---:|---:|---:|---:|---|---|
| `image_604.jpg` | `0jRe8fpRDE5fLgAJrYvT` | 1 | 1 | 5 | 4 | 4 | `NO_LOW_SCORE_CANDIDATES_RETURNED` | `cc88d0a2-6b6d-409c-b2d2-fc44c36cff1c` |
| `000760.jpg` | `0xxsYWiz1FZBYERolu4z` | 2 | 2 | 16 | 14 | 18 | `LOW_CONFIDENCE_NEEDS_REVIEW` | `06e315e4-bd4d-4030-b979-6125232fd37b` |
| `Kathiah Gets a Chance03.jpg` | `0jGu9euJp1MbvkLtfBcs` | 4 | 4 | 29 | 25 | 26 | `LOW_CONFIDENCE_NEEDS_REVIEW` | `48d1a139-86cc-4612-85a8-e16a65dba10a` |
| `h1.jpg` | `0oVmRAxL0SM1PWqZCNyM` | 0 | 0 | not reported here | not reported here | 0 | `NO_LOW_SCORE_CANDIDATES_RETURNED` | `20b164c3-386c-4639-a23d-0e8bceb98a30` |

All four engineering runs returned `association_status_constant=ASSOCIATION_UNKNOWN` and `policy_status_constant=POLICY_UNKNOWN`; the first three returned `PERSON_CANDIDATES_DETECTED_COVERAGE_UNVERIFIED`, and `h1.jpg` returned `PERSON_COVERAGE_UNKNOWN`. The latter says **no person was detected**, not that no person actually exists. In `000760.jpg`, 18 pairs across 14 PPE/absence-like candidate boxes and two person detections show why pairwise geometry cannot be assumed unique or correct. In `image_604.jpg`, one person and four geometric pairs also do not independently prove correct wearer identification.

## Explicitly NOT proven
- No actual `MATCHED` or `AMBIGUOUS` *per-item algorithmic output* exists in v0.2. Every `ASSOCIATION_UNKNOWN` value is a deliberate constant.
- No human person inventory, confirmed item ownership or visually checked `PRESENT/ABSENT/UNKNOWN` rows have yet been saved. Old image annotations are detection labels, **not** human per-worker reference.
- No documented worksite/task PPE mandate. No worker `COMPLIANT` or `VIOLATION` decision.
- No Validation threshold selection, independent Test result, association precision/recall/F1, false-clearance rate, XAI faithfulness, or measured joules.

## Research gate for the next iteration
1. Single-curator visual review of all four source images with the separate protocol `WORKER_ASSOCIATION_REFERENCE_PROTOCOL_V01.md` and JSON schema `WORKER_ASSOCIATION_REFERENCE_SCHEMA_V01.json`.
2. Before marking a case `complete`, record all people (including potentially missed by detector), item-to-person attribution, per-worker PPE status and source/task-policy uncertainty. Keep unknown if not verifiable; never infer visual absence from non-detection.
3. Implement a **separate** v0.3 algorithm that produces *candidate* per-item ownership with justified `MATCHED` / `AMBIGUOUS` / `UNKNOWN`, if native blocks support exact criteria; otherwise record an implementation gap. Do not edit original model or v0.2.
4. Design Eval Spec and BindingSet only once the human-reference contract and v0.3 output shape agree; Validate and freeze thresholds on Validation with clear denominators. The historical Test is not a pristine independent holdout.
