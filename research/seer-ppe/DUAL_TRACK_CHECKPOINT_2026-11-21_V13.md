# SEER-PPE V13 checkpoint — direct photo-content verification and source evidence

**Completed 21 November 2026.** A 16-image direct photo pilot and then **all 459 candidate Valid→Clean17 pairs** ran against the actual source/export media, with both ends individually checked against their historical frozen SHA-256. All 459 scored high technical content-consistency, with minimum gray SSIM 0.90624, median 0.98079 and maximum normalized RGB MAE 0.03084. No missing images, Test decoding, retraining, new model inference or source/Eval writes.

A separate original Train↔Valid audit examined **76 original Source images** across **50 candidate comparisons** (46 old close pairs + four named-site School 22 May edges). It yielded **7** strong same-frame *technical candidates* and 43 not strongly pixel-aligned; none proves source independence. Of seven high candidates, two remain existing holds, four were retained Clean17 images already flagged but not formally held, and one was historically excluded. No automatic new holds or signed human source-family verdicts were entered.

Person–PPE still contains 19 human-approved links and 38/42 recorded worker visual states; exactly four Case B fields and a human zero-person signoff for D remain outstanding. The [V13 recording packet](PERSON_PPE_PENDING_HUMAN_SIGNOFF_2026-11-21_V13.json) captures gaps without assigning guessed statuses or redoing accepted image reviews.

The original model and source/image labels/splits were not modified. Protected Test image bytes were not opened or scored. The V11 evaluator can now verify the V13 evidence-based source→Clean17 technical matching instead of relying on the V12 unsigned candidate flag, but its source-family, person-level GT and signed Validation-freeze gates remain closed. **`scoring_ready=false`.**

[Full direct Valid/Clean17 results](ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json) · [Original cross-split evidence](DIRECT_ORIGINAL_TRAIN_VALID_SOURCE_EVIDENCE_V13.json) · [V13 detailed report](DIRECT_IMAGE_AND_SOURCE_EVIDENCE_REPORT_2026-11-21_V13.md).
