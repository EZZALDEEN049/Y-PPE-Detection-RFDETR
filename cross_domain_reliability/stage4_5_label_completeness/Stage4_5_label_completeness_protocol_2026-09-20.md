# Stage 4.5 — Label-Completeness and Background-Policy Audit

**Status:** executed; conservative correction policy frozen; corrected v2 fingerprint run pending  
**Applies before:** any full Stage 5 YOLO11m or RF-DETR Small training/evaluation

## Why this gate exists

Stage 4 retained every cleaned source image while dropping annotations that are outside the frozen nine-class shared ontology. That transformation is structurally reproducible, but it can create an invalid learning/evaluation target if an excluded native annotation is the only label for a visible object that belongs to one of the retained shared classes.

The concrete risk is false-background / missing-ground-truth corruption. Examples include:

- Y-PPE `Child` versus retained `Persons`;
- Y-PPE `No Safety Attire` versus retained `Persons`;
- Y-PPE `Soft Hat` versus retained `Hard Hat` / `No Hard Hat`;
- Construction-PPE `none` versus retained `Person`.

`No Safety Vest` and Construction-PPE `no_goggle` are also audited as informational semantic-overlap cases, but they do not by themselves establish that a retained shared object is missing.

## Frozen audit rules

1. **No model predictions are used.**
2. **No test image pixels may be opened during policy design.**
3. Native annotation metadata may be parsed for train, validation, and test.
4. Visual review is restricted to train/validation images.
5. The current Stage 4 datasets are not modified by the audit script.
6. Structural matching for an excluded object to a candidate retained object is:
   - IoU >= 0.50, **or**
   - at least 80% of the excluded box area is contained in a candidate retained box.
7. Train/validation images that become harmonized-empty or contain a critical unmatched excluded object are rendered for review.
8. Test risk is handled only through a policy declared from native annotation metadata, never by viewing test pixels or model outputs.
9. If the audit leads to any split-membership or annotation change, Stage 4 is superseded by a **new harmonized derivative/version/fingerprint**. Existing Stage 4 fingerprints must not be silently reused.

## Dataset-specific critical checks

### Y-PPE

Critical:
- `Child` -> `Persons`
- `No Safety Attire` -> `Persons`
- `Soft Hat` -> `Hard Hat` or `No Hard Hat`

Informational:
- `No Safety Vest` -> `Safety Vests`

### Construction-PPE

Critical:
- `none` -> `Person`

Informational:
- `no_goggle` -> `goggles`

## Executed audit evidence

Successful run:

- Run ID: `35485667262`
- Artifact ID: `10597440734`
- Artifact digest: `sha256:086489f617e19c6483b3da5e7deb3f53acffb3701f279ffd835883fecf3b44ab`
- Test pixels opened: **false**
- Model predictions used: **false**

The audit generated the required structural summaries, per-image risk tables, excluded/shared overlap tables, and train/validation-only visual review panels.

## Pre-training protocol amendment: conservative annotation-only membership rule

After inspecting the structural output and targeted train/validation visual evidence, a stricter rule was frozen **before any Stage 5 model training or test prediction**. This rule supersedes the need for case-by-case visual adjudication of every flagged image:

> Exclude an entire image if either (a) it becomes empty after nine-class harmonization, or (b) it contains at least one critical unmatched source annotation under the frozen structural match rule.

The same deterministic rule is applied to train, validation, and test using native annotation metadata/geometry only. Therefore:

- no test-image visual inspection is needed for membership decisions;
- no model result can influence membership;
- ambiguous images are removed rather than relabeled or silently treated as negative background.

Expected frozen exclusions from the successful audit are:

- Y-PPE: 510 total = 359 train + 103 validation + 48 test;
- Construction-PPE: 36 total = 31 train + 2 validation + 3 test.

The full rationale is recorded in `Stage4_5_conservative_adjudication_decision_2026-09-20.md`.

## Required corrected outputs

The correction/freeze workflow must produce:

- annotation-only exclusion manifests for both datasets;
- filtered native derivatives;
- rebuilt nine-class harmonized derivatives;
- zero harmonized-empty images after correction;
- new SHA256 dataset fingerprints;
- exact retained train/validation/test counts;
- evidence that test pixels were not opened and predictions were not used.

## Decision gate

Stage 4.5 is closed only after:

1. the conservative annotation-only rule is applied deterministically;
2. expected exclusion counts are reproduced exactly;
3. corrected harmonized derivatives are rebuilt;
4. zero harmonized-empty images remain;
5. new fingerprints/counts are frozen;
6. Stage 5 experiment matrix and reconstruction pipeline are updated to those final fingerprints.

Until all six are complete, the Stage 5 full-training gate remains **HOLD**.
