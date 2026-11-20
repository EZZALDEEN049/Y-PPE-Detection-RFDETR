# SEER-PPE V09 — executed Train-only Roboflow Workflow engineering preflight (21 November 2026)

**Real execution:** Invoked the existing **published** [SEER-PPE Conservative Review Cues v0.2](https://app.roboflow.com/softyyemen/workflows/edit/seer-ppe-conservative-review-cues-v02-1794873200805) Workflow (`61llCTFuQ4Aq4goQ9HiP`) on original **Train** Sources A, B, C and D, one image per call. It uses the original **RF-DETR Small, 17-class model `altayyar-0oflt-lafos-qqauz/2`** at an engineering-only candidate confidence of **0.20** (high-band cue **0.60**), with Active Learning disabled.

Before running, inspected the workflow's published-step configuration and verified all steps were read-only object detection, filtering, overlap analysis, expressions, and visualizations; no external write, source-label update, retraining or Eval persistence block. Only summary counts/codes were retained here, **not images or inference URLs**.

## Direct returned output summary (engineering results only)

| Train pilot | Raw candidates | High band | Low band | `Persons` candidates | Positive PPE candidates | Old-label absence-marker candidates | Center-overlap candidates | Pairwise geometry candidates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A — `image_604.jpg` | **5** | 5 | 0 | **1** | 3 | 1 | 4 | 4 |
| B — `000760.jpg` | **16** | 15 | 1 | **2** | 11 | 3 | 14 | 18 |
| C — `Kathiah Gets a Chance03.jpg` | **29** | 26 | 3 | **4** | 14 | 11 | 24 | 26 |
| D — `h1.jpg` | **1** | 1 | 0 | **0** | 1 | 0 | 0 | 0 |

The numbers above are counts of *model output candidates*, **not correct detections or research outcomes**. Center overlap/pairwise geometry do **not** establish a worker's ownership of an item, and an old `No ...` class prediction does not prove physical absence or a safety-policy violation. The high/low bands are provisional engineering filters, not validated confidence cutoffs.

All four live Workflow calls returned the **original model ID** and conservative uncertainty outputs: **`ASSOCIATION_UNKNOWN` and `POLICY_UNKNOWN`**. B and C each returned **`LOW_CONFIDENCE_NEEDS_REVIEW`**; A and D returned `NO_LOW_SCORE_CANDIDATES_RETURNED`. A/B/C returned `PERSON_CANDIDATES_DETECTED_COVERAGE_UNVERIFIED`; **D returned `PERSON_COVERAGE_UNKNOWN` despite zero detected Persons**. The latter correctly avoids turning a model miss into the researcher's signed zero-person reference.

**No new mAP, F1, per-worker compliance, false-clearance rate, explanation fidelity, joules/image or mean latency was measured.** Protected Test untouched; no adjustment to original labels/splits/model and no change to any of 19 approved wearer–equipment links.

## Person–PPE handoff

Re-read all four separate Eval Dataset cases after these Train Workflow calls. A/B/C/D revisions are unchanged at **2/2/4/1**, all remain `incomplete`, existing **19** researcher-approved item→worker links remain intact and **38/42** worker×PPE visual cells are saved. Four B face-mask/boot cells and D's signed no-person decision remain unentered; all task mandates remain `POLICY_UNKNOWN`. **Workflow predictions were not promoted to human gold labels.**

[Machine-readable real Workflow output summary](TRAIN_ONLY_UNSCORED_PREFLIGHT_2026-11-21_V09.json) · [V08 author image-review acceptance](AUTHOR_VISUAL_REVIEW_ACCEPTANCE_2026-11-21_V08.md).
