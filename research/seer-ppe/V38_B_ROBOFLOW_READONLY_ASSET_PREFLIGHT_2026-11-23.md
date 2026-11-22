# V38-B — Read-only Roboflow pre-inference availability preflight

**Date:** 23 November 2026. **Phase:** V38-B pre-registration; **no hosted model inference executed**.

## Verified connected-workspace facts

- Target project: `softyyemen/altayyar-0oflt-lafos-qqauz`. Project inspection confirms 2,327 original project images, 17 class names, and `468` currently indexed in split `valid`.
- Connected Roboflow model listing for dataset version **2** has exactly one trained model row with URL/ID `altayyar-0oflt-lafos-qqauz/2`, type `rfdetr-small`. This is the locked model identified in historical V26–V35 research records.
- Roboflow workspace read-only RoboQL: `project:altayyar-0oflt-lafos-qqauz split:valid`. Fetched three paginated metadata-only result pages, **468 unique asset IDs**, and compared all **24 frozen V38-B source image IDs** against current valid membership.
- **24/24 frozen V38-B candidate source image IDs present in current Roboflow Valid; 0 missing, 0 wrong-split.** Current project Valid has 468, while the archived V26 diagnostic ledger has 459 scored original-source Valid entries; this is not a contradiction or a new evaluation cohort.
- Preflight requested only asset IDs/split metadata. **No image pixels, face crops, detector predictions, masks, training, Test data or hosted inference were accessed**.

## What the read-only check does not prove

- Image bytes have **not yet been SHA-256 matched** against the V26 frozen image bytes; image IDs and split membership are only access/precondition checks.
- Project membership does not certify distinct construction sites, image copyright/publication rights, human-identifiable consents or external validation independence.
- The corresponding author's available Roboflow credits/cost per hosted call were not established.
- **No new V38-B performance or XAI results exist.**

## Current release gate

**Selection and budget: frozen. Candidate availability: 24/24 pass. Model identity: listed. Inference permission: HOLD.**

Before committing up to **6,000** attempted hosted model calls, complete read-only pixel/hash/geometry preflight, verify actual account costs and check execution hard-stop controls. A separate explicit author authorization of the maximum request count is required. The sample is fixed; do not replace selected targets based on an unfavorable result.

Linked manifest: [V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json](V38_B_FROZEN_CANDIDATE_SAMPLE_2026-11-23.json).  
Linked protocol: [V38_B_PROSPECTIVE_PROTOCOL_AND_6000_CALL_BUDGET_2026-11-23.md](V38_B_PROSPECTIVE_PROTOCOL_AND_6000_CALL_BUDGET_2026-11-23.md).
