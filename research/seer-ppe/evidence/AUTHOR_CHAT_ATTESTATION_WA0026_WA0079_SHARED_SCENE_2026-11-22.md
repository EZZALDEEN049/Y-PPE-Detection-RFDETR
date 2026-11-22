# Author chat attestation — WA0026 / WA0079 shared scene with modifications

**Record date:** 2026-11-22  
**Project:** SEER-PPE / Y-PPE-Detection-RFDETR  
**Attestation channel:** Direct response by the dataset author in the active project conversation.

## Question put to the author

"هل الصورتان WA0026 (Validation) وWA0079 (Train) تمثلان نفس الصورة الأصلية/نسخة منها، أم نفس المشهد مع تغييرات ومعالجات، أم مشهدين مختلفين؟"

## Author's response (verbatim as typed)

"ليس نفي الصورة وانما نفس المشهد مهع تغيرات عليه ومعالجات"

## Normalized interpretation

The response is interpreted as: **"ليست الصورة نفسها؛ وإنما المشهد نفسه مع تغييرات ومعالجات."** This normalization corrects apparent typing slips for readability; the verbatim response above is preserved unchanged.

## Source records

| Split | Original filename | Source ID | Clean17 export |
|---|---|---|---|
| Valid | IMG-20250416-WA0026.jpg | yeEvdkqXtNgsj7PZFDvI | IMG-20250416-WA0026_jpg.rf.a3294f67d828b9a7fd892bc2820063c9.jpg |
| Train | IMG-20250416-WA0079.jpg | xyKCHH49Xr7oCONLC9nN | Not a Clean17 Validation export |

## Human verdict and limits

**Verdict:** `SHARED_SCENE_WITH_MODIFICATIONS_OR_PROCESSING`  
**Scene-family ID:** `scene_wa0026_wa0079_modified_processed`

The author confirms that the two records represent the same scene content with changes and processing. This is a cross-split shared-scene relationship and is not evidence of independent Validation provenance.

The attestation does **not** claim that the two files are byte-identical, the exact same unmodified photograph, a known crop of one particular original file, or from one identified capture session. No capture-session ID is supplied. The existing visual triage for WA0026 records visible text identifying مدرسة الشهيد العلفي; this prior label is retained as context, not expanded into a separate new site attestation.

The prior direct technical comparison recorded gray SSIM 0.93240, 756 ORB good matches and 751 inliers, while raw bytes were not identical. Those measurements are corroborating technical context only; they do not independently establish the human source lineage.

## Research consequences

- Keep Valid WA0026 excluded from source-independent scientific scoring because its scene content is shared with Train WA0079 after modifications/processing.
- Preserve its pre-existing historical hard hold; this attestation does not release it.
- Do not treat the Train and Valid records as independent scene/source families.
- Do not infer an exact source-frame identity, crop lineage, capture session, or acquisition date.
- Do not change original images, annotations, split membership, Roboflow records, model weights, or Test data.

## Evidence integrity

The repository SHA-256 pins this transcription's integrity; it does not independently authenticate the author's identity or prove the truth of the statement.
