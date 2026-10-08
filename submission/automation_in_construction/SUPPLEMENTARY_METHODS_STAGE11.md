# Supplementary Methods — Expanded Reviewer-Remediation Version

## S1. Source datasets and final harmonized derivatives

### Y-PPE source
Original localized source:
- 2,327 annotated images;
- 16,520 annotated instances;
- 17 source classes.

### Construction-PPE source
Ultralytics Construction-PPE v1.0.0:
- 1,416 source images;
- 11 source classes.

### Final shared ontology
The exact canonical order used for every Stage 5–11 experiment is:

0. person
1. helmet
2. gloves
3. vest
4. boots
5. goggles
6. no_helmet
7. no_gloves
8. no_boots

| Canonical class | Y-PPE source label | Construction-PPE source label | Decision |
|---|---|---|---|
| person | Persons | Person | accept with normalization |
| helmet | Hard Hat | helmet | accept with normalization |
| gloves | Gloves | gloves | accept with normalization |
| vest | Safety Vests | vest | accept with normalization |
| boots | Safety Boots | boots | accept with normalization |
| goggles | Goggles | goggles | accept with normalization |
| no_helmet | No Hard Hat | no_helmet | accept with normalization |
| no_gloves | No Gloves | no_gloves | accept |
| no_boots | No Safety Boots | no_boots | accept with normalization |

Excluded:
- Y-PPE No Safety Vest: no direct no_vest counterpart.
- Construction-PPE no_goggle: no explicit Y-PPE no_goggles counterpart.
- Construction-PPE none: no direct semantic equivalent.

The negative-state labels are dataset-defined visual states. Their presence does not, by itself, establish that a PPE item was normatively required in every depicted scene.

## S2. Polygon normalization

The shared task is bounding-box object detection.

Y-PPE polygon rows were deterministically converted to enclosing axis-aligned boxes before class filtering. Source annotations were not modified.

Stage 4 accounting:
- polygon rows observed: 436;
- retained shared-class polygon rows converted: 309;
- nonshared-class polygon rows dropped with their excluded class: 127;
- invariant: 436 = 309 + 127.

Construction-PPE contained no polygon rows in the pinned source used here.

## S3. Stage 4.5 label-completeness problem

Dropping nonshared labels can turn a visible shared-type object into false background. The prespecified audit therefore checked whether excluded native annotations structurally corresponded to retained shared objects.

Critical semantic relationships:

### Y-PPE
- Child versus Persons;
- No Safety Attire versus Persons;
- Soft Hat versus Hard Hat / No Hard Hat.

Informational only:
- No Safety Vest versus Safety Vests.

### Construction-PPE
- none versus Person.

Informational only:
- no_goggle versus goggles.

## S4. Exact structural match rule

For an excluded source annotation and a candidate retained object, the pair was considered structurally matched if either condition held:

1. IoU >= 0.50; **or**
2. at least 80% of the excluded-box area was contained inside the candidate retained box.

No model predictions were used.

During policy design:
- native annotation metadata could be parsed for all splits;
- image pixels could be viewed only in train/validation;
- held-out test pixels were not opened.

## S5. Final conservative image-membership rule

The final v2 freeze uses the stricter deterministic rule:

> Exclude an entire image if it would become empty after nine-class harmonization, or if at least one critical excluded source annotation remains unmatched under the structural rule above.

The same annotation-only rule was applied to train, validation, and test before Stage 5 training.

### Exclusion flow

| Dataset | Stage-4 train | Removed | Final train | Stage-4 val | Removed | Final val | Stage-4 test | Removed | Final test |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Y-PPE | 1,595 | 359 | 1,236 | 459 | 103 | 356 | 234 | 48 | 186 |
| Construction-PPE | 1,077 | 31 | 1,046 | 134 | 2 | 132 | 141 | 3 | 138 |

Total exclusions:
- Y-PPE: 510.
- Construction-PPE: 36.

Y-PPE pre-correction structural evidence reported:
- 341 images with at least one critical-unmatched excluded annotation;
- 282 harmonized-empty images (198 train, 53 validation, 31 test).

Because these categories overlap and the final union contains 510 images:
- critical-only = 228;
- harmonized-empty-only = 169;
- both conditions = 113.

This decomposition is reported at total-dataset level because the retained repository evidence does not preserve a split-by-split mutually exclusive reason table. The split-level **total** removals are fixed exactly in the table above.

## S6. Final dataset identities

### Y-PPE-h9-v2
- train: 1,236 images;
- validation: 356 images;
- test: 186 images;
- retained shared-class instances: 9,471;
- manifest SHA-256: 82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8.

### Construction-PPE-h9-v2
- train: 1,046 images;
- validation: 132 images;
- test: 138 images;
- retained shared-class instances: 9,514;
- manifest SHA-256: 59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14.

## S7. Stage 5 training configuration

All completed runs:
- architecture: YOLO11m;
- initialization: yolo11m.pt;
- epochs: exactly 100;
- input size: 640 × 640;
- seeds: 17, 42, 2026;
- physical batch size: 8;
- workers: 2;
- CUDA AMP: enabled;
- online stochastic augmentation for this controlled experiment: disabled;
- early stopping: disabled;
- Ultralytics optimizer policy: optimizer=auto;
- resolved logs: AdamW, lr≈0.000769, momentum=0.9, weight decay=0.0005 for decayed parameter groups;
- primary original Stage 6 checkpoint policy: final-epoch last.pt;
- hardware: NVIDIA Tesla T4;
- Python: 3.13.15;
- PyTorch: 2.11.0+cu128;
- CUDA runtime: 12.8;
- Ultralytics: 8.4.156.

The older 17-class Roboflow-managed thesis benchmark used different settings and is not the experiment reported in the present paper.

## S8. Checkpoint-policy sensitivity

The saved validation trajectories show that epoch 100 was not the maximum-validation mAP50:95 epoch.

| Run | Best validation epoch | Best mAP50:95 | Epoch-100 mAP50:95 | Best − final |
|---|---:|---:|---:|---:|
| Y_s17 | 54 | 0.27881 | 0.25961 | 0.01920 |
| Y_s42 | 38 | 0.27847 | 0.24846 | 0.03001 |
| Y_s2026 | 35 | 0.27379 | 0.25060 | 0.02319 |
| C_s17 | 9 | 0.26288 | 0.23670 | 0.02618 |
| C_s42 | 12 | 0.26626 | 0.23474 | 0.03152 |
| C_s2026 | 15 | 0.25313 | 0.22959 | 0.02354 |

Therefore Stage 11 evaluates both best.pt and last.pt on the same leakage-safe test population. This is a post-hoc sensitivity analysis; it does not retroactively change the original frozen Stage 6 policy.

## S9. Held-out evaluation settings

AP evaluation:
- input size: 640;
- AP confidence floor: 0.001;
- prediction NMS IoU: 0.70;
- no test-time augmentation;
- metrics: mAP50:95, mAP50, mAP75, per-class AP50:95.

Fixed operating point:
- confidence threshold: 0.25;
- class-matched IoU threshold: 0.50;
- prediction NMS IoU: 0.70.

## S10. Fixed-operating-point matching algorithm

For each class independently:

1. sort predictions by descending confidence;
2. for each prediction, compute IoU against unmatched ground-truth boxes of the same class;
3. greedily assign the highest-IoU unmatched GT if IoU >= 0.50;
4. assigned predictions are TP;
5. unassigned predictions are FP;
6. unassigned GT objects are FN.

Class precision, recall, F1, and aggregate micro metrics are calculated from these counts.

## S11. Consensus false-negative definition

For a given source-training domain and target test domain, the three seed realizations are evaluated independently.

A safety-class GT object is a **consensus false negative** when all three seed realizations fail to match that GT object at the frozen operating point.

This measures **failure persistence under training stochasticity**. It is not interpreted as three independent replications because the three models share architecture, training data, and protocol.

## S12. Cross-split exact and near-duplicate audit

After external review, the frozen derivatives were subjected to a stricter post-hoc leakage audit.

Methods:
1. SHA-256 exact image hashes;
2. 64-bit DCT pHash;
3. 64-bit dHash;
4. ORB local-feature matching;
5. RANSAC homography confirmation.

A conservative high-confidence same-scene pair was defined as:
- ORB/RANSAC inliers >= 100;
- inlier ratio >= 0.50;
- source spatial coverage >= 0.05.

No exact SHA-256 cross-split duplicates were found.

High-confidence test images linked to train and/or validation:
- Y-PPE: 6/186;
- Construction-PPE: 25/138.

The Stage 11 leakage-safe sensitivity populations therefore contain:
- Y-PPE: 180 test images;
- Construction-PPE: 113 test images.

This is a post-hoc sensitivity correction based only on image similarity, not model results.

## S13. Full per-seed outputs

The repository retains:
- Stage 6 12-cell original frozen results;
- Stage 7 group and seed-level summaries;
- Stage 7 safety-object audit;
- Stage 11 leakage-audit evidence;
- Stage 11 leakage-safe best-vs-last evaluator.

The final manuscript will cite a frozen commit after Stage 11 results are complete.
