# Stage 11F — Literature and Novelty Matrix

This matrix reframes novelty as a **deployment-oriented reliability evaluation gap**, not as a claim that domain shift or domain adaptation in construction is new.

| Study | Domain-shift setting | Target adaptation/training | Construction/PPE focus | External/unseen-domain evaluation | Reliability feature most relevant here |
|---|---|---|---|---|---|
| Nath et al. (2020), Automation in Construction | Uncontrolled jobsite PPE detection | No explicit domain adaptation | PPE: hard hat/vest | Primarily within collected jobsite data | Establishes real-time PPE feasibility, not cross-domain reliability auditing |
| Kim, Seong & Jung (2024), Automation in Construction | Different construction monitoring settings/sites | Unsupervised domain adaptation using target-site images | Construction monitoring; worker/hardhat context | Yes, target construction sites/unseen-site comparison | Shows performance degradation across sites and improvement through adaptation |
| Bharathi et al. (2024), ISARC | Robot-collected construction safety imagery | Unsupervised domain adaptation | Construction safety guardrails | Domain-adaptation evaluation | Demonstrates domain adaptation for automated safety inspection beyond PPE |
| Tran et al. (2025), JCEM | Environmental/site variation plus long-tailed classes | Semisupervised domain adaptation | Construction workers/vehicles and risk scenarios | Evaluated on construction CCTV data | Couples site adaptation with class-imbalance handling |
| Seong, Kim & Jung (2026), Automation in Construction | 11 construction sites; 5 unseen test sites | Domain-generalization method, no target-specific retraining at final unseen sites | Construction object detection/safety | Yes | Strong recent cross-site DG benchmark; includes YOLOv11, Faster R-CNN and DETR corroboration |
| Wang (2026), Scientific Reports | General-context/body-worn images to construction non-PPE | Domain-adaptive Faster R-CNN | Explicit non-PPE | Yes | Directly addresses PPE/non-PPE domain adaptation |
| Vukicevic et al. (2024) | Review of PPE compliance variability | N/A | PPE | Review | Identifies industrial variability and deployment barriers |
| Barlybayev et al. (2026) | Review of practical PPE CV conditions | N/A | PPE | Review | Highlights cross-domain generalization, imbalance and practical performance variability |
| Recht et al. (2019) | New test sets from nominally same benchmark generation process | None | General vision | Yes | Shows that nominal same-task external test sets can reveal material accuracy drops |
| Ovadia et al. (2019) | Dataset shift | None | General ML | Yes | Establishes that reliability/uncertainty can degrade under shift |
| Koh et al. (2021), WILDS | Naturally occurring real-world distribution shifts | None in baseline benchmark | General ML/CV | Yes | Formalizes in-domain vs out-of-distribution evaluation as a deployment benchmark |
| Gulrajani & Lopez-Paz (2021) | Domain generalization benchmarks | No target adaptation | General ML/CV | Yes | Emphasizes fair experimental controls and model-selection policy |
| Zhou et al. (2023) | Domain generalization survey | N/A | General ML/CV | Review | Provides formal DG framing and distinction from domain adaptation |

## Revised gap statement

Recent construction research already demonstrates both **domain adaptation** and **domain generalization** across sites. The present paper therefore does not claim that construction-domain shift is unexplored and does not compete as a new adaptation algorithm.

The narrower gap is evaluation-oriented:

> Deployment-oriented PPE studies still provide limited evidence that separates (i) aggregate external-domain degradation, (ii) failure to learn explicit negative-state classes even in-domain, and (iii) persistent cross-domain false negatives under a frozen zero-shot protocol, while also testing whether the conclusion survives split-dependence sensitivity.

The contribution is consequently a **reliability audit design**: bidirectional zero-shot external evaluation, repeated seed realizations, explicit safety-class learnability-versus-transfer decomposition, consensus-failure persistence, and post-hoc dependence sensitivity, rather than novelty-by-combination or a new detector.
