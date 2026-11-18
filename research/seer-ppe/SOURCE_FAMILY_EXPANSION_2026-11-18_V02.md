# SEER-PPE — Expanded source-family inventory and review gate v0.2

**Date:** 2026-11-18. **Scope:** 50 candidate images in two filename families, not the entire project. **Status:** `PRE-SCORING / NO GOLD LABELS`.

## Live Roboflow inventory
| Candidate filename family | Train | Valid | Test | Total |
|---|---:|---:|---:|---:|
| `IMG-20250416-WA*` | 25 | 4 | 1 | 30 |
| `worker wearing mask_*` | 15 | 3 | 2 | 20 |
| **Total** | **40** | **7** | **3** | **50** |

Split assignment and image IDs were re-read via `images_workspace_search` (not inferred from file names). Native Dataset annotations for all **seven Valid images** were read without modifications; all seven annotation envelopes reported `annotation_valid=true`, which confirms readable stored geometry **not semantic correctness**.

The expanded candidate inventory contains **17/50** images visually inspected by AI across the earlier adjudication and this follow-up (**8 earlier + 9 new**). The other **33/50 have not been visually reviewed** in this workflow. Two extra Train comparator images outside the 50 were inspected, and **no additional Test originals** were viewed in this follow-up. The two Test images viewed previously for governance must still be disclosed; a strictly never-viewed test cannot be asserted.

## Review observations added in this pass

- `WA0033` (Valid) shows a worker within a stone/excavation trench; `WA0048` (Train) also shows a stone-lined trench. **POSSIBLE shared worksite/scene family, NOT CONFIRMED**. Keep `WA0033` under review; no new site ID assigned.
- `WA0034` (Train) shows a rural hut scene, visually different from the trench. `WA0030` and `WA0024` (Train) also show rural/outdoor scenes. This further demonstrates that the `WA*` stem cannot be treated as a physical site key.
- `mask_368` (Valid) and Train comparators `mask_464` and `image_782` show visually different scenes/subjects.
- `mask_126` (Valid) and Train comparators `image_719` and `mask_475` show visually different scenes/subjects.
- These pairwise visual differences reject *the inspected exact-pair duplicate hypothesis only*. They **do not establish** source-family independence over the remaining collection or clear either Valid mask image for testing.

## Valid gate (all seven candidates)

| Image | Decision | Rationale |
|---|---|---|
| `WA0063` | `HOLD_CONFIRMED_SITE_OVERLAP` | Named 22 May School seen in Train/Valid |
| `WA0051` | `HOLD_CONFIRMED_SITE_OVERLAP` | Same |
| `WA0033` | `REVIEW_POSSIBLE_SCENE_FAMILY` | Possible scene connection to Train `WA0048` |
| `WA0026` | `REVIEW_NAMED_SITE_UNCLEARED` | Different named Alalafi School, full independence unknown |
| `mask_322` | `HOLD_PREVIOUS_SOURCE_FAMILY_REVIEW` | Prior hold retained |
| `mask_368` | `REVIEW_UNVERIFIED_INDEPENDENCE` | Sample neighbor comparisons are not exhaustive |
| `mask_126` | `REVIEW_UNVERIFIED_INDEPENDENCE` | Sample neighbor comparisons are not exhaustive |

**None of the seven is declared eligible for site-independent validation at this stage.** This is a *governance gate*, not a rejection of these images as examples or as ordinary Train content.

## Annotation inventory (not adjudication)

The seven Valid images have saved person boxes (one in each except `mask_322`, which has two). Legacy negative-marker labels appear on `WA0026`, `mask_322`, `mask_368`, and `mask_126`. They are **not** ground-truth proof of PPE absence or policy violations. `WA0033` also contains polygon-shaped labels; consumers should not silently discard polygon metadata when validating geometry.

## Next technically blocked requirements

1. Review remaining 33 candidate images' source/site context, preferably prioritizing Train candidates likely to share the seven Valid locations, and record *actual* evidence rather than filename-stem grouping.
2. Finish a source/family-isolated Valid development shortlist; do not use Test to adjust thresholds.
3. Acquire an independent human-reviewed person–item reference and task policy before computing pair-level or safety-compliance metrics.
4. Only then run controlled baseline/prototype development comparisons and final test evaluation.

**Preserved:** original RF-DETR detector, all Roboflow image splits/annotations, 19 researcher-approved associations, existing `PRESENT` and `UNKNOWN` decisions, and all four incomplete Eval Cases. **No new AP, mAP, F1 or Accuracy** has been computed.

Artifacts: [JSON inventory](SOURCE_FAMILY_EXPANSION_2026-11-18_V02.json), [original visual 10](VISUAL_SOURCE_FAMILY_ADJUDICATION_2026-11-18_V01.md), [existing conservative register](EVALUATION_ELIGIBILITY_REGISTER_2026-11-18_V01.md).
