# Y-PPE v2 Clean — Stage 2 Integrity / Leakage Audit Closure

Date: 2026-09-20

## Status

**CLOSED / PASS after deterministic correction + manual adjudication.**

The clean derivative is reconstructed ephemerally from immutable Roboflow Version 2. Raw images are not committed to GitHub.

## Evidence run

- Workflow: `Y-PPE v2 Clean Stage 2 Audit`
- Run ID: `35470939201`
- Conclusion: `success`
- Core audit exit code: `0`
- Explicit source-group audit exit code: `0`
- Audit artifact: `y-ppe-v2-clean-stage2-audit`
- Artifact SHA256: `cd18eb6e4afab331bdc5695072de7ae109f9c93f7f7184e6fb17862ed9ce0d66`

## Frozen clean derivative counts

| Split | Images | Labeled images | Instances |
|---|---:|---:|---:|
| Train | 1,595 | 1,595 | 11,698 |
| Validation | 459 | 459 | 3,471 |
| Test | 234 | 234 | 1,131 |
| **Total** | **2,288** | **2,288** | **16,300** |

The locked test split was preserved at 234 images.

## Corrections applied

- 39 source images excluded from non-test splits using the conservative correction manifest.
- 68 exact duplicate annotation rows removed.
- 1 confirmed near-identical duplicate annotation row removed.
- `ppe_0466` train duplicate removed while preserving the test copy.
- Cross-split source/video leakage groups (`Sapi-7_mp4`, `RPReplay_Final1667001201_MP4`, `43_MOV`) resolved.

## Post-correction audit findings

- Critical integrity issues: **0**.
- Cross-split exact byte duplicates: **0**.
- Cross-split exact pixel duplicates: **0**.
- Explicit cross-split video/source groups: **0**.
- Missing label files: **0**.
- Seven residual dHash near-duplicate candidates remain, but all seven had already been visually adjudicated in the frozen near-duplicate review as **not leakage / false positives** and were intentionally retained:
  - ND003 — different trouser products.
  - ND004 — trousers vs glove.
  - ND016 — different glove pose/gesture.
  - ND017 — different glove color/pose/subject.
  - ND019 — different goggle designs.
  - ND029 — different helmet designs.
  - ND034 — different safety-glasses designs.

Therefore the residual `issue_count=7` is non-critical and does not reopen the leakage gate.

## Scientific use rule

For all new cross-domain experiments, this clean derivative — not Roboflow Version 1 and not uncorrected Version 2 — is the reference Y-PPE source. Any future change to exclusions, labels, preprocessing, or split membership requires a documented pre-execution protocol amendment and a new integrity audit.

## Next required gate

Stage 2 integrity/leakage is closed for Y-PPE. Before harmonized training begins, complete:

1. Construction-PPE raw Stage 2 integrity/leakage audit.
2. Cross-dataset semantic geometry audit for the strict 9-class Y-PPE ↔ Construction-PPE ontology.
3. Stage 1 protocol amendments already identified (calibration support rule, safety-cost wording, and common augmentation policy).
