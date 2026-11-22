# E1 historical COCO export status — 22 November 2026

## Verified export links

Both historical model-training versions have a ready COCO export. The links below are temporary Roboflow export links and are intentionally not stored in GitHub.

| Track | Exact project version | COCO export | Reported size | Status |
|---|---|---|---:|---|
| YOLOv11m | `master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh/1` | Ready | 329.326929 MB (Roboflow reported size) | User download required |
| RF-DETR Small | `softyyemen/altayyar-0oflt-lafos-qqauz/2` | Ready | 329.523979 MB (Roboflow reported size) | User download required |

## Transfer limitation

A download was attempted from the active container, but the environment could not resolve `app.roboflow.com` (DNS/network restriction). No ZIP archive was retrieved into the working filesystem. Consequently:
- no archive SHA-256 has been calculated;
- no archive members have been inspected;
- no split-level membership or raw image hashes have been compared.

This is a transfer limitation, not a Roboflow export failure. Both Roboflow exports returned `ready=true`.

## Required user action

Download both COCO ZIP archives using the fresh export links provided in the ChatGPT conversation, then upload both ZIPs into the same conversation. Do not rename the source versions in the evidence record and do not substitute current YOLO v2 or RF-DETR v3.

## Next audit steps after upload

1. Record file sizes and SHA-256 hashes.
2. Inspect archive integrity and COCO annotation JSON.
3. Extract per-split image membership.
4. Compare Train, Validation and Test membership across YOLO v1 and RF-DETR v2.
5. Compare raw image SHA-256 and decoded pixel hashes.
6. Audit Test bytes and source-family/site/session overlap.
7. Keep E1 **NOT PASSED** until the full evidence is adjudicated.
