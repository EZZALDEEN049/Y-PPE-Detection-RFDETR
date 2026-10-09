# Cross-Domain Reliability of YOLO11m for Safety-Critical PPE Monitoring: A Multi-Seed Bidirectional Evaluation

**Author:** Ezzaldeen Nabil Ghaleb Obadi Al-Tayar  
**Affiliation:** Faculty of Engineering and Information Technology, Taiz University, Yemen  
**Corresponding author:** azzaltayyar@gmail.com

## Abstract

Computer-vision systems for personal protective equipment (PPE) monitoring are commonly evaluated within the same dataset used for model development, although real deployment requires reliability across sites, cameras, and visual domains. This study evaluates the cross-domain reliability of YOLO11m for safety-critical PPE monitoring using two harmonized nine-class construction datasets, Y-PPE-h9-v2 and Construction-PPE-h9-v2. Six completed models were analyzed: three independent random seeds per source domain (17, 42, and 2026). Each final-epoch checkpoint was evaluated on both the in-domain and alternate held-out test set under a protocol frozen before held-out evaluation, producing 12 primary evaluation cells without further training, adaptation, checkpoint reselection, or threshold tuning. Y-PPE-trained models achieved an in-domain mAP50:95 of 0.291 ± 0.007, decreasing to 0.121 ± 0.003 on Construction-PPE, a 58.4% relative loss. Construction-PPE-trained models decreased from 0.252 ± 0.004 in-domain to 0.082 ± 0.005 on Y-PPE, a 67.4% relative loss. PPE-negative-state behavior was heterogeneous: Y-PPE-trained models showed clear transfer degradation for no_helmet, no_gloves, and no_boots, whereas under the primary final-epoch policy the Construction-PPE-trained models were already near floor for these classes in-domain. A prespecified validation-selected checkpoint sensitivity analysis materially improved some in-domain negative-state recalls, especially for Construction-PPE, but the aggregate cross-domain mAP50:95 gaps remained large: 0.191 (61.0%) for Y-PPE → Construction-PPE and 0.170 (63.3%) for Construction-PPE → Y-PPE. A separate split-dependence sensitivity analysis likewise preserved substantial aggregate gaps after strict near-duplicate exclusion and conservative train-scene exclusion. The findings therefore support a robust aggregate domain-shift conclusion while showing that class-level safety interpretation can depend on checkpoint policy and should be reported separately from aggregate detection performance.

**Keywords:** personal protective equipment; construction safety; domain shift; cross-domain evaluation; YOLO11m; false negatives.

## 1. Introduction

Automated PPE monitoring is increasingly studied as a means of supporting occupational-safety supervision in construction environments. However, a model that performs well on a held-out subset drawn from the same dataset may still rely on dataset-specific visual regularities that do not transfer to a different construction site or data source.

The deployment problem is therefore not only whether a detector achieves high in-domain accuracy, but whether safety-critical decisions remain reliable under domain shift. This distinction is especially important for non-compliance classes such as workers without helmets, gloves, or protective boots, where false negatives directly undermine the purpose of automated monitoring.

This study focuses on cross-domain reliability rather than architecture competition. Two harmonized nine-class PPE datasets are used in a bidirectional design. YOLO11m is trained independently on each source domain using three random seeds and is then evaluated both in-domain and on the alternate held-out domain. The study additionally separates aggregate detection performance from safety-critical PPE-negative-state reliability and performs a deterministic consensus-failure audit across seeds.

The final contributions are:

1. a frozen, bidirectional, multi-seed cross-domain evaluation of six completed YOLO11m models across two harmonized PPE domains;
2. quantification of absolute and relative domain-generalization gaps using mAP, precision, recall, and F1;
3. safety-critical evaluation of no_helmet, no_gloves, and no_boots that distinguishes in-domain class learnability from additional transfer degradation, using fixed-threshold recall, false-negative rates, and three-seed consensus failures;
4. dataset-side diagnostic analysis of class support, imbalance, and object-scale distributions;
5. prespecified robustness checks for train–test dependence and validation-selected checkpoint policy; and
6. an evidence-based deployment interpretation showing that in-domain performance alone can substantially overstate PPE-monitoring readiness while class-level failure mechanisms may remain checkpoint-sensitive.

### 1.1 Related work and research gap

Computer-vision PPE monitoring has progressed from hard-hat detection toward richer multi-class compliance systems. Fang et al. [19] evaluated non-hardhat-use detection across far-field surveillance data from multiple construction sites, while Wu et al. [20] introduced a hardhat benchmark covering varied on-site conditions. Nath et al. [8] demonstrated real-time hard-hat/vest compliance detection in uncontrolled jobsite imagery; Wang et al. [23] compared multiple YOLO variants on a dedicated real-construction-site PPE dataset; and later work incorporated geometric reasoning and body-part structure for multi-PPE compliance analysis [21,22]. Ferdous and Ahsan [7] and the SH17 dataset study [6] further expanded detector and dataset configurations. These studies establish increasingly realistic PPE detection benchmarks, but most report performance within their own acquisition/benchmark setting rather than treating external-domain reliability as a primary estimand. Recent systematic reviews likewise identify environmental variability, class imbalance, acquisition conditions, and limited external validation as persistent deployment barriers [1,2].

Importantly, construction-domain shift is already an active research problem. Kim, Seong, and Jung [11] evaluated unsupervised domain-adaptive object detection for construction-site monitoring and reported gains after adapting to target sites. Bharathi et al. [13] applied unsupervised domain adaptation to robot-based construction safety inspection, while Tran et al. [12] combined semisupervised domain adaptation with long-tailed object detection for construction workers and vehicles. More recently, Seong et al. [3] proposed Cross-HNM and evaluated cross-site generalization across 11 sites and five unseen test sites, including corroboration across YOLOv11, Faster R-CNN, and DETR. For PPE specifically, Wang [4] used domain-adaptive Faster R-CNN for non-PPE identification across general-context and construction imagery. These studies demonstrate that both adaptation and generalization across construction domains are established research directions.

The broader machine-learning literature provides a mature basis for interpreting such results. Torralba and Efros [24] demonstrated that dataset bias can materially affect cross-dataset recognition, and Ben-David et al. [27] formalized learning under source/target distribution differences. Domain-adaptation methods subsequently targeted invariant representations or detector alignment [26,28], while modern robustness work has shown that high benchmark performance does not guarantee transfer under natural distribution change [17,29]. Geirhos et al. [25] described shortcut learning as a general mechanism by which models can exploit benchmark-specific regularities that fail under more challenging conditions. WILDS formalized naturally occurring distribution shifts as a benchmark problem [14]; Ovadia et al. [18] showed that predictive reliability can degrade under dataset shift; and domain-generalization work emphasizes controlled model-selection and evaluation protocols [15,16].

Against this background, the present study is not framed as the first demonstration of domain shift, nor as a new domain-adaptation or domain-generalization algorithm. The narrower research gap is **deployment-oriented reliability evaluation for explicit PPE negative-state classes**. Existing method-development studies primarily ask how to improve target-domain detection performance. Here the question is different: under a frozen zero-shot detector, can aggregate cross-domain degradation be separated from in-domain class learnability failure, and do explicit PPE-negative classes show persistent false-negative behavior across training stochasticity? The study further tests whether its aggregate conclusion survives train–test dependence sensitivity. The contribution is therefore an evaluation framework combining bidirectional external-domain testing, repeated seed realizations, safety-class learnability-versus-transfer decomposition, consensus-failure persistence, and dependence sensitivity rather than novelty-by-combination.

## 2. Materials and Methods

### 2.1 Study design

The final experiment used a YOLO11m-only, multi-seed, bidirectional cross-domain design. The initial experimental plan included an additional detector architecture; however, incomplete runs were excluded before the final held-out analysis. The reported study therefore includes only the six fully completed YOLO11m runs and does not make architecture-comparison claims.

Two source domains were used:

- Y-PPE-h9-v2;
- Construction-PPE-h9-v2.

Three independent seeds were completed for each source domain: 17, 42, and 2026. Each model was evaluated on the held-out test set of its own source domain and the held-out test set of the alternate domain, producing 12 evaluation cells. Here, zero-shot cross-domain evaluation means that a source-domain model is evaluated on the alternate target domain without any target-domain training, fine-tuning, adaptation, checkpoint reselection, or threshold tuning.

### 2.2 Dataset sources, provenance, and harmonized class space

The first source corpus was the localized Y-PPE dataset developed for PPE monitoring in Yemeni development-project environments. The original corpus contains 2,327 annotated images, 16,520 annotated instances, and 17 classes. The thesis documentation describes the primary images as routine field documentation obtained through formal coordination with the Social Fund for Development and partner civil-society organizations, supplemented by a limited number of vetted open-access images for rare/contextual categories. The public Roboflow Universe project currently declares the dataset under CC BY 4.0 [9]. This public license declaration is reported as source-platform metadata; the available study documentation does not provide a separate institutional approval identifier specifically for public redistribution of the primary field images.

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

Average precision and fixed operating-point metrics were treated as complementary. AP-based metrics summarize confidence-ranked detection performance across thresholds, whereas the frozen confidence threshold of 0.25 provides a deployment-style operating point at which TP, FP, FN, recall, and F1 can be interpreted directly for PPE-negative-state classes.

For every evaluation cell, the analysis extracted:

- mAP50:95;
- mAP50;
- mAP75;
- per-class AP50:95;
- fixed-threshold micro precision, recall, and F1;
- fixed-threshold class-level TP, FP, FN, precision, recall, and F1;
- PPE-negative-state-focused false negatives for no_helmet, no_gloves, and no_boots.

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

A qualitative failure audit was then performed at the same frozen fixed operating point. A consensus false negative was defined as a ground-truth PPE-negative-state object missed by all three independently trained source-domain seeds in the same transfer direction.

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

### 3.3 Safety-critical PPE-negative-state classes: learnability versus transfer degradation

For Y-PPE-trained models, the safety classes showed clear additional degradation after transfer. In-domain mean recall was 0.310 for no_helmet, 0.303 for no_gloves, and 0.367 for no_boots; on Construction-PPE, the corresponding values fell to 0.117, 0.039, and 0.000. The absolute recall decreases were therefore 0.193, 0.264, and 0.367, respectively. This direction provides direct evidence that already-learned negative-state behavior did not transfer robustly to the alternate domain.

The reverse direction must be interpreted differently. Construction-PPE-trained models already exhibited near-floor in-domain recall for the same PPE-negative-state classes: 0.027 for no_helmet, 0.020 for no_gloves, and 0.000 for no_boots. Cross-domain evaluation on Y-PPE yielded 0.024, 0.015, and 0.000. The additional recall decreases were only 0.003, 0.005, and 0.000. Consequently, the Construction-PPE → Y-PPE safety-class results do not support attributing these class failures primarily to domain shift; they instead reveal a substantial in-domain learnability limitation under the evaluated dataset/training protocol.

**Table 2. PPE-negative-state recall at the frozen operating point (mean ± SD across three seeds).**

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

The deterministic consensus audit showed that the majority of cross-domain PPE-negative-state instances were missed by all three seed realizations of the same architecture and training protocol. This consensus quantifies persistence under training stochasticity; it should not be interpreted as independent replication across architectures or sites.

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

**Table 3. Three-seed consensus false negatives for PPE-negative-state classes.**

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

### 3.7 Validation-selected checkpoint sensitivity

A separate prespecified sensitivity analysis evaluated the validation-selected `best.pt` checkpoint from each of the six completed Stage 5 runs under the unchanged Stage 6 held-out evaluation settings. No retraining, target-domain adaptation, threshold tuning, or test-informed checkpoint selection was performed.

For Y-PPE-trained models, mean in-domain mAP50:95 increased from 0.291 ± 0.007 with `last.pt` to 0.312 ± 0.006 with `best.pt`, while cross-domain Construction-PPE performance changed only from 0.121 ± 0.003 to 0.122 ± 0.002. The resulting `best.pt` domain gap was 0.191, corresponding to an approximately 61.0% relative reduction from in-domain performance. The seed-level `best.pt` gaps were 0.187, 0.197, and 0.188 for seeds 17, 42, and 2026, respectively.

For Construction-PPE-trained models, mean in-domain mAP50:95 increased from 0.252 ± 0.004 to 0.269 ± 0.002 and cross-domain Y-PPE performance increased from 0.082 ± 0.005 to 0.099 ± 0.005. The resulting `best.pt` gap was 0.170, or approximately 63.3% relative. Seed-level gaps remained positive at 0.167, 0.167, and 0.177.

The class-level safety interpretation was more checkpoint-sensitive than the aggregate result. For Y-PPE-trained models, `best.pt` retained clear negative-state transfer losses: no_helmet 0.262 → 0.117, no_gloves 0.458 → 0.046, and no_boots 0.433 → 0.000. For Construction-PPE-trained models, `best.pt` improved in-domain no_helmet and no_gloves recall to 0.198 and 0.092, while cross-domain recall on Y-PPE was 0.000 and 0.011; no_boots remained 0.000 in both domains. Thus, the aggregate domain-shift conclusion was robust to checkpoint policy, whereas the decomposition between in-domain learnability failure and additional transfer loss for individual negative-state classes was partly checkpoint-dependent.

**Table 4. Validation-selected `best.pt` sensitivity summary (mean ± SD across three seeds).**

| Training domain | Test domain | mAP50:95 | Fixed-point recall | Fixed-point F1 | no_helmet recall | no_gloves recall | no_boots recall |
|---|---|---:|---:|---:|---:|---:|---:|
| Y-PPE | Y-PPE | 0.312 ± 0.006 | 0.596 ± 0.030 | 0.682 ± 0.010 | 0.262 ± 0.149 | 0.458 ± 0.046 | 0.433 ± 0.067 |
| Y-PPE | Construction-PPE | 0.122 ± 0.002 | 0.419 ± 0.018 | 0.507 ± 0.010 | 0.117 ± 0.041 | 0.046 ± 0.011 | 0.000 ± 0.000 |
| Construction-PPE | Construction-PPE | 0.269 ± 0.002 | 0.694 ± 0.021 | 0.708 ± 0.010 | 0.198 ± 0.113 | 0.092 ± 0.060 | 0.000 ± 0.000 |
| Construction-PPE | Y-PPE | 0.099 ± 0.005 | 0.344 ± 0.013 | 0.384 ± 0.014 | 0.000 ± 0.000 | 0.011 ± 0.000 | 0.000 ± 0.000 |

## 4. Discussion

The results demonstrate a substantial distinction between in-domain PPE detection performance and cross-domain reliability under the evaluated training protocol. In the original held-out analysis, transfer to the alternate domain produced an approximately 0.17 absolute loss in mAP50:95 in both directions, and the sign of the gap was consistent across all three seed realizations. Two independent robustness checks strengthened this aggregate conclusion. First, the Stage 11A split-dependence sensitivity analysis preserved substantial gaps after removing confirmed near-duplicate derivatives and after conservative exclusion of high-confidence train-related test scenes. Second, validation-selected `best.pt` checkpoints also retained large gaps—0.191 for Y-PPE-trained models and 0.170 for Construction-PPE-trained models. The aggregate reliability result is therefore not specific to the final-epoch checkpoint policy or to the identified train–test dependence cases.

The class-level PPE-negative-state results are more nuanced than the aggregate mAP result. Under the primary final-epoch policy, Y-PPE-trained models had non-trivial in-domain recall for all three negative-state classes and then lost 0.193–0.367 recall after transfer, providing clear evidence of safety-relevant transfer degradation. Construction-PPE-trained final-epoch models were near floor in-domain, so the primary reverse-direction results alone could not cleanly separate poor class learnability from domain shift. The `best.pt` sensitivity analysis changed that interpretation for no_helmet and no_gloves: in-domain recall increased to 0.198 and 0.092, but cross-domain recall on Y-PPE remained 0.000 and 0.011. Thus, some reverse-direction class failure is checkpoint-policy sensitive and includes additional transfer loss when a stronger validation-selected checkpoint is used. In contrast, no_boots remained 0.000 in-domain and cross-domain under both checkpoint policies, indicating a persistent class-learnability failure for that category. The central safety lesson is therefore that aggregate metrics can conceal multiple failure modes, and class-level causal interpretation should not be generalized from a single checkpoint policy.

The dataset diagnostic audit identified several plausible contributors. Construction-PPE showed greater class imbalance and considerably lower no_boots training support than Y-PPE. The two domains also differed in object-scale distributions, especially for no_boots. These characteristics are consistent with the observed failures but are not sufficient as complete causal explanations. Construction-PPE no_helmet had nontrivial training support yet near-floor negative-state performance, and consensus failures in the Construction-PPE → Y-PPE direction occurred even for medium and large objects.

Accordingly, the observed reliability collapse appears broader than a rare-class or small-object problem. Plausible mechanisms include domain-specific appearance, contextual cues, annotation semantics, scene composition, and learned correlations that do not transfer between datasets. These mechanisms remain hypotheses rather than experimentally isolated causes.

A central methodological implication is that conventional same-dataset train/validation/test evaluation can overstate deployment readiness across the evaluated domains. For safety-critical PPE systems, external-domain evaluation should be treated as a distinct evidence requirement before broader deployment. Multi-seed evaluation is also useful because it separates persistent transfer failure from random training variability. Finally, class-specific recall and false-negative analysis should accompany aggregate mAP because the operational consequence of missing a PPE-negative-state instance in a context where that PPE is required is not captured by overall detection accuracy alone.

### 4.1 Limitations

This revised study includes only one completed detector architecture. The original plan included RF-DETR, but incomplete RF-DETR runs were excluded before final held-out analysis. The study therefore does not support claims of YOLO11m superiority over another architecture or architecture-independent generalization.

Only two harmonized datasets and three seeds per source domain are included. The evidence is sufficient to demonstrate reproducible degradation in this experiment but not to represent all construction domains.

The primary training recipe is intentionally controlled and uses final-epoch checkpoints with online stochastic augmentation disabled. A validation-selected `best.pt` sensitivity analysis was added and confirmed that the aggregate cross-domain mAP50:95 gap persisted, but some class-level PPE-negative-state recalls changed materially. The results therefore support checkpoint-robust aggregate degradation under this training recipe but do not characterize every plausible YOLO11m recipe. Sensitivity to a standard augmentation policy remains untested.

The dependence audit identified a small number of Y-PPE near-duplicate derivatives and a larger set of Construction-PPE related-scene test images. Prespecified sensitivity evaluation showed that substantial aggregate cross-domain gaps persisted, but scene dependence remains a property of the source datasets that should be considered when interpreting absolute in-domain performance.

The image-cluster bootstrap added uncertainty intervals for cross-domain PPE-negative-state recall and consensus false-negative rates. A corresponding image-level bootstrap interval for mAP50:95 is not reported in this journal-submission version because the original Stage 6 summaries did not retain the per-image ranked prediction statistics required to recompute AP exactly under resampling. Aggregate mAP uncertainty is therefore summarized by seed-level SD together with the prespecified split-dependence and checkpoint-policy sensitivity analyses rather than by an approximate object-level bootstrap.

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

This study shows that aggregate in-domain detection performance is not sufficient evidence of deployment readiness across the evaluated PPE domains. Across two harmonized construction PPE domains and three random seeds per source domain, YOLO11m exhibited substantial aggregate cross-domain degradation that persisted under both split-dependence sensitivity analysis and validation-selected `best.pt` checkpoint sensitivity. The latter produced mean mAP50:95 gaps of 0.191 for Y-PPE-trained models and 0.170 for Construction-PPE-trained models, confirming that the principal aggregate finding is not specific to final-epoch checkpoint selection.

Class-level PPE-negative-state behavior was less uniform. Y-PPE-trained models showed strong transfer degradation under both checkpoint policies. Construction-PPE results were more checkpoint-sensitive: validation-selected checkpoints improved in-domain no_helmet and no_gloves recall, revealing additional transfer loss that was masked by the weaker final-epoch class performance, while no_boots remained undetected in both domains. These findings support a deployment-oriented evaluation principle: safety-critical computer-vision systems should be assessed not only by same-domain mAP but by external-domain generalization, multi-seed robustness, checkpoint-policy sensitivity, class-specific recall, and false-negative behavior.

## Data and Code Availability

The experimental code, frozen protocols, dataset fingerprints, evaluation scripts, and analysis workflow are available in the public GitHub repository **EZZALDEEN049/Y-PPE-Detection-RFDETR** (https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR), with the Stage 11 revision maintained on the `stage11-major-revision` branch. The frozen Y-PPE-h9-v2 and Construction-PPE-h9-v2 manifest fingerprints are reported in Methods, and the Stage 4.5 exclusion manifests and reproducibility records are retained in the repository/workflow artifacts. The analysis code used for the final sensitivity runs is pinned to immutable Git commit `10e7b7e116288869647c61287d0c88056bf0a972`. The submitted manuscript and associated reproducibility files are preserved on the `submission-final-2026-10-09` branch. Source-image access remains subject to the licensing and governance terms of the originating datasets.

## Declarations

**Funding:** This research received no external funding.

**Competing interests:** The author declares that he has no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

**Author contributions:** Ezzaldeen Nabil Ghaleb Obadi Al-Tayar: Conceptualization; Methodology; Software; Validation; Formal analysis; Investigation; Data curation; Writing - original draft; Writing - review and editing; Visualization; Project administration.

**Ethics and image governance:** The Y-PPE corpus used secondary images originally captured during routine field monitoring in Yemeni development projects. The source study documents that acquisition occurred in the researcher's professional safety-monitoring context, that geographic and personal metadata were removed before analysis, and that the AI workflow was framed as a safety-management and decision-support tool rather than punitive surveillance. The source documentation reports alignment with Taiz University guidelines for responsible research. No formal ethics approval identifier is stated in the available source materials. The public Y-PPE project page declares CC BY 4.0; that platform declaration is reported here without inferring a separate third-party redistribution authorization that is not documented in the available study records.

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
19. Fang Q, Li H, Luo X, Ding L, Luo H, Rose TM, An W. Detecting non-hardhat-use by a deep learning method from far-field surveillance videos. *Automation in Construction*. 2018;85:1–9. doi:10.1016/j.autcon.2017.09.018.
20. Wu J, Cai N, Chen W, Wang H, Wang G. Automatic detection of hardhats worn by construction personnel: A deep learning approach and benchmark dataset. *Automation in Construction*. 2019;106:102894. doi:10.1016/j.autcon.2019.102894.
21. Chen S, Demachi K. Towards on-site hazards identification of improper use of personal protective equipment using deep learning-based geometric relationships and hierarchical scene graph. *Automation in Construction*. 2021;125:103619. doi:10.1016/j.autcon.2021.103619.
22. Xiong R, Tang P. Pose guided anchoring for detecting proper use of personal protective equipment. *Automation in Construction*. 2021;130:103828. doi:10.1016/j.autcon.2021.103828.
23. Wang Z, Wu Y, Yang L, Thirunavukarasu A, Evison C, Zhao Y. Fast Personal Protective Equipment Detection for Real Construction Sites Using Deep Learning Approaches. *Sensors*. 2021;21(10):3478. doi:10.3390/s21103478.
24. Torralba A, Efros AA. Unbiased Look at Dataset Bias. In: *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*. 2011:1521–1528. doi:10.1109/CVPR.2011.5995347.
25. Geirhos R, Jacobsen JH, Michaelis C, et al. Shortcut learning in deep neural networks. *Nature Machine Intelligence*. 2020;2:665–673. doi:10.1038/s42256-020-00257-z.
26. Chen Y, Li W, Sakaridis C, Dai D, Van Gool L. Domain Adaptive Faster R-CNN for Object Detection in the Wild. In: *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition*. 2018:3339–3348. doi:10.1109/CVPR.2018.00352.
27. Ben-David S, Blitzer J, Crammer K, Kulesza A, Pereira F, Vaughan JW. A theory of learning from different domains. *Machine Learning*. 2010;79:151–175. doi:10.1007/s10994-009-5152-4.
28. Ganin Y, Ustinova E, Ajakan H, Germain P, Larochelle H, Laviolette F, Marchand M, Lempitsky VS. Domain-Adversarial Training of Neural Networks. *Journal of Machine Learning Research*. 2016;17(59):1–35.
29. Taori R, Dave A, Shankar V, Carlini N, Recht B, Schmidt L. Measuring Robustness to Natural Distribution Shifts in Image Classification. *Advances in Neural Information Processing Systems*. 2020;33:18583–18599.
