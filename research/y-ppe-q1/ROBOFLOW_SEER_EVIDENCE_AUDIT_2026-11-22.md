# Roboflow and SEER-PPE evidence audit for Y-PPE Q1

**Audit date:** 22 November 2026  
**Purpose:** document evidence retrieved for Q15 Option C and Q14 evidence reuse.  
**Important:** this is a metadata and existing-artifact audit. No raw dataset export was downloaded in this audit.

## 1. Roboflow raw-project metadata

| Property | YOLOv11m-linked project | RF-DETR-linked project |
|---|---|---|
| Public project | master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh | softyyemen/altayyar-0oflt-lafos-qqauz |
| Model ID | altayyar-0oflt-lafos-qqauz-ty5nh/1 | altayyar-0oflt-lafos-qqauz/2 |
| Version | 1 | 2 |
| Model type | yolov11m | rfdetr-small |
| Training state | finished in public version metadata | finished in connected-workspace training record |
| Raw project images | 2,327 | 2,327 |
| Raw train/valid/test | 1,625 / 468 / 234 | 1,625 / 468 / 234 |
| Raw class count | 17 | 17 |
| Generated version images | 5,577 | 5,577 |
| Generated train/valid/test | 4,875 / 468 / 234 | 4,875 / 468 / 234 |
| Preprocessing | Auto-Orient; stretch 640×640 | Auto-Orient; stretch 640×640 |
| Augmentation metadata | 3 image versions; Mosaic | 3 image versions; Mosaic |
| YOLOv8 export | ready=true | ready=true |

The two raw project records expose the same 17 class names and same split counts. This is not a file-level identity check. The generated 5,577 count includes training augmentation outputs and must not be confused with the 2,327-image raw source corpus.

## 2. Training and platform metrics — historical metadata only

**YOLOv11m:** the public version record identifies a finished YOLOv11m training, model ID altayyar-0oflt-lafos-qqauz-ty5nh/1, and training ID nKL5CfN5VpO91BXCrmq3/1/training/0. The cross-workspace Roboflow connection rejected models_list and trainings_get for the YOLO project because it belongs to master-fylfq, not the connected softyyemen workspace. This is an access-scope limitation, not evidence that the model is absent.

**RF-DETR Small:** model ID altayyar-0oflt-lafos-qqauz/2; training status finished; platform training summary reports mAP50 93.97%, precision 94.36%, recall 88.0%. Evaluation record KyzP9neuyNTN5eQpGCAY reports platform mAP 0.9622053873, precision 0.952, recall 0.934, F1 0.942. These platform records are source-of-results evidence, not an independent re-computation. Do not assume the platform mAP field's IoU convention without its evaluation configuration.

The platform metrics from the two tracks must not be compared as if they were produced by a common evaluator until exact split membership, metric definition, operating thresholds and evaluation artifacts are reconciled.

## 3. Export and checkpoint access

- Both Roboflow dataset export requests returned ready=true for YOLOv8 format.
- The export archives were not downloaded or locally inspected.
- No SHA-256 manifest was generated from the two exports.
- No raw checkpoint binary was downloaded for either model.
- Temporary signed export URLs and their access keys are intentionally omitted.
- No new inference was run from the YOLOv11m public endpoint.

## 4. SEER-PPE technical evidence eligible for reuse

### 4.1 Original Train/Validation source audit
SEER-PPE's full original-source audit records:
- 2,093 source images: 1,625 Train and 468 Validation.
- 0 missing files and 0 decode errors.
- 0 exact SHA-256 Train–Validation matches.
- 0 decoded-RGB exact Train–Validation matches.
- 46 perceptually close dHash pairs involving 31 Validation images.

This supports a scoped file-integrity and exact-image comparison statement for the audited SEER source files. It does not prove scene/session/site independence.

### 4.2 Clean17 reconstruction audit
SEER-PPE Phase 5 records 2,288 images and 16,300 labels after its reconstruction/cleaning process, including 39 excluded images and annotation duplicate/near-duplicate corrections. These are SEER-PPE results and are not automatically the Q1 manuscript's final dataset version.

### 4.3 Crosswalk and source-family limits
The SEER V12 crosswalk records:
- 468 original Validation images;
- 459 provisional Clean17 Validation candidates;
- 9 historically excluded Validation images;
- provisional_mapping_is_confirmed_image_identity=false;
- 0 individual author source-family signatures;
- 0 scoring-eligible images.

The SEER V26 summary also records original_source_independence_verified=false. Consequently, source-family/site/session independence is not claimed as closed for the Q1 track.

## 5. RF-DETR V26 stored predictions — independent arithmetic re-check

The 12 V26 geometry shards were read and independently re-scored using class-exact, one-to-one matching at IoU≥0.50 and the stored confidence floor 0.20.

| Scope | Images | GT | TP | FP | FN |
|---|---:|---:|---:|---:|---:|
| All 17 classes | 459 | 3,471 | 3,297 | 806 | 174 |
| Six missing-PPE marker classes | 459 | 1,004 | 953 | 283 | 51 |

For the six missing-PPE marker classes: pooled FPPI = 283 / 459 = **0.617**. Conservation checks passed: GT = TP + FN and predictions = TP + FP.

This is retrospective RF-DETR-only Validation evidence, not a paired comparison or fresh independent Test result. V26 predictions are truncated below confidence 0.20, so the full Q5 19-threshold sweep from 0.05 to 0.95 cannot be reconstructed.

## 6. Exploratory Q14 apparent-scale table

| Missing-PPE class | Small FN/GT | Medium FN/GT | Large FN/GT |
|---|---:|---:|---:|
| No Hard Hat | 0/18 | 0/25 | 1/13 |
| No Safety Boots | 7/29 | 1/25 | 0/39 |
| No Safety Vest | 1/2 | 0/60 | 3/98 |
| No Face Mask | 9/115 | 2/117 | 0/48 |
| No Safety Attire | 0/1 | 3/29 | 4/57 |
| No Gloves | 13/104 | 5/164 | 2/60 |

This table is post hoc, RF-only, and based on Validation outputs. Sparse cells are unstable. It is not a confirmatory Q14 result and cannot support a model superiority claim.

## 7. Audit conclusion

**Reusable now:** Roboflow project/version metadata, historical model identifiers and training-state records, SEER source-file integrity evidence, SEER similarity-screening history, and the RF-DETR-only V26 arithmetic diagnostic with explicit limitations.

**Still required:** downloaded and hashed YOLO/RF dataset exports; exact split identity; definitive mapping of SEER source IDs to the Q1 source roster; complete class/box convention reconciliation; accessible checkpoint/training provenance; predictions for both models on the same admissible images; Q5 validation-only threshold selection; and an eligible independent evaluation partition.

**Decision:** Q15 Option C is partially executed. E1 and E2 are not passed. The Q1 empirical publication gate remains NO-GO.


## 8. Direct comparison of the current Roboflow dataset versions — 22 November 2026

A public copy of the YOLO-linked project was forked into the connected Roboflow workspace solely to enable read-only cross-project metadata and annotation comparison:
- Original public project: `master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh`.
- Comparison copy: `softyyemen/altayyar-0oflt-lafos-qqauz-ty5nh-b1in5`.
- The original public project was not modified. The fork has no generated dataset versions and was not used for training or inference.

The current raw dataset versions are YOLO-linked v2 and RF-DETR-linked v3. Each exposes 2,327 images with Train/Valid/Test counts of 1,625/468/234 and 17 classes.

A duplicate-aware comparison of all 2,327 records per current project found:
- 2,233 unique filenames in each project;
- 64 filename groups containing repeated names;
- zero mismatches between the two projects' filename-group multisets when compared on filename, split, image width/height, annotation count, and per-class annotation counts;
- 19 paired annotation-geometry checks with exact matches (13 stratified examples across Train/Validation/Test plus six duplicate-filename ambiguities resolved using saved geometry).

The source IDs differ between the two workspace copies. This is expected for separate workspace copies and is not evidence of different image content. Conversely, filename/metadata parity and sampled geometry matches do **not** prove that all 2,327 raw image byte streams are identical. No full binary hash comparison was completed.

Machine-readable record: [current dataset parity JSON](Y_PPE_CURRENT_DATASET_PARITY_2026-11-22.json).

## 9. Important version chronology correction — model-training versions versus current versions

The model-linked historical versions are not the same version numbers as the latest current raw datasets:

| Track | Historical model-training version | Current raw version | Historical version images/splits | Current version images/splits |
|---|---:|---:|---|---|
| YOLOv11m | v1 | v2 | 5,577; 4,875/468/234 | 2,327; 1,625/468/234 |
| RF-DETR Small | v2 | v3 | 5,577; 4,875/468/234 | 2,327; 1,625/468/234 |

Both historical training versions record three image versions plus Mosaic augmentation. Their preprocessing records Auto-Orient and stretch resize to 640×640. The current v2/v3 versions have no linked training runs and no augmentation metadata. The 5,577 historical count must not be mistaken for 5,577 unique raw source images; the 4,875 Train count reflects the generated training-version content.

COCO export requests returned ready=true for all four versions (YOLO v1/v2 and RF-DETR v2/v3). However, the ZIP archives were not downloaded or locally inspected in this environment, and no SHA-256 manifests were generated. Temporary signed export URLs are intentionally not stored. The YOLO training-detail endpoint remains restricted by the cross-workspace Roboflow permission boundary; public version metadata still confirms its finished status and model ID.

**Consequence:** current-version parity does not establish the exact membership of the two historical model-training versions. The historical training-version archives remain the priority evidence needed to close the split-identity component of E1.

## 10. SEER-PPE V13 cross-split evidence mapped to the current Y-PPE source roster

The V13 source manifest identifies the RF-DETR current project v3 and covers 2,093 Train/Validation sources (1,625 Train and 468 Validation; no Test bytes). The 50 V13 cross-split pairs comprise 46 earlier dHash-close pairs plus four named-site pairs. Direct pixel comparison recorded seven high automated same-frame candidates, 43 non-high pairs whose acquisition independence remains unresolved, and zero raw-byte-identical pairs.

A read-only reconciliation established:
- all 76 unique source IDs used in the 50 pairs exist in the RF-DETR v3 source manifest;
- all 76 saved annotation records were returned and marked valid;
- all 76 image dimensions agree with the source manifest;
- all 50 valid-side filenames are present in the current Y-PPE Validation split, and all 50 train-side filenames are present in the current Y-PPE Train split;
- the seven high automated candidates are therefore present by filename/split in the current Y-PPE source roster, but exact raw-byte identity across the YOLO workspace copy has not been established;
- six duplicate-filename ambiguities were resolved by exact saved annotation geometry. This does not replace a binary image hash.

The four School 22 May – Aseefrah pairs are named-site overlap evidence. The two Valid images in this named site remain ineligible for a site-independent claim until the required source-family/site review is signed. The V15 attestation overlay remains empty: zero human source-family signoffs, zero signed independence attestations, and scoring_ready=false.

Machine-readable record: [V13 source-overlap transfer JSON](Y_PPE_SEER_V13_SOURCE_OVERLAP_TRANSFER_2026-11-22.json).

## 11. Updated gate assessment and next action

- E1 remains **NOT PASSED**. Current-version metadata parity is now supported, and the V13 source-overlap candidates are mapped to the current RF source roster, but the historical training-version archives remain uninspected, raw Train/Valid/Test hashes are not available, Test bytes have not been audited, and source-family/site/session independence remains unsigned.
- E2 remains **NOT PASSED**. Neither model's exact checkpoint binary and complete exposure history has been authenticated for a common eligible evaluation roster.
- E3 remains **NOT STARTED** for a new admissible paired test.
- Q1 publication remains **NO-GO**.

The next required input is the two historical model-training-version COCO archives: YOLO project version 1 and RF-DETR project version 2. They must be downloaded from their respective public Roboflow project pages and uploaded into the controlled working session. Do not substitute the current YOLO v2 or RF-DETR v3 exports. Do not publish the temporary signed export URLs.
