# E1 historical COCO archive retrieval — 22 November 2026

## Exact source versions

Both required exports were requested directly from Roboflow and returned `ready=true` in COCO format.

| Track | Project/version | Model | Images | Train | Validation | Test | Training status |
|---|---|---|---:|---:|---:|---:|---|
| YOLOv11m | `master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh/1` | `altayyar-0oflt-lafos-qqauz-ty5nh/1` | 5,577 | 4,875 | 468 | 234 | finished |
| RF-DETR Small | `softyyemen/altayyar-0oflt-lafos-qqauz/2` | `altayyar-0oflt-lafos-qqauz/2` | 5,577 | 4,875 | 468 | 234 | finished |

Both versions record Auto-Orient, Stretch resize to 640×640, three image versions, and Mosaic augmentation.

## Export retrieval status

- Roboflow COCO export request: **ready** for both versions.
- Export URLs are temporary signed URLs and are not recorded in this repository.
- Archive download, local file integrity check, archive extraction, and SHA-256 manifests are pending.
- Do not substitute the current raw dataset versions (YOLO v2 or RF-DETR v3).
- The two exports originate from different project workspaces; matching image counts and split counts do not prove identical raw image membership.

## Next steps

1. Download both signed COCO archives in the active working session.
2. Record exact byte sizes and SHA-256 hashes for each archive.
3. Inspect archive members and COCO JSON structure without modifying source data.
4. Build per-split image manifests from the image files actually included in each archive.
5. Compare Train/Validation/Test membership and raw image hashes across model tracks.
6. Audit Test images and source-family/site/session independence.
7. Keep E1 **NOT PASSED** until all required source and split-integrity evidence is resolved.
