# SEER-PPE — Worker/PPE human-reference protocol v0.1
**Date:** 2026-11-17 (Asia/Aden)  
**Status:** Protocol ready; **human adjudication NOT STARTED**. Development-only, single-curator reference; not a scientific association accuracy result.

## Purpose and immutable boundaries
Create a *person-level* visual reference independent of SEER-PPE detector predictions, separating (a) visible persons, (b) physical PPE items or absence evidence, (c) item-to-person ownership, (d) worker–PPE visual state, and (e) applicability of a specific documented task/site PPE rule. Original 17-class model `altayyar-0oflt-lafos-qqauz/2`, historical labels, original project splits, training weights, baseline Workflows, and deployments are frozen. Only a **separate Roboflow Workflow Eval Dataset** and research documentation may be written for this phase.

- Workspace/project: `softyyemen/altayyar-0oflt-lafos-qqauz`.
- Candidate Workflow v0.2: `61llCTFuQ4Aq4goQ9HiP` (21 native, read-only blocks; `ASSOCIATION_UNKNOWN` and `POLICY_UNKNOWN` are **constants**).
- Roboflow Eval Dataset ID: `9c2679df-f2b9-4e25-b88d-9c6ac9033a95`; label: `SEER-PPE worker association reference — Train pilot v0.1`.
- All initial cases have `groundTruthState=incomplete` and `groundTruth={}`. No ground-truth arrays should be interpreted as reviewed zero counts before human review.

## Image-level intake
For each case record: workspace image ID, filename, original split, dimensions, image/source-family identifier if known, rights/privacy assessment (`CLEARED`, `RESTRICTED`, `UNREVIEWED`), any suspected same-session / near-duplicate group, task/site context or `UNKNOWN`, curator ID/role, review date, review pass, and evidence notes. **Never publish image pixels, identifiable personal details, or direct media URLs to the public repository without rights/privacy clearance.** Train cases are for protocol development; neither validation calibration nor independent testing.

## Visual person inventory (including missed persons)
Inspect the **actual image**, ideally without viewing model outputs first. Enumerate *all discernible people*, including partially occluded, truncated, or missed by `Persons` detections. Assign stable within-image IDs `P001`, `P002`, ... in left-to-right centroid order with top-to-bottom tie-break. Record normalized `xyxy` in [0,1] for the visible/full estimated person region and flag whether it was estimated, visibility/occlusion, crop truncation, and annotator uncertainty. A model or dataset box is a **candidate**, never a human-confirmed inventory. Record visually indeterminate human-like figures separately as unresolved; do not silently discard them. An image with zero detector `Persons` is not proof of zero actual persons.

## PPE item inventory and visible-state evidence
For each visible item, give `E001`, `E002`, ...; equipment kind (hard_hat, safety_vest, face_mask, goggles, glove, safety_boot, etc.), original detection class if any, normalized box, visible body-region support and uncertainty, and whether it is a positive PPE item or only an absence-like detector marker. Pair-sided items (gloves/boots) need side/visibility information where possible. `Soft Hat` must **not** be silently interpreted as an approved hard hat. Neither `Pants` nor `No Safety Attire` is a policy-compliance decision.

For each **person × relevant PPE type** write `PRESENT`, `ABSENT`, or `UNKNOWN`:
- `PRESENT`: visually confirmed equipment on that person and sufficiently supported association.
- `ABSENT`: the pertinent anatomical region is clearly visible and the PPE truly not worn, with human evidence. Non-detection and a `No …` detector class **alone are insufficient**.
- `UNKNOWN`: occluded, too small, out-of-frame, ambiguous attachment, uninterpretable, or unable to verify visually. Keep left/right and partial visibility notes.
These visual states are **not** compliance states.

## Association adjudication
Each PPE item `E###` receives an independent person-association record:
- `MATCHED`: single visually supported wearer `P###` (not merely max IoU), with explainable head/torso/hand/foot evidence; `person_id` must exist.
- `AMBIGUOUS`: at least two plausible person IDs or a real tie with no convincing discriminatory visual evidence; record the alternative IDs; do not auto-break ties.
- `UNKNOWN`: person missing/unresolved, item occluded or detached, irrelevant crop, or no defensible association; record why.

Do not call a unique geometric overlap a verified `MATCHED`. Association by containment/center overlap is a **proposal**; a top-two score margin, PPE-specific anatomical regions and a robust one-to-many/one-to-one assignment rule are **algorithmic candidates to be developed and checked**. Do not conflate `AMBIGUOUS` (multiple viable candidates) with `UNKNOWN` (insufficient/absent support). Each record must include `basis`, `uncertainty_reason`, and reviewer evidence. Retain orphan PPE items without forcing a wearer. Multiple distinct gloves/boots can attach to the same person; a single item cannot be confidently assigned to two people.

## Task/site PPE policy is a separate axis
For a person and PPE type, record `REQUIRED`, `NOT_REQUIRED` or `POLICY_UNKNOWN`. `REQUIRED` and `NOT_REQUIRED` require documented worksite/task/time/role mandate, issuer or authoritative document, version/date, and applicability justification; a hard hat appearing in a picture does not establish a mandate. Without policy evidence, `POLICY_UNKNOWN`. A possible `VIOLATION` reference would require both `REQUIRED` **and** human-verified `ABSENT` for the same worker/PPE under verified applicable context; unresolved association or coverage must remain review-only. **This phase creates no compliance/violation labels.**

## Pilot sample (all TRAIN; initial labels unreviewed)
| Case | Workspace image ID | Filename | Original annotated Persons count | Review challenge |
|---|---|---|---:|---|
| A | `0jRe8fpRDE5fLgAJrYvT` | `image_604.jpg` | 1 | Candidate unique-wearer control |
| B | `0xxsYWiz1FZBYERolu4z` | `000760.jpg` | 2 | Candidate multiple-wearer/tie challenge |
| C | `0jGu9euJp1MbvkLtfBcs` | `Kathiah Gets a Chance03.jpg` | 4 | Candidate crowded/coverage challenge |
| D | `0oVmRAxL0SM1PWqZCNyM` | `h1.jpg` | 0 | No *annotated* person; coverage-unknown control |

*Counts reflect old dataset geometry only, not audited ground truth. Candidate challenge tags are not human-confirmed `MATCHED`/`AMBIGUOUS`/`UNKNOWN` labels.*

## Roboflow Eval data fields
The separate Eval Dataset declares `InferenceImage` input `image` and six ground-truth fields: `persons[]`, `ppe_items[]`, `worker_ppe_states[]`, `associations[]`, `task_mandates[]`, and `source_review`. See `WORKER_ASSOCIATION_REFERENCE_SCHEMA_V01.json` for a reference format and value constraints. The typed field array is a storage contract, **not** an existing evaluator for per-item attribution. An Eval Run must **not** be presented as valid until labels are reviewed, a supported evaluator/output binding is specified and validated, and relevant cases are complete.

## Single-curator process and QA
1. Open source image in Roboflow; review rights/source context and visually inventory all people blind to predictions, then all visible PPE.
2. Human-label item ownership and worker × PPE visual states with evidence; unknowns/occlusions explicitly recorded.
3. Separately inspect applicable, **documented** mandate; leave `POLICY_UNKNOWN` when missing.
4. Check referential integrity: person IDs exist, item IDs exist, allowed codes, coordinates in [0,1], no invalid `MATCHED` target; do a second self-review pass with changed decision log.
5. Mark Eval Case `complete` only when it is actually adjudicated; otherwise retain `incomplete`. The single curator cannot claim inter-rater agreement or independent blind consensus.

## Future evaluation gates (not achieved here)
- On Train: build/revise a deterministic candidate assignment algorithm with per-PPE/body-region evidence; retain abstentions. Report debug examples and disagreements, never safety efficacy.
- On Validation: preregister then calibrate score/ambiguity margins and review policy; account for source-family duplicates and rights restrictions; report eligible-item association precision/recall/F1, matched coverage, ambiguous/unknown rates, reviewer burden, and false-clearance rate **with explicit denominators**. No arbitrary pass threshold is currently approved.
- On historical Test: only one clearly caveated internal check after all rules are frozen; prior exposure means not an independent untouched test.
- No false scientific claim of real-world violations, explanation faithfulness, energy in joules, or publication readiness. `ASSOCIATION_UNKNOWN` from v0.2 is constant, not an algorithmic prediction.
