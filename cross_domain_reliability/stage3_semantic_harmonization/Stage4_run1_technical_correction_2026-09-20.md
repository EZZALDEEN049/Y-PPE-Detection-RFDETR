# Stage 4 Run 1 — Technical Invariant Correction

**Date:** 2026-09-20  
**Affected run:** GitHub Actions run `35476090938`  
**Scientific status:** no model training occurred; no target-test visual inspection occurred; dataset construction and audits completed before the final invariant check.

## What failed

The first Stage 4 run failed only at the workflow step `Enforce frozen ontology and split invariants`.

The failed assertion incorrectly required:

`polygon_rows_seen == polygon_rows_converted`

For Y-PPE, the harmonizer reported:

- polygon rows seen in the cleaned 17-class source: **436**
- retained shared-class polygon rows converted to bounding boxes: **309**
- difference: **127** rows

The 127-row difference is expected because Stage 4 intentionally drops annotations from native classes that are outside the frozen nine-class ontology. Polygon rows belonging to those nonshared classes must be dropped rather than converted into the harmonized derivative.

## Why this is a workflow-accounting bug, not a data-integrity failure

Before the failed invariant step, both harmonized derivatives were successfully built and passed their structural audits:

- Y-PPE-h9: critical issues = 0
- Construction-PPE-h9: critical issues = 0
- cross-split source/video group leakage after harmonization = 0 for both datasets
- frozen class order = `person, helmet, gloves, vest, boots, goggles, no_helmet, no_gloves, no_boots`
- test images were not visually adjudicated

The Y-PPE harmonized derivative retained **11,618** shared-class instances; Construction-PPE retained **9,904** shared-class instances.

## Correction applied before rerun

The harmonization script now records `polygon_rows_dropped_nonshared` explicitly. The invariant is changed to the auditable accounting identity:

`polygon_rows_seen == polygon_rows_converted + polygon_rows_dropped_nonshared`

Thus every source polygon row must be accounted for either as:

1. a retained shared-class polygon converted deterministically to its enclosing axis-aligned bounding box, or
2. a polygon annotation dropped because its native class is outside the frozen nine-class ontology.

For Construction-PPE all three polygon counters must remain zero because the official source labels are bounding-box rows.

This correction changes no ontology decision, split membership, image, retained class, target-test policy, or empirical model result. It only fixes the reproducibility gate so that it distinguishes retained polygons from intentionally dropped nonshared polygons.
