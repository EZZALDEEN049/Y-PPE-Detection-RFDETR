# Related-work collision audit (verified source metadata, 2026-10-29)

**Purpose:** protect the proposed SRAC-PPE paper against unsupported novelty claims. This is not a comprehensive systematic review, nor confirmation of journal quartile category/year.

| Work | Verified contribution that overlaps SRAC-PPE | What SRAC-PPE must still establish |
|---|---|---|
| Angelopoulos, Bates, Fisch, Lei & Schuster, *Conformal Risk Control*, ICLR 2024 | Already develops general risk-controlled prediction and distribution-shift extensions. https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html | Bonferroni + Clopper–Pearson is an established statistical procedure, **not** a claimed novel theorem. |
| Huseljic et al., *Systematic Evaluation of Uncertainty Calibration in Pretrained Object Detectors*, IJCV 2025; DOI:10.1007/s11263-024-02219-z | Explicitly accounts for missing object predictions in calibration analysis. https://link.springer.com/article/10.1007/s11263-024-02219-z | Show added value from context-verified, *worker-level routing risk* rather than simply accounting for missing detections. |
| Seong, Kim & Jung, *Improving cross-site generalization in construction object detection via hard negative mining*, Automation in Construction 2026; DOI:10.1016/j.autcon.2026.106761 | Evaluates 11 construction-site datasets and five unseen test sites; includes transformer detectors. https://www.sciencedirect.com/science/article/pii/S0926580526000026 | Distinguish risk-limited compliance decisions from training a more transferable detector, and prove site provenance. |
| Zhang, *Visual detection of workers' personal protective equipment for underground construction safety management*, Frontiers in Earth Science 2026; DOI:10.3389/feart.2026.1878141 | Explicit worker-level evidence, uncertainty, visibility and human review — substantial idea overlap. https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2026.1878141/full | Worker association, visibility and REVIEW alone cannot be claimed as novel; evaluate the independently bounded false-clearance/missed-worker risk and scarce labels. |
| Akhazhanov et al., *Multi-Label PPE Classification from Construction-Site Person Crops*, Buildings 2026; DOI:10.3390/buildings16173536 | Person-level PPE recognition with calibration, repeated seeds, and video-group splits. https://www.mdpi.com/2075-5309/16/17/3536 | Demonstrate end-to-end detector+worker omission and site-conditional risk effects; avoid claiming novelty for basic temperature scaling. |
| Liang et al., *Gaze-guided activity recognition for task-specific PPE compliance monitoring in hot work*, Advanced Engineering Informatics 2026; vol.70, article 104211 | Incorporates task-specific PPE rules and ontology reasoning. https://www.sciencedirect.com/science/article/abs/pii/S1474034625011048 | Context-sensitive PPE requirements are necessary but are not independently novel. |
| Robinson et al., *RF-DETR: Neural Architecture Search for Real-Time Detection Transformers*, ICLR 2026 | RF-DETR established independently as a real-time detection transformer. https://proceedings.iclr.cc/paper_files/paper/2026/hash/5bed8703db85ab27dc32f6a42f8fbdb6-Abstract-Conference.html | Frozen RF-DETR is a preexisting backbone; the new paper's original contribution must be downstream decision reliability or new evaluation evidence. |

## Working novelty claim — deliberately narrow and falsifiable
Candidate contribution: a **context-adjudicated, worker-level** evaluation and policy layer over a fixed detector, reporting simultaneous one-sided bounds on **false CLEAR** and **missed-or-cleared** risk at independently audited target sites, including *statistical infeasibility/abstention under limited violation labels*, and comparison against **strong matched-review baselines**.

This currently describes a *research hypothesis and evaluation design*, **NOT demonstrated novelty or superiority**. The benchmark may show no advantage; such a result must be reported transparently.

## Required before Q1 submission
1. Broaden the literature search with query/date/eligibility logs; complete exact author/DOI verification.
2. Check whether subsequent 2026 work already tests finite-sample PPE-specific selective risk with missed-worker accounting.
3. Pre-register baselines and risk/coverage endpoints without viewing final-test labels.
4. Supply actual independent field results or narrow the manuscript to a clearly identified methodological feasibility study.
5. Verify target journal's SJR/JCR quartile **by category and year**; an article's content cannot itself be labeled Q1.
