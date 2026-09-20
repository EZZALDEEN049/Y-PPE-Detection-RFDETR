# Stage 4.5 — Label-Completeness and Background-Policy Audit

**Status:** pre-execution scientific gate  
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
7. Every train/validation image that becomes harmonized-empty is visually reviewed.
8. Every train/validation image containing a critical excluded object without a structural retained match is visually reviewed.
9. Test risk is handled only through a policy declared from native annotation metadata, never by viewing test pixels or model outputs.
10. If the audit leads to any split-membership or annotation change, Stage 4 is superseded by a **new harmonized derivative/version/fingerprint**. Existing Stage 4 fingerprints must not be silently reused.

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

## Required outputs

For each dataset the audit produces:

- `structural_summary.json`
- `image_risk_table.csv`
- `excluded_shared_overlap_table.csv`
- train/validation-only rendered review images
- train/validation-only contact sheets

The summary must explicitly record `test_pixels_opened: false`.

## Decision gate

Stage 4.5 is **not closed** merely because the script runs successfully.

Closure requires:

1. structural output reviewed;
2. train/validation visual panels adjudicated;
3. a written test policy based only on pre-model native annotation metadata;
4. any corrective derivative rebuilt and fingerprinted;
5. Stage 5 experiment matrix updated to the final accepted fingerprints/counts.

Until all five are complete, the Stage 5 full-training gate remains **HOLD**.
