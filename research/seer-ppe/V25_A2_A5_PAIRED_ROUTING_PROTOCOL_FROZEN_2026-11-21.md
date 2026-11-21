# SEER-PPE V25 — pre-execution frozen paired offline routing protocol: A0 / A2 / A5

**Frozen 21 November 2026 before any V25 policy-score computation.** This file documents implementation parameters and inputs for a **real deterministic policy execution on saved real original RF-DETR Small predictions**, not new inference or a worker safety improvement trial. The original 17-class model is `altayyar-0oflt-lafos-qqauz/2`; no new model training, original image/annotation edits, Test use, physical energy instrumentation or human re-review are permitted.

## 1. Actual inputs and development-only population

- `ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json`: **four** already hosted-inferred Train photos A/B/C/D (51 fixed real model detection boxes), development pilot, known original source split `train`.
- `VALID_ORIGINAL_SOURCE_CURRENT_BBOX_MODEL_PILOT_V23.json`: **five** preselected previously development-exposed original Source `valid` photos (23 existing fixed-model real hosted detection boxes); original current ground-truth annotation boxes are present in this file for separate object-bbox testing but are **prohibited as routing inputs**. Source model remains the same. V23 identifiers and native image dimensions are mandatory.
- Total nine images and 74 already-saved real detector predictions. This is **not** new inference, representative Valid scoring, an independent acquisition cohort or 459-image current-reference assessment. The four Train and five Valid exploratory photos can be used only as an engineering test. Do not incorporate historical Test.

## 2. Original 17-class cue taxonomy — frozen

Treat **Persons** as detector person candidates, *not verified coverage*. Only the following **12 class names** are provisional typed PPE cues:
- Present-like object cues: `Hard Hat`, `Safety Vests`, `Safety Boots`, `Gloves`, `Goggles`, `Face Masks`;
- Negative-named detector cues: `No Hard Hat`, `No Safety Vest`, `No Safety Boots`, `No Gloves`, `No Face Mask`, `No Safety Attire`.

The remaining `Pants`, `Soft Hat`, `Animal`, and `Child` are context categories, **not PPE clearance decisions**. Negative-named cues are **not** verified equipment absence or genuine legal/site policy violations. Unobserved PPE classes are not automatically absent. Never infer worker-specific PPE state or site/task mandate from object classes alone.

## 3. Bounding box geometry and uncertainty

All predictions use original-image center-`x,y,width,height` pixel geometry and unchanged confidence threshold `≥0.20` and hosted overlap parameter `0.50`; every record must contain unique prediction IDs and exactly the original fixed model ID. For each cue and detected Person candidate, calculate the fraction `(cue center vertical offset inside person bbox) / person bbox height`. Candidate person associations require cue center **inside** Person bbox AND vertical-fraction in the fixed PPE-zone:
- head/eyes/face (`Hard Hat`, `No Hard Hat`, `Goggles`, `Face Masks`, `No Face Mask`) in **[0, 0.48]**;
- vest/attire (`Safety Vests`, `No Safety Vest`, `No Safety Attire`) in **[0.13, 0.87]**;
- gloves (`Gloves`, `No Gloves`) in **[0.25, 0.92]**;
- boots (`Safety Boots`, `No Safety Boots`) in **[0.62, 1.00]**.

Geometrically eligible Persons are ranked by the fraction of the cue box lying inside the Person box, then descending Person confidence, then lexicographic Person ID. A **single** eligible person produces `TENTATIVE_SINGLE`, **not** verified ownership. At least two candidates with top-two containment difference **≥0.15** yield `TENTATIVE_MARGIN`, otherwise `ASSOCIATION_AMBIGUOUS`. Zero candidates yield `ASSOCIATION_UNKNOWN`; zero detected persons is `PERSON_CANDIDATE_NOT_DETECTED`. *All geometry is tentative, not human-verified person/PPE links*. The strict overall person coverage gate is always `PERSON_COVERAGE_UNVERIFIED`.

Define uncertainty `u=1-confidence` and severity `s(class)` as **engineering selection proxies only**, not empirically validated occupational risk:
- `Hard Hat`/`No Hard Hat`: **0.12**;
- `Safety Boots`/`No Safety Boots`: **0.10**;
- `Safety Vests`/`No Safety Vest`/`No Safety Attire`: **0.08**;
- `Goggles`: **0.08**;
- `Gloves`/`No Gloves`: **0.04**;
- `Face Masks`/`No Face Mask`: **0.03**.

## 4. Arms and identical no-false-clearance constraints

- **A0 (raw fixed RF-DETR):** Record unchanged 74 detection cues, without additional policy classification, added explanation or a worker safety claim. A0 raw output is **not** a comparable worker-clearance decision policy.
- **A2 (confidence-only selective comparator):** For every image, rank its typed PPE cues descending by `u=1-confidence`, with ID as stable tie break. Its first cue is eligible for **one proposed explanation request and one proposed human review item**, if any cue exists. Neither request is actually run or dispatched. Does **not** treat high confidence as evidence of safe clearance.
- **A5 (SEER policy engineering implementation):** For every typed PPE cue, calculate `q = u + 0.26×negative-named + 0.24×unresolved-association + s(class)`. Unresolved association means `ASSOCIATION_AMBIGUOUS`, `ASSOCIATION_UNKNOWN` or `PERSON_CANDIDATE_NOT_DETECTED`. Use the top `q` (ties by ID) for **one proposed target-matched explanation request and one proposed human review item**. The risk proxy is a fixed **unvalidated priority heuristic**, not clinical/occupational risk estimation. When no cue exists, select none.
- **Matched budgets:** Maximum **one** proposed additional explanation *and* **one** proposed human-review item per image per policy (A2 and A5 have **exactly the same cap**); if a scene contains a cue, both use the single available slot. Proposed only; zero actual extra inference, zero actual XAI, zero human tasks dispatched, and no measured latency/energy savings. Compare selections, not pseudo resource savings.
- **Identical mandatory safety guard on both A2 and A5:** `task_policy_status=POLICY_UNKNOWN`, `individual_visible_PPE_status=NOT_ADJUDICATED`, `person_coverage_status=PERSON_COVERAGE_UNVERIFIED`. For **every** detected person and scene: `worker_compliance_verdict=null`, `verified_violation_verdict=null`, `scene_safe_clearance=null`, `action_confirmed=false`. Every unselected cue stays `PENDING_EVIDENCE_NOT_CLEARED` even after the per-image budget is exhausted. For a scene with no Person detection, person coverage must **not** be marked complete. No high-confidence or negative-class-based automatic clearance.
- The human review and explanation queue is **not dispatched**. Do not call the proposed requests completed or evidence of enhanced safety. The principal strong selective PPE verification comparator with actual review, XAI computation, and genuine worker safety reference is **still pending**; A2 is only a controlled confidence-only development comparator.

## 5. Predefined executed diagnostic outcomes and fail-closed tests

Report exactly: number of real input images/boxes and person/PPE/context cue counts; per-arm proposal counts; per-image request ID, cue type, confidence, geometry provisional association and fixed deterministic priority; number of images on which A2 and A5 request the same cue; number on which they differ; unselected PPE cues pending; no-person scenes; unknown/abstaining person cases; zero actual reviewer/XAI/inference calls and zero safe-clearance/verified-violation claims.

Optional post-routing **object-box only** analysis: V23 already has class-and-IoU matches; joining the selected detection ID to a known V23 `FP` result is permitted as an explicitly separate **descriptive selection/error-alignment diagnostic after routing**, not as a ranking feature. No worker-specific false-clearance or violation inference is permitted. Do not overclaim differences based on the single known `Safety Vests` FP.

Must fail on missing/mismatched model identity, split/source IDs, input changes, duplicate detection IDs, unsupported classes, invalid images/boxes, score below the original hosted 0.20 floor, wrong budgets, invented action dispatch, any Test, automatic clearance, or user annotation becoming a routing feature. Unit tests must include zero detected persons, no typed PPE cues, overlapping Persons/tied geometry, and the preservation of abstention on all such cases.

## 6. Scientific interpretation and release

This is an **actual run of post-detector routing decision code on real saved outputs**, exceeding an unexecuted proposal, but still **offline, exploratory and not a measured effectiveness comparison**. Neither A2 nor A5 executes explanations or human review, which remain unavailable outcomes. Any risk-priority proxy values are arbitrary prespecified engineering design parameters; no threshold optimization is supported by this nine-image dataset. Results cannot establish fewer workplace injuries, improved verified PPE compliance, superior XAI faithfulness, faster execution or actual Joule savings. Strict independent-source worker safety `NOT_FROZEN`/`scoring_ready=false`; no second image review, no model retraining and no Test access. Keep source outputs and V25 deterministic script public, but not image bytes or ephemeral hosted URLs.
