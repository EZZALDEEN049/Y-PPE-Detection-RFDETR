# SEER-PPE — complete original Roboflow Source image fingerprint audit (21 November 2026)

**Verified execution:** [GitHub Actions run 44834307184](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44834307184), job `136626717923`, **completed/success**. Code was run from commit `9720fd263fe441b2ce76b45244ce8b2e15a0b0d1`. The actual job log contains `ALL_2093_ORIGINAL_SOURCE_BYTES_HASHED_SCORING_STILL_BLOCKED`. The complete downloaded metadata ZIP was independently opened and its SHA-256 digest verified as `4303a220ef1ceb5d9c688c6a57b6b74ce1c8e53826c9b5fca52590199cb6e212` (Actions artifact **14676718549**).

## Reproducible original-source integrity findings

| Measure | Verified result |
|---|---:|
| Original Source images in **Train** | **1,625 / 1,625** |
| Original Source images in **Valid** | **468 / 468** |
| Total original images successfully downloaded and decoded | **2,093 / 2,093** |
| Missing Source files | **0** |
| Decode failures | **0** |
| Cross-split original image comparisons | **760,500** |
| Exact raw-byte SHA-256 equal Train↔Valid pairs | **0** |
| Exact EXIF-corrected RGB-pixel SHA-256 equal Train↔Valid pairs | **0** |
| 64-bit dHash near pairs at Hamming distance `<=8` | **46** |
| Distinct Valid Source IDs involved in those near pairs | **31** |
| Protected Test image sources read | **0** |

**dHash distance distribution across 46 near pairs:** 0:4, 1:3, 2:2, 3:3, 4:2, 5:6, 6:3, 7:4, 8:19.

**Scientific distinction:** Zero raw-byte/RGB matches is genuine evidence that none of the tested *Train–Valid original image pairs* is byte-identical or has exactly the same decoded, EXIF-normalized RGB pixels. It is **not** proof of source-family, capture-session, video-sequence, worksite, person or product-media independence. dHash is a coarse perceptual screen: a zero distance is **not** identical RGB, and distances above eight do not prove independent photographic origin.

## Priority human source-family triage (new AI-only single-image reviews included)

| Valid → Train | dHash | Current evidence | Decision |
|---|---:|---|---|
| `Safety-Glasses-Toolbox-Talk.jpg` → `image_719.jpg` | **0** | Earlier descriptions match worker PPE portrait; similar original framing | **High-priority candidate common portrait**, not signed |
| `Sapi 7_mp4-223.jpg` → `Sapi 7_mp4-224.jpg` | **0** | Neighboring frame numbers and previous original-image review | **Possible shared video/media sequence**, not signed |
| `images13.jpg` → `10-kv165-kavsun-brown-original-imagafu3jwrkxact2.jpeg` | **0** | New separate AI descriptions agree on brown thong sandals, dark trousers and leaf-covered pavement; 261×193 vs 300×222 | **Possible rescaled/cropped commercial photo**, not signed |
| `h20.jpg` → `h2.jpg` | **0** | New AI descriptions agree on a white helmet and a prominent `SAFETY FIRST` strap with cross symbols; different resolutions | **Possible shared product asset**, not signed |
| `fridolin_23.jpg` → `fridolin_25.jpg` | **1** | Both AI descriptions mention forward-facing tan calf, feeder arch, field fence and trees; both 480×600 | **Possible same scene/session**, not signed |
| `image_153-1-.jpg` → `image_153.jpg` | **1** | AI describes matching uniformed person with raised gloved hands, blue Indonesian sign, fence and painted curb; 640×640 vs 640×480 | **Strong shared photograph/crop hypothesis**, not signed |
| `IMG-20250416-WA0026.jpg` → `IMG-20250416-WA0079.jpg` | **1** | Existing named-site evidence already in a prior research hold | **Keep prior hold** |
| `TimePhoto_٢٠٢٤١١٠٩_١٥٢٨٢٠.jpg` → `TimePhoto_٢٠٢٤١١٠٩_١٥٢٨١٩.jpg` | **2** | Images have adjacent timestamp-style names; both AI descriptions identify same rural construction streambed with stone-carrying worker and analogous surroundings | **Strong possible shared photo session/site**, not signed |
| `image_314.jpg` → `gettyimages-173233703-612x612.jpg` | **2** | Independent AI descriptions agree on worker, crossed arms, white helmet, yellow vest, gray backdrop and Getty/iStock watermark/asset number | **Strong possible shared stock portrait**, not signed |

Additional **37** near pairs have dHash distances 3–8; all remain human-review candidates rather than confirmed image/source duplicates.

**No model inference or PPE compliance judgment** was derived from these visual descriptions. Independent **human** side-by-side inspection and photographic-source provenance evidence remain mandatory before assigning each source family. Preserve the five earlier Valid-specific research holds pending explicit reconsideration.

## Revised Valid review workload

- V05 existing unified review queue: **83** distinct Valid Source IDs.
- Near-hash scan: **31** distinct Valid IDs; **15** already present in V05 queue, **16** newly flagged.
- Distinct Valid Source IDs now requiring prioritized source-family review: **99** (`83+16`) out of 468.
- **Five** pre-existing specific Valid holds retained; **zero new automated holds**. The other **94** queued Valid images have *undetermined* source-eligibility, not a proof of independence or a newly imposed hard exclusion.
- The remaining **369** Valid IDs are not in this candidate shortlist; this alone does not prove their independent acquisition.

[Machine-readable 99-Valid-ID unified queue with all 46 original dHash pairs](SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.json) · [Human review guide](SOURCE_FAMILY_REVIEW_QUEUE_2026-11-21_V06.md).

## Boundaries and next stage

1. Have the curator compare actual original image pairs and source/session/site information. Categories: `EXACT_IMAGE`, `DERIVED_COMMON_ASSET`, `SHARED_SESSION_OR_SITE`, `DISTINCT_PRODUCT_PHOTOS`, `INDEPENDENT_PROVENANCE`, or `UNCERTAIN`; record evidence and reviewer/date.
2. Freeze chosen independent Validation subsets only **after** curator review and appropriate source-family constraints; do not change original Roboflow splits just to remove apparent overlap.
3. Finish human Person–PPE Eval review (Case B mask/boot gaps, Case D empty-person control, A–D case completeness and task policy).
4. The external scientific evaluation gate remains `scoring_ready=false` even though the full **pixel audit has succeeded**.

**Privacy/security:** No original image bytes, signed URLs, or API credentials were uploaded to GitHub. The Actions ZIP artifact contains checksum and review metadata only and has short retention; the key numerical findings and candidate queue are permanently documented in GitHub.
