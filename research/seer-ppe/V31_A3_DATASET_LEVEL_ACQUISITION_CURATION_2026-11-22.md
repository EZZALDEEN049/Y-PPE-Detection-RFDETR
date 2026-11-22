# V31-A3 — Dataset-level acquisition and completed curation decision

**22 November 2026 · Research-methodology decision**

## Decision

Per-image identification of every worksite, project or civil-society organization is **not required** for the SEER-PPE research question. The Y-PPE corpus will be described at the aggregate level as a multi-project, multi-location field-image collection assembled in Yemen in the context of civil-society organization projects.

The researcher states that image review and curation were completed during the original database-preparation and collection phase. This is consistent with the previously accepted V18 single-curator policy. The thesis will not require reopening every photograph simply to reconstruct site names.

## Why this is academically appropriate

The study investigates PPE object detection and the development of evidence-grounded occupational-safety decision support. It does not estimate site-specific prevalence, compare named projects or organizations, or claim a representative probability sample of all Yemeni worksites. Consequently, named site/project identity is not a necessary per-image analytical variable. The corpus is an author-curated applied dataset, not a documented probability sample of all Yemeni worksites or civil-society projects; multi-project diversity must not be translated into national prevalence estimates or independent site-level generalization.

The correct disclosure is aggregate provenance, single-curator curation, and the limits of source-family metadata. Do not invent per-image project IDs or claim that every image comes from an independent site.

## What remains mandatory

Not identifying every site does **not** waive cross-split leakage control. Exact duplicates, derivatives, highly similar scenes and confirmed shared-scene/site families can inflate evaluation if related content appears in Train and Validation.

Therefore:
- Preserve the two Valid School 22 May images as hard holds because their site family is represented in Train.
- Preserve Valid WA0026 as a hard hold because the author confirmed that it shares scene content with Train WA0079 after changes/processing.
- Preserve the other eight unresolved P0 cases under their current holds/quarantines.
- Use the existing image-level detection evaluation and report M0/M1/M2 as full, high-risk-excluded and broader-risk-excluded sensitivity cohorts, without calling any cohort acquisition-independent.
- Keep source-family unknowns as unknown. The dataset-level statement does not create independent site/session IDs.
- Keep worker-level Person–PPE gold, task mandates, independent reviewer agreement and independent multi-site generalization as separate claims with separate evidence requirements.

## Accepted analysis path

1. Describe the corpus at aggregate multi-project/multi-location level.
2. Accept the original author-curated image/object review for the narrow internal image-level detection endpoint; do not repeat full-corpus review.
3. Use exact original Source ID, label and prediction joins.
4. Retain known overlap holds and report risk-sensitive cohort results.
5. State explicitly that site-independent generalization is not established.

## Author evidence

The verbatim statement and normalized interpretation are preserved in [the dataset-level attestation](evidence/AUTHOR_DATASET_LEVEL_ACQUISITION_AND_PRIOR_CURATION_2026-11-22.md), SHA-256 `201e16d8c24a0704fedab42ecccdc0fe5caf8a0abef205951bcf73f1ebdb901c`. The decision is also represented in [the machine-readable V31-A3 record](V31_A3_DATASET_LEVEL_ACQUISITION_CURATION_2026-11-22.json).

**Result:** per-image site identification is removed as a blanket prerequisite for internal image-level analysis; no known overlap hold is released and no independent-source claim is added.
