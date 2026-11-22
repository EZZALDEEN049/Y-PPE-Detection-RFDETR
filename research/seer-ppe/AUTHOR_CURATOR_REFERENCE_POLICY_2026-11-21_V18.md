# SEER-PPE V18 — completed author curation accepted as primary annotation reference

**Date:** 21 November 2026. **Method:** single-curator dataset provenance, no mandatory second human reviewer.

## Author statement

> «مايحتاج مراجع بشري انا اللي اهترت الصور وقيمتها وصنفتها وضحتها وتم التاكد وفحص مل سورة قبل وبعد واثناء»

The owner states that the images were personally collected/selected, assessed, classified and checked through their fieldwork and development stages. Previous declaration: «تم مراجع كل الصور تمام». The dataset is described at aggregate level as a multi-project, multi-location collection in Yemen associated with civil-society organization projects; individual site/project names are not required for the internal image-level detection endpoint. These statements establish author-asserted completion of the original image review process. **Do not ask the owner to repeat image review, reconstruct every site name, or recruit an independent reviewer as a mandatory prerequisite.** See the V31-A3 dataset-level acquisition and curation record.

## Use existing author-curated evidence, not a fabricated new gold set

1. **Existing object-detection annotations:** original image IDs, object categories and bounding boxes annotated and quality-checked by the author may serve as the **single-curator reference** for historical *internal descriptive object detection evaluation* after exact source/label/prediction alignment. No independent second rater required. This is not independently collected, blinded or out-of-sample evaluation: acknowledge historical Validation/Test development exposure and any shared acquisition groups.
2. **Previously recorded Person–PPE observations:** preserve existing 19 manually approved Train item–person owner links and 38/42 visual entries without asking to relabel them. If a worker/PPE visual state was not individually recorded, mark it **NOT_RECORDED**. Do not infer ABSENT, PRESENT or human-reviewed UNKNOWN from a missing annotation. The four B cells and D zero-person decision in V16 are not secretly filled by this process-wide statement. Limit worker-level metrics to defensibly recorded evidence instead of re-reviewing every photograph.
3. **Actual occupational mandates and safety outcomes:** visual PPE classification is not identical to PPE requirements at a specific site/task. Policy-required gear, true occupational violation, false-clearance rates and confirmed mitigation require separate original supporting evidence. Where unavailable, report **NOT_ESTIMABLE** rather than using model negatives as true violations.

## Separate the two evaluation paths

**Path A — author-annotation-backed historical internal detection analysis:** use existing original labels as reference and fixed original RF-DETR output, check classes/IDs/boxes, report any descriptive object detection metrics only after valid paired input and denominators exist, with exposure and source-family caveats. Existing dataset curation replaces mandatory fresh per-image human gold for this *narrow* endpoint. Reuse available metadata/source-family checks; uncertainty becomes a declared limitation and sensitivity, not a demand for a complete reinspection.

**Path B — verified worker-level SEER safety and independent-source claims:** the V15 strict signed Person–PPE/source-independence protocol remains protective if these higher-level claims are attempted. These claims may be skipped or honestly narrowed rather than blocked by a requirement to recruit an additional human. A source-quality inspection by itself does not demonstrate distinct sites/capture sessions; retain the five historical holds and six technical quarantines and use SOURCE_UNKNOWN where appropriate.

This change acknowledges and accepts the owner's completed annotation and visual checking. It is **not** fabricated independent inter-rater agreement, per-image source-family independence, an all-worker PPE gold record, or proof that the detector is safer. Do not alter original model, images, labels, splits or Test. Strict verified-safety evaluation remains NOT_FROZEN with scoring_ready=false until its own evidence criteria are satisfied.

### Research methodology disclosure

The dataset reference annotations were created, selected and inspected by the same primary researcher who developed the system. This supports reproducible single-curator supervision but creates possible curation/confirmation bias; no independent second reviewer or inter-annotator reliability is claimed. Historical Test exposure, incomplete site/capture-family identification and missing worker-level mandate data must be reported separately.
