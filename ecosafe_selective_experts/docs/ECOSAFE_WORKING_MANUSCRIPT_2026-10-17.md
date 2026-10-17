# EcoSafe Selective Experts: Domain-Conditioned Complementarity and Safety–Computation Tradeoffs in PPE Monitoring

**Working manuscript — 2026-10-17**  
**Status:** DEVELOPMENT EVIDENCE ONLY. Not a peer-reviewed or submission-ready manuscript. The held-out test, multiple-seed validation, uncertainty, resource benchmarking and publication permissions remain outstanding.

## Abstract (provisional; not for journal submission)

Multi-expert personal protective equipment (PPE) monitoring may improve the detection of safety-critical violations when detectors trained on different construction-image domains make complementary errors. However, invoking a secondary detector on every image increases inference work and may introduce false alarms, while confidence-triggered selective invocation is beneficial only if the trigger identifies recoverable failures. We propose EcoSafe, a development-stage framework for testing the tradeoff between safety-object recall, false positives and secondary-detector invocation rate using pre-existing, fixed YOLO11m experts trained on Y-PPE and Construction-PPE. The design preserves three previously completed training seeds per source domain, locks final-epoch checkpoint identities and reserves held-out test images until router selection is frozen. A preliminary seed-17 analysis of two frozen development partitions reveals strong direction asymmetry: class-aware joint nonmaximum suppression increased matched critical-object detections from 8 to 13 on the 132-image Construction-PPE validation set (98 safety GT objects), but did not improve the Y-PPE-trained expert’s 106 of 345 matches on the 356-image Y-PPE validation set. The second expert also added false positives. Exploratory confidence-only routing generally failed to yield meaningful reductions in secondary invocations while preserving the weak always-both safety reference. These findings motivate a prespecified oracle-complementarity and absolute safety-threshold gate before any adaptive-routing or sustainability claim. No energy advantage, independent generalization gain or deployable safety adequacy is established.

**Keywords (working):** PPE safety monitoring; selective inference; domain shift; expert complementarity; false negatives; resource-constrained computer vision.

## 1. Motivation and research question

A detector optimized on one PPE image source can behave very differently on another source. The prior bidirectional domain-shift study already examined cross-domain reliability of YOLO11m over two frozen nine-class PPE collections; EcoSafe must **not** duplicate those findings or describe the old model training as a new experiment. Its distinct, prospective question is:

> Given fixed, previously trained domain-specific experts, can a lightweight primary-only routing decision selectively invoke a second expert **on the frames where it is genuinely useful**, preserving a prespecified operational violation-detection standard with fewer second-expert executions than an always-both fusion reference?

This question requires distinguishing an expert *switch* (discard primary outputs and use secondary instead) from actual dual-expert fusion. The original pilot controller conflated these policies; the correction and object-level matching algorithm are implemented and tested in the branch associated with this working manuscript.

## 2. Study resources and methodology

### 2.1 Immutable expert and data provenance

Six YOLO11m `last.pt` detector checkpoints, three random seeds (17, 42, 2026) for each training domain, were independently re-hashed against the existing frozen checkpoint lock. Models will never be retrained for the primary EcoSafe study. The distinct nine-class frozen sources are Y-PPE-h9-v2 (validation n=356) and Construction-PPE-h9-v2 (validation n=132). The safety-negative classes are `no_helmet`, `no_gloves` and `no_boots`. Both datasets retain original frozen manifests and full class mappings. Raw images, checkpoint binaries and per-image predictions remain in private storage.

### 2.2 Primary, secondary and fusion policies

For each seed and both primary directions, compare: (i) Y expert alone, (ii) Construction expert alone, (iii) always run both and merge with fixed class-aware NMS, (iv) a genuinely selective primary-first cascade that uses exactly the same merger **only upon escalation**, and (v) a raw-concatenation upper-bound matching oracle. The fifth policy is *not* deployable; it only upper-bounds matchable ground-truth objects using both prediction sets.

The current exploratory detector export uses 640-pixel input, confidence floor 0.001 and per-model NMS IoU 0.70. The fixed safety operating point is confidence 0.25 with class-aware GT matching at IoU >=0.50. Joint class-wise NMS uses IoU 0.70. Primary-only uncertainty features are computed without secondary predictions or ground-truth access. These settings were evaluated on development data and **are not yet a prospectively locked held-out research protocol**.

For robust critical-object evaluation, maximum-cardinality class-aware bipartite matching is used, not differences between two aggregate FN totals. A separate NetworkX implementation cross-checks cardinalities on development images. A missing zero-detection frame must remain a frame with zero predictions, not an omitted record.

### 2.3 Outcomes and conditions for a legitimate sustainability claim

The principal safety outcomes must include per-class counts, TP, FN, FP, fixed-point recall and precision, with repeated seeds and grouping-aware uncertainty wherever source relationships are available. Compute proxies include secondary invocation fraction and expected expert executions per image. **Calls/image is not energy**: calibrated hardware-specific joules/image, memory, model loading, actual end-to-end latency, overhead and relevant carbon factors are separate future measurements. A relative non-inferiority margin to an already weak always-both detector is insufficient to demonstrate absolute worksite safety.

### 2.4 Training, threshold selection and held-out lock

Any logistic, calibrated or other learned lightweight router may be fitted only on development data with out-of-fold/cross-fitted predictions, preferably accounting for source groups. Candidate reference policies and an externally justified absolute safety target must be frozen before test access. No held-out images, labels or results are admissible in feature selection, threshold selection or the decision to retain EcoSafe.

## 3. Results — exploratory development analysis, seed 17 only

### 3.1 Fixed-threshold violation recall and precision

| Validation domain (safety GT) | Y expert TP | Construction expert TP | Joint NMS TP | Concatenation oracle TP |
|---|---:|---:|---:|---:|
| Construction-PPE (98) | 7 | 8 | 13 | 14 |
| Y-PPE (345) | 106 | 1 | 106 | 106 |

On Construction validation, joint NMS achieved fixed-IoU recall 13.27% but precision 16.25%, whereas the Construction expert alone achieved recall 8.16% and precision 50.00%. On Y validation, joint NMS retained the Y expert’s 106 matches (30.72% recall) while reducing precision from 75.18% to 74.13% because it added two false positives. In **all 356** Y validation images, concatenation and joint NMS matched exactly the same number of safety GT objects as Y alone.

These percentages are **NOT COCO mAP**, and the two domains have different denominators and class distributions. They cannot establish a population-wide asymmetry or safety adequacy with seed-17 data alone.

### 3.2 First confidence-only selective-routing diagnostic

Define the exploratory primary-only uncertainty score as `1 - maximum safety-class confidence`, set to 1 if no safety-class detection is produced, and escalate when score >=0.50. On Construction validation this escalated 75.0% of images with Y as primary, retaining only 9/98 safety matches versus 13/98 for always joint NMS. With Construction as primary it escalated 94.7% of images, retaining 13/98 matches. On Y validation, Y-primary escalation invoked the secondary in 79.5% of images without any safety recall gain above the single Y expert. With Construction as primary it invoked Y in 99.7% of images to retain the joint NMS recall.

The simple confidence heuristic is therefore **not validated as an efficiency solution** under these settings. The scores and threshold are development-time diagnostics only, not a frozen optimal threshold or an energy benchmark.

## 4. Discussion (provisional)

The presence of some complementary object-level detections on Construction-PPE but none on Y-PPE (at this operating point and seed) suggests that domain and directional asymmetry may dominate the practical value of an extra expert. It is inappropriate to infer unconditional safety gains from ensembling or sustainable-compute gains from invoking fewer networks.

Most importantly, the extremely low measured critical-state recall on Construction-PPE illustrates why selective-inference non-inferiority alone could be misleading: preserving an inadequate reference system is not evidence of field readiness. Any final paper must report the absolute safety target, miss costs, alert burden, site governance, uncertainty and performance under source dependence. If the multi-seed oracle gain remains near zero or selective routing cannot meet the safety gate at a materially lower invocation rate, the scientifically valid result is a **NO-GO** for the proposed cascade, not a manufactured positive contribution.

## 5. Mandatory work before a submission-ready paper

- Finish development inference with all six immutable checkpoints across both validation domains.
- Quantify object-level complementarity by seed/direction and class, verify complete frame coverage, handle rare-class support and source dependence.
- Freeze the actual fusion operator and predeclare the cost/safety objective and margin using development-only evidence.
- Test learned and non-learned routing against primary-only, secondary-only, always-joint, matched-rate random and upper-bound oracle controls.
- Conduct the **first** final held-out test only after the policy is documented and locked; provide paired/clustered CIs.
- Measure actual CPU/edge latency, RAM and instrumented J/image plus router overhead if claiming energy efficiency; report CO2e only with justified electricity factors and system boundaries.
- Resolve data governance and publication image rights; perform novelty/literature verification, methods/reporting review and an independent Q1 peer-review checklist.

## Publication integrity statement

This working draft records early research results, including negative findings. Its abstract, tables and conclusions are explicitly preliminary. It does not claim Q1 readiness, acceptance, field safety, unseen-domain improvement or lower carbon emissions, and it does not represent Stage 5/6 prior study results as a newly trained or independently tested architecture experiment.
