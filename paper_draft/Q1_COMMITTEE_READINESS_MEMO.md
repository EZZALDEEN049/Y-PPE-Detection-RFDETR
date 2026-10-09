# Q1 Committee Readiness Memo

## Manuscript
**Cross-Domain Reliability of YOLO11m for Safety-Critical PPE Monitoring: A Multi-Seed Bidirectional Evaluation**

**Current committee-review manuscript:** `paper_draft/MANUSCRIPT_STAGE12_Q1_COMMITTEE_FINAL.md`

## Overall readiness
**Ready for Q1 committee review.**

The manuscript has passed the major-revision cycle that addressed the principal risks identified in the strict reviewer audit. The central aggregate result is now supported by three complementary evidence layers:

1. the frozen 12-cell primary last.pt evaluation;
2. split-dependence sensitivity analysis after near-duplicate and conservative train-scene exclusions;
3. validation-selected best.pt checkpoint sensitivity across all six completed runs.

The aggregate mAP50:95 degradation persists under all three.

## Strongest final evidence

### Primary final-epoch analysis
- Y-PPE → Construction-PPE: 0.291 → 0.121, 58.4% relative loss.
- Construction-PPE → Y-PPE: 0.252 → 0.082, 67.4% relative loss.

### Split-dependence sensitivity
- Strict near-duplicate exclusion preserved gaps of approximately 0.166 and 0.169.
- Conservative train-scene exclusion preserved gaps of approximately 0.181 and 0.140.

### Validation-selected best.pt sensitivity
- Y-PPE → Construction-PPE: 0.312 → 0.122; gap 0.191, approximately 61.0% relative.
- Construction-PPE → Y-PPE: 0.269 → 0.099; gap 0.170, approximately 63.3% relative.
- All six seed-level best.pt gaps remained positive.

## Important interpretation refinement
The aggregate cross-domain conclusion is robust, but individual PPE-negative-state classes are more checkpoint-sensitive.

- Y-PPE-trained no_helmet, no_gloves, and no_boots retain strong transfer degradation under both checkpoint policies.
- Construction-PPE best.pt improves in-domain no_helmet and no_gloves recall, showing that the final-epoch near-floor pattern partly reflected checkpoint policy.
- Construction-PPE no_boots remains at zero recall in-domain and cross-domain under both checkpoint policies.

The final manuscript therefore avoids attributing all safety-class failure to one mechanism.

## Major reviewer objections and final disposition

| Concern | Final disposition |
|---|---|
| Duplicate/near-duplicate leakage | Addressed with SHA-256, perceptual/geometric/manual audit plus sensitivity evaluation |
| Scene-level dependence | Quantified and conservatively sensitivity-tested |
| Learnability vs domain shift | Reframed and further refined by best.pt sensitivity |
| Checkpoint-policy dependence | Addressed with completed 12-cell best.pt analysis |
| Harmonization/filtering reproducibility | Exact rules, thresholds, pseudocode, exclusions, class counts, fingerprints documented |
| Sparse literature / weak novelty framing | Related work expanded to 29 references; novelty reframed as deployment-reliability evaluation |
| Weak uncertainty analysis | Image-cluster bootstrap CIs added for PPE-negative-state recall and consensus FN |
| Consensus across seeds misinterpreted | Explicitly described as persistence under training stochasticity |
| Repository/data statement | Public repository, fingerprints, manifests, code SHA and governance wording added |
| Figure numbering / package mismatch | Corrected and frozen |

## Remaining limitation for committee awareness
The current committee-review manuscript does not report an image-level bootstrap CI for mAP50:95 because the original Stage 6 summary did not retain the ranked per-image prediction statistics required to reconstruct AP exactly. The manuscript discloses this as a limitation and does not substitute an invalid object-level bootstrap.

A Stage 11E2 inference-only archive/bootstrapping procedure has been designed but is not required to interpret the current point estimates and two completed robustness analyses. The committee may recommend completing it before journal upload if it considers an image-level AP interval essential.

## Recommendation to committee
The manuscript is scientifically suitable for full Q1-level review. The strongest remaining question is not whether the aggregate domain gap exists—the evidence for that is now robust—but whether the committee wishes to require the additional image-level AP bootstrap before journal submission.
