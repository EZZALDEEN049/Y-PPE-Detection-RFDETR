# V31-A2 — Author confirmation of shared scene with modifications: WA0026 / WA0079

**22 November 2026 · Human source-scene attestation recorded.**

The dataset author clarified that Validation `IMG-20250416-WA0026.jpg` and Train `IMG-20250416-WA0079.jpg` are **not the same presented image; they represent the same scene with changes and processing**.

## Source pair

| Split | Original filename | Source ID | Existing disposition |
|---|---|---|---|
| Valid | `IMG-20250416-WA0026.jpg` | `yeEvdkqXtNgsj7PZFDvI` | Historical hard hold retained |
| Train | `IMG-20250416-WA0079.jpg` | `xyKCHH49Xr7oCONLC9nN` | Train comparison member |

**Verdict:** `SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING`  
**Scene-family ID:** `scene_wa0026_wa0079_modified_processed`

The response does not claim byte identity, an exact unmodified source frame, a known crop/export chain, or a shared capture-session ID. No capture session or site ID is inferred. The previous visual triage for WA0026 records the visible school name **مدرسة الشهيد العلفي**; that remains contextual evidence for the Valid image, not a new site attestation for the Train record.

## Existing technical corroboration

The frozen pair comparison recorded SSIM **0.93240**, **756** ORB good matches and **751** inliers; raw bytes were not identical. This supports the need to preserve the cross-split overlap hold but is not treated as independent proof of image lineage.

## Scientific handling

- WA0026 remains excluded from source-independent Validation scoring because the author confirms shared scene content with Train WA0079 after changes/processing.
- Its pre-existing historical hard hold is preserved; no hold is released.
- The pair is not treated as independent scene/source families.
- No exact-frame, crop-chain, capture-session or acquisition-date claim is made.
- No original image, annotation, split, model, Test asset or Roboflow record is modified.

## Evidence and verification

The verbatim author response and normalized interpretation are preserved in [the SHA-pinned evidence record](evidence/AUTHOR_CHAT_ATTESTATION_WA0026_WA0079_SHARED_SCENE_2026-11-22.md).  
SHA-256: `d75d626a38c65c3b81c74b7619e5ceae38fb38d30de2d910dea76129d9c706d7`

The hash protects the stored transcription's integrity; it is not an independent identity credential or proof of truth.
