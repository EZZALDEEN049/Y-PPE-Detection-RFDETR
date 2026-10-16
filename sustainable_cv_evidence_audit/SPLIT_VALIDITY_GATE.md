# Stage 2 split integrity: source-identity and leakage audit

**Version:** 0.2 (2026-10-16)
**Real datasets analyzed in this workstream:** NONE.
**Execution status:** Synthetic-code tests only. Do not claim real dataset split identity.

## Scientific motivation

The legacy script scripts/compare_splits.py uses sets of SHA-256 hashes.
Sets remove duplicate multiplicity, and exact exported bytes can diverge after
resize/augmentation even when images derive from a common source photograph.
Therefore hash equality is not proof of original-scene independence.

The new read-only split_integrity.py distinguishes:
- Equality of per-split MULTISETS of image-file byte hashes.
- Repeated exact-byte copies within a split.
- Exact-image bytes crossing train, validation and test.
- Exact-image bytes appearing in incompatible splits across two dataset exports.
- Candidate source-ID crossings when external source-ID crosswalks are provided.

## Execution

Supported image layouts:
- dataset/train/images, dataset/valid/images, dataset/test/images
- dataset/images/train, dataset/images/val, dataset/images/test

Command:

    python split_integrity.py /secure/yolo_export /secure/rfdetr_export \
        --output /secure/reports/export_split_audit.json

Optional CLI flag: --require-identical-exported-bytes
This exits with code 2 when exported byte multisets differ or any exact-byte
cross-split leak is detected. It does NOT attest to source-level identity.

The utility does not read labels or evaluate model predictions.
It publishes counts/Boolean findings, not input filenames, source IDs or hashes.

## Optional source-ID crosswalk

Provide two complete independent CSVs with columns:

    split,file,source_id
    train,training_image.jpg,verified_original_asset_id_01
    valid,validation_image.jpg,verified_original_asset_id_02
    test,test_image.jpg,verified_original_asset_id_03

Every exported image must have one mapping row. The file column uses its relative
path inside the split image directory. Acceptable split names are train, valid,
val, validation, and test. Mapping the same original photo across two different
Roboflow projects requires a genuine shared identifier or manually adjudicated
crosswalk backed by source records. NEVER derive a "verified" source identifier
solely from an exported filename stem or the part before ".rf.".

    python split_integrity.py /secure/yolo_export /secure/rfdetr_export \
        --source-map-a /secure/yolo_source_map.csv \
        --source-map-b /secure/rfdetr_source_map.csv \
        --output /secure/reports/source_identity_audit.json

Augmented variants may legitimately share a source ID within ONE split.
The same source in TRAIN and TEST is potential leakage even if transformed
exports have entirely different SHA-256 hashes.

The report calls these IDs "candidate/operator supplied" and keeps provenance
verification false. An independent original-image and collection-group
adjudication remains necessary before source-level assertions.

## Additional controls before a common-model comparison

1. Original asset identifiers, near-duplicates, video/source group, and site
   identity are checked by a human and supported with protected provenance.
2. Image consent/ethical governance, attribution, permitted usage and public
   availability have been reviewed.
3. Final class ontology, annotation files, missing-label policy, confidence
   threshold handling and evaluator are frozen for both models.
4. Evaluate BOTH pre-trained fine-tuned models on ONE held-out, source-disjoint,
   otherwise comparable test set.
5. Check the availability and legality of local trained checkpoints or a
   reproducible self-hosted Roboflow Inference runtime.
6. Freeze hardware, software, input resolution, inference warm-up, repetitions,
   batch size, precision, power instrumentation and boundaries.
7. Report safety-class false negatives and domain/site differences separately
   from aggregate mAP, not as a single sustainability score.

No test set is downloaded or images inspected by this CI pipeline. Run the
private dataset check in a properly authorized environment, and store signed
provenance and sensitive images outside public GitHub.

## Interpretation

Identical exported hashes: evidence of exact exported-byte identity only.
Matched user-provided source IDs: candidate source-level identity only.
No hash overlap: does not rule out transformed copies of the same original.
No identified leak: not evidence of generalization across different sites.
Even proven split identity: does not establish a common evaluation protocol.
Absent electricity metering: does not establish low energy/CO2 per inference.
