# SEER-PPE V15 — evidence-pinned per-image source-family and Person–PPE reviewer signoff

**21 November 2026. State: executable evidence verification; NOT human-certified, NOT a Validation scoring freeze.**

V14 already completed all **99 flagged original Valid Source IDs** against **280 candidate Train pairs** and linked all **459 corrected Clean17 Valid** files to original image content. Because cross-split site and capture-session families are not established by low image similarity, **no** Safe-for-Science Validation subset can be declared without acquisition evidence and signed individual decisions.

## A single source-specific signoff record (future, authored by an actual reviewer)

Append a decision to [the intentionally empty source family overlay](SOURCE_FAMILY_SIGNED_ATTESTATIONS_V15.json), identifying exactly the frozen **Original Valid Source ID, original filename, Clean17 export filename, reviewer and date**, personal examination of this original source image, evidence location, **pinned SHA-256 of that evidence file**, and verdict (INDEPENDENT_SOURCE_SUPPORTED / SHARED_CAPTURE_SESSION_OR_SITE / SAME_IMAGE_OR_DERIVATIVE / SAME_ITEM_DISTINCT_PHOTO / UNRESOLVED). A claimed independent source additionally needs a **specific site ID, capture session ID, acquisition family ID, a signed completed crosscheck against Train site/session families, a no-overlap rationale, and a second evidence-file SHA pin**. Evidence file content and signer's truthfulness require genuine human review; the software only checks integrity/structure and refuses absence.

The **5 historical holds** and **6 high technical-overlap quarantines** remain hard-blocked even if someone writes an ordinary independent-source assertion; a separate documented conflict resolution/release procedure is necessary. Signed decisions for other sources are marked **HUMAN_ATTESTED...NOT_FROZEN**, not automatically scored.

## Minimal remaining Train-only Person–PPE signoff

[The intentionally empty Train-person attestation overlay](TRAIN_REFERENCE_SIGNED_ATTESTATIONS_V15.json) supports exactly **four** `B` worker visual states (`P001/P002 × face_mask/safety_boot`) and one human review decision for `D` (confirm zero visible persons or not-confirmed). `UNKNOWN` is a valid **human-signed** response where visibility is insufficient, but it may **not** be auto-filled from AI descriptions. Every entry must contain the actual Roboflow Case ID + case revision, reviewer/date, original-image observation attestation and SHA-pinned evidence reference. No existing Roboflow Eval Case is edited by this software. Previous A/C signatures are retained; new B/D signatures are still **zero**. Even all five Train-only decisions would not constitute human **Validation** labels.

## Freeze lock and test protection

[The V15 executable gate](tools/compile_v15_source_qualification_and_ppe.mjs) joins the full corrected Valid Source-ID crosswalk with direct V13 file-content evidence, V14 quarantine and the two author-signed overlays, then audits **459 rows**. `--self-test` creates *synthetic-only* good/bad signed evidence and verifies collision, missing evidence, malformed attestation, false PPE labels and Test Source-ID injection fail closed. `--audit <output>` produces a non-scoring cohort readiness ledger. `--gate` refuses to exit successfully until source, complete independently reviewed **Validation** Person–PPE reference and the frozen authorized protocol are all genuinely in place.

No model retraining, Test inference, annotation edits, source splits or actual scientific accuracy/XAI/energy scoring is performed. The current result is intentionally **0 eligible images and `scoring_ready=false`**. A passing engineering CI run attests that blocking works, **not** that the master’s thesis experiment is finished.
