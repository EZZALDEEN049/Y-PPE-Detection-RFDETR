# SEER-PPE V16 — read-only Train preflight and human-grounded cue-conflict interpretation

**21 November 2026 | engineering result, NOT independent Validation model performance.**

## Inputs and execution

Existing published Roboflow `SEER-PPE Conservative Review Cues v0.2` Workflow `61llCTFuQ4Aq4goQ9HiP` ran on **A/B/C/D Train-only** Eval Cases by reading temporary authorized image URLs. The workflow uses fixed original RF-DETR Small `altayyar-0oflt-lafos-qqauz/2`, confidence candidate threshold **0.20** and "high cue" threshold **0.60**, with active learning disabled. The output JSON stores **only numerics**, no image, signed URLs or screenshots. A previous V09 pilot already documented the same case-wise counts; V16 stores detailed per-detection records and a reproducible post-processing method, rather than calling the Train exercise a new scientific experiment.

Across four actual Train images the detector emitted **51** candidates: A 5, B 16, C 29, D 1, with 7 Person candidates (A1/B2/C4/D0) and 4 lower-confidence cues. This is a pipeline function check, not an estimate of generalization.

## Deterministic review cue method

Each specific PPE-class detection can overlap multiple detector Person boxes. Compute intersection/PPE area, retain candidates at overlap ≥**0.25**; propose a single strongest geometry owner only when best overlap ≥**0.75** and the runner-up is under **0.45** or the best–runner-up margin is ≥**0.30**. For uncertainty, retain candidate person IDs and mark review; **never** assert `MATCHED` or a worker `PRESENT/ABSENT` GT state. `No Face Mask`, `No Safety Boots` and other `No ...` legacy classes are **negative detector cues**, not proven physical absence or policy violations. `No Safety Attire` is a generic non-specific context cue. Each inferred policy status is `POLICY_UNKNOWN`. Case D has one `Hard Hat` candidate and no Person detection; it cannot be labeled a zero-person scene from the model output.

## Comparison to existing recorded human Train reference

The live Roboflow human reference (unchanged) has A/B/C/D source IDs, revisions **2/2/4/1**, **19** human-approved item/person links and **38/42** human visual state cells. A separate non-scoring deterministic comparison of model Person boxes with human Person boxes used globally one-to-one IoU ≥0.50 **only as candidate correspondence**. Model confidence labels and single-box geometry proposals were never used to revise human reference. Directional PPE cue classes were classified into mutually exclusive categories:

| Cue direction versus saved human visual state (not model metric) | Count |
|---|---:|
| Detector cue direction compatible with saved PRESENT/ABSENT | **21** |
| Detector cue direction opposes saved PRESENT/ABSENT | **4** |
| Saved human visual state UNKNOWN | **7** |
| Individual human visual state not recorded | **2** |
| No unambiguous detector-person to human-person geometric link | **4** |
| **All typed PPE review cues** | **38** |

All four opposing cues are **`No Safety Boots`** markers in Train C: two geometrically propose P001, one P003 and one P004; each human visual reference says **PRESENT**. This is *not* a false-positive count or four separate human violations. It demonstrates why detector negative markers, PPE visibility, physical certification, and site policy have to be distinguished. Four B `face_mask/safety_boot` reference cells and D zero-person scene signoff remain incomplete. The reviewer approved the general visual review in earlier work; these individual missing formal entries are preserved rather than invented.

## Reproducibility and protective controls

- [Roboflow actual detector numeric output](ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json)
- [Train human reference numeric geometry snapshot](TRAIN_ONLY_LIVE_HUMAN_REFERENCE_GEOMETRY_V16.json)
- [Deterministic PPE geometry and abstention tool](tools/review_real_train_detection_geometry_v16.mjs) and [its metadata-only output](TRAIN_ONLY_PERSON_PPE_GEOMETRIC_REVIEW_V16.json)
- [Non-scoring cue-versus-human diagnostics](tools/triage_v16_train_cues_against_existing_reference.mjs) and [report](TRAIN_ONLY_DETECTOR_VS_ACCEPTED_HUMAN_REVIEW_V16.json)
- Successful [Train geometry CI run 44849621364](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44849621364) and [cue disagreement CI run 44849892529](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44849892529).

Scientific limitations: existing Train cases are neither source-independent Validation nor Test, no person association performance or mAP is computed, no energy/XAI risk endpoints measured, original model and Roboflow reference/labels/splits are unchanged, Test has not been opened for this stage. The [V15 eligibility freeze](VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json) remains unapproved, `scoring_ready=false`.
