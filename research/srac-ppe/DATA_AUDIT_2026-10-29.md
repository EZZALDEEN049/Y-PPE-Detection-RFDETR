# Reproducible, read-only Y-PPE-h9-v2 archive audit

**Date:** 2026-10-29. **Archive:** `Y-PPE-h9-v2_RFDETR_Roboflow.zip`, accessed through the researcher's connected Google Drive and mounted in the analysis session. **No private images are published in this repository.**

## Checks actually executed
- `manifest.jsonl` SHA-256 equals `PACKAGE_MANIFEST.json.manifest_sha256`: **PASS**.
- Each of the **1,778** image+label SHA-256 pairs matches the corresponding manifest record: **PASS**.
- YOLO label format/class/coordinates and split file pairing checked for **1,778** images: **PASS**.
- Exactly identical image bytes across train/valid/test split boundaries: **0 groups**.
- Exactly identical image bytes duplicated within a split: **1 group in training**. Needs curated handling before re-training; no direct cross-split exact-byte leakage was found.
- **Perceptual** 64-bit dHash screening with Hamming distance <=4: train–test **0**, valid–test **0**, train–valid **2 candidate pairs**. Candidate pairs are **NOT** proof of source/scene leakage; a zero count also cannot rule out same-scene video frames.

| Split | Images | YOLO objects | Person boxes | Images with person label | no_helmet boxes | Images with no_helmet |
|---|---:|---:|---:|---:|---:|---:|
| train | 1236 | 6656 | 1298 | 688 | 113 | 88 |
| valid | 356 | 2122 | 383 | 196 | 40 | 27 |
| test | 186 | 693 | 121 | 91 | 14 | 12 |
| **total** | **1778** | **9471** | **1802** | **975** | **167** | **127** |

The test includes **14 no-helmet boxes in 12 images**, not 14 independent, adjudicated occupational PPE violations. `person` and `no_helmet` co-occur in all 12 of those test images, without proving unambiguous worker assignment or helmet-required context.

## Update: more sensitive overlap audit
The first-stage dHash<=4 screen is **not sufficient** to certify scene independence. A second pHash<=8 screening followed by visual review identified **four train–test related pairs (3 distinct test images)** and **two train–validation related pairs (2 distinct validation images)**. See [scene audit](SCENE_LEAKAGE_AUDIT_2026-10-29.md) and [candidate exclusion list](QUARANTINE_CANDIDATES_2026-10-29.csv). The split independence gate remains **OPEN**, and the ZIP remains unchanged.

## Geometric association feasibility, **GT-box-only diagnostic**
Using a heuristic top-40%-of-person-bounding-box head ROI with ±5% padding, assigning each `no_helmet` box *center* to GT person boxes produced:
- train: 107 unique / 4 unmatched / 2 overlapping multiple workers (113 boxes);
- valid: 39 unique / 1 unmatched / 0 ambiguous (40);
- test: 13 unique / 0 unmatched / 1 ambiguous (14).

**This is a feasibility test of geometry using ground-truth boxes only, not accuracy of the learned detector or the deployed worker association algorithm.** It cannot prove occupational violation status.

## Sources and limitations
- ZIP manifest gives class order `person, helmet, gloves, vest, boots, goggles, no_helmet, no_gloves, no_boots`.
- Manifest's `val` split maps to ZIP directory `valid`, accounted for in integrity comparison.
- Any prior claim about verified scene-level leakage must be reproduced via source/group metadata and independent visual adjudication; dHash<=4 is an incomplete screen.
- Model identity `altayyar-0oflt-lafos-qqauz/2` is a separately trained **17-class** model. This nine-class archive is not automatically a model-independent external test.
- No new RF-DETR inference, fresh risk-calibration trial or end-to-end performance estimates were conducted by this audit.

## Mathematical calibration feasibility (research-planning only)
At δ=.05 and 2 risk families × 9 fixed thresholds, minimum independent confirmed violations to support FC<=5% if at most k FC errors are observed: 115 at k=0, 159 at k=1, 196 at k=2, 231 at k=3, 296 at k=5. The analogous requirements for UC<=15% are 37, 51, 63, 74, 95. Checked numerically against SciPy Clopper–Pearson Beta quantiles. These calculations do not establish empirical risk control.
