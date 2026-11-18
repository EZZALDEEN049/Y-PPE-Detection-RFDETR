# SEER-PPE — Combined source-integrity gate (research safety)

**Date:** 2026-11-18 | **Status:** `PRE_SCORING_NOT_READY`

This is a **read-only analysis gate**, not a change to Roboflow. It merges:

- The **two confirmed named-school cross-split sites** in [source-family v0.3](SOURCE_FAMILY_EXPANSION_2026-11-18_V03.md), placing **three Valid images on site-overlap hold**: `WA0063`, `WA0051`, `WA0026`.
- The **two highly suspicious Train↔Valid shared-scene/derivative shoe pairs** in [project-wide triage v0.1](PROJECT_WIDE_FILENAME_COLLISION_TRIAGE_2026-11-18_V01.md), placing their **two Valid images on conservative source-integrity hold**.
- The earlier `mask_322` family-review hold remains, with `WA0033`, `mask_368`, `mask_126` still requiring source evidence. These do **not** become independent-validation-ready by being absent from an observed collision.
- The **31 exact-filename cross-split name groups**, comprising **82 image records** across the groups, are a **candidate review queue**. They are not automatically 31 duplicate events. Only the selected non-Test pairs have undergone visual examination, and one `images.jpeg` Train/Valid pair was clearly different.

## Safeguard

At this checkpoint **five specifically identified Valid images** have a strong site/source overlap hold (three from named sites plus two from visually similar shoe-source pairs). This does **not** constitute an exhaustive list of all potential holds: remaining images lack complete site/family adjudication and human ground truth. No overall validation or Test F1, mAP, Accuracy, or PPE-compliance metric is authorized by this gate.

**Run:**

```bash
node research/seer-ppe/tools/source_integrity_readiness_gate.mjs --self-test
node research/seer-ppe/tools/source_integrity_readiness_gate.mjs
```

The script reports distinct categories for *site-held*, *highly suspicious shared-scene held*, *prior family hold*, *family unknown* and *filename-only candidates*, and **always returns `model_metric_scoring_ready:false`** until a separate, fully evidenced readiness procedure is developed. This is deliberate fail-closed behavior.

Original RF-DETR, annotations, split assignments, researcher decisions, the 19 approved person-item associations, and existing Eval Cases were **not modified**. No newly inspected Test images, no new model run, no independent second human adjudication.
