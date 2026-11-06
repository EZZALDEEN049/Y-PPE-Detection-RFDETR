# SEER-PPE — blinded double annotation and provenance protocol v0.4

**Research-only.** Never publish photos or original data by default. Pilot is a seeded, stratified sample of *original* train/valid images; membership in the 2,288-image corrected dataset has not yet been established.

## Before opening photos
1. Cross-check each Roboflow image ID, file name and split against the physical 17-class clean archive. Mark clean17 membership VERIFIED or EXCLUDED; replace excluded units using the same preregistered strata/seed before accessing final-test labels.
2. Resolve source-family ID (site/camera/video/product-photo family) and rights for *viewing* and *research analysis*. `rights_review=UNKNOWN` means reviewer circulation is NOT authorized until checked. Source & rights fields remain internal/private.
3. Verify preview does not show original GT bounding boxes or ALTAYYAR predictions to the reviewers.

## Independent annotation
- A and B separately inspect the approved image. Enumerate every visually present person, not only people detected by ALTAYYAR or labeled `Persons`.
- Record worker/bystander/unknown role; bbox when visible; evidence quality (CLEAR/PARTIAL/OCCLUDED/UNKNOWN).
- For each person, assess each predeclared PPE class: worn / not worn / occluded / not visible / ambiguous, plus whether an observed item is uniquely assigned to that worker.
- **Do not infer PPE mandate from the `No ...` object label.** Requirement `REQUIRED/NOT_REQUIRED/UNKNOWN` needs separately sourced task/site policy, unavailable policy stays UNKNOWN; do not use later adjudicated truth as a runtime input.
- Traditional attire or abaya alone is not a noncompliance judgment.
- Both annotate independently; version and preserve A, B and adjudicated decisions. Resolve disagreements with a third expert; record unresolved items explicitly.

## Completion metrics
Report number of eligible images, identified persons, unresolved ambiguous cases, A/B raw agreement and, where supported by sample size and categories, Cohen's kappa or suitable alternate agreement statistic. Cluster by source family for inference; never treat neighboring video frames as independent workers. Do not compute error rates before reviewer adjudication is complete.

## Included review files (private research package)
- `review_internal/SAMPLE_INTERNAL_RESEARCH_ONLY.csv` (strata and existing box counts; NEVER give to blinded annotators).
- `review_internal/REVIEWER_A_BLIND_QUEUE.csv` and reviewer B equivalent.
- `review_internal/WORKER_LEVEL_GT_BLANK.csv` (one seeded placeholder per image, add rows per person/PPE).
- `review_internal/SOURCE_PROVENANCE_AND_FREEZE_GATE.csv` (all unknown until verified).
