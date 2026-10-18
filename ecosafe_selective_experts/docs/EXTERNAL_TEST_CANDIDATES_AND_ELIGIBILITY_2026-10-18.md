# EcoSafe independent external validation — source screening and access plan

**2026-10-18 | Screening only. No new images retrieved, no original image bytes exposed, no model evaluation, no contacted author, and no independent performance claims.**

## Source candidates checked against the EXACT three safety-negative class ontology

Research requires ground-truth object boxes directly annotating three compliance violations (`no_helmet`, `no_gloves`, `no_boots`) under geometry definitions compatible with the harmonized nine-class labels; an ordinary worn equipment box or person's bare hand is NOT silently a missing-equipment violation label. Publication license, independent original-capture families, permissions, model training source exclusion and adequate support per verified site all matter. Missing original-site metadata must not be replaced by arbitrary frame-level bootstrap groups.

| Candidate and original source | Published data | Ontology fit | Research-use/access and source-independence limits | Verdict before any inference |
|---|---|---|---|---|
| Ahmad & Rahimi, *SH17*, original authors' GitHub: https://github.com/ahmadmughees/SH17dataset ; Zenodo https://zenodo.org/records/12659325 ; journal DOI https://doi.org/10.1016/j.jnlssr.2024.09.002 | 8,099 images, 17 PPE/body part classes, CC BY-NC-SA 4.0 asserted by creators; Pexels source permissions also apply | **Does not annotate no_helmet/no_gloves/no_boots as three direct absence classes**, so it cannot supply full three-class GT FNs/recall with no new manual labeling | Downloadable, industrial scenes, but generic sites and family grouping uncertain | **NO-GO for immediate direct three-violation external confirmation**. Could be a separately scoped positive-equipment robustness benchmark, NOT equivalent test. |
| Huang et al., *Dataset of personal protective equipment*, *Data in Brief* 62 (2025), 111988; https://pmc.ncbi.nlm.nih.gov/articles/PMC12398887/ | 2,286 YOLO-annotated images; article lists 4 classes Helmet, NoHelmet, Vest, NoVest | **Only no-helmet matches a member of required trio**; missing no-gloves/no-boots | Open access article with Mendeley Data repository; rights/original image sources need per-record verification | **NO-GO for full three-critical-class evaluation**; possible helmet-only supplementary check with a separately declared limited claim. |
| Wang, Kim, Yeo & Kim, *YOLOv10-based multi-scale variant object detection for multi-category PPE non-compliance monitoring on construction sites*, *Scientific Reports* 16:24591 (2026); https://doi.org/10.1038/s41598-026-53052-y | 4,060 images five absence classes; article states a 313-image external test from 132 real-site + 181 general images and that data are **available from corresponding author on reasonable request** | **Potential** no-helmet/no-glove. *No-shoes* may NOT mean the same class and annotation extent as our *no_boots*. Requires original GT schema and manual definition adjudication; no automatic conversion. | NOT downloaded/accessible yet; current no-helmet, no-glove and no-shoes boxes and per-source group identity must be verified; the article's published external cohort itself mixes real-site and general image sources | **CANDIDATE ONLY — request access and independent capture records; no eligibility decision yet**. |
| Prior Ultralytics Construction-PPE and Roboflow ALTAYYAR exports / any remix of either | Sources already used to train/validate/test Stage 5 and previously scored in Stage 6 | Direct ontology fit only after harmonization | **Not fresh independent sources** even if repackaged in a new Kaggle/GitHub repository or shuffled | **NO-GO as new independent confirmation.** Reused analysis must be disclosed as secondary. |

The existing Stage 6 test sets are **already known to this wider project** from the preceding manuscript, and historical Stage 4.5 used test-annotation metadata for sample filtering. Repeating evaluation on these images would not constitute genuinely new independent confirmation.

## Current lead: request original study evaluation materials, without analyzing them yet

The corresponding author identified on the *Scientific Reports* article is **Juhyung Kim**; contact information is in the official paper. No email has been sent or permission assumed. A future research-use request should explain that the goal is evaluation of a **pre-existing, frozen** detector under three specifically defined absence classes, with no commercial distribution or public image uploads, and seek:

1. a permitted research copy of original 313-image external cohort (or approved separate comparable cohort), YOLO/VOC boxes, ground-truth class names and class-ID order, and exact no-shoes vs missing *protective boots* annotation definitions;
2. a source steward's private nonidentifying per-image capture-family/site/camera/session group keys and confirmation that no frames derive from the Roboflow ALTAYYAR Version 2 or Ultralytics Construction-PPE sources;
3. source-linked per-image image SHA-256 registry for exact-overlap checking, without sharing faces/identifiable workers or original image paths publicly;
4. source license/permission to analyze privately and publish **aggregated** outcomes; whether original images may appear in the paper as examples is a separate rights question;
5. proof of absence-label completeness and annotation box geometry for all three violation classes, with each appearing in multiple independently documented capture-site groups (if claiming site generalization), and a completed inter-annotator or manual consistency review if available.

**Even if these are provided**, data eligibility is not equivalent to *scientific* test authorization. The operational threshold/policy, primary inferential family and absolute safety criteria still must be frozen before the first new detector test run.

## Executable metadata-only preflight

The new `scripts/15_external_cohort_preflight.py` accepts two **PRIVATE** JSON registries: `--candidate-private` and `--historical-private`. These include a stable source group namespace, SHA-256 image hashes, original-family/site/camera/session keys, per-image three-class GT counts and explicit evidence status flags. **No image bytes or model predictions are loaded.** It refuses unknown groups, known prior-group overlap, exact image overlap, absent violation classes, insufficient multi-site support, missing source/rights attestations and post hoc model selection intent.

```bash
python ecosafe_selective_experts/scripts/15_external_cohort_preflight.py \
  --candidate-private /private/new_source_registry.json \
  --historical-private /private/all_stage5_stage6_source_registry.json \
  --aggregate-out /private/review/external_eligibility_report.json
```

Required top-level candidate flags:
`source_origin` (new unique source), `source_group_namespace` (same namespace as the historical table), `rights_review: research_use_documented`,
`object_geometry_review: confirmed_comparable_no_helmet_no_gloves_no_boots`,
`annotation_quality_review: completed_before_inference`,
`policy_lock: independent_external_confirmatory_not_used_for_model_selection`,
`historical_stage6_excluded: true`,
`original_capture_attestation: verified_with_dataset_steward`.

Each private candidate `records` row contains `sha256`, `original_family_key`, `site_key`, `camera_key`, `session_key`, and `gt_critical_count` mapping **exactly** `no_helmet/no_gloves/no_boots` to integer counts. Historical rows contain the same hash/group keys and do not require GT. Values must be **authentic**, never invented to satisfy the gate. Original reference group IDs need consistent namespaces across studies. If old site IDs cannot be mapped, the script must return BLOCKED rather than guess non-overlap.

Passing metadata preflight means only **eligible for an independent scientific protocol review**. The tool intentionally returns `claim_is_independently_validated:false` and `operational_safety_target_approved:false`. It never authorizes opening test outcomes.

## Explicit completion status

- [x] Original external candidate search and ontology-screening report.
- [x] Fail-closed new-cohort metadata checker and synthetic tests.
- [ ] Actual external image/label access permission received.
- [ ] No-shoes/boots semantic and box geometry adjudicated.
- [ ] Original image-family and site/camera source registry verified across **all** earlier used sources.
- [ ] Independent safety authority/committee defines minimum acceptable class recall and alert burden.
- [ ] Analysis/code/hardware policy and primary comparison frozen, prior to test.
- [ ] Real out-of-source evaluation with appropriate data and aggregate disclosure.
- [ ] Physically instrumented power traces, actual RAM and end-to-end latency if the paper claims sustainability.

**Conclusion:** an external dataset cannot be declared independent merely because it is downloadable or published by a different group. No stage beyond dataset-source screening has been completed in this report.
