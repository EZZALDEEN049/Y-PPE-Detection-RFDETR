# Stage 4.5 Conservative Adjudication Decision — 2026-09-20

## Status

**Decision frozen; corrected harmonized derivative still pending fingerprint run.**

Stage 5 full training remains **HOLD** until the filtered harmonized derivatives are rebuilt, fingerprinted, and the Stage 5 matrix is updated to those fingerprints.

## Evidence basis

Successful GitHub Actions run:

- Workflow: `Stage 4.5 Label-Completeness Audit`
- Run ID: `35485667262`
- Head SHA: `fa9fbd140a960a0866f7c6bfef2aa2d48cb4817c`
- Artifact: `stage4-5-label-completeness-evidence`
- Artifact ID: `10597440734`
- Artifact digest: `sha256:086489f617e19c6483b3da5e7deb3f53acffb3701f279ffd835883fecf3b44ab`

The audit opened train/validation pixels only for review panels. **No test image pixel was opened.** Test decisions below use only native annotation labels and geometry, before any model prediction or test metric exists.

## Structural findings

### Y-PPE clean source

- train: 1,595 images; 359 structurally flagged for review
- validation: 459 images; 103 structurally flagged for review
- test: 234 images; 48 structurally flagged by annotation metadata only
- harmonized-empty images: 198 train, 53 validation, 31 test
- critical source-label relationships audited:
  - `Child` vs `Persons`
  - `No Safety Attire` vs `Persons`
  - `Soft Hat` vs `Hard Hat` / `No Hard Hat`

### Construction-PPE clean source

- train: 1,077 images; 31 structurally flagged for review
- validation: 134 images; 2 structurally flagged for review
- test: 141 images; 3 structurally flagged by annotation metadata only
- one train image becomes harmonized-empty
- critical source-label relationship audited: `none` vs `Person`

## Adjudication policy

A deliberately conservative, model-independent rule is adopted for the corrected harmonized derivative:

> **Exclude an entire image if either (a) it would become empty after nine-class harmonization, or (b) Stage 4.5 detects at least one critical unmatched source annotation under the frozen structural rule (IoU >= 0.50 OR excluded-box containment >= 0.80).**

This policy avoids making case-by-case test-image visual judgments and avoids silently treating ambiguous source-only annotations as negative background for a retained target class.

The rule is applied identically before training/evaluation and uses only source annotations. No model score, prediction, test performance, or threshold can affect membership.

### Expected deterministic exclusions from the successful audit

- Y-PPE: **510 images total**
  - train: 359
  - validation: 103
  - test: 48
- Construction-PPE: **36 images total**
  - train: 31
  - validation: 2
  - test: 3

Expected retained source-image counts before nine-class remapping:

- Y-PPE: train 1,236; validation 356; test 186
- Construction-PPE: train 1,046; validation 132; test 138

These counts are now frozen as execution assertions. Any drift stops the workflow.

## Why this rule is preferred

The original Stage 4 derivative kept every cleaned source image after dropping nonshared annotations. That could convert semantically ambiguous source-only objects into apparent negative background. The conservative rule removes the entire ambiguous image rather than guessing a new label, inventing an ignore region, or visually inspecting the held-out test set.

This is intentionally stricter than maximizing dataset size. The resulting evaluation population must therefore be described as the **structurally harmonizable subset** of each clean source dataset, not the full cleaned source dataset.

## Informational nonshared classes

`No Safety Vest` in Y-PPE and `no_goggle` in Construction-PPE remain nonshared and are not by themselves exclusion triggers because the frozen nine-class ontology has no corresponding shared target class. They are still dropped during harmonization.

## Next gate

1. Rebuild filtered native derivatives using `apply_stage4_5_conservative_filter.py`.
2. Re-run the frozen Stage 4 nine-class builder on those filtered derivatives.
3. Verify zero harmonized-empty images in the corrected derivative.
4. Freeze new dataset fingerprints and counts.
5. Update Stage 5 experiment matrix and reconstruction pipeline.
6. Only then may GPU execution parameters be frozen and Stage 5 training begin.
