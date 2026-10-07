# Stage 9 — Literature Positioning and Novelty Matrix

**Search date:** 2026-10-08  
**Purpose:** position the revised YOLO11m-only paper against recent PPE and construction-domain generalization literature.

## Core literature

| Study | Main setting | Domain/generalization design | Safety-failure emphasis | Relation to current study |
|---|---|---|---|---|
| Vukicevic et al., *Artificial Intelligence Review* (2024), DOI: 10.1007/s10462-024-10978-x | Systematic review of CV-based PPE compliance | Reviews datasets, algorithms, environments, barriers to wider adoption | Highlights industrial variability, data limitations, and deployment barriers | Establishes that real-world variability and deployment remain unresolved; supports external-domain reliability motivation |
| Barlybayev et al., *Computers* (2026), DOI: 10.3390/computers15060388 | Systematic review of PPE-compliance CV | Explicitly identifies cross-domain generalization/domain shift as an open research challenge | Recommends safety-aware metrics that weight false negatives rather than headline mAP alone | Closely motivates this paper's external-domain and false-negative-oriented evaluation |
| Seong, Kim & Jung, *Automation in Construction* 182 (2026) 106761, DOI: 10.1016/j.autcon.2026.106761 | Construction object detection across sites | Cross-HNM evaluated across 11 sites and 5 unseen test sites; cross-site generalization is the primary target | Focus is general construction object detection and hard-negative mining, not PPE-negative-state consensus failure | Strong evidence that cross-site shift is a recognized construction-vision problem; current paper contributes a diagnostic PPE-specific reliability audit rather than a new adaptation method |
| Wang, *Scientific Reports* 16 (2026) 4793, DOI: 10.1038/s41598-026-35148-7 | Non-PPE identification | Domain-adaptive Faster R-CNN aligns general-context and construction-site domains | Evaluates five non-PPE categories | Shows domain adaptation can mitigate PPE-domain shift; current paper asks the prior diagnostic question: how severe is zero-shot failure before adaptation? |
| Wang et al., *Scientific Reports* 16 (2026) 24591 | Multi-category PPE non-compliance | Includes external validation on two previously unseen construction sites | Five non-compliance classes; analyzes small/far-field/overlap failures | Closest validation precedent; current paper differs through bidirectional harmonized transfer, three seeds per source domain, frozen final-epoch checkpoints, and consensus FN analysis |
| Ahmad & Rahimi, *Journal of Safety Science and Resilience* 6(2) (2025) 175–185, DOI: 10.1016/j.jnlssr.2024.09.002 | SH17 PPE dataset, 8,099 images and 17 classes | Reports cross-domain validation of PPE models | Broad PPE/body-part dataset; not centered on missing-PPE consensus failure | Demonstrates value of heterogeneous PPE datasets and cross-domain checking; current paper adds controlled bidirectional safety-reliability analysis |
| Ferdous & Ahsan, *PeerJ Computer Science* (2022), DOI: 10.7717/peerj-cs.999 | PPE detector and CHVG dataset | Primarily within-dataset PPE detector benchmarking | Detection accuracy and real-time behavior | Representative of the dominant detector-development paradigm that motivates stronger external-domain validation |
| Nath, Behzadan & Paal, *Automation in Construction* 112 (2020) 103085, DOI: 10.1016/j.autcon.2020.103085 | Real-time hard-hat/vest detection | Real-world jobsite images, but not the present bidirectional cross-dataset reliability design | Practical PPE monitoring | Foundational construction-PPE detection reference; useful for historical context |

## Construction-PPE dataset source

The external Construction-PPE source is documented by Ultralytics as:

- 1,416 images;
- 11 classes;
- 1,132/143/141 train/validation/test;
- version 1.0.0;
- AGPL-3.0 license.

The current paper uses a prespecified nine-class conservative derivative rather than the raw 11-class source.

## What is genuinely novel in the current study

The strongest defensible novelty is **not** "a new detector" and **not** "the first study of domain shift."

The contribution is the combination of:

1. **bidirectional zero-shot cross-domain evaluation** between two PPE datasets after an explicit semantic harmonization protocol;
2. **three independent random seeds per source domain**, allowing the domain gap to be separated from one-run stochastic variation;
3. a **held-out protocol frozen before test exposure**, with final-epoch checkpoints and no test-informed threshold/checkpoint selection;
4. explicit focus on **safety-negative classes** (`no_helmet`, `no_gloves`, `no_boots`) rather than aggregate mAP alone;
5. **three-seed consensus false-negative analysis**, quantifying violation objects missed by every independently trained source-domain model;
6. a post-hoc but non-adaptive **dataset diagnostic audit** linking failure patterns to class support and object-scale distributions without claiming unsupported causality;
7. evidence from a **resource-constrained Yemeni visual domain** paired with a global/public construction PPE dataset.

## Novelty wording recommended for the manuscript

Avoid absolute priority language such as "the first ever."

Use:

> Recent studies have begun to address domain adaptation, unseen-site validation, and cross-site generalization in construction vision. However, among the literature reviewed here, we did not identify a PPE study combining bidirectional zero-shot transfer over a harmonized label space, three independent seeds per source domain, a pre-frozen held-out protocol, and consensus false-negative analysis of explicit PPE non-compliance classes. This study addresses that reliability-evaluation gap rather than proposing a new detector architecture.

## Why the paper remains publishable without RF-DETR

The literature already contains many architecture-improvement papers. A weaker version of this work would add another model comparison.

The revised paper instead answers a deployment-reliability question:

> How much does a completed PPE detector degrade when moved between visually and semantically harmonized construction domains, and do the safety-critical failure modes persist across independent training seeds?

That question is independently valuable and is aligned with the open challenges identified in recent PPE systematic reviews.

## Citation list to integrate

1. Vukicevic AM, Petrovic M, Milosevic P, et al. A systematic review of computer vision-based personal protective equipment compliance in industry practice: advancements, challenges and future directions. *Artificial Intelligence Review*. 2024;57:319. doi:10.1007/s10462-024-10978-x.
2. Barlybayev A, Milosz M, Amangeldy N, Li G, Razakhova B, Tazhibay A, Nazyrova A, Lamasheva Z. Systematic Review of Computer-Vision Technologies for Personal Protective Equipment Compliance Monitoring. *Computers*. 2026;15(6):388. doi:10.3390/computers15060388.
3. Seong J, Kim HS, Jung HJ. Improving cross-site generalization in construction object detection via hard negative mining. *Automation in Construction*. 2026;182:106761. doi:10.1016/j.autcon.2026.106761.
4. Wang S. Domain-adaptive faster R-CNN for non-PPE identification on construction sites from body-worn and general images. *Scientific Reports*. 2026;16:4793. doi:10.1038/s41598-026-35148-7.
5. Wang S, Kim H, Yeo J, et al. YOLOv10-based multi-scale variant object detection for multi-category PPE non-compliance monitoring on construction sites. *Scientific Reports*. 2026;16:24591. doi:10.1038/s41598-026-53052-y.
6. Ahmad HM, Rahimi A. SH17: A dataset for human safety and personal protective equipment detection in manufacturing industry. *Journal of Safety Science and Resilience*. 2025;6(2):175-185. doi:10.1016/j.jnlssr.2024.09.002.
7. Ferdous M, Ahsan SMM. PPE detector: a YOLO-based architecture to detect personal protective equipment (PPE) for construction sites. *PeerJ Computer Science*. 2022;8:e999. doi:10.7717/peerj-cs.999.
8. Nath ND, Behzadan AH, Paal SG. Deep learning for site safety: Real-time detection of personal protective equipment. *Automation in Construction*. 2020;112:103085. doi:10.1016/j.autcon.2020.103085.
