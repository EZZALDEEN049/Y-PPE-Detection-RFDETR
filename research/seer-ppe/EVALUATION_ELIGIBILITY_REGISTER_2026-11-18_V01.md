# SEER-PPE — Evaluation eligibility register (site-aware, conservative) v0.1

**Date:** 2026-11-18  
**Status:** `PRE_SCORING_GOVERNANCE_ONLY` — not a gold reference and not a completed evaluation.

## Purpose

Translate the 10 visually reviewed original images into an auditable **candidate eligibility register**, without changing Roboflow, the frozen detector, dataset annotations, or split membership. A status of `REVIEW_REQUIRED` is **not** permission to score; the absence of an observed cross-split collision does not establish independence.

## Decision rules

1. `HOLD_SITE_OVERLAP`: confirmed named site appears in Train and Valid in the inspected evidence. Exclude corresponding Valid images from **site-independent validation**, while preserving their native Roboflow split.
2. `REVIEW_REQUIRED_SITE_UNKNOWN`: source site cannot be established visually. No affirmative eligibility inference.
3. `REVIEW_REQUIRED_SITE_INDEPENDENCE`: a site is identified but a full-family Train/Valid/Test review is incomplete.
4. `REVIEW_REQUIRED_TASK_CONTEXT`: image may show a class-related visual example but lacks reliable worker/task context for per-person compliance scoring.
5. `TEST_GOVERNANCE_ONLY`: Test images were viewed for administrative/visual provenance review; not used for tuning, and do **not** qualify for a strictly never-viewed test claim.
6. `REVIEW_REQUIRED_SOURCE_FAMILY`: semantic similarity or filename family alone cannot prove either duplicate or independence.

**Gating:** `eligible_for_site_independent_scoring=false` for all rows in this *incomplete screening register*. This is an evidence-coverage flag, not a claim that all ten images are intrinsically invalid. Scoring requires verified family isolation, a completed independent human reference, frozen thresholds, and a separately documented test policy.

## Recorded decisions

| Image | Native split | Site-independent scoring now | Reason |
|---|---|---|---|
| `WA0063` | Valid | **HOLD** | Named 22 May School appears in Train |
| `WA0051` | Valid | **HOLD** | Same cross-split named site |
| `WA0067` | Train | NOT EVALUATION | Source-side member of named site |
| `WA0066(1)` | Train | NOT EVALUATION | Source-side member of named site |
| `WA0026` | Valid | REVIEW | Different named site; full independence unproven |
| `WA0035` | Test | GOVERNANCE ONLY | Site unknown, previously visually inspected |
| `mask_322` | Valid | REVIEW / PREVIOUS HOLD REMAINS | Not exact duplicate of mask_259; family not cleared |
| `mask_259` | Test | GOVERNANCE ONLY | Visually distinct; prior test exposure disclosed |
| `image_252` | Train | NOT EVALUATION | Visually distinct from mask_322, site unknown |
| `298.JPG` | Valid | REVIEW | Bare feet visible; person/task compliance and old label semantics unresolved |

The prior hold for `mask_322` is **not lifted** solely because one Test pair was found to be visually different. Prior `image_1282` annotation review remains unresolved; it is **not** among these ten visually adjudicated rows.

## Next sampling and evaluation prerequisites

- Expand the **candidate** sets `IMG-20250416-WA*` (previously 30: Train 25 / Valid 4 / Test 1) and `worker wearing mask_*` (previously 20: Train 15 / Valid 3 / Test 2), reviewing original image/site/session evidence; do not group by filename alone.
- Add `site_id`, `capture_session_id` when independently supported; use `null` for unknown, never an invented identifier.
- Run a deterministic site-family gate on the expanded register and record all `Train↔Valid`/`Train↔Test` collisions. Do not inspect additional Test images for threshold tuning.
- Select eligible **development** samples only after source independence checks; run person-to-PPE associations with `MATCHED/AMBIGUOUS/UNKNOWN` explicitly differentiated.
- Do not calculate AP, F1, Accuracy or safety-compliance rates until independent human gold adjudication and reference completeness are established.

## Provenance and safeguards

This register is derived **only** from the earlier 10-image visual adjudication, not a new Roboflow model run. Prior 19 approved links, all researcher `PRESENT` observations, all `UNKNOWN` decisions, and four `incomplete` evaluation cases remain unchanged. No dataset or model mutation, no new expert reviewer, no fabricated score.

Sources: [Visual evidence](VISUAL_SOURCE_FAMILY_ADJUDICATION_2026-11-18_V01.md), [machine-readable evidence](VISUAL_SOURCE_FAMILY_ADJUDICATION_2026-11-18_V01.json), [existing gate](tools/site_family_split_gate.mjs), [association protocol](ASSOCIATION_EVALUATION_PROTOCOL_V01.md).
