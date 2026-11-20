# SEER-PPE V06 — 99 Valid image source-family review queue (2026-11-21)

**Scope:** Curator worklist, not a dataset split change or machine proof of source-family independence. Based on [verified complete original-source audit](SOURCE_ORIGINAL_FULL_AUDIT_2026-11-21_V01.md).

## Coverage and integrity

- Original-source SHA-256/RGB/dHash audit: **2,093 / 2,093** files processed, **zero missing/decode failures**, zero cross-split byte/RGB-identical pairs.
- **46** dHash-close Train↔Valid pairs (`distance<=8`), referring to **31** unique Valid Source IDs.
- Previous queue **83** unique Valid IDs; **15** overlaps with near-hash list; **16** genuinely new Valid review candidates.
- **99 distinct Valid IDs** in [machine-readable V06 queue](SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.json); **5 pre-existing research holds retained**; no new automated holds.
- **94 other queue cases** require human adjudication but are **not classified as proven leakage or new research holds**. The **369** Valid IDs outside the queue are not source-independent-certified by their absence from the shortlist.

## Review ordering

1. **Highest priority:** Four dHash=0 candidates (worker portrait, Sapi adjacent MP4 frames, same-looking sandal product scene, same-looking white helmet/`SAFETY FIRST` product scene). Pixel SHA-256 values are **different** in all cases; their identical dHash is only a similarity clue.
2. **Very high priority:** Three dHash=1 candidates (`fridolin_23/fridolin_25` cattle outdoor scene; `image_153-1-/image_153` uniformed worker with matching signage and pose; already-held `IMG-20250416-WA0026/WA0079`), plus two dHash=2 candidates (`TimePhoto...` adjacent-second construction images and `image_314/gettyimages-173233703...` probable common stock portrait).
3. **Other dHash near pairs:** 37 cross-split pairs at distances 3–8, prioritized with historic filename/site/embedding evidence. Retain 83 older queue sources even when dHash>8.
4. **Existing five holds:** remain held until reviewed individually; lack of byte identity cannot automatically clear them.

## Required human record per pair

Retain both immutable Roboflow Source IDs, original filenames and split, old site/group decision, byte/RGB equality and dHash distance, side-by-side scene markers, source or capture-session evidence, explanation of the conclusion, reviewer and date. Allowed verdicts:

- `SAME_IMAGE_OR_DERIVATIVE`: direct evidence that images are the same photo or transformed versions
- `SHARED_CAPTURE_SESSION_OR_SITE`: related views from same project, location, camera session or video; images need not be pixel-identical
- `SAME_ITEM_DISTINCT_PHOTO`: same product but different photo with supported separate provenance
- `INDEPENDENT_SOURCE_SUPPORTED`: documented independent source/acquisition with convincing evidence
- `UNRESOLVED`: evidence insufficient

Neither different original pixels nor a larger dHash distance equals `INDEPENDENT_SOURCE_SUPPORTED`. AI one-image descriptions are **pre-reviews only**, not curator signoffs. No new human verdict was entered in this version.

**Scope of decision:** source independence for research use, not legal ownership review, model accuracy or worker PPE policy. Do not reopen the researcher's previously accepted worker-item assignments.

[Machine queue](SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.json) · [Full original audit](SOURCE_ORIGINAL_FULL_AUDIT_2026-11-21_V01.md) · [Issue #17](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/issues/17).
