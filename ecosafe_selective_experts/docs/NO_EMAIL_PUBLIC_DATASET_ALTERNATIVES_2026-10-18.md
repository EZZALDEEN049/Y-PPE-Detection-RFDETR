# EcoSafe no-email external evaluation alternative — public dataset screening

**Date: 2026-10-18. Status: source URLs/source metadata screened only; no dataset downloaded, annotated, passed as source independent, or model scored.** This replaces the misconception that we MUST email a private dataset owner to continue. **The previous Gmail draft remains UNSENT and OPTIONAL.**

## Public self-service candidate matrix — publisher pages checked

| Priority | Candidate and publisher URL | Image count shown | Safety-negative labels that already appear | License shown | Major reservations |
|---|---|---:|---|---|---|
| 1 | [1-500 by My Workspace](https://universe.roboflow.com/my-workspace-adhtt/1-500-yqoby) | **499** | `noboots`, `noglove`, `nohelmet` (also `boots/glove/safetyhelmet`) | **CC BY 4.0** per page | No dataset-description provenance or capture site groups disclosed; requires checking image family ancestry and actual annotated GT counts. |
| 2 | [Small PPE Dataset by QSphere](https://universe.roboflow.com/qsphere/small-ppe-dataset) | **150** original images on overview (page separately advertises derived checkpoint with 390 images) | `No Safety Boots`, `No Safety Gloves`, `No Safety Helmet` | **CC BY 4.0** per page | Very small, unknown class/object support and site sources; **do not conflate original 150 images with augmentation-expanded 390 model-source images**. |
| 3 — only if semantic adjudication | [Split 1 PPE DS by ppe](https://universe.roboflow.com/ppe-7cs01/split-1-ppe-ds) | **5,494** | `no-helmet`, `no-gloves`, `no-shoes` | **CC BY 4.0** per page | `no-shoes` is NOT demonstrably `no_boots` / missing protective work boots; may be a different GT task. Underlying source family/site grouping not documented in project description. |
| PRIOR used / no first-independent-test claims | [Ultralytics Construction-PPE v1.0.0](https://docs.ultralytics.com/datasets/detect/construction-ppe) or Roboflow ALTAYYAR/Y-PPE v2 | 1,416 and source Y v2 original images | Direct ontology after historical processing | Ultralytics original source AGPL-3.0, Y v2 version-specific license requires check | **Already used** to train/test Stage 5 and in separate Stage 6 prior paper; re-hosted copies cannot become a fresh independent test via new URL. |

**Sources accessed 2026-10-18**: above official Roboflow Universe project pages, original official Ultralytics dataset docs and project data lineage reports. Page-level image/ontology/license claims are **not** verification of downloaded annotation correctness, worker consent, original photographer rights or novel capture site independence.

## Preferred NO-EMAIL workflow (two distinct publication choices)

### Path A: self-service, prospective *candidate* external experiment

1. **Only if accessible under publisher terms:** use Roboflow's public dataset export/download flow (an account or authenticated Roboflow API key MAY still be required; no email to a paper author). Preserve publisher page, project version and explicit allowed research license; do not share any API credentials.
2. Privately store original downloaded JPG/PNG, YOLO annotation files, source YAML and versions. Make immutable hashes and confirm that **all three critical absence classes actually have GT instances** and reviewed box geometry. Do not claim a class is present solely because listed on the project page.
3. Independently review per-frame class completeness and no-boots box/absence semantics **without running detector model scoring**. A checked-in license does not guarantee identical label convention or complete GT of empty-looking worker areas.
4. SHA-256 and perceptual near-duplicate comparison to *all* historical Stage 5 train/val/test sources (not merely the final validation files); include re-encoded/cropped/augmented image family duplicates and assess likely source project lineage. Prior Roboflow republishes of Construction-PPE with same 11 class names are common, hence an unfamiliar title alone is NOT a fresh site.
5. Request or derive **verified** original capture family/site/camera/session IDs if possible. If absent, at most use the cohort as a **descriptive public-image robustness check**, NEVER "independent worksite confidence interval." Existing `scripts/15_external_cohort_preflight.py` will explicitly BLOCK a fresh-independent-site claim until authenticated group metadata exists.
6. Before scoring models on the newly accepted source, lock checkpoint hashes, threshold 0.25, class-aware GT IoU 0.50, fusion NMS IoU 0.70, all seeds, policies and comparator/statistical endpoints on DEVELOPMENT only. Then do a single external evaluation and transparently publish all aggregate positive and negative outcomes. No external-data-based threshold rescue.

**Under this path the proposed base choice is #1, and small #2 is an auxiliary stress check only if its original capture groups and GT support are adequate.** Do NOT simply append public images to the old test to increase nominal n without source and label adjudication.

### Path B: finish a scoped reproducibility/limits paper, NO new external test required for its basic **descriptive** claim

Do not imply site-independent generalization, safe operation or measured energy/carbon. Use all completed 2 domains × 3 seeds × 2 checkpoint policies, the true operational class-wise fusion and GT-privileged nondeployable oracle, negative confidence-routing outcomes and added false-detection burden as an honest **within-dataset failure-mode analysis**. The prior cross-domain Stage 6 model-only test exposure and historical Stage 4.5 test-label filtering are disclosed. Acceptance in a selective Q1 venue remains **unknown** and must be assessed by novel methodology and transparent limits; this path has a lower evidentiary claim but does not turn descriptive results into confirmatory science.

**Practical recommendation:** pursue Path A *screening of candidate data* while concurrently preparing Path B as the conservative fallback. Do NOT spend more CPU time training or measuring external performance until label rights/independence checks pass. The unsent message to a journal author may remain optional backup if source metadata are unavailable.

## Implemented local public YOLO evidence audit (2026-10-18)

The no-email route now includes `scripts/17_public_yolo_source_label_audit.py`, a standard-library-only PRIVATE export reader that verifies Roboflow YOLO `data.yaml` class-ID order, an explicitly researcher-reviewed three-class map, matching image and YOLO box label files, normalized bounding box geometry, class-specific GT support and exact-image hashes crossing candidate splits. It fails closed for `no_shoes` treated as `no_boots` without a separately justified ontology. It saves only anonymous counts with `independent_experiment_completed:false` and `human_worksite_groups_verified:false`. The matching **11 synthetic tests** passed in the repository CPU gate; these tests are not a real external study.

Full private export instructions and a map template are in `docs/PUBLIC_ROBOFLOW_YOLO_IMPORT_AND_TEST_EMBARGO_2026-10-18.md`. Official Roboflow Python documentation confirms an account login or API credential is generally needed for an actual version export. A connected Google Drive search found no existing `1-500` or `small-ppe-dataset` export. Hence **no new image/label bytes were obtained, no author was contacted, no new detector score was computed**, and the original site-independence gate remains unpassed.

## Status / gates

- [x] Three relevant freely listed datasets and their page-level licenses/classes were found.
- [x] Existing pre-test metadata-only eligibility code and 84 synthetic CPU CI tests available.
- [ ] Genuine public dataset archive and exact version downloaded/accessed; this has NOT occurred.
- [ ] Original image ancestry, cross-source overlap and per-class GT quality verified.
- [ ] Reliable distinct original site/camera/session grouping confirmed (if site-independent inference desired).
- [ ] Prospective analysis permission/freeze completed; no new test outcomes evaluated.
- [ ] Real wall-energy instrumentation, if sustainability is claimed.
