# EcoSafe public self-service dataset export: private import and evidence gate

**Prepared 2026-10-18. No external image download or independent experiment has occurred in this branch.** This is a no-email research route, but the dataset host may require the account holder's own Roboflow authentication. No API keys, faces, raw labels, images or source IDs should be placed in GitHub/this chat.

## 1. Choose a source and lock its VERSION BEFORE model prediction

Primary candidate page: https://universe.roboflow.com/my-workspace-adhtt/1-500-yqoby (page claims 499 images and missing-helmet/glove/boots classes); alternative https://universe.roboflow.com/qsphere/small-ppe-dataset (page claims 150 original images, potentially augmented export versions). The publisher's label list/license **do not establish per-class GT support, original image ancestry, worksite independence or benchmark rights**. Confirm actual version and original-versus-augmented counts on the downloadable version page.

Use the official Roboflow package only within the dataset access you control:

```bash
python -m pip install roboflow
# Authenticate interactively without printing or pasting an API key in the manuscript.
python - <<'PY'
import roboflow
roboflow.login()
from roboflow import Roboflow
rf=Roboflow()
proj=rf.workspace("my-workspace-adhtt").project("1-500-yqoby")
print("Inspect available dataset versions in your own Roboflow account; choose a version before any model testing.")
# After selecting a version, use: data=proj.version(YOUR_VERIFIED_VERSION).download("yolov8")
PY
```

**Do not enter a guessed version or use a convenient favorable split from a public benchmark as an independent site cohort.** For the second dataset, replace the workspace/project slug with `qsphere/small-ppe-dataset`. The export should be PRIVATE and immutable (store full archive SHA-256 and source metadata).

## 2. Review original annotation class-ID order and semantics

Read the exported `data.yaml` `names` in numeric-ID order; map exactly the native missing-helmet, missing-gloves, missing-protective-boots classes. Verify actual box extents and that visible but unannotated violation objects will not create invalid evaluation false positives. A label `no_shoes` is deliberately NOT automatically accepted as `no_boots`.

Prepare a PRIVATE JSON file with fields:

```json
{
  "reviewed_class_map": {
    "<actual native integer class ID for no-helmet>": "no_helmet",
    "<actual native integer class ID for no-gloves>": "no_gloves",
    "<actual native integer class ID for no-boots>": "no_boots"
  },
  "research_use_acknowledged": true
}
```

**The placeholder values in the example are NOT valid class IDs.** Replace them using the retrieved version's *actual YAML* after an authorized visual annotation-semantics review, not merely from the web page names. A map that is not independently reviewed may pass a basic spelling check yet still represent incompatible labels; the review status is author/steward responsibility.

## 3. Run pre-inference annotation and exact duplicate audit

```bash
python ecosafe_selective_experts/scripts/17_public_yolo_source_label_audit.py \
  --private-export-root /private/new_ppe_dataset_export \
  --private-reviewed-map /private/reviewed_map.json \
  --aggregate-out /private/new_ppe_evidence/annotation_preflight.json
```

The stdlib-only Python script checks original class-name order (`data.yaml`), image/YOLO label pairing, normalized rectangle geometry, zero-byte files, three critical GT counts, and identical byte hashes across *exported* train/validation/test splits. It reads image BYTES for hashing but does not render workers, run a detector or publish file names and original image hashes. Unsupported polygon annotations or non-rectangular geometries are blocked. The output intentionally sets `human_worksite_groups_verified:false`, `test_authorized:false`, `independent_experiment_completed:false`, `energy_measured:false`.

**Never interpret a successful local quality scan as evidence of a fresh independent test.** A positive `exact_cross_split_duplicate_sha_groups` means the source candidate needs remediation BEFORE any prospective benchmark. Even zero exact overlap does not establish non-overlap with the earlier Stage 5/6 sources.

## 4. Check historical overlap/source-family independence separately

For a rigorous external inference claim, obtain controlled original site/camera/session/family provenance and an all-split historical reference registry, and apply existing `scripts/15_external_cohort_preflight.py` to candidate vs historical **private** source-group/hashes. Ensure label definitions coincide and independent-source support spans multiple sites. Where original site IDs cannot be authenticated, report the public candidate as an exploratory **public-image robustness** collection, not independently sampled construction worksites.

## 5. Freeze, evaluate, and publish only if science gate passes

The existing `docs/EXTERNAL_CONFIRMATION_DESCRIPTIVE_PROTOCOL_DRAFT_2026-10-18.md` defines development-locked class-aware matching, fixed confidence 0.25, IoU 0.50, joint NMS 0.70, all three seeds/checkpoint factors and TP/FP/FN summaries. It is NOT automatically authorized just because the data are downloadable. Obtain actual data rights and a defensible external-safety interpretation, lock the study policy before inspecting test model outcomes, and do NOT choose the best seed/threshold retrospectively.

If the gates fail, keep the paper as an explicitly scoped **limitations and failure-mode audit** based on the completed development data. There is no scientifically acceptable shortcut through an unknown-source data mirror, extra augmentation or a newly named copy of Construction-PPE.

**Honest outcome of this turn:** import/evidence code and synthetic tests are complete, but external image access and future held-out metrics remain NOT COMPLETED. No email to a dataset author is required to use the self-service route.
