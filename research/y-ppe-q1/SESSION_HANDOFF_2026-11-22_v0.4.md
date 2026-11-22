# Y-PPE complete research handoff — v0.4

**Audit date:** 22 November 2026  
**Canonical proposal:** v3.5.0  
**Repository:** `EZZALDEEN049/Y-PPE-Detection-RFDETR`  
**Latest verified repository commit before this handoff:** `babac56863627c334c6555bb537dfd6a57a988ab`

## 1. Executive status

- Weighted project-management progress: **48.75% (49% rounded)**. This is not a probability of publication or a measure of scientific validity.
- Research Hold is active: no new training, no new model-performance comparison, and no superiority claim until E1 and E2 are passed.
- E1 — Data integrity/provenance: **NOT PASSED**.
- E2 — Model eligibility/comparability: **NOT PASSED**.
- E3 — New admissible paired comparison: **NOT STARTED**.
- E4/Q14 — RF-only exploratory diagnostic exists in the separate evidence track; it is not a paired Y-PPE comparison and is not transferable as a Y-PPE result.
- E5 — Deferred.
- E6 — Not started.
- Q1 publication decision: **NO-GO**.

## 2. Historical model-training versions — exact identities

The historical versions linked to the trained models are not the same as the latest raw dataset versions.

| Track | Historical training version | Model ID | Training ID | Status |
|---|---|---|---|---|
| YOLOv11m | `master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh/1` | `altayyar-0oflt-lafos-qqauz-ty5nh/1` | `nKL5CfN5VpO91BXCrmq3/1/training/0` | finished |
| RF-DETR Small | `softyyemen/altayyar-0oflt-lafos-qqauz/2` | `altayyar-0oflt-lafos-qqauz/2` | `CznUs9fXTpbyRFbcRZDR/2/training/0` | finished |

Each historical training version reports 5,577 generated images:
- Train: 4,875
- Validation: 468
- Test: 234

Both record Auto-Orient and Stretch resize to 640×640, three image versions, and Mosaic augmentation.

Roboflow's historical model metadata reports YOLOv11m mAP 92.25, recall 87.20, precision 95.25, and RF-DETR Small mAP 93.97, recall 88.00, precision 94.36. These are platform-reported historical metadata only; they are **not** a new controlled paired comparison, and no superiority conclusion may be drawn from them.

## 3. Current raw dataset versions — parity audit

The latest raw versions are YOLO-linked v2 and RF-DETR-linked v3. Each exposes 2,327 images, with 1,625/468/234 Train/Validation/Test and 17 classes.

A duplicate-aware comparison of all 2,327 records in each current project found:
- 2,233 unique filenames per project;
- 64 repeated-filename groups;
- zero mismatches in the multiset of filename, split, dimensions, annotation count, and per-class annotation-count signatures;
- 19 paired annotation-geometry checks with exact matches (13 stratified checks across Train/Validation/Test plus six duplicate-name ambiguity resolutions).

The workspaces use different image IDs. The current comparison is metadata and sampled annotation-geometry parity, **not** proof that all raw image bytes are identical. No complete SHA-256 image-level audit has been performed.

Read: `Y_PPE_CURRENT_DATASET_PARITY_2026-11-22.json`.

## 4. SEER-PPE V13 source-overlap evidence transferred to the Y-PPE source roster

The V13 source manifest is for RF-DETR current project v3 and contains 2,093 Train/Validation sources (1,625 Train and 468 Validation); it contains no Test image bytes.

The cross-split evidence comprises 50 pairs:
- 46 earlier dHash-close pairs;
- four additional named-site pairs;
- seven high automated same-frame/content candidates;
- 43 non-high pairs for which acquisition/source independence remains unresolved;
- zero raw-byte-identical pairs.

All 76 unique source IDs in the 50-pair list were found in the RF-DETR v3 manifest. All 76 saved annotation records were valid, and all 76 dimensions matched the manifest. All 50 Validation-side filenames appear in current Y-PPE Validation, and all 50 Train-side filenames appear in current Y-PPE Train. This is a filename/split crosswalk, not byte-level identity across the YOLO workspace copy.

The four named-site pairs identify School 22 May – Aseefrah across Train and Validation. Two Validation images remain held for site-independent claims pending source-family/site adjudication. V15 records zero human source-family signoffs and `scoring_ready=false`.

Read:
- `Y_PPE_SEER_V13_SOURCE_OVERLAP_TRANSFER_2026-11-22.json`
- `ROBOFLOW_SEER_EVIDENCE_AUDIT_2026-11-22.md`

## 5. Historical COCO export retrieval

Roboflow export requests were made for the exact historical model-training versions:
- YOLOv11m historical v1 — COCO export returned `ready=true`; Roboflow-reported size value 329.326929.
- RF-DETR Small historical v2 — COCO export returned `ready=true`; Roboflow-reported size value 329.523979.

A direct download attempt from the active execution environment failed because it could not resolve `app.roboflow.com` (DNS/network restriction). **Neither ZIP archive was downloaded.** Therefore:
- no archive SHA-256 has been calculated;
- no ZIP integrity or archive-member inspection has been performed;
- no exact split membership comparison has been performed on the historical archives;
- no raw image SHA-256 or decoded-pixel hash comparison has been performed.

The export URLs are temporary signed links and are intentionally not committed to GitHub. They were provided to the researcher in the conversation; if expired, regenerate the COCO export from the exact same project/version.

**Required user action:** download both historical COCO ZIP archives and upload both into the active conversation. Do not substitute current YOLO v2 or RF-DETR v3.

Read: `E1_HISTORICAL_COCO_EXPORT_RETRIEVAL_2026-11-22.md`.

## 6. E1/E2/E3 decision and next steps

### E1 must remain NOT PASSED until:
1. Both historical archives (YOLO v1 and RF-DETR v2) are available.
2. Archive SHA-256 hashes and ZIP integrity are recorded.
3. Per-split image membership is reconstructed from the actual archives.
4. Train/Validation/Test membership and raw image hashes are compared across tracks.
5. Test bytes are audited.
6. Source-family/site/session independence, including the seven high-priority candidates and four named-site pairs, is adjudicated with documented human signoff where required.
7. Class-index order, label semantics, ignored regions, and bounding-box conventions are reconciled.

### E2 may begin only after E1 passes:
- authenticate exact model checkpoint identities and binaries;
- verify training exposure, preprocessing, class mappings, and evaluation configuration;
- establish a common eligible test roster and comparable inference settings.

### E3 may begin only after E1 and E2 pass:
- freeze the paired evaluation protocol;
- generate both models' predictions on the same admissible images;
- run paired statistical analyses and report uncertainty without unsupported safety weights.

## 7. Repository navigation

- `README.md`
- `PROJECT_STATE_2026-11-22.json`
- `PROGRESS_CHECKPOINT_2026-11-22.md`
- `DECISION_REGISTER_Q1_Q15.md`
- `ROBOFLOW_SEER_EVIDENCE_AUDIT_2026-11-22.md`
- `Y_PPE_CURRENT_DATASET_PARITY_2026-11-22.json`
- `Y_PPE_SEER_V13_SOURCE_OVERLAP_TRANSFER_2026-11-22.json`
- `E1_HISTORICAL_COCO_EXPORT_RETRIEVAL_2026-11-22.md`
- `MANUSCRIPT_PEER_REVIEW_v0.1_2026-11-22.md`
- `MANUSCRIPT_REVISION_LOG_v0.2_2026-11-22.md`

The repository contains public-safe research records and evidence summaries. Temporary signed export URLs, API credentials, raw private data, model-weight binaries, and unpublished DOCX binaries are not committed.

## 8. Binding research rule

No new training, no performance comparison, and no superiority claim before both E1 and E2 are formally passed. A ready export is not a downloaded archive; a filename match is not raw-byte identity; a non-high image-similarity score is not proof of independent acquisition; and a historical platform metric is not a new experiment.
