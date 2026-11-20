# SEER-PPE — Unified Train–Valid source triage & pixel-audit intake (21 Nov 2026)

**Status:** `REVIEW_QUEUE_ONLY`; not pixel duplication verification and not independent-scoring clearance. The original Roboflow sources, original model, annotations and splits are unchanged. Test images, Test embeddings and Test inference were **not** accessed.

## Consolidated coverage

- Source-ID indexed **1,625 Train** and **468 Valid** images; inherited **760,500** semantic cosine comparisons (not recomputed here).
- **5** previously identified source/site-related Valid holds are **preserved unchanged**; 31 filename-collision groups remain candidate-only, not 31 duplicates.
- **7** Valid images have maximum cosine with Train ≥0.98; **52** ≥0.95. Those are visual embedding similarities, **not** proof of equal bytes, identical decoded pixels or shared capture sessions.
- Distinct Valid records requiring follow-up across known holds, family flags, exact-name collisions and cosine≥0.95: **79**. Overlap between sets is deduplicated by Roboflow Source ID; this is a **review workload**, not a leak count.

## Prioritized review workload

| Priority group | Unique Valid records |
|---|---:|
| `P0_KEEP_EXISTING_HOLD` | 5 |
| `P1_REVIEW_STRONG_EMBEDDING` | 6 |
| `P2_REVIEW_EMBEDDING` | 45 |
| `P3_REVIEW_FILENAME` | 21 |
| `P4_REVIEW_FAMILY` | 2 |

## Seven highest-ranking semantic neighbors (not confirmed duplicates)

| # | Valid source image | Nearest Train source image | Cosine |
|---:|---|---|---:|
| 1 | `v126.jpg` (`FamTszkxp5aOfuAcZwtn`) | `v125.jpg` (`ol5tvzeJJtiq9Ng0oFqC`) | 0.991050 |
| 2 | `Safety-Glasses-Toolbox-Talk.jpg` (`HRYvLu8UFRgGlQQoJN7G`) | `image_719.jpg` (`nhXMHxaCM0f7kNLOKU8Z`) | 0.998663 |
| 3 | `v141.jpg` (`V7nP50xtllhmv7ex0OZf`) | `v140.jpg` (`8vE1Ov0KTilzHRh7gtpq`) | 0.990562 |
| 4 | `cf8fc8d6c849430e927fd6fa13b6ba79.jpg` (`qBtfzUgi6Mpg3A5TE0ln`) | `cf8fc8d6c849430e927fd6fa13b6ba79.jpg` (`NAzs8sLreuFWQeOYDa2w`) | 0.980171 |
| 5 | `construction-worker-wearing-safety-equipment-19672694.jpg` (`qealvsJAhBFs6A668kak`) | `image_798.jpg` (`ngf3QT4XU6cS6p2Kegzy`) | 0.985266 |
| 6 | `h39.jpg` (`rjjkVbdcd3dCIoxywUJE`) | `h34.jpg` (`y1pL7pvPcML2CbzYYqdy`) | 0.982068 |
| 7 | `Sapi 7_mp4-223.jpg` (`sPdt3S9xyB3XzrWa3DaE`) | `Sapi 7_mp4-224.jpg` (`x4li7ZpEZqRlWEFBMom3`) | 0.992380 |

## Adjudication procedure

1. Obtain **real Source original bytes** mapped to immutable Source IDs, then run `tools/source_pixel_hash_audit.py` using the 2,093-image manifest. Check complete decoded-image coverage.
2. For each candidate retain different statuses for **identical file bytes**, **identical orientation-normalized RGB pixels**, **dHash-near appearance only**, **same scene/session**, **visually different**, or **insufficient evidence**. Do not derive verdicts from a filename or cosine threshold alone.
3. Distinguish consecutive video frame filenames (e.g. `Sapi 7_mp4-223.jpg` vs `Sapi 7_mp4-224.jpg`) as a **possible shared source sequence**, not identical imagery without review.
4. Human source and scene adjudication should be documented with reviewer, date, supporting non-sensitive evidence and uncertainty; preserve historic Confirmed Site holds unless specifically re-reviewed.
5. Keep the entire Test split outside tuning and triage. Historical governance access to two Test originals is already acknowledged; no blanket claim of untouched historical Test.
6. Read results into a research-only gate; **never** delete, reassign, retrain or relabel images as a consequence of this triage file.

[Complete de-duplicated candidate register](UNIFIED_TRAIN_VALID_TRIAGE_2026-11-21_V01.json) • [Hash tool](tools/source_pixel_hash_audit.py) • [Source-ID manifest](SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json).
