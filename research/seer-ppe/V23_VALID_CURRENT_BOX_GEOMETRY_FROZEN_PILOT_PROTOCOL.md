# SEER-PPE V23 — FROZEN current original-source Valid box evaluation PILOT (not a population estimate)

**Frozen before querying hosted model predictions:** 2026-11-21. Original model remains the previously trained RF-DETR Small `altayyar-0oflt-lafos-qqauz/2`, with the Roboflow project `softyyemen/altayyar-0oflt-lafos-qqauz`. This **read-only exploratory, already historically exposed Validation pilot** does not meet the independently signed source-worker safety gate and must not be used to tune Test or claim an SEER policy gain.

## Selection policy fixed BEFORE new prediction results

Take the first five lexicographically sorted **original Source image IDs from M2's 367 unflagged but source-independence-uncertified Valid IDs**, as recorded in the untouched [V19 source risk JSON](VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json). These five were selected solely from existing Source IDs and current annotation metadata, **not** based on model prediction correctness or appearance. They are not a random sample or a representative prevalence sample. Their original Source files and present annotation object count are:

| Source ID | Original filename | Current Source boxes | Valid status |
|---|---|---:|---|
| `07BnOpgFJyNaOhuzvh5i` | `image_1282.jpg` | 13 | valid, M2 unflagged uncertified |
| `084u5kuwQXhWa4EKdsQ5` | `5731201_4.jpg` | 1 | valid, M2 unflagged uncertified |
| `09WO3iVNf9jOt21QAxmb` | `c1e5a26df8225afb5be5beceae128ad5.jpg` | 3 | valid, M2 unflagged uncertified |
| `0ABzMrjnd6I0Ws6FH7qo` | `imagem40.jpg` | 5 | valid, M2 unflagged uncertified |
| `0aGYjxE5LmocXyvuLHs8` | `a16ea468abd845e68ea9ccbbe4f9762e.jpg` | 1 | valid, M2 unflagged uncertified |

**Current saved author-reference object counts = 23 across 5 originals.** No image needs to be visually checked again by the author; no second reviewer. Roboflow `annotations_get` supplies current native bbox geometry; the prior author curation is accepted. Fail closed if any source ID, source filename, width/height, stored box count, annotation validity, split, original model ID or settings mismatch.

## Pre-fixed inference and matching criteria

1. Retrieve only these **five original Source Valid** media URLs via read-only `images_workspace_search` with exact filenames and confirm native Source IDs. Do not query Test, any original image outside the five, or derivative generated export JPEGs. Do not persist original image bytes or transient media URLs in GitHub.
2. Call `models_infer` once per exact Source ID using unchanged original `model_id=altayyar-0oflt-lafos-qqauz/2`, **confidence floor 0.20**, **overlap 0.50**. The returned object class and original-space `x,y,width,height` boxes are the only model observations.
3. Map each current Source `annotation.boxes` `label, x,y,width,height` (or stored enclosing bbox for polygon annotations) to the same original pixel coordinate system; confirm all positive dimensions.
4. On each image, sort all predicted class boxes descending by confidence; greedily match only to the as-yet-unused ground truth of **the same exact 17-class name** with maximum bbox IoU ≥ **0.50**; a reference/prediction may match at most once. TP, FP and FN sum micro across all five, with precision `TP/(TP+FP)`, recall `TP/(TP+FN)`, F1 `2TP/(2TP+FP+FN)`; undefined denominators are null. No posthoc confidence optimization or per-class performance promise.
5. Preserve per-image counts, original Source IDs, model identity, settings, request date and aggregate counts in an artifact, with **nonrepresentative Valid pilot, historically exposed original model, single-curator reference, no source-independent evaluation, no worker-compliance claims**.
6. **Legacy V20 stored provider metrics are untouched** and are not substituted for newly returned prediction geometry. Actual P/R/F1 on the five are a descriptive current-source implementation check, **not a new SEER-PPE safety gain**, COCO mAP, independently valid generalization or full 459 current-label benchmark.

## Explicit scientific firewall

No retraining; no original image, label, split or model alteration; no Test; no new PPE mandate inference; no complete worker-level source reviewer signatures; no electrical energy or XAI; no SEER A5-vs-A2 inference; strict independent source and worker safety `NOT_FROZEN/scoring_ready=false`. These five Valid originals become explicitly **V23 development-exposed pilot IDs** and must not be represented as prospectively unseen in any later current-reference analysis. Their size and deterministic selection provide only pipeline feasibility.

**Completion criteria:** signed-by-computation provenance checks + five valid real model inference responses + five current saved original author annotations + a deterministic re-entrant numeric scorer and successful GitHub CI. If any prediction service or Source geometry is unavailable, report the failure, do not fabricate results or silently loosen thresholds.
