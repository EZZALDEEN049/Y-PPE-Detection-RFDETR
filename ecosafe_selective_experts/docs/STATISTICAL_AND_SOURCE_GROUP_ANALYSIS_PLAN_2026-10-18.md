# EcoSafe — Statistical analysis plan and source-dependence gate
**Prospective design draft: 2026-10-18; NOT APPROVED, NOT a claim that historical development analyses were preregistered.**

## Scientific status

The 2026-10-17/18 last.pt and best.pt results are completed **development** diagnostics; their checkpoint/threshold/oracle results are exploratory and cannot be described as independent confirmatory tests or prospective pre-registration. Original validation n=356 Y-PPE images with 345 safety GT objects and n=132 Construction images with 98 safety GT objects. These are recurring image sets observed under three training seeds and two existing original checkpoint policies. **Six weights ≠ six independent target populations.** Original frozen manifests do not establish camera, capture session, worksite, sequence, identity or site group independence. No held-out test opened for new policy selection.

## Question hierarchy and null comparators

**RQ1 (primary descriptive checkpoint audit):** At a fixed operating point, how many critical-class GT objects match (a) domain-aligned single expert, (b) opposite-domain expert, (c) actual same-class joint NMS, and (d) raw-concatenation nondeployable oracle? How many matched objects, false detections, affected frames and false-negative events vary by (i) domain and (ii) checkpoint-policy last.pt vs best.pt?

**RQ2 (retrospective conditional value):** How concentrated are *positive* per-frame \`TP_joint - TP_primary\` gains, and can primary-only confidence features rank the frames in which the actual class-aware merger improves object matching? Oracle labels consult GT and **may only serve as upper-bound diagnostics**.

**RQ3 (exploratory compute proxy):** For 0% escalation, always both (100%), development-only static confidence policies and mathematically matched-rate random-routing **expected** policies, how do recall and FP vary versus second-expert invocation fraction? Invocations are *not energy*.

**No confirmatory claim for a new safe/sustainable router** unless an independently accepted absolute safety standard, source independence, a frozen prospective router and fully measured costs exist *before first final test access*.

## Unit of analysis

- Detector output matching: one-to-one class-aware maximum-cardinality matching at fixed IoU >=0.50; never equate raw detector counts with TP. Empty detection frames explicitly retained.
- Primary class outcomes \`no_helmet\`, \`no_gloves\`, \`no_boots\` plus pooled micro-recall; per-class GT denominator and per-image safety-positive denominators reported.
- The inference unit for uncertainty is **the independent original capture group**, not detector boxes or random training seeds. If verified independent capture groups are not supplied, report conditional image-level resampling solely as exploratory and do NOT infer generalization across work sites.
- A single image can contain multiple matched GT objects. GT objects should never be treated as independent for CI; group resampling must carry **all detections, GT, seeds and checkpoint policies together** to preserve pairing.
- YOLO repeat seeds change model training but share identical domain validation cases. Summarize seeds as repeated model factor (not independent data replications); report every seed, mean and range/SD only descriptively.
- If domain Y and domain C capture sources are distinct/unknown, do not pool their GT denominators or assume identical prevalence of the three safety classes.

## Planned estimands and intervals — conditional on clearing source provenance

For a fixed domain \`d\`, class \`c\`, checkpoint policy \`k\`, seed \`s\`, and operational policy \`p\`:

\`\`\`
Recall(d,c,k,s,p) = sum_i TP_i(c,p) / sum_i GT_i(c)
FNR = 1 - Recall
Precision = sum_i TP_i / (sum_i TP_i + sum_i FP_i)
False alerts per frame = sum_i FP_i / number_of_frames
Secondary call fraction = sum_i I(secondary invoked on frame i) / number_of_frames
Delta recall = Recall(joint) - Recall(primary), PAIRED on the same images.
Delta FP/frame = (sum_i FP_i(joint) - FP_i(primary)) / number_of_frames.
\`\`\`

- **Non-negotiable:** keep fixed class ID mapping, confidence, IoU and joint NMS settings and model checkpoint SHA for each report. Report undefined precision as NA, never 0, when there are no detections.
- For adequately numerous *verified* worksite/sequence groups: group-wise paired nonparametric bootstrap with **predefined random seed, B>=5000**, sampling independent groups WITH replacement and recomputing the micro-estimand each replicate; carry both policies/seeds and all frames in each group together. Report 95% percentile two-sided CI with number of original independent groups and effective resample support. Consider BCa as sensitivity only, not a post hoc precision fix.
- For only a few groups, prefer exact descriptive groupwise paired differences and caution, not asymptotic p-values that pretend box independence. Cluster bootstrap CIs can be unstable if the number of truly independent groups is small.
- If site IDs cannot be verified: a fixed B=5000 *paired image-cluster* resample can illustrate within-export sensitivity but **must be labeled non-source-generalizable**. No manuscript-wide "statistically significant real-world safety gain" language.
- For rare \`no_boots\` in Construction validation (4 total GT), report observed TP/FN with denominator and wide uncertainty; no class-safety noninferiority test can be credibly powered from this cell.
- For conditional-value AUC on 6–8 or 1–3 positive-benefit frames, report prevalence and ordinary ROC AUC as diagnostic; PR-AUC may be reported with prevalence baseline, but not stable cross-site intervals. Avoid presenting a fitted AUC/threshold as validation of a controller.

## Missing identities, multiple comparisons and interpretation

**Source gate:** develop a private table of (SHA-256 or internal image ID → original worksite ID, camera, session, capture date, sequence, original image family) from owner-authorized records. This table is PRIVATE; do not publish worker names, camera locations, faces or raw IDs. Source provenance must be obtained **without opening untouched test images** or obtaining test outcomes for policy selection.

**Multiplicity:** the matrix is 2 target domains × 2 checkpoint policies × 3 random seeds × at least 2 primary directions × 3 safety classes × exploratory confidence grid. Retrospectively inspecting many cells creates selection bias; keep descriptive cross-tabulation, avoid selective p-values or a fabricated Holm-corrected primary hypothesis. If a confirmatory test is later authorized, separately declare a **single** primary comparison/primary critical outcome, direction, checkpoint policy, fixed threshold, safety margin, alpha, CI construction, and secondary family before evaluation.

**Safety non-inferiority:** a recall margin \`epsilon\` relative to an **inadequate** always-both baseline is scientifically insufficient. An externally defensible lower bound for absolute recall for each critical class (and allowable false alarms at expected prevalence) must be supplied by a responsible domain safety authority/committee. Do not invent a target like 90% or 95% without such approval.

**Invalid analyses to avoid:** selecting the favorable seed or domain; cherry-picking best.pt validation as independent confirmation; training a router with post hoc labels and reporting its in-sample AUC as test; CI by treating the 98/345 GT objects or all 3 seeds as independent; mixing nine-class harmonized Stage 5 sources with the distinct 17-class Roboflow export audit; claiming energy saved by fewer expert calls.

## Proposed final outputs once authorized

1. Source-group provenance availability report (aggregated group counts only) and adjudicated leak/near-duplicate status.
2. Locked policy registry: SHA/ontology/operating confidence/IoU/fusion/primary direction, positive control, negative controls, GT oracle separate, code commit and preregistered stats.
3. For each independent test domain: per-class TP/FN and FP, exact GT and frame denominators, seedwise results, paired groupwise uncertainty if warranted, and a single declared primary inferential comparison (or descriptive-only results if weak source evidence).
4. Real energy and latency only from instrumented same-device workflows. Keep analysis source fingerprints separate from any results and avoid private-data GitHub publication.

**Current decision:** test remains EMBARGOED. This plan is a transparent methodological proposal; it is not signed by a safety authority, supervisor or ethics/data governance representative.
