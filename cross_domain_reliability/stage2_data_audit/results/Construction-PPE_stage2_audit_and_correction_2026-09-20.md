# Construction-PPE Stage 2 audit and conservative correction plan — 2026-09-20

## Source frozen
- Official Ultralytics Construction-PPE archive: `construction-ppe.zip` from Ultralytics assets release v0.0.0.
- Archive SHA256 observed by the workflow: `bef8dcb599aa4e9d9f5e602cb6fa7143d3c84d7f6a0ff40463d7f2a4c2632ccc`.
- Official YAML pinned to Ultralytics commit `42044baf5eda3d52aa4bd7d8a098375d2c7fdad7`.
- Original split counts: train 1,132; val 143; test 141.

## Audit findings
- 1,416 images total; every image has a paired label file.
- 11 classes and 11,521 object instances in the official split.
- 10 critical orphan label files in `labels/train` with `(1)` suffixes and no matching image stem.
- 1 exact duplicate annotation row in `labels/train/image187.txt`.
- 76 dHash cross-split near-duplicate candidates: 21 train↔val and 55 train↔test.
- Visual adjudication of all 19 contact-sheet pages: **74 leakage/source-family pairs** and **2 false positives** (`ND015`, `ND030`).
- No explicit filename-derived cross-split video groups were detected.

## Conservative correction policy
The official test set is preserved unchanged. All train images implicated in visually confirmed leakage are excluded. For train↔val source-family findings, the implicated validation representatives are also excluded because the same staged source families visibly occur in the test split even when dHash > 4. This avoids validation-mediated source leakage while retaining a fixed test set.

Planned exclusions: **64 images** (55 train, 9 val, 0 test).
Projected cleaned split: **train 1,077 / val 134 / test 141 = 1,352 images**.
Projected instance counts after image exclusions and exact-row deduplication: **train 8,752 / val 1,106 / test 1,251**.

The 10 orphan labels are removed because they have no corresponding image and cannot constitute valid training examples. The duplicate annotation row is reduced to one copy. Raw official source data are not overwritten; the cleaned derivative is reconstructed deterministically.

## Remaining limitation
Construction-PPE does not provide verified project/video/source-group metadata for every image. Therefore the cleanup is a conservative visual/perceptual source-family audit, not a claim of exhaustive provenance reconstruction. This limitation must be stated in the manuscript.

## Gate
Do not use the cleaned Construction-PPE derivative for experiments until the deterministic clean audit returns: critical issues = 0 and core audit exit code = 0. Non-critical dHash candidates may remain only if visually adjudicated as not leakage.
