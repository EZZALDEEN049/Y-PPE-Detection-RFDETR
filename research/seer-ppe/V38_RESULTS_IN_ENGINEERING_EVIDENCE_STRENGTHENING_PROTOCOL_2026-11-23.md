# V38 — Results in Engineering scientific evidence strengthening: prospective execution protocol

**Created:** 23 November 2026. **Classification:** research planning, no model calls authorized or executed by this document.  
**Submission target:** Results in Engineering (Elsevier).  
**Approved title:** Cross-Resolution Consistency of Target-Matched Perturbation Sensitivity Maps for Personal Protective Equipment Detection.  
**Frozen base:** existing V26 detection reference (459 Valid images), V30 8×8 target data (1,068 historical hosted model calls), V33B 4×4 (496 calls), V34A/V34B spatial correlations, V35 numeric audit, V36/V37 editorial artifacts. Preserve original RF-DETR Small 17-class checkpoint, 17 class mapping, source labels, splits and held-out Test.

## A. Strengthen evidence without model inference — first

1. V38-A: run exact-source, image-grouped leave-one-image-out and equal-image weighted descriptive sensitivity for rho, tau and top-four overlap. **Done**; see `research/seer-ppe/V38_A_IMAGE_CLUSTER_SENSITIVITY_REPORT_2026-11-23.md`.
2. For paper: add no-spurious-significance wording; disaggregate ten target values, compare image and target weighting, keep the zero-overlap map and the 39/40 valid AUC accounting visible.
3. Reconcile 17 per-class TP/FP/FN, 459 cohort and M1/M2, noting selection/label uncertainty; do not treat 459 images as an independent external evaluation.
4. Literature matrix: side-by-side our exact target-matched 8×8 vs 4×4 paired grid protocol against Andrés et al., *Results in Engineering* 24 (2024), article 103498, D-RISE/D-MFPP/D-Deletion, doi:10.1016/j.rineng.2024.103498; add precise citation after metadata check. Our method does not claim priority for XAI or grid perturbation generally.
5. Curate an auditable first-release independent figure, target-level table and versioned source scripts; retain a record of human images disclosure restrictions.

## B. New experiments only with a frozen prospective protocol and a cost estimate

**B1 — sample diversity (highest empirical priority):** Design a separate diagnostic replication cohort of *about 40–60 target detections across at least 20–30 distinct images* with several PPE classes, confidence bands and difficult/easy conditions. These are provisional feasibility planning targets, not a publisher requirement or validated power calculation. A truly independent-source generalization claim additionally requires distinct acquisition-project/site families outside previous development; **merely sampling another Valid image does not provide that independence**. If independent, lawful imagery is not available, report the analysis as an enlarged development-exposed diagnostic set. Never repurpose protected Test for method tuning.

**B2 — random and rule baselines:** For prespecified targets, compare against at least 20–30 distinct seeded random rankings (budget permitting) rather than one; estimate per-target random AUC distribution and empirical rank, and compare saliency vs a simple predefined geometry/centrality ranking when feasible. Match number of model calls and perturbed area across comparisons. The present one-random control and overlapping A5/A6 selections do not prove winner or explainability quality.

**B3 — perturbation confounding control:** Prespecify gray-fill vs Gaussian blur vs a lawful/feasible replacement baseline; test whether occluding one coarse 4×4 region in a **single call** differs from separately occluding its four 8×8 subregions and then aggregating. This diagnoses interaction/nonlinearity that cell-area normalization cannot eliminate. Keep signed negative responses and target loss/ambiguity rules visible.

**B4 — published comparator:** If inference budget permits, evaluate one publicly documented, detection-specific model-agnostic explainer such as D-RISE or D-MFPP on matched targets with a comparable model-call budget, and reproduce its scoring conventions as closely as possible; only compare if target match, area coverage and evaluation endpoint are genuinely comparable. A citation/literature contrast is mandatory even if expensive model-based method comparison is infeasible.

**B5 — optional decision relevance:** If paper scope expands beyond map consistency, first design genuine worker-to-PPE association and authorized task-specific annotation with independent review; otherwise explicitly defer compliance and human-use claims. No safety claims from image-level object classification.

## C. Statistical analysis for prospective replication

- **Primary endpoint:** image-level mean Fisher-free Spearman rho of aligned signed sensitivity ranks between directly scored 4×4 map and area-weighted fine 8×8 map; also report median, dispersion and target distribution. Keep negative sensitivity values.
- **Co-primary/descriptive:** top-four overlap per target, Kendall tau-b; separate per-image and per-target summaries. Decide formal primary vs supportive outcomes *before* acquiring data.
- **Uncertainty:** independent-image/site-family clustered or hierarchical bootstrap **only when sample design supports inference**; report 95% intervals transparently as exploratory when nonprobabilistic selection is used. Do not use cells as independent sample replicates.
- **Exposure diagnostics:** show performance separately for truly acquisition-independent and development-exposed source groups; do not label M2 independently held-out.
- **Design QA:** fixed image source IDs/hashes, exact target detection IDs, deterministic masks and seeds, original-image pixel alignment, 4×4 and 8×8 area fractions; predefine missing ambiguous curve treatment (null, never replaced by a success). Include no silent post hoc target exclusions.
- **Stop/release gate:** compare worst-case evidence quality; retain zero-overlap cases and negative results, do not add repeated trials until a preferred p-value appears. Document any deviation from plan. No claim of a measured power/sample-size guarantee from a target count chosen for practical reasons.

## D. Practical ordering and resource gate

1. **Zero new model calls:** V38-A complete, citation matrix and draft limitation/novelty refinement next.
2. **Cost-controlled pilot:** select a predeclared diversified candidate set and estimate hosted RF-DETR call budget based on deduplicated images, shared cell calls, number of curves, seeds and comparison methods *before* inference.
3. **Reproduction:** execute only approved-budget new calls against same frozen checkpoint, log every call and missing target outcome.
4. **Journal deliverables:** publish new target-level tables, confidence/uncertainty/variability visualizations and sensitivity-ablation results; report current 459-image F1 only as internal diagnostic context. Human review, authenticity/right-to-publish, CRediT/COI/funding/AI and figure guidelines remain separate V37 sign-off gates.

**Strongest defensible message:** perturbation sensitivity maps exhibit quantitatively measurable, target-specific **resolution dependence**. Better controls improve evidence for the scope of this result but do not prove correct explanation, model causal faithfulness or worker safety benefits.
