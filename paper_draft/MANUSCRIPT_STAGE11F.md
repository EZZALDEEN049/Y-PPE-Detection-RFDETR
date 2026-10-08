# Cross-Domain Reliability of YOLO11m for Safety-Critical PPE Monitoring: A Multi-Seed Bidirectional Evaluation

**Author:** Ezzaldeen Nabil Ghaleb Obadi Al-Tayar  
**Affiliation:** Faculty of Engineering and Information Technology, Taiz University, Yemen  
**Corresponding author:** azzaltayyar@gmail.com

## Abstract

Computer-vision systems for personal protective equipment (PPE) monitoring are commonly evaluated within the same dataset used for model development, although real deployment requires reliability across sites, cameras, and visual domains. This study evaluates the cross-domain reliability of YOLO11m for safety-critical PPE monitoring using two harmonized nine-class construction datasets, Y-PPE-h9-v2 and Construction-PPE-h9-v2. Six completed models were analyzed: three independent random seeds per source domain (17, 42, and 2026). Each final-epoch checkpoint was evaluated on both the in-domain and alternate held-out test set under a protocol frozen before held-out evaluation, producing 12 evaluation cells without further training, adaptation, checkpoint reselection, or threshold tuning. Y-PPE-trained models achieved an in-domain mAP50:95 of 0.291 ± 0.007, decreasing to 0.121 ± 0.003 on Construction-PPE, a 58.4% relative loss. Construction-PPE-trained models decreased from 0.252 ± 0.004 in-domain to 0.082 ± 0.005 on Y-PPE, a 67.4% relative loss. Safety-critical violation classes were substantially less reliable than aggregate metrics suggested, but the failure modes were asymmetric. For Y-PPE-trained models, violation recall showed clear additional transfer degradation: no_helmet decreased from 0.310 to 0.117, no_gloves from 0.303 to 0.039, and no_boots from 0.367 to 0.000. In contrast, Construction-PPE-trained models were already near floor for these violation classes in-domain (0.027, 0.020, and 0.000, respectively), so their poor reverse-transfer safety performance primarily indicates limited class learnability under the evaluated training protocol rather than additional domain-shift loss. A post-hoc dependence sensitivity analysis found no exact cross-split byte duplicates; removing confirmed near-duplicate Y-PPE test derivatives or conservatively excluding high-confidence train-related test scenes preserved substantial aggregate cross-domain gaps. The findings therefore separate two deployment risks: reproducible aggregate cross-domain degradation and dataset/protocol-specific failure to learn some explicit safety-violation classes.

**Keywords:** personal protective equipment; construction safety; domain shift; cross-domain evaluation; YOLO11m; false negatives.

## 1. Introduction

Automated PPE monitoring is increasingly studied as a means of supporting occupational-safety supervision in construction environments. However, a model that performs well on a held-out subset drawn from the same dataset may still rely on dataset-specific visual regularities that do not transfer to a different construction site or data source.

The deployment problem is therefore not only whether a detector achieves high in-domain accuracy, but whether safety-critical decisions remain reliable under domain shift. This distinction is especially important for non-compliance classes such as workers without helmets, gloves, or protective boots, where false negatives directly undermine the purpose of automated monitoring.

This study focuses on cross-domain reliability rather than architecture competition. Two harmonized nine-class PPE datasets are used in a bidirectional design. YOLO11m is trained independently on each source domain using three random seeds and is then evaluated both in-domain and on the alternate held-out domain. The study additionally separates aggregate detection performance from safety-critical violation reliability and performs a deterministic consensus-failure audit across seeds.

The final contributions are:

1. a frozen, bidirectional, multi-seed cross-domain evaluation of six completed YOLO11m models across two harmonized PPE domains;
2. quantification of absolute and relative domain-generalization gaps using mAP, precision, recall, and F1;
3. safety-critical evaluation of no_helmet, no_gloves, and no_boots that distinguishes in-domain class learnability from additional transfer degradation, using fixed-threshold recall, false-negative rates, and three-seed consensus failures;
4. dataset-side diagnostic analysis of class support, imbalance, and object-scale distributions;
5. an evidence-based deployment interpretation showing that in-domain performance alone can substantially overstate PPE-monitoring readiness.

### 1.1 Related work and research gap

Computer-vision PPE monitoring has progressed from real-time hard-hat/vest detection toward richer multi-class compliance systems. Nath et al. [8] demonstrated real-time PPE detection in uncontrolled construction imagery, while Ferdous and Ahsan [7] and the SH17 dataset study [6] expanded the range of PPE classes and benchmark configurations. Recent systematic reviews conclude that strong laboratory metrics alone do not resolve industrial deployment barriers associated with environmental variability, class imbalance, acquisition conditions, and limited external validation [1,2].

Importantly, construction-domain shift is already an active research problem. Kim, Seong, and Jung [11] evaluated unsupervised domain-adaptive object detection for construction-site monitoring and reported gains after adapting to target sites. Bharathi et al. [13] applied unsupervised domain adaptation to robot-based construction safety inspection, while Tran et al. [12] combined semisupervised domain adaptation with long-tailed object detection for construction workers and vehicles. More recently, Seong et al. [3] proposed Cross-HNM and evaluated cross-site generalization across 11 sites and five unseen test sites, including corroboration across YOLOv11, Faster R-CNN, and DETR. For PPE specifically, Wang [4] used domain-adaptive Faster R-CNN for non-PPE identification across general-context and construction imagery. These studies demonstrate that both adaptation and generalization across construction domains are established research directions.

The broader machine-learning literature likewise shows that nominally strong in-distribution performance can degrade on externally sampled or shifted data. Recht et al. [17] observed substantial accuracy drops on newly collected test sets; WILDS formalized naturally occurring distribution shifts as a benchmark problem [14]; Ovadia et al. [18] showed that predictive reliability can degrade under dataset shift; and domain-generalization work emphasizes the importance of controlled model-selection and evaluation protocols [15,16].

Against this background, the present study is not framed as the first demonstration of domain shift, nor as a new domain-adaptation or domain-generalization algorithm. The narrower research gap is **deployment-oriented reliability evaluation for explicit PPE negative-state classes**. Existing method-development studies primarily ask how to improve target-domain detection performance. Here the question is different: under a frozen zero-shot detector, can aggregate cross-domain degradation be separated from in-domain class learnability failure, and do explicit PPE-negative classes show persistent false-negative behavior across training stochasticity? The study further tests whether its aggregate conclusion survives train–test dependence sensitivity. The contribution is therefore an evaluation framework combining bidirectional external-domain testing, repeated seed realizations, safety-class learnability-versus-transfer decomposition, consensus-failure persistence, and dependence sensitivity rather than novelty-by-combination.

## 2. Materials and Methods

### 2.1 Study design

The final experiment used a YOLO11m-only, multi-seed, bidirectional cross-domain design. The initial experimental plan included an additional detector architecture; however, incomplete runs were excluded before the final held-out analysis. The reported study therefore includes only the six fully completed YOLO11m runs and does not make architecture-comparison claims.

Two source domains were used:

- Y-PPE-h9-v2;
- Construction-PPE-h9-v2.

Three independent seeds were completed for each source domain: 17, 42, and 2026. Each model was evaluated on the held-out test set of its own source domain and the held-out test set of the alternate domain, producing 12 evaluation cells. Here, zero-shot cross-domain evaluation means that a source-domain model is evaluated on the alternate target domain without any target-domain training, fine-tuning, adaptation, checkpoint reselection, or threshold tuning.

### 2.2 Dataset sources, provenance, and harmonized class space

The first source corpus was the localized Y-PPE dataset developed for PPE monitoring in Yemeni development-project environments. The original corpus contains 2,327 annotated images, 16,520 annotated instances, and 17 classes. The thesis documentation describes the primary images as routine field documentation obtained through formal coordination with the Social Fund for Development and partner civil-society organizations, supplemented by a limited number of vetted open-access images for rare/contextual categories. The public Roboflow Universe project currently declares the dataset under CC BY 4.0 [9]. [[AUTHOR CONFIRMATION REQUIRED: insert the exact organizational permission/ethics wording governing field-image use and public redistribution.]]

The second source was Construction-PPE v1.0.0 from Ultralytics, which contains 1,416 images and 11 source classes and is released under AGPL-3.0 [10].

Because the source ontologies are not identical, the benchmark used a prespecified semantic harmonization stage before model training. The final shared class order was:

1. person;
2. helmet;
3. gloves;
4. vest;
5. boots;
6. goggles;
7. no_helmet;
8. no_gloves;
9. no_boots.

The mapping retained only classes with sufficiently aligned object/state meaning and localization targets. Y-PPE `No Safety Vest` was excluded because Construction-PPE has no direct `no_vest` class. Construction-PPE `no_goggle` and `none` were excluded because no strict Y-PPE semantic counterparts were established.

A two-stage deterministic harmonization/filtering procedure was frozen before model training. Stage 4 first preserved every cleaned source image in its original split, mapped only the nine shared classes, dropped nonshared annotation rows, and converted retained Y-PPE polygon annotations to enclosing axis-aligned bounding boxes. This keep-all transformation produced 1,595/459/234 Y-PPE train/validation/test images and 1,077/134/141 Construction-PPE images.

Stage 4.5 then addressed the risk that dropping a nonshared annotation could create false background for a retained class. Critical source relationships were prespecified as Y-PPE `Child`→`Persons`, `No Safety Attire`→`Persons`, and `Soft Hat`→`Hard Hat` or `No Hard Hat`; and Construction-PPE `none`→`Person`. For each critical excluded box E and candidate retained box R, a structural match was accepted if either `IoU(E,R) >= 0.50` or at least 80% of the excluded-box area was contained inside R. A `critical_unmatched` flag was assigned when no candidate satisfied either criterion.

The final image-membership rule was: exclude the entire image if it would become empty after nine-class harmonization or if it contained at least one critical unmatched source annotation. If an image contained both shared and nonshared annotations, it was otherwise retained. The same annotation-only rule was applied to train, validation, and test. No model prediction, loss, confidence, or test metric contributed to membership decisions, and held-out test image pixels were not visually adjudicated.

**Table M1. Conservative Stage 4.5 image filtering.**

| Dataset | Split | Pre-filter images | Excluded | Final images |
|---|---|---:|---:|---:|
| Y-PPE | train | 1,595 | 359 | 1,236 |
| Y-PPE | validation | 459 | 103 | 356 |
| Y-PPE | test | 234 | 48 | 186 |
| Construction-PPE | train | 1,077 | 31 | 1,046 |
| Construction-PPE | validation | 134 | 2 | 132 |
| Construction-PPE | test | 141 | 3 | 138 |

The final Y-PPE-h9-v2 derivative contains 9,471 retained shared-class instances and Construction-PPE-h9-v2 contains 9,514. Their frozen manifest fingerprints were `82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8` and `59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14`, respectively. Because the membership rule uses source annotations, the final benchmark should be interpreted as the prespecified **structurally harmonizable subset** of each cleaned source dataset rather than the full source population. Full exclusion manifests, reason counts, and before/after class-support tables are reported in the Supplementary Methods.

### 2.3 Model training and reproducibility controls

Only completed YOLO11m runs were eligible. The six runs were:

- Y_YOLO_s17;
- Y_YOLO_s42;
- Y_YOLO_s2026;
- C_YOLO_s17;
- C_YOLO_s42;
- C_YOLO_s2026.

All six runs followed the frozen Stage 5 YOLO11m protocol. Models were initialized from `yolo11m.pt` and trained for exactly 100 epochs at 640 × 640 resolution. The random seeds were 17, 42, and 2026 for each source domain. Physical batch size was 8, worker count was 2, CUDA automatic mixed precision was enabled, online stochastic augmentation was disabled for the primary controlled comparison, and early stopping was disabled. Training was executed on an NVIDIA Tesla T4 under Python 3.13.15, PyTorch 2.11.0+cu128, CUDA runtime 12.8, and Ultralytics 8.4.156.

The frozen optimizer policy used Ultralytics `optimizer=auto` and recorded the resolved framework-native recipe in the training logs. Representative logs from both source domains resolved to AdamW with learning rate 0.000769, momentum 0.9, and weight decay 0.0005 for decayed weight groups.

For every run, the primary evaluation checkpoint was the final-epoch `last.pt` checkpoint. The validation-selected `best.pt` checkpoint was not used for primary results. No model was retrained, fine-tuned, adapted, or reselected after held-out evaluation began.

These settings belong to the current nine-class cross-domain experiment and should not be confused with the earlier 17-class thesis benchmark, which used a separate Roboflow-managed training workflow.

### 2.4 Frozen held-out evaluation protocol

The held-out protocol was frozen before any Stage 6 test evaluation. Evaluation used:

- input resolution: 640;
- no test-time augmentation;
- AP confidence floor: 0.001;
- prediction NMS IoU: 0.70;
- primary AP metrics: mAP50:95, mAP50, and mAP75.

For fixed operating-point reliability analysis:

- confidence threshold: 0.25;
- class-matched detection IoU: 0.50;
- prediction NMS IoU: 0.70.

No threshold was selected or changed after inspecting the test results.

### 2.5 Evaluation outcomes

Average precision and fixed operating-point metrics were treated as complementary. AP-based metrics summarize confidence-ranked detection performance across thresholds, whereas the frozen confidence threshold of 0.25 provides a deployment-style operating point at which TP, FP, FN, recall, and F1 can be interpreted directly for safety-violation classes.

For every evaluation cell, the analysis extracted:

- mAP50:95;
- mAP50;
- mAP75;
- per-class AP50:95;
- fixed-threshold micro precision, recall, and F1;
- fixed-threshold class-level TP, FP, FN, precision, recall, and F1;
- violation-focused false negatives for no_helmet, no_gloves, and no_boots.

Results across the three seeds were summarized using mean and sample standard deviation.

### 2.6 Domain-generalization gap

For a metric in which higher values are better, the domain-generalization gap was defined as:

`G = M_in - M_cross`

where `M_in` is in-domain performance and `M_cross` is cross-domain performance for the same source training domain and seed. Positive values therefore indicate degradation under domain shift.

Relative mAP50:95 degradation was computed as:

`D_rel (%) = 100 × (M_in - M_cross) / M_in`

### 2.7 Dataset diagnostic audit

A post-evaluation diagnostic audit was performed without model retraining or threshold modification. For each dataset and split, the audit quantified:

- class-instance frequencies;
- maximum-to-minimum nonzero class imbalance ratio;
- safety-class support;
- normalized bounding-box area;
- object-size strata;
- stored image resolution and aspect ratio.

For descriptive scale analysis, normalized box area was grouped into study-specific strata: small (<0.01), medium (0.01–<0.10), or large (≥0.10). These bins are descriptive categories defined for this study and are not the standard COCO object-size categories.

### 2.8 Deterministic consensus false-negative audit

A qualitative failure audit was then performed at the same frozen fixed operating point. A consensus false negative was defined as a ground-truth safety-violation object missed by all three independently trained source-domain seeds in the same transfer direction.

To reduce cherry-picking risk, examples were selected deterministically rather than visually. The audit retained the same confidence, IoU, image resolution, and final-epoch checkpoint policy used in Stage 6. The audit was a post-evaluation diagnostic only. It was not used for model selection, checkpoint selection, threshold tuning, or quantitative re-estimation and therefore did not alter any Stage 6 result.

### 2.9 Statistical position

The study uses three independent seeds per source domain. Accordingly, mean ± SD and paired seed-level generalization gaps are treated as descriptive summaries of training stochasticity. The seeds are repeated model-training realizations; they are not independent construction sites and their SD should not be interpreted as population uncertainty across deployment environments. The study therefore avoids population-level significance claims and does not claim causal identification of the mechanism behind domain shift.

For the cross-domain safety outcomes, a post-evaluation nonparametric cluster bootstrap was added to quantify test-image sampling uncertainty without treating multiple objects from the same image as independent observations. Images were resampled with replacement within each transfer direction and safety class for 10,000 percentile-bootstrap replicates using deterministic seed 20261009. The same sampled-image multiplicities were applied to all objects in an image. Reported bootstrap intervals are conditional on the already trained seed realizations and should not be interpreted as site-level population confidence intervals.

### 2.10 Train–test dependence audit and sensitivity analysis

Following peer-review-style scrutiny of possible split dependence, the frozen derivatives were audited for exact duplication, transformed near-duplication, and high-confidence scene-level dependence. Exact byte-level duplication was assessed using SHA-256. Candidate visual relationships were then screened with perceptual and geometric similarity methods and manually classified conservatively as independent, related-scene, or near-duplicate. Visual similarity alone was not treated as leakage.

No exact cross-split byte duplicates were found. The audit identified four visually confirmed near-duplicate Y-PPE test derivatives and additional high-confidence train-related scenes. Construction-PPE candidates were conservatively classified as scene-level dependence rather than confirmed near-duplicates.

Two sensitivity subsets were frozen before re-evaluation. The strict subset removed only the four confirmed Y-PPE near-duplicate test derivatives. The conservative subset removed all high-confidence direct train-related test images, leaving 180 Y-PPE and 115 Construction-PPE test images. The six trained checkpoints and all Stage 6 evaluation settings remained unchanged; no retraining, checkpoint reselection, or test-informed threshold tuning was performed.

## 3. Results

### 3.1 Cross-domain degradation

Y-PPE-trained models achieved an in-domain mAP50:95 of 0.291 ± 0.007 and a cross-domain mAP50:95 of 0.121 ± 0.003 on Construction-PPE. The absolute gap was approximately 0.170, corresponding to a 58.4% relative degradation.

Construction-PPE-trained models achieved an in-domain mAP50:95 of 0.252 ± 0.004 and a cross-domain mAP50:95 of 0.082 ± 0.005 on Y-PPE. The absolute gap was again approximately 0.170, but the relative degradation was larger at 67.4%.

The degradation was reproduced across all three seeds. Y-PPE-trained mAP50:95 gaps were 0.173, 0.178, and 0.159 for seeds 17, 42, and 2026. Construction-PPE-trained gaps were 0.172, 0.166, and 0.171, respectively.

**Table 1. Primary in-domain and cross-domain performance (mean ± SD across three seeds).**

| Training domain | Test condition | mAP50:95 | mAP50 | mAP75 | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Y-PPE | In-domain | 0.291 ± 0.007 | 0.551 ± 0.018 | 0.275 ± 0.009 | 0.881 | 0.516 | 0.651 |
| Y-PPE | Construction-PPE | 0.121 ± 0.003 | 0.293 ± 0.017 | 0.079 ± 0.001 | 0.711 | 0.382 | 0.497 |
| Construction-PPE | In-domain | 0.252 ± 0.004 | 0.467 ± 0.002 | 0.241 ± 0.010 | 0.921 | 0.580 | 0.712 |
| Construction-PPE | Y-PPE | 0.082 ± 0.005 | 0.187 ± 0.011 | 0.057 ± 0.004 | 0.766 | 0.209 | 0.328 |

### 3.2 Fixed operating-point reliability

Y-PPE-trained models decreased from mean precision/recall/F1 of 0.881/0.516/0.651 in-domain to 0.711/0.382/0.497 on Construction-PPE.

Construction-PPE-trained models decreased from 0.921/0.580/0.712 in-domain to 0.766/0.209/0.328 on Y-PPE. The particularly large recall loss in this direction indicates that cross-domain degradation manifested strongly as missed detections.

### 3.3 Safety-critical violation classes: learnability versus transfer degradation

For Y-PPE-trained models, the safety classes showed clear additional degradation after transfer. In-domain mean recall was 0.310 for no_helmet, 0.303 for no_gloves, and 0.367 for no_boots; on Construction-PPE, the corresponding values fell to 0.117, 0.039, and 0.000. The absolute recall decreases were therefore 0.193, 0.264, and 0.367, respectively. This direction provides direct evidence that already-learned violation behavior did not transfer robustly to the alternate domain.

The reverse direction must be interpreted differently. Construction-PPE-trained models already exhibited near-floor in-domain recall for the same violation classes: 0.027 for no_helmet, 0.020 for no_gloves, and 0.000 for no_boots. Cross-domain evaluation on Y-PPE yielded 0.024, 0.015, and 0.000. The additional recall decreases were only 0.003, 0.005, and 0.000. Consequently, the Construction-PPE → Y-PPE safety-class results do not support attributing these class failures primarily to domain shift; they instead reveal a substantial in-domain learnability limitation under the evaluated dataset/training protocol.

**Table 2. Safety-violation recall at the frozen operating point (mean ± SD across three seeds).**

| Train/Test condition | no_helmet | no_gloves | no_boots |
|---|---:|---:|---:|
| Y-PPE → Y-PPE | 0.310 ± 0.109 | 0.303 ± 0.029 | 0.367 ± 0.033 |
| Y-PPE → Construction-PPE | 0.117 ± 0.031 | 0.039 ± 0.034 | 0.000 ± 0.000 |
| Construction-PPE → Construction-PPE | 0.027 ± 0.000 | 0.020 ± 0.000 | 0.000 ± 0.000 |
| Construction-PPE → Y-PPE | 0.024 ± 0.041 | 0.015 ± 0.007 | 0.000 ± 0.000 |

**Table 2b. Separation of in-domain learnability from additional transfer degradation.**

| Source training domain | Class | In-domain recall | Cross-domain recall | Additional transfer loss |
|---|---|---:|---:|---:|
| Y-PPE | no_helmet | 0.310 | 0.117 | 0.193 |
| Y-PPE | no_gloves | 0.303 | 0.039 | 0.264 |
| Y-PPE | no_boots | 0.367 | 0.000 | 0.367 |
| Construction-PPE | no_helmet | 0.027 | 0.024 | 0.003 |
| Construction-PPE | no_gloves | 0.020 | 0.015 | 0.005 |
| Construction-PPE | no_boots | 0.000 | 0.000 | 0.000 |

### 3.4 Consensus failure across seeds

The deterministic consensus audit showed that the majority of cross-domain safety violations were missed by all three seed realizations of the same architecture and training protocol. This consensus quantifies persistence under training stochasticity; it should not be interpreted as independent replication across architectures or sites.

For Y-PPE → Construction-PPE, consensus false-negative rates were:

- no_helmet: 31/37 = 83.8%;
- no_gloves: 47/51 = 92.2%;
- no_boots: 15/15 = 100%.

For Construction-PPE → Y-PPE:

- no_helmet: 13/14 = 92.9%;
- no_gloves: 85/88 = 96.6%;
- no_boots: 30/30 = 100%.

At the frozen operating point, no_boots exhibited a 100% three-seed consensus false-negative rate in both transfer directions. In Y-PPE → Construction-PPE this accompanies a clear recall collapse from 0.367 to 0.000; in Construction-PPE → Y-PPE it instead reflects a class that was already undetected in-domain.

Image-cluster bootstrap intervals reinforced the high miss-rate interpretation while showing the uncertainty associated with finite test-image support. For Y-PPE → Construction-PPE, consensus false-negative rates were 0.838 (95% CI 0.694–0.947) for no_helmet, 0.922 (0.848–0.980) for no_gloves, and 1.000 (1.000–1.000) for no_boots. For Construction-PPE → Y-PPE, the corresponding estimates were 0.929 (0.750–1.000), 0.966 (0.925–1.000), and 1.000 (1.000–1.000). Mean cross-domain recall across the three fixed seed models was 0.117 (0.036–0.226), 0.039 (0.007–0.085), and 0.000 for Y-PPE → Construction-PPE; and 0.024 (0.000–0.083), 0.015 (0.000–0.034), and 0.000 for Construction-PPE → Y-PPE.

**Table 3. Three-seed consensus false negatives for safety-violation classes.**

| Transfer direction | Class | GT objects | Missed by all three seeds | Consensus FN rate |
|---|---|---:|---:|---:|
| Y-PPE → Construction-PPE | no_helmet | 37 | 31 | 83.8% |
| Y-PPE → Construction-PPE | no_gloves | 51 | 47 | 92.2% |
| Y-PPE → Construction-PPE | no_boots | 15 | 15 | 100.0% |
| Construction-PPE → Y-PPE | no_helmet | 14 | 13 | 92.9% |
| Construction-PPE → Y-PPE | no_gloves | 88 | 85 | 96.6% |
| Construction-PPE → Y-PPE | no_boots | 30 | 30 | 100.0% |

**Table 3b. Image-cluster bootstrap uncertainty for cross-domain safety outcomes.**

| Transfer direction | Class | Mean recall (95% CI) | Consensus FN rate (95% CI) |
|---|---|---:|---:|
| Y-PPE → Construction-PPE | no_helmet | 0.117 (0.036–0.226) | 0.838 (0.694–0.947) |
| Y-PPE → Construction-PPE | no_gloves | 0.039 (0.007–0.085) | 0.922 (0.848–0.980) |
| Y-PPE → Construction-PPE | no_boots | 0.000 (0.000–0.000) | 1.000 (1.000–1.000) |
| Construction-PPE → Y-PPE | no_helmet | 0.024 (0.000–0.083) | 0.929 (0.750–1.000) |
| Construction-PPE → Y-PPE | no_gloves | 0.015 (0.000–0.034) | 0.966 (0.925–1.000) |
| Construction-PPE → Y-PPE | no_boots | 0.000 (0.000–0.000) | 1.000 (1.000–1.000) |

### 3.5 Dataset-side diagnostics

Both frozen derivatives were stored as 640×640 square images, so stored resolution and aspect ratio did not differ across domains.

The training-set max-to-min nonzero class-frequency ratio was 11.49 in Y-PPE and 21.76 in Construction-PPE, indicating greater imbalance in the latter.

Safety-class support also differed. Y-PPE contained 113 no_helmet, 677 no_gloves, and 226 no_boots training instances. Construction-PPE contained 352, 403, and 74, respectively.

The strongest object-scale mismatch occurred for no_boots. Y-PPE training contained approximately 30.5% small, 21.2% medium, and 48.2% large no_boots instances. Construction-PPE contained approximately 77.0% small and 23.0% medium no_boots instances and no large instances.

However, object size alone could not explain the cross-domain collapse. In Construction-PPE → Y-PPE transfer, all 30 ground-truth no_boots objects were missed by all three models despite spanning 6 small, 10 medium, and 14 large instances.

### 3.6 Dependence sensitivity analysis

The split-dependence audit found no exact byte-level cross-split duplicates. Four Y-PPE test images were visually confirmed as transformed near-duplicate derivatives of training images, while additional candidates in both datasets were classified conservatively as related-scene dependence.

Under the strict sensitivity scenario, which removed only the four confirmed Y-PPE near-duplicate test derivatives, the Y-PPE-trained in-domain mAP50:95 changed from 0.291 to 0.287, while Y-PPE → Construction-PPE remained 0.121. The resulting gap was 0.166 (57.8% relative). Construction-PPE-trained in-domain mAP50:95 remained 0.252 and cross-domain Y-PPE performance was 0.083, giving a gap of 0.169 (67.2% relative).

Under the more conservative train-scene exclusion, Y-PPE-trained in-domain mAP50:95 was 0.289 and cross-domain Construction-PPE performance was 0.108, yielding a gap of 0.181 (62.6% relative). Construction-PPE-trained in-domain performance decreased to 0.224 after removing train-related Construction-PPE test scenes, while cross-domain Y-PPE performance was 0.084, yielding a gap of 0.140 (62.6% relative).

Thus, scene dependence affected the magnitude of some in-domain estimates, particularly for Construction-PPE, but substantial aggregate cross-domain degradation persisted under both prespecified sensitivity scenarios.

## 4. Discussion

The results demonstrate a substantial distinction between in-domain PPE detection performance and cross-domain reliability under the evaluated training protocol. In the original held-out analysis, transfer to the alternate domain produced an approximately 0.17 absolute loss in mAP50:95 in both directions, and the sign of the gap was consistent across all three seed realizations. The Stage 11A sensitivity analysis further showed that this aggregate degradation remained substantial after removing confirmed near-duplicate derivatives and after a more conservative exclusion of high-confidence train-related test scenes. This reduces, but does not eliminate, concern that the central aggregate domain-gap result is an artifact of split dependence.

The safety-class results require an asymmetric interpretation. Y-PPE-trained models had non-trivial in-domain recall for all three explicit violation classes and then lost 0.193–0.367 recall after transfer, providing direct evidence of safety-relevant domain degradation. By contrast, Construction-PPE-trained models were already near floor for these classes in-domain, including zero no_boots recall. Their reverse-transfer consensus failures therefore cannot be attributed primarily to domain shift; they reveal that a model can achieve moderate aggregate in-domain detection while failing to learn particular explicit non-compliance classes at the frozen operating point. The central safety lesson is consequently twofold: aggregate metrics can conceal both poor class learnability and additional transfer degradation.

The dataset diagnostic audit identified several plausible contributors. Construction-PPE showed greater class imbalance and considerably lower no_boots training support than Y-PPE. The two domains also differed in object-scale distributions, especially for no_boots. These characteristics are consistent with the observed failures but are not sufficient as complete causal explanations. Construction-PPE no_helmet had nontrivial training support yet near-floor violation performance, and consensus failures in the Construction-PPE → Y-PPE direction occurred even for medium and large objects.

Accordingly, the observed reliability collapse appears broader than a rare-class or small-object problem. Plausible mechanisms include domain-specific appearance, contextual cues, annotation semantics, scene composition, and learned correlations that do not transfer between datasets. These mechanisms remain hypotheses rather than experimentally isolated causes.

A central methodological implication is that conventional same-dataset train/validation/test evaluation can overstate deployment readiness across the evaluated domains. For safety-critical PPE systems, external-domain evaluation should be treated as a distinct evidence requirement before broader deployment. Multi-seed evaluation is also useful because it separates persistent transfer failure from random training variability. Finally, class-specific recall and false-negative analysis should accompany aggregate mAP because the operational consequence of missing a safety violation is not captured by overall detection accuracy alone.

### 4.1 Limitations

This revised study includes only one completed detector architecture. The original plan included RF-DETR, but incomplete RF-DETR runs were excluded before final held-out analysis. The study therefore does not support claims of YOLO11m superiority over another architecture or architecture-independent generalization.

Only two harmonized datasets and three seeds per source domain are included. The evidence is sufficient to demonstrate reproducible degradation in this experiment but not to represent all construction domains.

The primary training recipe is intentionally controlled and uses final-epoch checkpoints with online stochastic augmentation disabled. The results therefore characterize YOLO11m under this frozen protocol, not every plausible YOLO11m training recipe. A separate sensitivity baseline using validation-selected best.pt checkpoints and/or a standard augmentation recipe would further test training-protocol dependence.

The dependence audit identified a small number of Y-PPE near-duplicate derivatives and a larger set of Construction-PPE related-scene test images. Prespecified sensitivity evaluation showed that substantial aggregate cross-domain gaps persisted, but scene dependence remains a property of the source datasets that should be considered when interpreting absolute in-domain performance.

The image-cluster bootstrap added uncertainty intervals for cross-domain safety recall and consensus false-negative rates, but a corresponding bootstrap interval for mAP50:95 and the mAP domain gap requires per-image ranked prediction statistics that were not retained by the original Stage 6 summary outputs. An inference-only prediction-archive analysis is therefore treated as a separate remaining statistical sensitivity step rather than approximating mAP uncertainty from object-level counts.

The diagnostic audit identifies associations with class support, imbalance, and scale but does not experimentally isolate causal mechanisms. In addition, semantic harmonization reduces label-space mismatch but cannot eliminate differences in annotation policy, contextual labeling practice, or the operational meaning assigned to negative-state classes across the two source datasets.

The Stage 4.5 membership rule also uses source ground-truth annotation metadata to restrict evaluation to a structurally harmonizable subset. Although this rule was frozen before training, applied identically to all splits, and independent of model/test performance, it changes the composition of the held-out population. Absolute in-domain and cross-domain estimates should therefore be interpreted for the filtered benchmark population rather than for every image in the original source datasets.

### 4.2 Future work

Future work should test:

- preregistered multi-domain training;
- balanced sampling or safety-class reweighting;
- scale-aware augmentation;
- external calibration;
- domain adaptation;
- additional architectures;
- additional geographically and visually distinct construction datasets;
- site-level prospective evaluation emphasizing safety-class recall and false negatives.

## 5. Conclusion

This study shows that aggregate in-domain detection performance is not sufficient evidence of deployment readiness across the evaluated PPE domains. Across two harmonized construction PPE domains and three random seeds per source domain, YOLO11m exhibited substantial aggregate cross-domain degradation that persisted under prespecified split-dependence sensitivity analyses. Safety-class analysis further revealed two distinct risks: Y-PPE-trained models showed marked additional transfer degradation for no_helmet, no_gloves, and no_boots, whereas Construction-PPE-trained models showed near-floor in-domain learnability for the same violation classes before transfer.

The findings support a deployment-oriented evaluation principle: safety-critical computer-vision systems should be assessed not only by same-domain mAP but by external-domain generalization, multi-seed robustness, class-specific recall, and false-negative behavior. In settings where site-specific retraining is difficult or expensive, such evidence should be established before operational use.

## Data and Code Availability

The experimental code, frozen protocols, dataset fingerprints, evaluation scripts, and analysis workflow are maintained in the project repository. The frozen Y-PPE-h9-v2 and Construction-PPE-h9-v2 fingerprints are reported in Methods. A tagged immutable release and archival identifier should be created before submission.

## Declarations

**Funding:** This research received no external funding.

**Competing interests:** The author declares that he has no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

**Author contributions:** Ezzaldeen Nabil Ghaleb Obadi Al-Tayar: Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing - original draft; Writing - review and editing; Visualization; Project administration.

**Ethics and image governance:** The Y-PPE corpus used secondary images originally captured during routine field monitoring in Yemeni development projects. The source study documents that acquisition occurred in the researcher's professional safety-monitoring context, that geographic and personal metadata were removed before analysis, and that the AI workflow was framed as a safety-management and decision-support tool rather than punitive surveillance. The source documentation reports alignment with Taiz University guidelines for responsible research. No formal ethics approval identifier is stated in the available source materials; one should not be added unless it exists.

## References

1. Vukicevic AM, Petrovic M, Milosevic P, et al. A systematic review of computer vision-based personal protective equipment compliance in industry practice: advancements, challenges and future directions. *Artificial Intelligence Review*. 2024;57:319. doi:10.1007/s10462-024-10978-x.
2. Barlybayev A, Milosz M, Amangeldy N, Li G, Razakhova B, Tazhibay A, Nazyrova A, Lamasheva Z. Systematic Review of Computer-Vision Technologies for Personal Protective Equipment Compliance Monitoring. *Computers*. 2026;15(6):388. doi:10.3390/computers15060388.
3. Seong J, Kim HS, Jung HJ. Improving cross-site generalization in construction object detection via hard negative mining. *Automation in Construction*. 2026;182:106761. doi:10.1016/j.autcon.2026.106761.
4. Wang S. Domain-adaptive faster R-CNN for non-PPE identification on construction sites from body-worn and general images. *Scientific Reports*. 2026;16:4793. doi:10.1038/s41598-026-35148-7.
5. Wang S, Kim H, Yeo J, et al. YOLOv10-based multi-scale variant object detection for multi-category PPE non-compliance monitoring on construction sites. *Scientific Reports*. 2026;16:24591. doi:10.1038/s41598-026-53052-y.
6. Ahmad HM, Rahimi A. SH17: A dataset for human safety and personal protective equipment detection in manufacturing industry. *Journal of Safety Science and Resilience*. 2025;6(2):175–185. doi:10.1016/j.jnlssr.2024.09.002.
7. Ferdous M, Ahsan SMM. PPE detector: a YOLO-based architecture to detect personal protective equipment (PPE) for construction sites. *PeerJ Computer Science*. 2022;8:e999. doi:10.7717/peerj-cs.999.
8. Nath ND, Behzadan AH, Paal SG. Deep learning for site safety: Real-time detection of personal protective equipment. *Automation in Construction*. 2020;112:103085. doi:10.1016/j.autcon.2020.103085.
9. SoftyYemen. ALTAYYAR/Y-PPE object-detection dataset. Roboflow Universe. Public project page; CC BY 4.0 license declaration. Accessed 2026-10-08.
10. Dalvi M, Singh N, Bhingarde S, Chalke K. Construction-PPE: Personal Protective Equipment Detection Dataset. Ultralytics; version 1.0.0; AGPL-3.0. 2025.
11. Kim HS, Seong J, Jung HJ. Optimal domain adaptive object detection with self-training and adversarial-based approach for construction site monitoring. *Automation in Construction*. 2024;158:105244. doi:10.1016/j.autcon.2023.105244.
12. Tran DQ, Jeon Y, Aboah A, Bak J, Park M, Park S. Leveraging Semisupervised Learning for Domain Adaptation: Enhancing Safety at Construction Sites through Long-Tailed Object Detection. *Journal of Construction Engineering and Management*. 2025;151(1):04024190. doi:10.1061/JCEMD4.COENG-15259.
13. Bharathi VV, Prieto SA, Garcia de Soto B, Teizer J. Automating Construction Safety Inspections using Robots and Unsupervised Deep Domain Adaptation by Backpropagation. In: *Proceedings of the 41st International Symposium on Automation and Robotics in Construction (ISARC 2024)*. 2024:855–862. doi:10.22260/ISARC2024/0111.
14. Koh PW, Sagawa S, Marklund H, et al. WILDS: A Benchmark of in-the-Wild Distribution Shifts. In: *Proceedings of the 38th International Conference on Machine Learning*. PMLR. 2021;139:5637–5664.
15. Gulrajani I, Lopez-Paz D. In Search of Lost Domain Generalization. *International Conference on Learning Representations*. 2021.
16. Zhou K, Liu Z, Qiao Y, Xiang T, Loy CC. Domain Generalization: A Survey. *IEEE Transactions on Pattern Analysis and Machine Intelligence*. 2023;45(4):4396–4415. doi:10.1109/TPAMI.2022.3195549.
17. Recht B, Roelofs R, Schmidt L, Shankar V. Do ImageNet Classifiers Generalize to ImageNet? In: *Proceedings of the 36th International Conference on Machine Learning*. PMLR. 2019;97:5389–5400.
18. Ovadia Y, Fertig E, Ren J, et al. Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift. *Advances in Neural Information Processing Systems*. 2019;32.
