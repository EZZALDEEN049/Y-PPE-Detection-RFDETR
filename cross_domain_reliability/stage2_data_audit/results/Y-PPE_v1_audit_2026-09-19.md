# Y-PPE Version 1 — Stage 2 Data Audit Result

**Audit date:** 2026-09-19  
**Dataset:** Y-PPE / ALTAYYAR  
**Roboflow workspace/project:** `master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh`  
**Version:** 1  
**Export:** YOLOv11  
**Current gate decision:** **FAIL / CORRECTION REQUIRED BEFORE EXPERIMENTS**

## What was verified

The GitHub Actions workflow successfully authenticated to Roboflow, downloaded Version 1, found the actual `data.yaml`, audited `train`, `valid`, and `test`, and uploaded the audit artifacts.

The actual class-ID order from `data.yaml` is:

0. Animal
1. Child
2. Face Masks
3. Gloves
4. Goggles
5. Hard Hat
6. No Face Mask
7. No Gloves
8. No Hard Hat
9. No Safety Attire
10. No Safety Boots
11. No Safety Vest
12. Pants
13. Persons
14. Safety Boots
15. Safety Vests
16. Soft Hat

The exported dataset metadata reports `nc: 17` and `CC BY 4.0` for Version 1.

## Split counts

| Split | Images | Labeled images | Missing label files | Instances |
|---|---:|---:|---:|---:|
| train | 4,875 | 4,875 | 0 | 62,586 |
| valid | 468 | 468 | 0 | 3,492 |
| test | 234 | 234 | 0 | 1,131 |

The validation and test instance totals match the documented controlled split. The training export is the augmented Version 1 and therefore is not directly comparable to the original 1,625-image / 11,897-instance training split.

## Mixed annotation format

The export contains both standard YOLO bounding-box rows and polygon rows. The audit therefore used a temporary read-only normalization in which polygons were converted to enclosing axis-aligned boxes only for integrity checks.

- Bounding-box rows: 65,176
- Polygon rows: 2,033
- Polygon rows by split: train 1,922; valid 79; test 32

The earlier large count of malformed rows was therefore a parser false positive and is no longer treated as evidence of corrupt annotations.

## Confirmed critical leakage

One exact image occurs in both training and test:

- train: `ppe_0466_jpg.rf.759adaad99d922ac51377c1a7c042e90.jpg`
- test: `ppe_0466_jpg.rf.5016b8e78cb2d5133da2ad72ee996e09.jpg`

The pair is identical both byte-for-byte (SHA-256) and after decoded-pixel hashing. This is confirmed cross-split leakage and blocks use of the current split for the planned cross-domain study until corrected.

## Other findings requiring adjudication

- 38 perceptual near-duplicate candidates across splits:
  - train ↔ valid: 19
  - train ↔ test: 15
  - valid ↔ test: 4
- dHash distances among these candidates: distance 0 = 8, 1 = 9, 2 = 5, 3 = 8, 4 = 8.
- 316 duplicate annotation rows, all in training, affecting 83 label files.
- 8 near-identical same-class box pairs in training with IoU ≥ 0.995.

The near-duplicate image candidates require visual/manual adjudication before deciding whether they are true leakage. The duplicate annotation rows also need source-row/provenance review because some may arise from the mixed bbox/polygon representation or from augmented images.

## Stage 2 decision for Y-PPE v1

**Do not train the new harmonized baselines on this Version 1 split yet.**

To close Y-PPE Stage 2:

1. Remove or reassign the confirmed `ppe_0466` train/test duplicate, preserving a locked test set.
2. Visually adjudicate all 38 cross-split near-duplicate candidates.
3. Review the 316 duplicate annotation rows and remove genuine duplicate objects while preserving valid distinct objects.
4. Review the 8 near-identical box pairs.
5. Re-export a corrected, frozen split and rerun the audit until there are no unresolved exact cross-split duplicates.
6. Complete the semantic geometry audit for the primary mapped classes, especially `No Hard Hat`, `No Gloves`, and `No Safety Boots`, before ontology freeze.

The present result is therefore **FAIL / CORRECTION REQUIRED**, not because Roboflow or the workflow failed, but because the audit correctly detected a confirmed train-test leak and unresolved annotation/near-duplicate issues.
