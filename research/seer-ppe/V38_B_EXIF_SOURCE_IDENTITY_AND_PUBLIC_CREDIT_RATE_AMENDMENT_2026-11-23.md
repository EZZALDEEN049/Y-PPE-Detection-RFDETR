# V38-B — EXIF-safe image identity and Roboflow pricing: pre-run amendment (no inference)

**Recorded:** 23 November 2026. **Author-approved manuscript title:** Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection.

## 1. Current read-only evidence

The 24 candidate IDs all occur in current project Validation and all 24 metadata dimensions match the V26 frozen selection. We then performed a read-only download of the 24 `source.roboflow.com` original JPEG files into memory on an ephemeral GitHub Actions runner, without any hosted model calls, model training, Test access, image uploads or modification of Roboflow content.

**Critical discovery:** one selected image `DDf9S1yCGLJlqesYanSY` has raw JPEG size **3840×2160** and EXIF orientation tag **6**. After `Pillow.ImageOps.exif_transpose`, its canonical decoded size is **2160×3840**, matching Roboflow metadata and the frozen V26 geometry. The remaining **23** images match V26 dimensions in raw orientation. All **24** match V26 dimensions after EXIF-aware decoding; 24 distinct raw-byte SHA-256 fingerprints were observed in the second preflight.

The failed first strict-raw-dimension audit is retained as `V38_B_CURRENT_SOURCE_READONLY_SHA256_PREFLIGHT_2026-11-23.json` with status `HOLD_CURRENT_SOURCE_IMAGE_IDENTITY_MISMATCH`. Do not hide this diagnostic. The corrected follow-up is archived independently as `V38_B_CURRENT_SOURCE_EXIF_AWARE_SHA256_PREFLIGHT_2026-11-23.json` after its workflow passes.

**Mandatory technical control before any future inference:** decode every V38-B original using `Pillow.ImageOps.exif_transpose(img).convert("RGB")`, **before** generating any grid masks or using frozen original-image target bounding boxes. At execution, check the canonical decoded RGB SHA-256 against the new frozen 24-image read-only preflight record. Reject any mismatch. Raw JPEG SHA-256 alone is not a canonical oriented-pixel fingerprint.

The V13 historical original/export comparison records only Boolean SHA-matched flags and image dimensions, and the V26 input records did not preserve source raw SHA-256. **Therefore we have NOT independently proven raw-byte identity between 2026-11-21 V26 acquisition and today's Roboflow bytes**. Current media dimensions, original-source IDs, V13 flags, current raw and canonical RGB digests provide a defensible *new execution checkpoint*, not retrospective proof of historical byte equality.

## 2. Offline numerical/mask and call-count preflight

The independent Python module `research/seer-ppe/tools/v38b_readonly_image_preflight.py` checks, without a detector:
- All 459 historical V26 rows from 12 original Validation shards and 24 selected rows.
- Exactly 24 unique frozen image IDs; 48 exact V26 prediction IDs/classes/confidence/bboxes, IoU≥0.50 to same-class current-curator GT, no V23 pilot overlap or four original V30 Valid image IDs.
- Exact grid pixel-area partition at 8×8 and 4×4, including each coarse region's four corresponding fine cells.
- 10 distinct SHA-256-seeded random 64-cell orders for each of 12 frozen targets.
- Worst-case **5,200** scientific-call plan; **800** transport retry reserve. The in-memory prototype guard reserves BEFORE an attempted call, rejects attempted call #6001 and counts failed attempts; **no hosted inference implementation is authorized or claimed finished**.
- A synthetic EXIF tag-6 JPEG proves correction changes axis order (11×7 → 7×11).
- No model weights, source annotations, split, target roster or saved scientific result was altered.

## 3. Current public posted inference rate (not a workspace billing read)

Sources reviewed 23 November 2026:
- https://docs.roboflow.com/deployment/roboflow-cloud/serverless-api/model-pricing — RF-DETR Small on Serverless Cloud API: **0.1875 credit / 1,000 model-image inferences** in the standard first-250k monthly usage tier.
- https://roboflow.com/pricing — additional prepaid credit starting **USD 4/credit**; on-demand credit **USD 6/credit**, with Enterprise or historic subscriptions possibly different.
- https://roboflow.com/credits — published rates and allowances subject to change, included/prepaid/flex consumption order, ability to disable flex overage.

At these PUBLIC, STANDARD terms, planned 5,200 image-inferences ≈**0.975 credit**; 6,000 cap ≈**1.125 credits**. Monetary *usage equivalence* if a marginal credit must be purchased: **USD 4.50 at $4/credit prepaid** or **USD 6.75 at $6/credit on-demand**; actual invoice may be zero if sufficient included/prepaid credits remain, different under plan-specific rates, or blocked when Flex billing is off. These dollar amounts are NOT an account-specific quote, purchase authorization, or verified remaining balance. The connected Roboflow tools do not expose balance or Plan & Billing ledger.

**Author action required:** visit the connected workspace's **Settings → Plan & Billing**, inspect remaining included/prepaid credits, configured Flex overage billing and RF-DETR Small inferences at that plan, then explicitly authorize both (i) up to 6,000 attempted model-image inferences and (ii) the applicable maximum financial exposure. A screenshot or account balance number can be used, but do not share payment card data or credentials.

## 4. Decision

**V38-B selection frozen; static numerical and geometry QA passed. Read-only source byte preflight must pass EXIF-aware decoding. Paid inference remains HOLD.** No author approval is inferred from approval to design experiments. A separate author-approved one-time execution authorization and hard-limit enforced **in the eventual actual runner** are prerequisites. No Test access and no claim of independent construction-project generalization.
