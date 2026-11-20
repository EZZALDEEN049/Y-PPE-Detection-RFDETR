# SEER-PPE — Direct AI visual cross-split media-family review (21 Nov 2026)

**Scope:** three selected **Train↔Valid** pairs (six original Roboflow images), including two sequences with video-like names and one named UNESCO media series. **Method:** one-image-at-a-time Roboflow vision analysis and subsequent comparison of the resulting scene descriptions; not a human side-by-side judgment and **not** pixel hashing. Test was not opened.

## Observations

| Pair (Valid → Train) | Prior cosine to exact paired Train | AI visual observations | Interpretation |
|---|---:|---|---|
| `Sapi 7_mp4-223.jpg` → `Sapi 7_mp4-224.jpg` | 0.992380 | Both show four cattle on a rural pasture, prominent tan cow facing right, palms/rustic shelter/hills; both have `BINGKENG TV` watermark, no people | Strong AI-level indication of related video frames; pixel identity **unverified** |
| `Sapi 7_mp4-42.jpg` → `Sapi 7_mp4-41.jpg` | 0.941476 | Both show a white adult cow and calves on a rural paved road with fence/trees; Valid summary detects `BINGKENG TV` watermark. Counts differ in descriptions | Plausible adjacent frames from related footage; not established exact same image |
| `UNESCO-Regional-Director-visits-some-houses-restored-in-old-Sanaa-04.jpg` → `...-03.jpg` | not in saved top-3 Train neighbors | Both depict groups with reflective/UNESCO-related clothing and traditional masonry, but the Valid scene is a smaller group under a striped canopy and Train is a larger group on an open terrace | Common named media-series hypothesis; visibly different immediate compositions according to AI summaries |

## Scientific interpretation

The first two pairs are particularly useful **candidate evidence of shared-media source between splits**; they do not automatically become 2 exact duplicates, and the three reviewed Valid images are **already included** among the earlier **83** candidate IDs. **No new distinct Valid IDs were added, and the original 5 definite research holds are unchanged**.

The cattle scenes also matter methodologically: they have **zero people in the AI descriptions** and may be deliberate **nonworker negative controls**, not mislabeled PPE scenes. A shared video source across train and validation can bias negative-control evaluation even when it is not a worker PPE case. Group-aware source controls are therefore worth planning; do not retroactively remove these source images or call them dataset errors without the original study intent.

### Evidence limitations

- Each scene description came from a **single-image vision model call**, not an independent human source-family judgment; image and watermark statements need human confirmation.
- No side-by-side pixel-level rendering was available in the current execution container, and no original Source-file SHA-256, decoded RGB hash, or dHash was calculated.
- The watermark observation is recorded only where specifically returned by the vision analysis; it is **not independently verified** for `Sapi 7_mp4-41.jpg`.
- These observations do not change the existing original RF-DETR, Roboflow labels, split assignments, or previous Person–PPE decisions, and they do **not** authorize new F1, mAP or PPE-compliance results.
- Unlike the above three pairs, the 83-image unified queue remains mostly **metadata-/embedding-triaged**, not fully visually reviewed.

### Required follow-up

1. Human side-by-side original-image and source/video-family review, specifically including the watermark and camera/background continuity, with reviewer/date and evidence.
2. Original-file SHA-256 and decoded-pixel/dHash audit on a securely obtained full Train/Valid Source-ID inventory.
3. Explicit **negative-control by source-group** sensitivity check at evaluation time if these remain in benchmark scope.
4. Do not tune any threshold on Test or use these candidates to change Roboflow splits before a documented study decision.

[Structured image IDs and separate AI descriptions](SOURCE_MEDIA_PAIR_VISUAL_TRIAGE_2026-11-21_V01.json) · [Current 83-image review queue](UNIFIED_TRAIN_VALID_TRIAGE_2026-11-21_V02.md) · [Original-source audit issue #17](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/issues/17).
