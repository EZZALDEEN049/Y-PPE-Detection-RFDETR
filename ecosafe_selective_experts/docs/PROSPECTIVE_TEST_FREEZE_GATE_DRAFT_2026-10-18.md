# EcoSafe prospective held-out TEST access gate (UNAPPROVED DRAFT)

**Written 2026-10-18, AFTER development validation and BEFORE final held-out test exposure.**

**This is a prospective planning draft, NOT a retrospective pre-registration of the past development experiments.** No held-out model evaluation, test-label use, test-threshold tuning or score-based paper claim is authorized by the existence of this file. The current scientifically justified decision remains **NO-GO for deployable safety and energy savings claims**.

## Proposed publication claim, narrowly scoped

Provisional candidate: **Checkpoint-policy sensitivity, sparse conditional value of a second expert and confidence-signal failure modes in critical PPE detection under domain shift.**

The intended result may be *negative*; it is not a new domain-adaptation algorithm, and conditional model cascades already exist. A high-quality paper needs a rigorous comparison to [TMLR 2023 model cascades](https://mlanthology.org/tmlr/2023/lebovitz2023tmlr-efficient/), [2025 confidence tuning](https://arxiv.org/abs/2502.19335), and existing PPE/construction-site domain-generalization research, including [Automation in Construction 2026 Cross-HNM](https://doi.org/10.1016/j.autcon.2026.106761). This related-work list is NOT exhaustive and Q1 acceptance cannot be inferred from it.

## Mandatory authorization gates before first held-out run

- [ ] **Independent source provenance verified**: evidence of worksite/recording/camera/session grouping and train/validation/test source independence for *both* nine-class frozen datasets. Hash and dHash preflights alone are insufficient.
- [ ] **Publication permissions and privacy**: consent/rights for the specific worker/field imagery, authorization to use private test data in derived statistical reports; de-identification and aggregate-only outputs.
- [ ] **Absolute safety standard**: externally justified minimum recall per critical PPE class, max false-positive burden and allowable missed event costs, rather than noninferiority to an already weak always-both reference.
- [ ] **Exact 2×3×2 checkpoint-factor design**: preserve original \`last.pt\` as the primary evidence; include separately disclosed \`best.pt\` sensitivity as a validation-selected model variant, not as retrospectively discovered independent improvement. Lock six exact SHA-256 IDs for EACH factor.
- [ ] **All operational thresholds and fusion policy specified** before looking at test data; no confidence/NMS tuning, seed cherry-picking or test-guided checkpoint switches. The development exploratory grid is *not* a pre-registered final test policy.
- [ ] **Hypothesis and null controls locked**: primary-only, secondary-only, always-joint NMS and GT-evaluation-only oracle; for any real router, matched-call-rate randomized baseline plus learned/signal baselines; note that the privileged GT oracle is NOT a deployable policy.
- [ ] **Primary metric and statistical family locked**: safety-class TP/FN, per-class recall/FNR, FP per image and alert burden, number of expert calls, and paired confidence intervals. Identify statistical unit **site/sequence group** if available; absent groups, no site-generalization inference.
- [ ] **Statistical assessment and sample-size sufficiency**: check rare classes (Construction validation had only 4 no_boots GT) and adjust claims, CI granularity and multiple comparisons in advance. Repeated seeds on the *same images* are not independent subjects/sites.
- [ ] **Actual resource measurement plan**, if sustainable inference is claimed: matched software/GPU/CPU/edge stack, warmup, batch size, device power instrumentation, idle/control baseline, end-to-end p50/p95 latency, RAM/VRAM, active second-expert load/wakeup, router overhead, joules/image including initialization amortization, and justified CO2e factors/system boundaries.
- [ ] **Provenance-locked analysis release**: frozen git commit/tag, software versions, data/checkpoint fingerprints, hash-verified private predictions and all predeclared aggregate outputs. Code tests passing are necessary but do not by themselves establish scientific validity.
- [ ] **Pre-test supervisor/author decision recorded** on whether to (A) pursue a negative/limits paper, (B) study a distinct revised detector family with new pre-registered evidence, or (C) stop the EcoSafe branch and submit the prior completed cross-domain reliability paper instead.

## Why the present results do NOT unlock this gate

The development best.pt sensitivity had fused safety-object recalls no greater than 38.84% on Y-PPE and 47.96% on Construction-PPE at confidence 0.25, often with many more FPs than TPs. A GT-privileged sparse-secondary-call oracle is not a practical router, and the most promising confidence ranking used only 6–8 positive-benefit Construction frames per seed. High ranking AUC with rare positives and model-selection optimism does not establish safe detection or meaningful energy reduction. These findings must be reported candidly; do not use the independent test to search for a favorable operating point.

## Explicit evaluation embargo

**Held-out test status:** NOT OPENED for EcoSafe policy evaluation. This draft does not authorize running or retrieving test labels/images, does not freeze a positive selective-inference policy, and cannot be cited as a time-travel pre-registration of development choices.

**Next safe action:** obtain original capture source-group/provenance information; review verified related work and define a defensible absolute safety metric. If the gate cannot be met, report the observed negative evidence as a scoped reproducibility/limitations study instead of fabricating a sustainable PPE system.
