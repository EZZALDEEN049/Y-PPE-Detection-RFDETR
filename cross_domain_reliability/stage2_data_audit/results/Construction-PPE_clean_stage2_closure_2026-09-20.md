# Construction-PPE Clean Stage 2 Closure — 2026-09-20

## Status
**CLOSED — PASS**

Workflow run: https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/35473715789

## Base dataset
Official Ultralytics Construction-PPE archive, pinned through the project audit workflow.
Original split: train 1,132 / val 143 / test 141 = 1,416 images.

## Frozen conservative corrections applied
- Source-family image exclusions: **64**
  - train: 55
  - val: 9
  - test: 0
- Orphan label files removed: **10**
- Exact duplicate annotation rows removed: **1**
- Test split was preserved unchanged.

## Clean derivative
- train: **1,077 images**, 1,077 label files, 8,752 instances
- val: **134 images**, 134 label files, 1,106 instances
- test: **141 images**, 141 label files, 1,251 instances
- total: **1,352 images**, 11,109 instances

## Audit outcome
- Core audit exit code: **0**
- Critical issue count: **0**
- Explicit cross-split video/source groups: **0**
- Missing label files: **0**
- Remaining dHash near-duplicate candidates: **2** only, both Hamming distance 4.

The two remaining candidates were visually re-adjudicated after cleaning and are **false positives / not leakage**:
1. train `image682.jpeg` vs val `image852.jpeg` — unrelated workers/scenes.
2. train `image124.jpg` vs test `image140.jpg` — unrelated PPE images with similar global low-frequency appearance.

Therefore no unresolved split leakage remains under the current audit protocol.

## Freeze statement
The original official archive is not modified. The clean dataset is reconstructed deterministically from the official source using committed correction manifests and scripts. This clean derivative is the eligible Construction-PPE source for subsequent semantic harmonization and cross-domain experiments.

## Next gate
Proceed to **Stage 2C / Semantic 9-Class Harmonization Audit** before any model training. The semantic audit must confirm object definition, box geometry policy, worn/visible semantics, and missing-PPE semantics for each mapped class across Y-PPE Clean and Construction-PPE Clean.
