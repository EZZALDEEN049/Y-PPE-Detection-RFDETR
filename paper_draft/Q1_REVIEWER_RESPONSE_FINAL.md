# Final Response to Q1-Style Major Revision

## Summary
The manuscript was substantially revised in response to the strict reviewer audit. The five highest-priority reviewer actions are now addressed.

## 1. Duplicate / near-duplicate audit
Completed. Exact SHA-256 cross-split duplicates were zero. Perceptual/geometric and manual review separated independent similarity, near-duplicates, and scene-level dependence. Four Y-PPE transformed near-duplicate test derivatives were confirmed. Construction-PPE candidates were conservatively treated as scene-level dependence. Strict and conservative sensitivity analyses were executed without retraining, and substantial aggregate domain gaps persisted.

## 2. Learnability versus transfer degradation
Completed and refined. The primary last.pt analysis showed near-floor Construction-PPE negative-state recall in-domain. The completed best.pt sensitivity demonstrated that no_helmet and no_gloves improve in-domain under validation-selected checkpoints while cross-domain performance remains poor. The final manuscript therefore treats class-level failure mechanisms as checkpoint-sensitive. no_boots remains a persistent learnability failure under both checkpoint policies.

## 3. Checkpoint sensitivity baseline
Completed. All six validation-selected best.pt checkpoints were evaluated on both test domains under the unchanged Stage 6 evaluator: 12 evaluation cells, no retraining, no adaptation, no threshold tuning, and no test-informed selection.

Mean best.pt domain gaps:
- Y-PPE-trained: 0.191, approximately 61.0% relative.
- Construction-PPE-trained: 0.170, approximately 63.3% relative.

All six seed-level gaps remained positive.

## 4. Harmonization/filtering reproducibility
Completed. The manuscript and supplement now report the exact nine-class mapping, deterministic polygon-to-bbox conversion, critical source-label relationships, the exact structural match rule (IoU >= 0.50 OR excluded-box containment >= 0.80), image-membership pseudocode, split-specific exclusion counts, exclusion-reason accounting, class counts before/after filtering, dataset fingerprints, and the structurally-harmonizable-subset limitation.

## 5. Literature, gap, repository, and figures
Completed. Related work was expanded to 29 references. Novelty is framed as deployment-oriented reliability evaluation rather than novelty-by-combination. Repository/data statements, figure numbering, captions, highlights, cover letter, and reproducibility documentation were repaired.

## Additional statistical revision
Image-cluster bootstrap with 10,000 replicates was added for PPE-negative-state recall and consensus false-negative rates. Images, not objects, were resampled.

A corresponding mAP50:95 image-level bootstrap is not included in the committee-review manuscript because exact AP reconstruction requires ranked per-image prediction archives that were not retained in the original Stage 6 summary. This limitation is disclosed explicitly rather than approximated from object-level counts.

## Final recommendation
**Manuscript status: READY FOR Q1 COMMITTEE REVIEW.**

The manuscript is not presented as architecture-independent evidence, a new detector, or proof of universal construction-site generalization. Its defensible contribution is a controlled, bidirectional, multi-seed reliability evaluation with explicit robustness checks and class-level failure analysis.
