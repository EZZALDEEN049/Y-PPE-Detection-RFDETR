# SEER-PPE — Whole-project exact-filename collision triage (metadata, not duplicate proof)

**Date:** 2026-11-18 | **Scope:** Live project `softyyemen/altayyar-0oflt-lafos-qqauz` metadata inventory of **2,327** images; no Roboflow changes.

## Enumeration
- **Train:** 1625; **Valid:** 468; **Test:** 234.
- All 2327 unique image IDs were paginated in 10 RoboQL pages (250/page except final).
- **64** repeated exact-filename groups (case-insensitive NFC normalized), including **31** groups whose filename appears across two or more splits.
- **Do not equate a matching filename with a duplicated image**, or a unique filename with independence. `images.jpeg` illustrates a false name match; some unique-looking hashes do correspond to the same source scene.

## Visually inspected non-Test pairs

| Exact shared filename | Native splits | Outcome | Action |
|---|---|---|---|
| `cf8fc8d6c849430e927fd6fa13b6ba79.jpg` | Train/Valid | Very similar tan boot + identical-looking indoor background, but boot placement/processing differs | `HIGH_VISUAL_SHARED_SCENE_OR_DERIVATIVE_CANDIDATE`; HOLD Valid for independent validation |
| `d3febe75f2cb4cb5875ff430dcdb2b95.jpg` | Train/Valid | Same tile/door and shoe context, slight variation in the shoe representation | `HIGH_VISUAL_SHARED_SCENE_OR_DERIVATIVE_CANDIDATE`; HOLD Valid |
| `images.jpeg` (one selected Train/Valid pair) | Train/Valid | Train shows a portrait, Valid shows animals; visually different | This **pair** disproves duplicate-by-name assumption, without clearing the other four images sharing this name |

No exact pixel hash was computed. These are AI visual observations for source-family screening, **not independent gold judgments**. The two suspect Valid images are **additional candidate holds**, separate from the three Valid school-site holds documented in [site-family v0.3](SOURCE_FAMILY_EXPANSION_2026-11-18_V03.md). Cross-group duplicate removal or split changes were **not performed**.

## Interpretation and follow-up

- The 31 cross-split name-collision groups require risk-prioritized review or image-hash/perceptual matching; their presence does **not** prove 31 leaks.
- Other visually related images may have completely different names. Therefore filename screening is a *candidate generator*, not a held-out readiness pass.
- Continue with a full-project source-family registry and a source-independent development/validation selection, while keeping **Test sealed for tuning**. Existing historical visual exposures to two Test images must be disclosed.
- The per-person PPE association ground truth still needs independent human review before reliable F1/mAP or compliance scoring.

Machine-readable collision groups, split IDs and the three reviewed pairs: [JSON](PROJECT_WIDE_FILENAME_COLLISION_TRIAGE_2026-11-18_V01.json).

**Preservation:** model, annotations, splits, prior 19 approved links, researcher observations, and Eval Cases were not modified. No new model metrics were calculated.
