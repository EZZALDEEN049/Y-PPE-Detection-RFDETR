# Frozen Stage 5 validation: exact-hash and dHash similarity preflight

**Date:** 2026-10-18. **Scope:** Y-PPE-h9-v2 and Construction-PPE-h9-v2 original **validation image files** plus train/validation SHA metadata in their existing immutable manifests. **No held-out test image or label was read**, and test was not used for training/selection or semantic adjudication.

## Immutable source metadata

| Domain | Manifest SHA-256 | Validation image files | Distinct exact-image SHA-256 in validation | Extra exact-byte train duplicates | Exact train↔validation common SHA groups |
|---|---|---:|---:|---:|---:|
| Y-PPE-h9-v2 | \`82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8\` | 356 | 356 | 1 | 0 |
| Construction-PPE-h9-v2 | \`59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14\` | 132 | 132 | 0 | 0 |

Exact-image hash overlap between the two **validation** sets was **0**. Cross-domain **Y validation ↔ Construction train** and **Construction validation ↔ Y train** exact-image hash intersection counts were also **0**. Only the manifest's frozen train/val SHA metadata was used for this comparison; no train images or held-out test images/labels were opened.

**Do not conflate with the separate original 17-class Roboflow Y-PPE export audit PR#15**, which did identify an exact train/test overlap in different exports. This note concerns the distinct harmonized **nine-class Stage 5** frozen datasets only and says nothing about that other track's held-out split.

## Visual similarity screen: 64-bit dHash, DEVELOPMENT frames only

A separate local PIL/Pillow-based diagnostic converted each validation image to 8-bit greyscale, resized to 9x8 pixels with LANCZOS, and formed horizontal-gradient comparison bits for each of the 8x8 pixel pairs; Hamming distance is the number of differing hash bits (0..64). Without looking at specific frames, the predeclared screen examined **three fixed distance cutoffs: <=0, <=4, <=8**. Counts are **image pairs**, not independent source scenes, for each comparison:

| Compared validation sets | dHash distance <=0 | <=4 | <=8 |
|---|---:|---:|---:|
| Y vs Y (within 356) | 0 | 1 | 3 |
| Construction vs Construction (within 132) | 0 | 0 | 4 |
| Y vs Construction (356 × 132) | 0 | 0 | 1 |

These are **candidate perceptual-similarity pairs, NOT verified image duplicates or site/scene matches**. dHash can match unrelated objects or miss genuinely related shots under cropping, resizing and viewpoint variation. No images/pairs were opened for qualitative adjudication and no per-image IDs/hashes/images were published.

## Provenance and scientific implications

The stage-five manifest contains \`image\`, \`image_sha256\`, \`label\`, \`label_sha256\`, \`retained_instances\`, \`split\`, but **no site/camera/video/recording/session or original capture group identifiers**. Thus:
- Exact train–validation byte overlap is **not observed**, but source-scene independence, close-frame/train-val dependence, and all held-out split independence remain **unverified**.
- Confidence-ranking AUC or image-level bootstrap CIs are descriptive *within these exported validation frames*, not valid independent-worksite generalization intervals.
- Do not infer independent sites or label validity from the absence of exact hashes or low dHash pair counts. Semantic group adjudication requires authorized private provenance and/or a reproducible image cluster policy frozen before final test.
- No final test results, energy advantage, safety adequacy or publication permissions are provided here.

This is an additional audit in support of the proposed EcoSafe limited-scope, development-only value-of-information study. Raw images, filenames, source hashes, worker faces, raw GT and model predictions are intentionally excluded from this public record.
