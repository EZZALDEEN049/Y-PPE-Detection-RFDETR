# SEER-PPE — Direct original-image description + saved annotation cross-split audit (V02, 21 Nov 2026)

This is an update to [AI visual pair triage V01](SOURCE_MEDIA_PAIR_VISUAL_TRIAGE_2026-11-21_V01.md), adding **read-only original Roboflow annotation box counts** for exactly six already inspected **Train/Valid** images. No Test, no source edits, no detector inference and no new human labels.

## Newly verified saved source annotation counts

| Pair | Split | Original filename | Source `Animal` boxes | Source `Persons` boxes | Total old boxes |
|---|---|---|---:|---:|---:|
| sapi-223-224 | valid | `Sapi 7_mp4-223.jpg` | 4 | 0 | 4 |
| sapi-223-224 | train | `Sapi 7_mp4-224.jpg` | 4 | 0 | 4 |
| sapi-41-42 | valid | `Sapi 7_mp4-42.jpg` | 3 | 0 | 3 |
| sapi-41-42 | train | `Sapi 7_mp4-41.jpg` | 3 | 0 | 3 |
| unesco-03-04 | valid | `UNESCO-Regional-Director-visits-some-houses-restored-in-old-Sanaa-04.jpg` | 0 | 6 | 42 |
| unesco-03-04 | train | `UNESCO-Regional-Director-visits-some-houses-restored-in-old-Sanaa-03.jpg` | 0 | 7 | 57 |

**Distinct, supported observations:**

- All **four** inspected `Sapi 7_mp4` images have saved `Animal` annotations only: **14 total Animal boxes**, **zero `Persons` boxes** across this four-image subset. Separate Roboflow image vision descriptions show cattle and no humans in three descriptions; the fourth (`Sapi 7_mp4-41`) describes only cattle but does not explicitly state no people. Therefore **zero human source boxes is a label fact, not a certified count of all actual people**.
- The `Sapi 223/224` pair has strong common-scene visual description and the same centered `BINGKENG TV` watermark stated for both images, with prior cosine `0.992380`. The `Sapi 41/42` pair depicts related roadside cattle scenes, with prior cosine `0.941476`; individual AI count descriptions differ. Neither is a **verified pixel duplicate**.
- The named UNESCO `03/04` pair contains **7 Train and 6 Valid saved `Persons` boxes** respectively, plus many legacy PPE/absence-class boxes. The image summaries depict different group views, so they cannot be called duplicate photos based on this evidence. Old `No ...` annotations are **not** human-confirmed PPE violations.

## Research implications

Cross-split **source-media families**, including potentially deliberate **Animal / nonworker negative controls**, may affect source-independent validation or negative-control specificity. Do **not** remove cattle images or reinterpret them as mislabeled construction imagery merely because they contain no workers; the task explicitly has an `Animal` class. **Intended experimental role remains to be documented**, and the title of a media file is not human evidence of location/session identity.

These new annotation readbacks do **not** add new unique Valid candidate IDs: the earlier unified review queue stays **83**, and previously established strong-source Valid holds remain **5**. Cases remain in human source-family review and the full 2,093 original-byte SHA-256/RGB SHA-256/dHash audit is still pending.

## Method and limits

- Source images: Roboflow image IDs already in the [V01 source-media log](SOURCE_MEDIA_PAIR_VISUAL_TRIAGE_2026-11-21_V01.json); stored native `annotations_get` responses all report `annotation_valid=true`.
- Per-image vision was AI one-image-at-a-time; never called independent human pairwise signoff.
- Native source annotations describe **what was saved**, not whether PPE is correctly assigned, certified or policy-required. No Test image/embedding examined and no model performance measured.
- No original image bytes were materialized in the execution container, so cryptographic/perceptual original-image hashes remain unexecuted.
- The 19 pre-existing researcher-approved Person–PPE source-item wearer links and four incomplete Train Eval Cases are unaffected.

[Machine-readable V02 audit](SOURCE_MEDIA_PAIR_VISUAL_TRIAGE_2026-11-21_V02.json) · [Source-audit Issue #17](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/issues/17).
