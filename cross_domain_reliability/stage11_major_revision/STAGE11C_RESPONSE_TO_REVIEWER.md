# Stage 11C — Response to Reviewer: Harmonization and Filtering Reproducibility

**Reviewer concern:** The exact structural exclusion criterion, overlap threshold, handling of mixed shared/unmatched labels, exclusion counts, class-distribution changes, and possible test-set selection bias were not sufficiently reproducible.

**Response:** Addressed in full.

Revisions now specify:

1. the exact 9-class source-to-canonical mapping;
2. deterministic Y-PPE polygon-to-bounding-box normalization;
3. the exact critical relationships:
   - Child→Persons;
   - No Safety Attire→Persons;
   - Soft Hat→Hard Hat/No Hard Hat;
   - none→Person;
4. the exact structural match:
   - IoU >= 0.50, **or**
   - excluded-box containment >= 0.80;
5. the exact image-membership rule:
   - exclude if harmonized-empty, **or**
   - exclude if any critical source annotation is unmatched;
6. the handling of images containing both shared and nonshared labels: they are retained unless one of the two exclusion conditions is met;
7. split-specific exclusion counts:
   - Y-PPE: 359/103/48 train/validation/test;
   - Construction-PPE: 31/2/3;
8. exclusion-reason accounting;
9. final per-split class frequencies;
10. class-support changes from the keep-all Stage 4 derivative to the final Stage 4.5 v2 derivative;
11. the interpretation that the benchmark estimates performance on a **structurally harmonizable subset**, not the full cleaned source population;
12. immutable workflow/artifact identifiers and dataset fingerprints.

The rule was frozen before Stage 5 training. Test-image pixels were not visually adjudicated for membership, and model predictions/test metrics were never used.

**Disposition:** Reviewer reproducibility objection closed.
