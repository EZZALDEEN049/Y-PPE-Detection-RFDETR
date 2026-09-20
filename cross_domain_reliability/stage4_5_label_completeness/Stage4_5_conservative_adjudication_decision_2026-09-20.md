# Stage 4.5 Conservative Adjudication Decision — 2026-09-20

## Status

**CLOSED — conservative policy executed and final harmonized derivatives frozen.**

The Stage 4.5 data-integrity gate is closed. Stage 5 model training still requires the separate Colab GPU/materialization/resource preflight; held-out test evaluation remains gated by the common evaluator.

## Evidence basis

Initial structural audit:

- Workflow: `Stage 4.5 Label-Completeness Audit`
- Run ID: `35485667262`
- Artifact: `stage4-5-label-completeness-evidence`
- Artifact ID: `10597440734`
- Digest: `sha256:086489f617e19c6483b3da5e7deb3f53acffb3701f279ffd835883fecf3b44ab`

Final conservative freeze:

- Workflow: `Stage 4.5 Conservative Harmonized v2 Freeze`
- Run ID: `35536050231`
- Head SHA: `eb87aa14dab07d7546e713c2d5eb68ef583f2d5a`
- Artifact: `stage4-5-conservative-harmonized-v2-evidence`
- Artifact ID: `10612876023`
- Digest: `sha256:24b5851f8eef044e17d6804272db2965fed9737098718ed229d0e5a57028786f`

No model predictions were used for membership decisions. Held-out test image pixels were not opened for adjudication; test membership was determined from native annotation metadata and geometry only.

## Frozen conservative rule

Exclude an entire image if either:

1. it would become empty after nine-class harmonization; or
2. Stage 4.5 detects at least one critical unmatched source annotation under the frozen structural rule: IoU >= 0.50 OR excluded-box containment >= 0.80.

Critical relationships were `Child` vs `Persons`, `No Safety Attire` vs `Persons`, and `Soft Hat` vs `Hard Hat`/`No Hard Hat` for Y-PPE; and `none` vs `Person` for Construction-PPE.

The rule is model-independent and is applied before training/evaluation. The final evaluation population is therefore the **structurally harmonizable subset** of each clean source dataset, not the full cleaned source dataset.

## Executed exclusions

- Y-PPE: 510 images total — train 359, validation 103, test 48.
- Construction-PPE: 36 images total — train 31, validation 2, test 3.

The final freeze verified zero harmonized-empty images in both corrected derivatives.

## Final dataset identities

### Y-PPE-h9-v2

- train: 1,236 images
- validation: 356 images
- test: 186 images
- retained shared-class instances: 9,471
- SHA256 fingerprint: `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8`

### Construction-PPE-h9-v2

- train: 1,046 images
- validation: 132 images
- test: 138 images
- retained shared-class instances: 9,514
- SHA256 fingerprint: `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`

These identities supersede the original Stage 4 keep-all-image derivatives and any interim Stage 4.5 identity produced before the conservative freeze.

## Next gate

Stage 5 may proceed only after the final identities above are reproduced end-to-end in the actual Colab runtime, the GPU/software environment is recorded, and architecture-specific batch size, gradient accumulation, worker count, and mixed-precision policy are frozen before full training. No held-out test metric may be computed before the common evaluator is frozen.
