# SEER-PPE — 50-image source-family visual review and second confirmed cross-split site (v0.3)

**Date:** 2026-11-18 | **Status:** `AI_VISUAL_TRIAGE_NOT_INDEPENDENT_HUMAN_GOLD` | **Dataset and model mutation:** NONE

## Coverage
Two candidate filename groups were re-listed live from Roboflow, with IDs and native splits: **50 images** (Train **40**, Valid **7**, Test **3**). **49/50** have now been visually examined across the earlier pass and these passes: all **40 Train**, all **7 Valid**, and **2 Test** images previously inspected solely for governance. The remaining Test image **`worker wearing mask_459.jpg` was intentionally NOT viewed** in order to avoid additional test exposure. Do not claim the Test split as strictly never-viewed: two Test images were already reviewed previously for administrative purposes.

> This visual screening is limited to the **two named candidate families**, not all project images. It was performed by an AI analyst and is **not** independent human gold adjudication. No model inference, training, GT updates, or performance scoring took place.

## Confirmed named-site cross-split groups

| Named site (legible on image) | Train images confirmed | Valid images confirmed | Action |
|---|---:|---:|---|
| **مدرسة 22 مايو – عصيفرة** | **5**: `WA0067`, `WA0066(1)`, `WA0062`, `WA0050`, `WA0053` | **2**: `WA0063`, `WA0051` | HOLD both Valid images from site-independent evaluation |
| **مدرسة الشهيد العلفي** | **1**: `WA0079` | **1**: `WA0026` | **New:** HOLD `WA0026` from site-independent evaluation |

The second finding **updates** the earlier `WA0026` status (previously named site but independence unknown) to **confirmed overlap**. **Three** Valid images from the two named schools are now held, whereas the earlier report had two.

**No files are removed from Roboflow; all decisions are analytical only.** `WA0052` and `WA0054` may belong to the 22 May School construction work, but without legible unique site-name evidence they remain `site_id=null`.

## Same underlying photograph suspected inside Train

`IMG-20250416-WA0016.jpg` and `IMG-20250416-WA0078.jpg` (both Train) show nearly identical people, background and posture. The latter is lower-resolution and includes a pink mark around footwear; the former lacks that mark. This is a strong **visual derivative/near-duplicate candidate** needing content hashing or direct image comparison; **not a verified identical-byte hash**. Because both are Train, no Train→Valid leakage is established by this pair. Do **not** remove or modify either image before separate deduplication approval.

## Data-quality observations, without rights re-investigation

`worker wearing mask_535.jpg`, `worker wearing mask_178.jpg` and `worker wearing mask_335.jpg` (Train) show visible stock-watermark text. Flagging that is an image-quality/source-domain issue; it does **not** establish licensing status and does not reopen the researcher's own image authorship issue. `worker wearing mask_498.jpg` shows healthcare-type face protection outside a clear construction-work context; task domain should be separated from PPE visual recognition.

## Valid candidate eligibility status

- **Confirmed named-site hold (3):** `WA0063`, `WA0051`, `WA0026`.
- **Retained earlier source-family hold (1):** `mask_322`.
- **Unresolved possible construction-scene family (1):** `WA0033` vs Train `WA0048`; site remains unknown.
- **Unverified source independence (2):** `mask_368`, `mask_126`. Pairwise visually distinct neighbor images are not full-family clearance.

Thus **0/7 Valid candidates** from these two families are declared site-independent/scoring-ready *by this conservative screening*. This does **not** mean those images are wrong or never usable; they have not met all evaluation-entry requirements.

The saved annotation envelopes for the seven Valid images could be decoded (read-only; `annotation_valid=true`), but legacy `No ...` labels are still **not** automatically PPE absence, and stored geometry is **not** a reviewed gold reference.

## Further work beyond this checkpoint

1. Check site/session independence **outside** these two filename families; potentially related images with other names exist.
2. Perform pixel/perceptual near-duplicate audit in a controlled, reproducible manner; confirm `WA0016`/`WA0078` derivation and examine any cross-split matches across the entire project.
3. Curate an independent human-reviewed reference (person–PPE pair labels and task-required PPE policies), while preserving prior 19 approved associations and researcher `PRESENT/UNKNOWN` observations.
4. Freeze method/thresholds on eligible development data; then compare detector and SEER-PPE association outputs on a genuinely independent test partition.

**Files:** [50-image machine register v0.3](SOURCE_FAMILY_EXPANSION_2026-11-18_V03.json) | [earlier v0.2 snapshot](SOURCE_FAMILY_EXPANSION_2026-11-18_V02.md) | [read-only gate](tools/expanded_source_family_gate.mjs).

**Gate command:** `node research/seer-ppe/tools/expanded_source_family_gate.mjs research/seer-ppe/SOURCE_FAMILY_EXPANSION_2026-11-18_V03.json` (must show two named-site cross-split groups).
