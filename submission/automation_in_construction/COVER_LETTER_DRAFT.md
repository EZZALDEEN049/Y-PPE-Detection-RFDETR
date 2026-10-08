Dear Editor,

Please consider my manuscript, “Cross-Domain Reliability of YOLO11m for Safety-Critical PPE Monitoring: A Multi-Seed Bidirectional Evaluation,” for publication as an Original Research Article in Automation in Construction.

The manuscript addresses a deployment-reliability problem in construction computer vision: whether a personal protective equipment detector that performs acceptably within its development domain remains reliable when transferred to a visually distinct construction domain. Two PPE datasets were harmonized to a shared nine-class ontology, three independently trained YOLO11m seed realizations were completed per source domain, the held-out evaluation protocol was frozen before test exposure, and every completed final-epoch checkpoint was evaluated both in-domain and on the alternate domain.

The aggregate result is a large and reproducible cross-domain degradation. Mean mAP50:95 decreased from 0.291 to 0.121 for Y-PPE-trained models and from 0.252 to 0.082 for Construction-PPE-trained models. A dedicated post-hoc split-dependence audit found no exact byte-level cross-split duplicates, and the principal aggregate domain-gap conclusion remained substantial after both strict near-duplicate exclusion and a more conservative train-scene exclusion sensitivity analysis.

The PPE-negative-state analysis is deliberately interpreted asymmetrically. Y-PPE-trained models showed clear additional transfer degradation for no_helmet, no_gloves, and no_boots. By contrast, Construction-PPE-trained models were already near floor for these explicit PPE-negative-state classes in-domain, so their poor reverse-transfer results are treated primarily as a class-learnability limitation under the evaluated training protocol rather than as additional domain-shift loss. This distinction is central to the paper: aggregate detection metrics can conceal both poor in-domain learning of deployment-critical classes and additional cross-domain degradation.

The contribution is not a new detector architecture or domain-adaptation algorithm. It is a deployment-oriented reliability evaluation that combines bidirectional zero-shot external-domain testing, repeated seed realizations, explicit learnability-versus-transfer decomposition, deterministic consensus-failure auditing, and split-dependence sensitivity analysis.

The manuscript reports only the six fully completed YOLO11m runs. Incomplete experiments from an earlier architecture-comparison plan are excluded from all quantitative claims. No target-domain fine-tuning, checkpoint reselection for the primary analysis, or test-informed threshold optimization was performed.

This is a single-author manuscript. I am the sole and corresponding author, and my contact email is azzaltayyar@gmail.com. This research received no external funding, I declare no competing interests, and the manuscript is not under consideration by another journal.

Thank you for your consideration.

Sincerely,

Ezzaldeen Nabil Ghaleb Obadi Al-Tayar
Faculty of Engineering and Information Technology
Taiz University, Yemen
azzaltayyar@gmail.com
