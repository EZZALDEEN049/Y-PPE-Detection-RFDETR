# SEER-PPE v0.5 — A/B reviewer handoff (NOT human-reviewed yet)

Current state: 30 pilot cases mapped to candidate clean17 export names, but photo identity and permission remain incomplete. A/B queues intentionally have **no original boxes, model predictions, class counts or sample strata**. Case-code lookup is analyst-only.

1. Research coordinator must privately verify source rights, photo identity and source group. Only then replace HOLD with an authorized secure, non-public image-access path. No redistribution of unknown-rights photos.
2. Select two independent qualified reviewers (A and B); prevent discussion or results sharing between reviewers until both submit. A/B queues are randomized differently.
3. Each reviewer inventories **all visible people**, including those with no `Persons` bounding-box label. For each person enumerate PPE wearing, visual observability, assignment ambiguity, role, and task-specific PPE requirement evidence.
4. Separate visually absent equipment from an adjudicated *occupational* violation. Unknown requirement => UNKNOWN/REVIEW. Cultural dress and abaya alone are never an equipment violation.
5. The coordinator checks complete inventories and compares A/B by predeclared variables. A qualified third person reviews conflicts, maintaining both original annotations and unresolved states.
6. Report raw agreement, feasible agreement coefficients and CIs at independent acquisition-group level. Do not conflate 30 deliberately enriched development images with population prevalence.

Tracker: `review_internal/REVIEW_CASE_LOOKUP_PRIVATE_v0.5.csv`; A/B queues and blank adjudication log in private Drive package. 

Completion status: A=0, B=0, reconciled workers=0; reviewed image rights=0; verified acquisition groups=0.
