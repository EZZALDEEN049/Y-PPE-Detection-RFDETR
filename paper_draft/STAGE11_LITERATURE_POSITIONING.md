# Stage 11 — Strengthened Literature Positioning

The paper no longer treats domain shift itself as novel. Recent construction-vision studies already establish that changes in site, camera, and monitoring setting can degrade model performance and motivate domain adaptation or cross-site generalization.

The revised research gap is narrower:

> Deployment-oriented PPE evaluation needs to distinguish aggregate cross-domain detector degradation from persistent failure of explicit safety-violation classes under a frozen zero-shot transfer protocol.

Key construction-domain studies to integrate:

1. Hong Y, Chern W-C, Nguyen TV, Cai H, Kim H. Semi-supervised domain adaptation for segmentation models on different monitoring settings. Automation in Construction. 2023;149:104773. doi:10.1016/j.autcon.2023.104773.
2. Kim H-S, Seong J, Jung H-J. Optimal domain adaptive object detection with self-training and adversarial-based approach for construction site monitoring. Automation in Construction. 2024;158:105244. doi:10.1016/j.autcon.2023.105244.
3. Xu J, Pan W. Deep learning-based object detection for dynamic construction site management. Automation in Construction. 2024;165:105494.
4. Wang X, El-Gohary N. Few-shot object detection and attribute recognition from construction site images for improved field compliance. Automation in Construction. 2024;167:105539. doi:10.1016/j.autcon.2024.105539.
5. Chan C-F, Wong PK-Y, Guo X, Cheng JCP, Chan JP-C, Leung P-H, Tao X. Context-aware vision-language model agent enriched with domain-specific ontology for construction site safety monitoring. Automation in Construction. 2025;177:106305. doi:10.1016/j.autcon.2025.106305.
6. Seong J, Kim H-S, Jung H-J. Improving cross-site generalization in construction object detection via hard negative mining. Automation in Construction. 2026;182:106761. doi:10.1016/j.autcon.2026.106761.

Recommended novelty wording:

> Prior construction-vision studies have demonstrated the need for domain adaptation and cross-site generalization. The remaining deployment-oriented PPE question addressed here is not whether domain shift exists, but whether aggregate detector metrics conceal persistent failure of explicit PPE non-compliance classes under frozen zero-shot transfer. The study evaluates this question bidirectionally over a harmonized label space, across three training seeds, with a prespecified held-out protocol and a consensus false-negative analysis interpreted as failure persistence under training stochasticity.

Avoid claims that the paper is the first domain-shift study or that the three seeds are independent replications.
