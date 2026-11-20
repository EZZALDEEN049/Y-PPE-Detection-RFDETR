# SEER-PPE — complete original Source Train/Valid hash audit request (21 November 2026)

**Authorization scope:** Read-only, for research source-integrity only, from the frozen [2,093-row original Roboflow Source-ID manifest](SOURCE_ID_MANIFEST_TRAIN_VALID_2026-11-19_V01.json): **1,625 Train + 468 Valid**. No Test originals, Test embeddings, Test predictions, training, model changes, dataset/split changes, annotation updates or Eval Case writes.

## Purpose

The successful six-image original-source byte audit [V05 pilot](SOURCE_ORIGINAL_PIXEL_PILOT_2026-11-21_V01.md) and [verified GitHub run 44833885353](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44833885353) establish that Source original bytes are accessible through the **existing repository Roboflow API secret** inside an ephemeral runner.

This request triggers the full, rate-limited original-source retrieval and pixel-hash computation with **four concurrent workers** and short bounded retries:

- Explicit Roboflow Source ID → `project.image(id).urls.original`, no generated/augmented dataset Version.
- For every original Source, compute raw SHA-256, EXIF-oriented decoded RGB SHA-256 with dimensions, and 64-bit horizontal dHash.
- Compare all **1,625 × 468 = 760,500** cross-split Train/Valid candidates, separating raw file equality, decoded-pixel equality, dHash proximity and independent human source-family review.
- Enforce zero missing/decoding failures and exact 2,093 Source coverage; incomplete retrieval cannot be passed off as success.
- Persist **hashes and comparison metadata only**, not image binaries, thumbnails, signed URLs or API keys. Original bytes live solely on the temporary GitHub runner and expire with its job.

A successful full audit still **does not** prove independently acquired source families, justify changing the five prior Valid holds or 19 researcher-signed Person–PPE wearer associations, or authorize SEER-PPE scientific metrics. Source-family human review and task-policy/reference completeness remain required.

[Full audit workflow](../../.github/workflows/seer-ppe-source-original-full.yml) · [full audit fetcher](tools/source_original_full_audit.py) · [pixel audit implementation](tools/source_pixel_hash_audit.py).

**Research scoring gate:** `false`.
