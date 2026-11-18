# SEER-PPE — Pixel-hash audit execution readiness (v0.1)

**Date:** 2026-11-19 | **Status:** `CODE_SELF_TESTED_ORIGINAL_PIXEL_HASH_SCAN_PENDING` | **No Roboflow dataset/model changes**

## Completed in this checkpoint

1. Exhaustively retrieved and compared Roboflow 768-dimensional visual embeddings for **1,625 Train** and **468 Valid** Sources (760,500 pairwise cosine comparisons), **no Test images or embeddings queried**. This is a visual *triage*, not an exact-image duplicate scan. Full evidence: [embedding report](EMBEDDING_CROSS_SPLIT_TRIAGE_2026-11-19_V01.md) and [machine register](EMBEDDING_CROSS_SPLIT_TRIAGE_2026-11-19_V01.json).
2. Saved a [2,093-item unique Source-ID manifest](SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json) from read-only Roboflow Source search. Counts: Train 1,625; Valid 468; Test 0. All IDs unique; all 468 embedding-screened Valid IDs appear in the manifest.
3. Implemented [source_pixel_hash_audit.py](tools/source_pixel_hash_audit.py) with three **distinct** signals: SHA-256 of original file bytes; SHA-256 of decoded RGB pixels (with EXIF orientation and dimensions); 64-bit dHash/Hamming nearest-neighbor candidates. The dHash threshold of <=8 is a **review queue heuristic**, not a calibrated duplicate verdict.
4. Executed the Python `--self-test` locally on synthetic images: **`SOURCE_PIXEL_HASH_AUDIT_SELF_TEST_PASS`**. It checks byte-identical copies, pixel-identical content in different file formats, Test-split rejection, and fail-closed scoring status. A separate missing-input test returned **exit code 2**, `full_2093_coverage=false`, `missing=2`, `scoring_ready=false`.
5. Cross-checked the GitHub manifest against earlier source-integrity reports: **3** named-site Valid holds + **2** suspected shared-shoe-scene Valid holds = **5 unique existing holds**; **31** cross-split filename-collision groups; **26** remaining filename-only Valid candidate IDs in the previous combined gate. Their status remains unchanged.

## Not completed — do not misreport

- The Roboflow **original image bytes were not successfully materialized** in the execution environment. Therefore **no SHA-256, decoded-pixel SHA-256, or dHash result has been computed for the actual 2,093 images yet**.
- Visual embeddings cannot establish pixel equality or guarantee independence. High similarity within a construction site, product photo category, or adjacent video frame may reflect related source material rather than identical images; low similarity does not prove independence.
- A local version-export/augmentation rendering is not automatically equivalent to each Source original. Source-specific pixel claims need access to original bytes tied to a stable Roboflow Source ID.
- No independently adjudicated full-site groups or complete person–PPE human gold labels, so **`scoring_ready=false`** for all model-performance reporting.

## Reproducible original-byte scan (once originals are available)

Install `Pillow` in the local Python environment and place image copies in **ID-indexed** folders, for example `./source-originals/train/<roboflow-image-id>.jpg` and `./source-originals/valid/<roboflow-image-id>.jpg`. The exact extension can vary. Alternatively fill each manifest row's `local_path` relative to the specified root. Do **not** match original images by filename alone, since names can collide.

```bash
python -m pip install Pillow
python research/seer-ppe/tools/source_pixel_hash_audit.py --self-test
python research/seer-ppe/tools/source_pixel_hash_audit.py \
  --manifest research/seer-ppe/SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json \
  --root ./source-originals \
  --output ./pixel_hash_audit_train_valid.json
```

The program refuses Test and unknown splits. It emits incomplete evidence with `scoring_ready=false` and exits 2 if original image coverage is incomplete; **neither a passing self-test nor 2,093 scanned images alone authorizes model evaluation**. DHash matches require visual/researcher adjudication, and a separate site/session hold-out strategy plus person–PPE reference must still be completed.

## Governing decisions

- Keep **all original splits and labels unchanged**; do not delete duplicate candidates.
- Retain five prior specific source holds and family uncertainty unless stronger evidence resolves them.
- Do not inspect additional Test originals or use Test to select thresholds.
- Preserve all prior researcher PPE-PRESENT / UNKNOWN decisions and the 19 approved person-item links; no authorship/licensing re-investigation.
