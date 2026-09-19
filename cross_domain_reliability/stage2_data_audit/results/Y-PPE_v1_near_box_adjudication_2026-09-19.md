# Y-PPE v1 — Near-Identical Bounding-Box Adjudication

**Date:** 2026-09-19  
**Source:** Stage 2 run #4 overlay bundle  
**Status:** all 8 reported near-identical same-class box pairs visually adjudicated.

## Decision

All **8/8** cases are duplicate annotations of the **same object/region**, not two distinct nearby objects. In every case, both boxes have the same class and IoU >= 0.995, and the overlay shows the boxes occupying effectively the same object extent.

The correction rule is deterministic: **retain the first reported row (row A) and remove the second reported row (row B)** for each case. These eight removals are separate from the previously identified 316 raw exact duplicate rows.

| Case | Class | IoU | Keep | Remove |
|---|---|---:|---:|---:|
| NB001 | Animal | 0.996364 | row 1 | row 2 |
| NB002 | Safety Vests | 0.996667 | row 10 | row 11 |
| NB003 | Gloves | 0.995556 | row 1 | row 2 |
| NB004 | Safety Vests | 0.995968 | row 13 | row 14 |
| NB005 | Gloves | 0.995455 | row 6 | row 7 |
| NB006 | Safety Vests | 0.996149 | row 1 | row 2 |
| NB007 | Safety Vests | 0.995708 | row 1 | row 2 |
| NB008 | Gloves | 0.996979 | row 5 | row 6 |

## Annotation-cleanup total now confirmed

- 316 raw exact duplicate bbox rows: remove one extra copy per group.
- 8 visually confirmed near-identical duplicate-object boxes: remove row B in each case.
- **Total confirmed annotation-row removals: 324.**

No correction has yet been applied to the source Roboflow dataset. These decisions belong in the correction manifest for the next clean/frozen export.

## Remaining blockers before Y-PPE Stage 2 can close

1. Resolve or conservatively group the 10 provenance-sensitive helmet/product-family cases that remain uncertain.
2. Apply the confirmed file-level leakage corrections, including whole-video grouping for the three explicit cross-split video groups.
3. Apply the 324 confirmed annotation-row removals.
4. Recover or reconstruct the original pre-augmentation 1,625-image training source set, or otherwise document the source-level identity of the 4,875 augmented training images before making the strongest leakage claim.
5. Complete semantic geometry review for `No Hard Hat`, `No Gloves`, and `No Safety Boots` before freezing the 9-class harmonized ontology.
6. Re-export and rerun Stage 2; only a corrected audit should be used as the basis for the harmonized baseline experiments.
