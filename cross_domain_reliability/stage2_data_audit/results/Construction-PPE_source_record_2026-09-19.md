# Construction-PPE — Stage 2 Source Record

**Prepared:** 2026-09-19  
**Status:** official source metadata verified; raw integrity/leakage audit pending.

## Official source

- Documentation: `https://docs.ultralytics.com/datasets/detect/construction-ppe`
- Dataset archive: `https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip`
- Official YAML: `ultralytics/cfg/datasets/construction-ppe.yaml`
- YAML source pinned for protocol reproducibility: Ultralytics commit `42044baf5eda3d52aa4bd7d8a098375d2c7fdad7` (2026-06-10).
- Documented dataset version: `1.0.0`.
- Documented license: `AGPL-3.0`.

## Official dataset structure

- Total images: 1,416
- Train: 1,132
- Validation: 143
- Test: 141
- Annotation task: object detection / Ultralytics YOLO format
- Classes: 11

Verified numeric class-ID order from the official YAML:

0. `helmet`
1. `gloves`
2. `vest`
3. `boots`
4. `goggles`
5. `none`
6. `Person`
7. `no_helmet`
8. `no_goggle`
9. `no_gloves`
10. `no_boots`

## Primary 9-class harmonized mapping for this study

The primary Y-PPE ↔ Construction-PPE benchmark retains:
`Person`, `helmet`, `gloves`, `vest`, `boots`, `goggles`, `no_helmet`, `no_gloves`, `no_boots`.

`none` and `no_goggle` are excluded from the primary mapping because no strict Y-PPE counterpart is established. Construction-PPE has no dedicated `no_vest` class, so Y-PPE `No Safety Vest` is also excluded from the strict primary mapping.

## Audit requirements before use

The official counts and class order are documentary facts, not evidence that the split is leakage-free. The raw archive still requires: image/label pairing checks, label geometry validation, exact and pixel-level cross-split duplicate screening, perceptual near-duplicate review, source-group review where recoverable, duplicate-object annotation checks, and manual semantic geometry auditing of `no_helmet`, `no_gloves`, and `no_boots` before ontology freeze.
