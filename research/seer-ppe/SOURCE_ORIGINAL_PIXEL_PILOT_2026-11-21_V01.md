# SEER-PPE V05 — first verified original-Source pixel-hash evidence (21 November 2026)

**Result:** Real original Roboflow Source bytes were accessed in a restricted ephemeral GitHub Actions runner via Source IDs; **6/6** bytes decoded and fingerprinted successfully, **three** locked Train↔Valid pairs compared. This is a material improvement on V04's AI-only source descriptions, **but it is not complete source-integrity clearance or permission to score SEER-PPE**.

## Execution evidence
- [Original-Source GitHub Actions run **44833885353**](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44833885353), successful job **136625309425**, commit `b135421b105cc7bfec9729ee7596411f8f604afd`.
- Artifact **14676968695**, exact ZIP digest `sha256:39608e279c822b841578f88a772392fb245af2db56486946cd7ff1807a2fc831`. It contains only fingerprint metadata, never original images or URLs.
- Source bytes fetched with the existing `ROBOFLOW_API_KEY` secret solely in runner memory/private transient disk. For each Source ID, checked manifest split, filename and dimensions; no Test accessed.
- Original access uses Roboflow SDK `project.image(image_id)` and its explicit original URL, not the Roboflow generated/augmented Dataset Version.

## Original byte and RGB-pixel results

| Valid ↔ Train | Raw SHA-256 equal? | EXIF-corrected decoded RGB SHA-256 equal? | dHash Hamming distance | Interpretation |
|---|---:|---:|---:|---|
| `v99.jpg` ↔ `v74.jpg` | No | No | **11** | Distinct files/pixels; source-family independence unconfirmed |
| `image_1372.jpg` ↔ `image_1342.jpg` | No | No | **29** | Distinct files/pixels; **AI-only shared-stock-image hypothesis not disproved** |
| `v16.jpg` ↔ `v15.jpg` | No | No | **18** | Distinct files/pixels; source-family independence unconfirmed |

Raw byte and RGB SHA-256 digests for all six IDs are stored in [machine record](SOURCE_ORIGINAL_PIXEL_PILOT_2026-11-21_V01.json). dHash is perceptual triage, **not** a source-lineage test; cropping, branding overlays and altered framing can materially change dHash even for shared upstream photographs.

## Preserved gates

- **6 / 2,093 original Train/Valid Source images measured**; original-byte collection for remaining **2,087** remains outstanding in this first pilot.
- **83** distinct candidate Valid source review IDs, the original **five** specific holds and the **19** human-approved worker-PPE links unchanged.
- Original Roboflow source labels, splits, model weights, saved Eval cases, and protected Test all untouched.
- No human source-family adjudication or PPE policy verdict added; `scoring_ready=false`.

Next: use the now-proven Source ID/credential path to run a coverage-verified complete Train/Valid audit, store checksum metadata without image bytes and seek human decisions on source-family implications before evaluation.

[Source-only pilot workflow](../../.github/workflows/seer-ppe-source-original-pilot.yml) · [pilot code](tools/source_original_acquire_pilot.py) · [previous checkpoint V04](DUAL_TRACK_CHECKPOINT_2026-11-21_V04.md).
