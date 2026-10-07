# Stage 10 — Simulated Q1 Peer Review

## Editorial decision

**Major Revision — scientifically promising and potentially publishable after targeted revision.**

The manuscript's strongest elements are the frozen held-out protocol, bidirectional cross-domain design, three seeds per source domain, safety-class false-negative analysis, and transparent exclusion of incomplete RF-DETR runs.

## Reviewer 1 — Methods and statistics

1. Present the final study as a completed YOLO11m multi-seed cross-domain reliability experiment. Mention the abandoned architecture comparison only once as a protocol deviation.
2. State clearly that seed-level mean ± SD describes training stochasticity, not population uncertainty across sites.
3. Explain that AP summarizes ranking across thresholds, whereas the frozen confidence=0.25 operating point provides interpretable TP/FP/FN and violation recall.
4. State that semantic harmonization reduces label-space mismatch but cannot remove annotation-policy or state-definition differences.
5. Clarify that the small/medium/large bins are study-specific normalized-area strata, not COCO size categories.

## Reviewer 2 — Safety interpretation and novelty

1. Promote the distinction between aggregate detection performance and safety reliability. Non-zero aggregate mAP can coexist with unacceptable violation-class false negatives.
2. Avoid causal wording for class imbalance and scale. Use association/plausible-contributor language.
3. Position novelty as a reliability-evaluation contribution: bidirectional zero-shot transfer, harmonized ontology, three seeds, frozen held-out protocol, and consensus safety false-negative analysis.
4. Scope deployment claims to the evaluated domains and avoid universal statements.
5. Resolve the exact image-use/ethics statement before submission.

## Reviewer 3 — Presentation

1. Add compact primary performance, safety recall, and consensus-FN tables to the manuscript.
2. Repair the malformed equation formatting in the Markdown source.
3. Shorten the title to: **Cross-Domain Reliability of YOLO11m for Safety-Critical PPE Monitoring: A Multi-Seed Bidirectional Evaluation**.
4. Define zero-shot cross-domain evaluation at first use.
5. State explicitly that the consensus-FN audit is post-evaluation diagnostic analysis and was not used for model or threshold selection.

## Editor synthesis

The study should be judged as a reliability/evaluation paper rather than an architecture-innovation paper. The scientific core is publishable in principle.

Remaining submission blockers are author-controlled declarations: image-use/ethics wording, funding, competing interests, final author contributions, and an immutable code/results archive identifier.

After those items and the Stage 10 revisions are completed, the manuscript would be suitable for final journal-specific formatting and another editorial-quality check.
