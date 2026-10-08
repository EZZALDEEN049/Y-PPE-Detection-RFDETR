# Final Figure Numbering Manifest

This manifest resolves the manuscript/package numbering mismatch identified during review.

| Final figure | Required filename | Content |
|---|---|---|
| Figure 1 | Fig1_experimental_workflow | Experimental workflow: frozen harmonization → six YOLO11m runs → bidirectional held-out evaluation → diagnostics/sensitivity |
| Figure 2 | Fig2_semantic_harmonization | Nine-class source-to-canonical semantic harmonization and excluded source classes |
| Figure 3 | Fig3_cross_domain_map5095 | In-domain versus cross-domain mAP50:95, mean ± SD across three seeds |
| Figure 4 | Fig4_seed_level_domain_gaps | Seed-level mAP50:95 domain-generalization gaps |
| Figure 5 | Fig5_safety_violation_recall | Safety-class recall at the frozen operating point |
| Figure 6 | Fig6_consensus_false_negative_rate | Three-seed consensus false-negative rate for negative-state classes |

## Captions

**Figure 1.** Experimental workflow for the frozen cross-domain reliability study. Dataset harmonization and structural filtering were completed before Stage 5 training; six YOLO11m runs were then evaluated bidirectionally without target-domain adaptation or test-informed threshold tuning. Post-evaluation analyses were diagnostic/sensitivity analyses and did not alter the primary checkpoints.

**Figure 2.** Semantic harmonization from the Y-PPE and Construction-PPE source ontologies to the nine-class benchmark. Shared classes were retained only when object/state meaning and localization targets were sufficiently aligned. Nonshared classes were excluded rather than force-mapped.

**Figure 3.** In-domain and cross-domain mAP50:95 for Y-PPE-trained and Construction-PPE-trained YOLO11m models. Bars show the mean across seeds 17, 42, and 2026; error bars show sample SD.

**Figure 4.** Seed-level mAP50:95 domain-generalization gaps, defined as in-domain minus cross-domain performance for the same source-domain seed.

**Figure 5.** Mean recall for no_helmet, no_gloves, and no_boots at the frozen confidence threshold. The Construction-PPE-trained in-domain row is intentionally shown to distinguish class learnability failure from additional transfer degradation.

**Figure 6.** Cross-domain consensus false-negative rates for explicit PPE-negative classes. Consensus means the ground-truth object was missed by all three seed realizations of the same architecture/protocol; it indicates persistence under training stochasticity, not independent replication.
