# Stage 3 - Semantic Harmonization Audit

This stage decides whether the proposed nine-class Y-PPE <-> Construction-PPE mapping is semantically defensible before any harmonized training.

## Audit rule
A mapping is accepted only when object/state definition and bounding-box extent are sufficiently comparable across datasets. Similar class names alone are not evidence of equivalence.

## Leakage protection
Visual sampling uses only training and validation/calibration splits. Test images remain unopened in this audit.

## Evidence bundle
The workflow generates one contact sheet per candidate shared class, a deterministic sample manifest, class-level geometry statistics, annotation-format counts, and a review template. Red boxes are the target class; blue boxes are person boxes. Each panel includes a zoom view for small PPE regions.

## Candidate ontology
The initial nine candidate mappings are person, helmet, gloves, vest, boots, goggles, no_helmet, no_gloves, and no_boots. `No Safety Vest`, `no_goggle`, and `none` are excluded from the shared ontology unless later evidence justifies a new mapping; no such inference is made by default.
