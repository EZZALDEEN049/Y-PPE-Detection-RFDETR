# Cross-Domain Reliability of YOLO11m for Safety-Critical PPE Monitoring in Construction: A Multi-Seed Bidirectional Evaluation

## Abstract

Computer-vision systems for personal protective equipment (PPE) monitoring are commonly evaluated within the same dataset used for model development, although real deployment requires reliability across sites, cameras, and visual domains. This study evaluates the cross-domain reliability of YOLO11m for safety-critical PPE monitoring using two harmonized nine-class construction datasets, Y-PPE-h9-v2 and Construction-PPE-h9-v2. Six completed models were analyzed: three independent random seeds per source domain (17, 42, and 2026). Each final-epoch checkpoint was evaluated on both the in-domain and alternate held-out test set under a protocol frozen before held-out evaluation, producing 12 evaluation cells without further training, adaptation, checkpoint reselection, or threshold tuning. Y-PPE-trained models achieved an in-domain mAP50:95 of 0.291 ± 0.007, decreasing to 0.121 ± 0.003 on Construction-PPE, a 58.4% relative loss. Construction-PPE-trained models decreased from 0.252 ± 0.004 in-domain to 0.082 ± 0.005 on Y-PPE, a 67.4% relative loss. Safety-critical violation classes were substantially less reliable than aggregate metrics suggested. Consensus false-negative analysis across all three seeds showed cross-domain miss rates of 83.8–92.9% for no_helmet, 92.2–96.6% for no_gloves, and 100% for no_boots in both transfer directions. Dataset diagnostics identified differences in class support, imbalance, and object-scale distributions, but these factors did not fully explain the observed failure. The findings show that acceptable in-domain object-detection performance is insufficient evidence of deployment readiness for safety monitoring and support the use of external-domain testing, multi-seed evaluation, and false-negative-oriented safety metrics before real-world deployment.

**Keywords:** personal protective equipment; construction safety; computer vision; domain shift; cross-domain evaluation; YOLO11m; reliability; false negatives; occupational safety.

## 1. Introduction

Automated PPE monitoring is increasingly studied as a means of supporting occupational-safety supervision in construction environments. However, a model that performs well on a held-out subset drawn from the same dataset may still rely on dataset-specific visual regularities that do not transfer to a different construction site or data source.

The deployment problem is therefore not only whether a detector achieves high in-domain accuracy, but whether safety-critical decisions remain reliable under domain shift. This distinction is especially important for non-compliance classes such as workers without helmets, gloves, or protective boots, where false negatives directly undermine the purpose of automated monitoring.

This study focuses on cross-domain reliability rather than architecture competition. Two harmonized nine-class PPE datasets are used in a bidirectional design. YOLO11m is trained independently on each source domain using three random seeds and is then evaluated both in-domain and on the alternate held-out domain. The study additionally separates aggregate detection performance from safety-critical violation reliability and performs a deterministic consensus-failure audit across seeds.

The final contributions are:

1. a frozen, bidirectional, multi-seed cross-domain evaluation of six completed YOLO11m models across two harmonized PPE domains;
2. quantification of absolute and relative domain-generalization gaps using mAP, precision, recall, and F1;
3. safety-critical evaluation of no_helmet, no_gloves, and no_boots using fixed-threshold recall, false-negative rates, and three-seed consensus failures;
4. dataset-side diagnostic analysis of class support, imbalance, and object-scale distributions;
5. an evidence-based deployment interpretation showing that in-domain performance alone can substantially overstate PPE-monitoring readiness.

**Literature-review citations and comparison with prior PPE domain-generalization studies remain to be inserted before submission.**

## 2. Materials and Methods

### 2.1 Study design

The final experiment used a YOLO11m-only, multi-seed, bidirectional cross-domain design. The initial experimental plan included an additional detector architecture; however, incomplete runs were excluded before the final held-out analysis. The reported study therefore includes only the six fully completed YOLO11m runs and does not make architecture-comparison claims.

Two source domains were used:

- Y-PPE-h9-v2;
- Construction-PPE-h9-v2.

Three independent seeds were completed for each source domain: 17, 42, and 2026. Each model was evaluated on the held-out test set of its own source domain and the held-out test set of the alternate domain, producing 12 evaluation cells.

### 2.2 Harmonized class space

Both frozen derivatives use the same nine-class order:

1. person;
2. helmet;
3. gloves;
4. vest;
5. boots;
6. goggles;
7. no_helmet;
8. no_gloves;
9. no_boots.

Y-PPE-h9-v2 contains 1,236 training, 356 validation, and 186 test images. Construction-PPE-h9-v2 contains 1,046 training, 132 validation, and 138 test images.

### 2.3 Model checkpoints and reproducibility

Only completed YOLO11m runs were eligible. The six runs were:

- Y_YOLO_s17;
- Y_YOLO_s42;
- Y_YOLO_s2026;
- C_YOLO_s17;
- C_YOLO_s42;
- C_YOLO_s2026.

For every run, the primary evaluation checkpoint was the final-epoch checkpoint, `last.pt`. The best-validation checkpoint was not used for primary results. No model was retrained, fine-tuned, adapted, or reselected after the held-out evaluation began.

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

[
G = M_{in} - M_{cross}
]

where (M_{in}) is in-domain performance and (M_{cross}) is cross-domain performance for the same source training domain and seed. Positive values therefore indicate degradation under domain shift.

Relative mAP50:95 degradation was computed as:

[
D_{rel} = 100 	imes rac{M_{in} - M_{cross}}{M_{in}}
]

### 2.7 Dataset diagnostic audit

A post-evaluation diagnostic audit was performed without model retraining or threshold modification. For each dataset and split, the audit quantified:

- class-instance frequencies;
- maximum-to-minimum nonzero class imbalance ratio;
- safety-class support;
- normalized bounding-box area;
- object-size strata;
- stored image resolution and aspect ratio.

For descriptive scale analysis, normalized box area was grouped as small (<0.01), medium (0.01–<0.10), or large (≥0.10).

### 2.8 Deterministic consensus false-negative audit

A qualitative failure audit was then performed at the same frozen fixed operating point. A consensus false negative was defined as a ground-truth safety-violation object missed by all three independently trained source-domain seeds in the same transfer direction.

To reduce cherry-picking risk, examples were selected deterministically rather than visually. The audit retained the same confidence, IoU, image resolution, and final-epoch checkpoint policy used in Stage 6. The audit was explanatory only and did not alter any quantitative result.

### 2.9 Statistical position

The study uses three independent seeds per source domain. Accordingly, mean ± SD and paired seed-level generalization gaps are treated as descriptive uncertainty summaries. The study does not make strong population-level inferential claims from three seeds and does not claim causal identification of the mechanism behind domain shift.

## 3. Results

### 3.1 Cross-domain degradation

Y-PPE-trained models achieved an in-domain mAP50:95 of 0.291 ± 0.007 and a cross-domain mAP50:95 of 0.121 ± 0.003 on Construction-PPE. The absolute gap was approximately 0.170, corresponding to a 58.4% relative degradation.

Construction-PPE-trained models achieved an in-domain mAP50:95 of 0.252 ± 0.004 and a cross-domain mAP50:95 of 0.082 ± 0.005 on Y-PPE. The absolute gap was again approximately 0.170, but the relative degradation was larger at 67.4%.

The degradation was reproduced across all three seeds. Y-PPE-trained mAP50:95 gaps were 0.173, 0.178, and 0.159 for seeds 17, 42, and 2026. Construction-PPE-trained gaps were 0.172, 0.166, and 0.171, respectively.

### 3.2 Fixed operating-point reliability

Y-PPE-trained models decreased from mean precision/recall/F1 of 0.881/0.516/0.651 in-domain to 0.711/0.382/0.497 on Construction-PPE.

Construction-PPE-trained models decreased from 0.921/0.580/0.712 in-domain to 0.766/0.209/0.328 on Y-PPE. The particularly large recall loss in this direction indicates that cross-domain degradation manifested strongly as missed detections.

### 3.3 Safety-critical violation classes

For Y-PPE-trained models, in-domain mean recall was 0.310 for no_helmet, 0.303 for no_gloves, and 0.367 for no_boots. On Construction-PPE, the corresponding values fell to 0.117, 0.039, and 0.000.

Construction-PPE-trained models already exhibited near-floor in-domain recall for the same violation classes: 0.027 for no_helmet, 0.020 for no_gloves, and 0.000 for no_boots. Cross-domain transfer to Y-PPE yielded means of 0.024, 0.015, and 0.000.

### 3.4 Consensus failure across seeds

The deterministic consensus audit showed that the majority of cross-domain safety violations were missed by all three source-domain models.

For Y-PPE → Construction-PPE, consensus false-negative rates were:

- no_helmet: 31/37 = 83.8%;
- no_gloves: 47/51 = 92.2%;
- no_boots: 15/15 = 100%.

For Construction-PPE → Y-PPE:

- no_helmet: 13/14 = 92.9%;
- no_gloves: 85/88 = 96.6%;
- no_boots: 30/30 = 100%.

The no_boots class therefore exhibited complete consensus failure in both transfer directions.

### 3.5 Dataset-side diagnostics

Both frozen derivatives were stored as 640×640 square images, so stored resolution and aspect ratio did not differ across domains.

The training-set max-to-min nonzero class-frequency ratio was 11.49 in Y-PPE and 21.76 in Construction-PPE, indicating greater imbalance in the latter.

Safety-class support also differed. Y-PPE contained 113 no_helmet, 677 no_gloves, and 226 no_boots training instances. Construction-PPE contained 352, 403, and 74, respectively.

The strongest object-scale mismatch occurred for no_boots. Y-PPE training contained approximately 30.5% small, 21.2% medium, and 48.2% large no_boots instances. Construction-PPE contained approximately 77.0% small and 23.0% medium no_boots instances and no large instances.

However, object size alone could not explain the cross-domain collapse. In Construction-PPE → Y-PPE transfer, all 30 ground-truth no_boots objects were missed by all three models despite spanning 6 small, 10 medium, and 14 large instances.

## 4. Discussion

The results demonstrate a substantial distinction between in-domain PPE detection performance and cross-domain safety reliability. Although YOLO11m retained moderate aggregate in-domain detection performance, transfer to the alternate domain produced an approximately 0.17 absolute loss in mAP50:95 in both directions. The consistency of this loss across all three seeds indicates a persistent domain-generalization limitation rather than a single stochastic training anomaly.

The safety implications are more severe than aggregate AP values alone suggest. The violation classes no_helmet, no_gloves, and no_boots exhibited very high false-negative behavior under transfer, and most violation instances were missed by all three independently trained source-domain models. The 100% consensus false-negative rate for no_boots in both directions is particularly important because it illustrates how a detector may retain nonzero aggregate mAP while completely failing a deployment-critical safety category.

The dataset diagnostic audit identified several plausible contributors. Construction-PPE showed greater class imbalance and considerably lower no_boots training support than Y-PPE. The two domains also differed in object-scale distributions, especially for no_boots. These characteristics are consistent with the observed failures but are not sufficient as complete causal explanations. Construction-PPE no_helmet had nontrivial training support yet near-floor violation performance, and consensus failures in the Construction-PPE → Y-PPE direction occurred even for medium and large objects.

Accordingly, the observed reliability collapse appears broader than a rare-class or small-object problem. Plausible mechanisms include domain-specific appearance, contextual cues, annotation semantics, scene composition, and learned correlations that do not transfer between datasets. These mechanisms remain hypotheses rather than experimentally isolated causes.

A central methodological implication is that conventional same-dataset train/validation/test evaluation can overstate deployment readiness. For safety-critical PPE systems, external-domain evaluation should be considered a distinct requirement. Multi-seed evaluation is also useful because it separates persistent transfer failure from random training variability. Finally, class-specific recall and false-negative analysis should accompany aggregate mAP because the operational consequence of missing a safety violation is not captured by overall detection accuracy alone.

### 4.1 Limitations

This revised study includes only one completed detector architecture. The original plan included RF-DETR, but incomplete RF-DETR runs were excluded before final held-out analysis. The study therefore does not support claims of YOLO11m superiority over another architecture or architecture-independent generalization.

Only two harmonized datasets and three seeds per source domain are included. The evidence is sufficient to demonstrate reproducible degradation in this experiment but not to represent all construction domains.

The diagnostic audit identifies associations with class support, imbalance, and scale but does not experimentally isolate causal mechanisms.

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

This study shows that in-domain detection performance is not sufficient evidence of deployment-ready PPE safety monitoring. Across two harmonized construction PPE domains and three random seeds per source domain, YOLO11m experienced large and reproducible cross-domain degradation. More importantly, the safety-violation classes failed at substantially higher rates than aggregate detection metrics implied, with no_boots reaching a 100% consensus false-negative rate in both transfer directions.

The findings support a deployment-oriented evaluation principle: safety-critical computer-vision systems should be assessed not only by same-domain mAP but by external-domain generalization, multi-seed robustness, class-specific recall, and false-negative behavior. In settings where site-specific retraining is difficult or expensive, such evidence should be established before operational use.

## Data and Code Availability

The experimental code, frozen protocols, evaluation scripts, and analysis workflow are maintained in the project repository. A final archival identifier and public-data statement should be inserted before submission.

## Declarations

**Funding:** To be completed before submission.

**Competing interests:** To be completed before submission.

**Author contributions:** To be completed before submission.

**Ethics:** No human-subject intervention was performed in the model evaluation reported here; the exact dataset licensing and image-source statement must be verified and inserted before submission.

## References

To be completed after the literature-review and citation-integration stage.
