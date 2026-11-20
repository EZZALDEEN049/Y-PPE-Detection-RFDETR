# SEER-PPE — Train/Valid source-family sequence expansion (v0.2, 21 November 2026)

**Status:** `SOURCE_FAMILY_CANDIDATE_TRIAGE_ONLY`. No images, original labels, split assignments, model or Test inspected or modified. The previous five strong Valid holds remain unchanged.

## Finding: distinctive numbered media sequences cross the Train–Valid split

The existing filename-equality and cosine screens were insufficient to capture every likely related acquisition/media sequence. A new **read-only string-pattern review** of all **2,093** Train/Valid Source IDs found two distinctive multi-image stems crossing the split. The shared filename stem is a *proven filename fact*, **not** a verified identical image, shared work site, or video-frame provenance finding.

| Filename family | Train | Valid | Evidence | Action |
|---|---:|---:|---|---|
| `Sapi 7_mp4-<number>.jpg` | 5 | 4 | Distinctive MP4-like stem, including adjacent frame-number pairs 223/224 and 42/41 | Review possible same underlying video before site-independent scoring |
| `UNESCO-Regional-Director-visits-some-houses-restored-in-old-Sanaa-<number>.jpg` | 1 | 1 | Distinctive article/media stem, sequential 03/04 | Review potential common publication/media family |

Among these **five** Valid images, **one** was already in the former 79-image queue (Sapi 223), so **four additional unique Valid IDs** now enter the review queue. The source review queue therefore grows from **79 to 83 distinct Valid images**, not to 83 verified duplicate/leaked items. New source-derived membership is a *review request only*; it does not establish automatic exclusion.

## Source-index adjacency pairs

| Valid filename | Nearest numbered Train filename | Numeric gap | Max all-Train cosine (previous screen) |
|---|---|---:|---:|
| `Sapi 7_mp4-111.jpg` | `Sapi 7_mp4-125.jpg` | 14 | 0.899926 |
| `Sapi 7_mp4-60.jpg` | `Sapi 7_mp4-41.jpg` | 19 | 0.845347 |
| `Sapi 7_mp4-223.jpg` | `Sapi 7_mp4-224.jpg` | 1 | 0.99238 |
| `Sapi 7_mp4-42.jpg` | `Sapi 7_mp4-41.jpg` | 1 | 0.941476 |
| `UNESCO-Regional-Director-visits-some-houses-restored-in-old-Sanaa-04.jpg` | `UNESCO-Regional-Director-visits-some-houses-restored-in-old-Sanaa-03.jpg` | 1 | 0.816399 |

For context, `Sapi 7_mp4-60.jpg` has cosine only 0.8453 to its globally nearest Train image, yet its explicit media-sequence stem suggests a follow-up question. This illustrates why embedding similarity alone cannot certify source-family independence.

## Evidence and limits

- The numeric patterns `image_###`, `ppe_####`, `video1_###` and short arbitrary stems are **too generic** for an automatic common-video/source claim and are not promoted to named-source findings.
- `fridolin_###` has a common numeric stem across splits, but unique family semantics cannot be established from name alone; do not assert a common location.
- **No original image-byte SHA-256, decoded-pixel SHA-256 or dHash was computed** in this follow-up; missing original-pixel access remains the blocker.
- **Neither Test nor model-inference outputs were used** to tune these categories.
- Hold lists and Person–PPE decisions are untouched.

## Follow-up

Adjudicate the **shared MP4/media-source hypothesis**, record human source-evidence and verify originals once accessible. Do not combine scene-sharing with pixel-identical classification.

[Full V02 unique-ID review queue](UNIFIED_TRAIN_VALID_TRIAGE_2026-11-21_V02.json) · [Earlier V01 queue](UNIFIED_TRAIN_VALID_TRIAGE_2026-11-21_V01.md).
