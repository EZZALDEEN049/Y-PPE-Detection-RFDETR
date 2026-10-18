# EcoSafe / Stage 5 exact dataset lineage, source licensing and test-selection audit

**Documented:** 2026-10-18. **Scope:** source and split provenance of the pre-existing nine-class Stage 5 datasets used by EcoSafe. This is an evidence reconciliation of original repository freeze records and currently documented source material; no model evaluation or test-image inspection was conducted for this note.

## 1. The original image collections ARE identified

**Y-PPE (research project source):** Roboflow workspace/project `master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh`, **Version 2**, `yolov11` export, project label **ALTAYYAR**. The reproduction script downloads this exact version via a private `ROBOFLOW_API_KEY` from `cross_domain_reliability/stage5_in_domain_baselines/prepare_stage5_frozen_datasets.py`. Original 17 native classes, including `No Hard Hat`, `No Gloves` and `No Safety Boots`, are harmonized to the final nine-class ontology. **Do not confuse** original **Version 1** (augmentation-expanded training source; its export reported `CC BY 4.0`) with the **Version 2** actual input. The public redistribution license applying specifically to Version 2 must be confirmed with the Roboflow project owner/source version; do not automatically transfer Version 1's license claim to Version 2.

**Construction-PPE (published upstream collection):** Ultralytics **Construction-PPE v1.0.0**, from https://docs.ultralytics.com/datasets/detect/construction-ppe and https://github.com/ultralytics/assets/releases/download/v0.0.0/construction-ppe.zip. The project's source-metadata freeze pins Ultralytics YAML commit `42044baf5eda3d52aa4bd7d8a098375d2c7fdad7`, source archive SHA-256 `bef8dcb599aa4e9d9f5e602cb6fa7143d3c84d7f6a0ff40463d7f2a4c2632ccc`, and license **AGPL-3.0** as reported by the official Ultralytics dataset page. Original 11 classes include `none` and `no_goggle`, omitted in the strict shared nine-class mapping. Cite the original dataset as Ultralytics / Dalvi, Singh, Bhingarde & Chalke (2025), *Construction-PPE: Personal Protective Equipment Detection Dataset*, v1.0.0, as the official publisher requests.

**The user's clarification (2026-10-18)** reports legitimate ordinary study/research use. Record that self-report accurately: it does not establish independent site capture metadata or guarantee unrestricted public redistribution of all source images.

## 2. Fully reconciled preprocessing and dataset selection

All counts are IMAGE COUNTS, never detection boxes or independent field sites. Original source and successive **pre-model-training** derivatives are intentionally different populations.

| Stage and split | Y train | Y val | Y test | Construction train | Construction val | Construction test |
|---|---:|---:|---:|---:|---:|---:|
| Original publisher / Roboflow Version 2 source | 1,625 | 468 | 234 | 1,132 | 143 | 141 |
| Stage 2 conservative cleaned source | 1,595 | 459 | 234 | 1,077 | 134 | 141 |
| Stage 4 first strict nine-class harmonization | 1,595 | 459 | 234 | 1,077 | 134 | 141 |
| **Stage 4.5 label-completeness filtered, final Stage 5 / EcoSafe h9-v2** | **1,236** | **356** | **186** | **1,046** | **132** | **138** |

Stage 2: Y-PPE excluded **39** images (30 train, 9 val, test 0), removed 68 exact and one near-identical duplicate annotation row, and resolved three known filename-inferred source-media cross-split group collisions in the clean Version 2 derivative. Construction Stage 2 excluded **64** images (55 train, 9 val, test 0), removed 10 orphan labels and one duplicate annotation row, with 74 visual source-family candidate pairs treated as leakage and two judged nonduplicates.

Stage 4: retained the cleaned image membership, mapped original 17/11 classes into exactly `person,helmet,gloves,vest,boots,goggles,no_helmet,no_gloves,no_boots`; source Y polygons were converted to enclosing axis-aligned bounding boxes when their class was retained. Stage 4 harmonization alone left some images with nonshared annotations only.

Stage 4.5: **before Stage 5 model training**, an annotation-only label-completeness policy excluded any image that (a) would become empty after nine-class mapping or (b) had a critical unmatched excluded-source annotation. It applied **to train, validation AND test** with a frozen, deterministic rule based on native annotation metadata/geometry. Exclusions: Y **510** total = **359 train + 103 val + 48 test**; Construction **36** = **31 train + 2 val + 3 test**. The protected original test image **pixels** were not visually opened to design the policy; model predictions were not consulted.

**Important interpretation correction:** Stage 2 preserved the original test split, but Stage 4.5 **did not preserve its full membership**. The final Stage 5 and EcoSafe tests are **pretraining, annotation-filtered held-out subsets**, not pristine originals. Membership selection consumed original test-label metadata (but not model predictions or performance) prior to freeze. The paper MUST state this to avoid calling test "untouched by any processing" or overgeneralizing performance to all original publisher images. The test population is conditioned on structural harmonizability, possibly different in prevalence and difficulty across domains.

**Selection rates relative to the Stage 2 clean derivative:**
- Y: 359/1,595 train (22.51%), 103/459 val (22.44%), **48/234 test (20.51%)**;
- Construction: 31/1,077 train (2.88%), 2/134 val (1.49%), **3/141 test (2.13%)**.
These rates differ dramatically across the two source domains, which is another reason not to infer an unbiased raw-source or site-level comparison.

## 3. Immutable primary Stage 5 derivative fingerprints

| Final dataset | Expected SHA-256 manifest | Train / val / test |
|---|---|---|
| `Y-PPE-h9-v2` | `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8` | 1,236 / 356 / 186 |
| `Construction-PPE-h9-v2` | `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14` | 1,046 / 132 / 138 |

The safe, prior validation-only bundle `ecosafe-frozen-validation-splits.zip` was locally SHA-256 verified as `5337fb80a7e74bbb56ebed497d56f129d5020efff1c36540d74095f2823ae1d7`. It contains exactly 356/132 val images and corresponding labels, with no final test images. Current EcoSafe work did not add another training dataset or open held-out test images to select a policy.

## 4. What split-independence evidence DOES and DOES NOT establish

**Known, audited controls** (see Stage 2 clean closure and Stage 4 closure): exact-byte/pixel train/validation/test overlap resolved under the frozen source-level audit; explicit video filename family overlap was removed where the source-media token allowed a defensible ID; remaining dHash candidates were adjudicated; final validation ZIP has no within-domain or cross-domain identical image hashes. Source capture/test-label **metadata** was used during historical preprocessing as declared above.

**Unresolved:** original capture `worksite_id`, session/camera/video identity for EVERY original image, external image family relations not expressed in filename, and independent-site stratification of the final test. Across the **356 Y validation images**, only **one** name exposes an explicit `_mp4`/`_mov` media-frame token recognized by the previously written Stage 2 checker; **none** of 132 Construction validation filenames does. This is **low coverage**, not evidence that 355/132 others are independent. A source publisher, not an arbitrary regex, must supply original group data for worksite-independent inference.

**Research claims permitted NOW:** use exact public/research-source identities and pretraining correction history; report class-aware developer-set results from the 488 final validation frames; state previous audits' bounded leakage checks. **Not justified:** unconditional independent-site claims; original full-dataset performance; untouched-original-test language; Q1 readiness; model safety or energy/carbon savings.

## 5. Primary code and documentary evidence (previously committed, independently checked)

- `cross_domain_reliability/stage2_data_audit/results/Y-PPE_v2_stage2_audit_and_correction_2026-09-19.md`
- `cross_domain_reliability/stage2_data_audit/results/Y-PPE_v2_clean_stage2_closure_2026-09-20.md`
- `cross_domain_reliability/stage2_data_audit/results/Construction-PPE_source_record_2026-09-19.md`
- `cross_domain_reliability/stage2_data_audit/results/Construction-PPE_clean_stage2_closure_2026-09-20.md`
- `cross_domain_reliability/stage3_semantic_harmonization/Stage4_harmonized_dataset_freeze_closure_2026-09-20.md`
- `cross_domain_reliability/stage4_5_label_completeness/Stage4_5_label_completeness_protocol_2026-09-20.md`
- `cross_domain_reliability/stage4_5_label_completeness/Stage4_5_conservative_adjudication_decision_2026-09-20.md`
- `cross_domain_reliability/stage5_in_domain_baselines/prepare_stage5_frozen_datasets.py`
- `ecosafe_selective_experts/results/FROZEN_DATA_AUDIT.md`
- Official Construction collection and reuse attribution: https://docs.ultralytics.com/datasets/detect/construction-ppe

**Policy:** No source-image binaries, worker faces, test labels, filenames, private access keys or per-image predictions are committed by this report. Final evaluation must use a prospectively frozen analysis plan and acknowledge pretraining test annotation filtering.
