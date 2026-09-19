# Stage 4 Harmonized Dataset Freeze Protocol

**Date:** 2026-09-20  
**Status:** pre-training transformation protocol.  
**Input:** Stage-2-clean Y-PPE and Construction-PPE plus `ontology_frozen_v1.yaml`.  
**Output:** deterministic 9-class bounding-box derivatives for later training/evaluation.

## Frozen transformation

1. Reconstruct the two cleaned Stage-2 derivatives from immutable/public source inputs and frozen correction manifests.
2. Standardize split names to `train`, `val`, and `test` without moving images between splits.
3. Retain all cleaned source images; only non-shared annotation rows are dropped.
4. Map native classes to canonical IDs in this exact order:
   `person, helmet, gloves, vest, boots, goggles, no_helmet, no_gloves, no_boots`.
5. Convert every retained Y-PPE polygon row to its enclosing axis-aligned YOLO bounding box. Construction-PPE is already bbox-only.
6. Write an empty label file for a preserved image that contains no retained shared-class instance; do not silently delete the image.
7. Create SHA256 image/label manifests and a dataset-level fingerprint for each derivative.
8. Re-run label-integrity, cross-split duplicate, perceptual-near-duplicate, and explicit source-group audits after transformation.

## Locked-test rule

Test images may be read by deterministic integrity code for hashing and label validation, but they are not opened for qualitative/visual adjudication. No model prediction on either test split is produced in Stage 4.

## Frozen image counts

The transformation must preserve the clean Stage-2 image counts exactly:

- Y-PPE: train 1,595; val 459; test 234.
- Construction-PPE: train 1,077; val 134; test 141.

Any mismatch is a hard failure.

## Training gate

No harmonized baseline training begins until Stage 4 passes. Once passed, class order, image membership, label conversion policy, and manifests are treated as frozen. Any later change requires a dated pre-test amendment; a change motivated by target-test performance cannot be presented as preregistered.
