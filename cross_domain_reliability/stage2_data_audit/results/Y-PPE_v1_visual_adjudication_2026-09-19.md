# Y-PPE v1 — Visual Adjudication of Cross-Split Near-Duplicate Candidates

**Date:** 2026-09-19  
**Basis:** Stage 2 run #3 contact sheets (10 pages) plus the near-duplicate manifest.  
**Status:** visual adjudication completed for all 38 dHash candidates; provenance-sensitive product-family cases remain unresolved until source metadata is checked or a conservative grouping rule is applied.

## Summary

- 38 candidates were visually reviewed.
- **21** were judged leakage / same-source or temporal near-duplicates.
- **7** were judged not leakage (dHash false positives / genuinely different content).
- **10** remain uncertain source-family/product-variant cases.
- The confirmed exact train-test duplicate `ppe_0466` is included among the 21 leakage decisions.
- The 316 duplicate annotation-row groups are all **raw exact bounding-box duplicates**, each occurring exactly twice. They are not polygon-normalization artifacts and affect 83 training label files.

### Decisions by split pair

| Split pair | Leakage | Not leakage | Uncertain |
|---|---:|---:|---:|
| train ↔ valid | 11 | 5 | 3 |
| train ↔ test | 8 | 2 | 5 |
| valid ↔ test | 2 | 0 | 2 |

## High-priority leakage groups

1. **Same sandal photograph spans train, validation, and test**: ND001 / ND020 / ND038. Preserve the locked test item and remove/exclude matching copies from train and validation.
2. **`ppe_0466` exact train-test duplicate**: ND033. Preserve test; remove/exclude the training copy.
3. **Same boot photograph across validation and test**: ND035. Preserve test; remove/exclude the validation copy.
4. **Sapi-7 temporal leakage**: ND005 (train-valid) and ND022 (train-test) are adjacent video frames. The whole source-video group must be assigned to a single split.
5. Other same-source photographs judged leakage: ND002, ND006, ND007, ND008, ND009, ND013, ND014, ND015, ND018, ND021, ND023, ND030, ND031, ND032.

## Not-leakage decisions

ND003, ND004, ND016, ND017, ND019, ND029, and ND034 are visually different subjects/products and are dHash false positives for leakage purposes.

## Uncertain source-family cases

ND010, ND011, ND012, ND024, ND025, ND026, ND027, ND028, ND036, and ND037 are mainly helmet product/color variants with very similar templates. Contact sheets alone do not prove whether they are derived from the same source asset. Before split freeze, either verify provenance or conservatively assign the entire source family to one split.

## Annotation duplicate finding

All 316 duplicate-row groups are standard bbox rows present twice in the raw exported labels (`raw_exact_duplicate`, `occurrences=2`). Therefore the extra repeated row can be removed deterministically while retaining one copy. Prefer correcting the source annotations in Roboflow and re-exporting; otherwise use a documented post-export exact-row deduplication step.

## Required correction order

1. Freeze current test identities and remove/exclude confirmed same-source copies from train/validation.
2. Resolve the 10 uncertain source-family cases conservatively before freeze.
3. Deduplicate the 316 raw exact bbox rows.
4. Produce visual overlays for the 8 near-identical same-class box pairs and adjudicate them.
5. Re-export a corrected Y-PPE version and rerun Stage 2 until no exact cross-split duplicates remain and no unresolved source-family cases cross split boundaries.
6. Complete semantic geometry auditing for `No Hard Hat`, `No Gloves`, and `No Safety Boots` before harmonized ontology freeze.

## Pair-level decision IDs

**Leakage:** ND001, ND002, ND005, ND006, ND007, ND008, ND009, ND013, ND014, ND015, ND018, ND020, ND021, ND022, ND023, ND030, ND031, ND032, ND033, ND035, ND038.

**Not leakage:** ND003, ND004, ND016, ND017, ND019, ND029, ND034.

**Uncertain:** ND010, ND011, ND012, ND024, ND025, ND026, ND027, ND028, ND036, ND037.
