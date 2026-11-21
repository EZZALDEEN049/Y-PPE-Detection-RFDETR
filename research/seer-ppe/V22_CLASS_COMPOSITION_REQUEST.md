# SEER-PPE V22 — run read-only current original-source Validation class composition audit

**21 November 2026.** This commit triggers reproducible, **offline** analysis of the current, already author-curated **459** original Valid Source annotation count snapshots, **not** new RF-DETR model inference.

Sources are frozen `V20_VALID_SOURCE_ANNOTATION_COUNTS_PART1_PRIVATE_WORKING.json` + `PART2`, the predefined `VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json` M0/M1/M2 membership manifest, the `HISTORICAL_VALID_INTERNAL_METRICS_V20.json` reference mismatch ledger, and the author's V18 completed single-curator review decision. The scientific source-independent worker safety freeze remains `scoring_ready=false`.

The analysis must calculate exact 17-class current Saved Source object box counts and per-class image support for M0=459, M1=448, M2=367; overall model-assisted provenance marker counts (only image level, not class level); risk exclusions' effect on class and object coverage; and current/reference image counts. **Never call the 2025 historic Eval's GT identical to current source GT**, claim A5 gain, or assume any Class label `No ...` is a verified occupational violation.

No new image review, new second reviewer, original image/label/model changes or Test access. Script must fail closed on source IDs, annotation class total conservation, old Eval identity, risk flag status and unsupported independent-source claims. Reproducible output will be `VALID_CURRENT_CLASS_SUPPORT_RISK_COHORTS_V22.json`.

## CI synthetic negative-case correction

The first attempt correctly failed on a self-test fixture that *accidentally supplied a valid one-object class total*. The fixture has been made unequivocally impossible (999,999 class objects); no experiment input, model output, source ID, author annotation, risk cohort or metric was modified. This request re-runs the fixed metadata-only audit.
