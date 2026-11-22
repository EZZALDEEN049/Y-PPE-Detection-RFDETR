# V38-B — Prospective no-inference execution implementation and JPEG payload amendment

**Recorded:** 23 November 2026. **Target journal:** Results in Engineering.  
**Exact approved paper title:** Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection.

## Phase status

- **Frozen sample:** unchanged 24 original Valid image IDs, 48 fixed detection targets across 11 PPE categories, as archived in `V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json`.
- **Historical numerical findings:** V26–V37 unchanged; no model weights, labels, splits, annotations, worker-level compliance definitions or protected Test images modified.
- **Author screenshots:** Research Plan 50 included credits/month; 2.49 credits used this November 2026 cycle; arithmetic monthly allowance headroom 47.51 credits at snapshot. This is NOT authorization to run paid inference.
- **New V38-B hosted detector calls thus far:** **ZERO**.

## Read-only input and transport QA

1. `fetch_v38b_originals_cloud.py` reads only the 24 frozen source originals to a temporary directory, with raw-byte SHA-256, EXIF-corrected pixel SHA-256 and exact image dimensions compared against the 24-image read-only identity archive. No credential, training or model inference required. One EXIF orientation-6 photo is transposed before masks are made. No source-image bytes may be committed/uploaded.
2. `run_v38b_xai.py --preflight --images-dir ...` checks all 24 inputs through the EXACT image loader intended for the paid runner and refuses any altered JPEG or orientation/coordinate mismatch. The same runner's `--self-test` uses two synthetic targets and a fake predictor, with **378 mock calls**, 24 11-point curves (8×8: saliency and 10 seeded random orders, 4×4: saliency, both deletion/insertion), all gray/blur-fill cell maps and diagnostics. It records each attempted call before use and rejects duplicate-run ledger paths, failures, and cap overshoots.
3. The hosted transport uses a single directly issued standard HTTPS POST per model image through Python stdlib, with automatic redirects and application-level automatic retries DISABLED. Each attempt is written to append-only JSONL and `fsync` occurs before the request. A mocked HTTP 503 and a mocked 200 response test both make **exactly one POST attempt** without network access. Model endpoint: `https://serverless.roboflow.com/altayyar-0oflt-lafos-qqauz/2`; confidence=20%, overlap=50%, identical to fractional 0.20/0.50 historical method.
4. **Execution safety:** no live inference can be started without an existing separately author-approved, exact-manifest-SHA-bound one-time authorization JSON (`approved_by_author`, exact intended=5,200, max=6,000 attempts, no Test/training, fixed wire encoding, and specified credit exposure), an explicit `--confirm-authorized-max-attempts 6000` CLI flag, matching 24 image pixel SHA values and an empty run ledger. No paid GitHub Actions workflow has been created or triggered.
5. Prospective sample decisions and experimental arm counts remain unchanged: **1,920** direct gray cell maps, **48** original/blurred baselines, **2,376** 8×8 progressive saliency/10 seeded random arms, **216** 4×4 saliency curves and **640** 8×8/4×4 blur-fill alternative maps; planned max **5,200 calls**, 800 **technical-only** headroom, hard **6,000** attempts inclusive of failures; implementation deliberately has **no automatic retry**, so the reserve is not spent automatically.

## PNG payload limit discovery and prospective method amendment

Zero-model-call GitHub image fetch and wire-size benchmark over the **same 24 current original JPEGs** found:

- Largest uncompressed-source-derived PNG encoded payload: **26,239,500 bytes** (about 26.24 MB); **1/24** original photos exceeded the runner's defensive 15 MiB payload cap. A PNG-only transport would therefore abort before useful science could complete.
- Re-encode the same EXIF-corrected original RGB images as **JPEG quality 95, 4:4:4 subsampling, optimize=False**: maximum measured size **9,183,493 bytes**, **0/24** exceeding 15 MiB on the unperturbed images. Pixel geometry, class boxes and masks are NOT resized.
- **Prospectively amended wire representation:** Every original baseline, blurred endpoint, gray/blur-filled single-cell map, deletion/insertion cumulative-mask image, 8×8/4×4 grid, and random comparator will use the same frozen JPEG quality=95 4:4:4 settings *for every image and trial*. Use a strict 15 MiB payload cap and abort with an explicit logged failure if any perturbed image exceeds it; do not silently resize, reduce quality, use per-image file formats or omit targets.
- **Research limitation:** JPEG is lossy. Fixed high-quality compression is a common transport choice, but it can influence sensitivity scores, especially fine boundaries; this is a potential perturbation-compression interaction. The design should disclose wire encoding under Methods and treat results as measured under this transmission setup. V30/V33 historical PNG results are NOT silently pooled; V38-B is a distinct prospectively amended diagnostic replication.
- No image inference has been performed under this amendment. A current image-canonical SHA check does not prove historical V26 image byte identity (historical raw hashes unavailable); the newly archived source hashes act as the baseline for future replication.

## Limitations and remaining approval

- Synthetic/mock tests are **not** an end-to-end verification of paid hosted model responses; actual target reproduction and confidence drift may fail (pre-specified ±0.08 baseline gate), and such failures must be reported, not replaced by another target.
- Valid cohort remains development-exposed and source-family independence NOT VERIFIED. Real worker PPE compliance, external generalizability and energy savings cannot be inferred.
- Public RF-DETR Small serverless tariff (~0.1875 credit per 1,000 model-image inferences) implies around **0.975 credits** for 5,200 calls and **1.125 credits** for 6,000 calls at standard rates; provider plan-specific rates or billing may differ. User screenshot headroom 47.51 credits supports capacity but does not authorize spending.
- **Remaining gate:** author explicitly approves the one-time V38-B attempt cap and account credit exposure. Only thereafter create the one-time authorization record, perform a final read-only manifest/image/available-credit check, and launch one supervised run with numeric-only evidence archiving and no automatic retry.

**Scientific operations verdict:** software and read-only source identity gate tested. **PAID MODEL INFERENCE: NOT AUTHORIZED / NOT STARTED.**
