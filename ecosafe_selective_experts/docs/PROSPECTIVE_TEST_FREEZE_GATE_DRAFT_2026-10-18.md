# EcoSafe prospective held-out TEST access gate (UNAPPROVED DRAFT)

**Written 2026-10-18, AFTER development validation and BEFORE final held-out test exposure.**

**This is a prospective planning draft, NOT a retrospective pre-registration of the past development experiments.** No held-out model evaluation, **new test-label use for EcoSafe router design**, test-threshold tuning or score-based paper claim is authorized by the existence of this file. **Historical exception to an entirely untouched-test claim:** the fixed Stage 4.5 pretraining preprocessing rule DID parse native test-annotation metadata and remove 48 Y-PPE plus 3 Construction-PPE test frames before any Stage 5 training. That selection was not based on predictions or test performance; its resulting test population is conditional on label completeness. The current scientifically justified decision remains **NO-GO for deployable safety and energy savings claims**.

## Proposed publication claim, narrowly scoped

Provisional candidate: **Checkpoint-policy sensitivity, sparse conditional value of a second expert and confidence-signal failure modes in critical PPE detection under domain shift.**

The intended result may be *negative*; it is not a new domain-adaptation algorithm, and conditional model cascades already exist. A high-quality paper needs a rigorous comparison to [TMLR 2023 model cascades](https://mlanthology.org/tmlr/2023/lebovitz2023tmlr-efficient/), [2025 confidence tuning](https://arxiv.org/abs/2502.19335), and existing PPE/construction-site domain-generalization research, including [Automation in Construction 2026 Cross-HNM](https://doi.org/10.1016/j.autcon.2026.106761). This related-work list is NOT exhaustive and Q1 acceptance cannot be inferred from it.

**Image-use status clarification (2026-10-18):** The researcher reports that the pictures are legitimate, routinely used academic/research images. This resolves a *presumed research-use objection* for planning purposes; it does not, by itself, establish independent image-source/site grouping, publicly distributable original-image rights, data-owner-specific test protocol approval or operational safety sufficiency. Do not delay ordinary authorized academic analysis solely based on a speculative prohibition on studying these images.

## Mandatory authorization gates before first held-out run

- [x] **Original source and derivative identity documented**: Roboflow ALTAYYAR Version 2 and official Ultralytics Construction-PPE v1.0.0, Stage 2, Stage 4 and historical label-based Stage 4.5 pretraining membership filtering; see `docs/DATASET_SOURCE_LINEAGE_AND_TEST_SELECTION_2026-10-18.md`. This is a source-record completion, not independent-site validation.
- [ ] **Independent source provenance verified**: evidence of worksite/recording/camera/session grouping and train/validation/test source independence for *both* nine-class frozen datasets. Hash and dHash preflights alone are insufficient.
- [x] **Researcher clarification about academic image use recorded**: the project researcher states images are legitimate/official research materials routinely used for study. This is a self-report of research-use permissibility, not an independent license audit.
- [ ] **Distinct public redistribution/figure permissions if original images are published**: review source license/consent and anonymization requirements before publishing originals or crops; aggregate-only research outputs are distinct from redistribution. Research-use clarification does not establish public-image reproduction rights.
- [ ] **Absolute safety standard**: externally justified minimum recall per critical PPE class, max false-positive burden and allowable missed event costs, rather than noninferiority to an already weak always-both reference.
- [ ] **Exact 2×3×2 checkpoint-factor design**: preserve original \`last.pt\` as the primary evidence; include separately disclosed \`best.pt\` sensitivity as a validation-selected model variant, not as retrospectively discovered independent improvement. Lock six exact SHA-256 IDs for EACH factor.
- [ ] **All operational thresholds and fusion policy specified** before looking at test data; no confidence/NMS tuning, seed cherry-picking or test-guided checkpoint switches. The development exploratory grid is *not* a pre-registered final test policy.
- [ ] **Hypothesis and null controls locked**: primary-only, secondary-only, always-joint NMS and GT-evaluation-only oracle; for any real router, matched-call-rate randomized baseline plus learned/signal baselines; note that the privileged GT oracle is NOT a deployable policy.
- [ ] **Primary metric and statistical family locked**: safety-class TP/FN, per-class recall/FNR, FP per image and alert burden, number of expert calls, and paired confidence intervals. Identify statistical unit **site/sequence group** if available; absent groups, no site-generalization inference.
- [ ] **Statistical assessment and sample-size sufficiency**: check rare classes (Construction validation had only 4 no_boots GT) and adjust claims, CI granularity and multiple comparisons in advance. Repeated seeds on the *same images* are not independent subjects/sites.
- [ ] **Actual resource measurement plan**, if sustainable inference is claimed: matched software/GPU/CPU/edge stack, warmup, batch size, device power instrumentation, idle/control baseline, end-to-end p50/p95 latency, RAM/VRAM, active second-expert load/wakeup, router overhead, joules/image including initialization amortization, and justified CO2e factors/system boundaries.
- [ ] **Provenance-locked analysis release**: frozen git commit/tag, software versions, data/checkpoint fingerprints, hash-verified private predictions and all predeclared aggregate outputs. Code tests passing are necessary but do not by themselves establish scientific validity.
- [ ] **Pre-test supervisor/author decision recorded** on whether to (A) pursue a negative/limits paper, (B) study a distinct revised detector family with new pre-registered evidence, or (C) stop the EcoSafe branch and submit the prior completed cross-domain reliability paper instead.

## Documented scientific pre-work now completed (NOT evidence gate approval)

As of 2026-10-18 the **design work** below has been completed without exposing held-out scores:

- [x] A targeted source-verified (but non-systematic) competitor matrix now separates prior two-model cascades, calibration, PPE cross-domain detection, construction cross-site generalization and physical-power methodology from our narrow candidate contribution; see `docs/LITERATURE_AND_NOVELTY_EVIDENCE_MAP_2026-10-18.md`.
- [x] A statistical/unit-of-analysis design has been written that explicitly forbids treating multiple detector seeds, GT boxes or correlated frames as independent source sites; see `docs/STATISTICAL_AND_SOURCE_GROUP_ANALYSIS_PLAN_2026-10-18.md`.
- [x] A protected capture-site/camera/session mapping request exists with no fabricated group IDs and no public image metadata; see `docs/PRIVATE_CAPTURE_PROVENANCE_REQUEST_2026-10-18.md`.
- [x] A matched full-system wall-meter protocol exists, with an offline physical-trace-only energy auditor and synthetic CPU test checks; see `docs/HARDWARE_WALL_ENERGY_BENCHMARK_PLAN_2026-10-18.md` and `scripts/14_audit_measured_wall_power.py`.
- [x] The English working manuscript is reframed as a narrowly supported checkpoint-sensitive safety-object failure-mode / conditional-value audit with verified original-source references.

**None of the above checks supplies a real capture-group map, an approved minimum safety standard, legal permission, final frozen operating policy, independent held-out result or measured Joules.** All corresponding authorization checkboxes in this file must remain unchecked until actual evidence is received.

## Dataset population restriction and historical test annotation access (explicit)

The two images sources are documented and usable as research inputs. Nevertheless, the final nine-class Stage 5 evaluation images **are NOT the unmodified publisher test splits**. Historical, pre-detector-training Stage 4.5 preprocessing used native train/validation/**test annotations** to exclude harmonized-empty or critically unmatched original-label images. It removed **48/234 Y-PPE** and **3/141 Construction** clean-source test images, leaving 186 and 138 final test images respectively. The original test image pixels were not opened for this exclusion policy and model performance did not influence the membership rule. This means the selection did not contaminate EcoSafe router development with test *performance*, but DOES condition the target test population on native annotation structure.

The researcher reports these official images are suitable for ordinary research; public reprinting of raw photographs still requires source-specific rights confirmation. The historical audits cleared explicit cross-split media-token leakage and confirmed near-duplicate source-family pairs, but **did not supply camera/site/session identities for every frame**. The appropriate embargo is on **model-prediction-based test performance access before a policy freeze**, not a false claim that no test annotation metadata was ever processed in the history of these datasets.

## Why the present results do NOT unlock this gate

The development best.pt sensitivity had fused safety-object recalls no greater than 38.84% on Y-PPE and 47.96% on Construction-PPE at confidence 0.25, often with many more FPs than TPs. A GT-privileged sparse-secondary-call oracle is not a practical router, and the most promising confidence ranking used only 6–8 positive-benefit Construction frames per seed. High ranking AUC with rare positives and model-selection optimism does not establish safe detection or meaningful energy reduction. These findings must be reported candidly; do not use the independent test to search for a favorable operating point.

## Explicit evaluation embargo

**Held-out model-scoring status:** no new EcoSafe router/fusion **test performance evaluation** conducted. Historical Stage 4.5 processed native test-label metadata prior to training and removed predefined structurally nonharmonizable frames, so do NOT claim wholly untouched original test annotations. This draft does not authorize new test scores, labels or visual inspection for routing selection; it cannot be cited as a retroactive pre-registration of development choices.

**Next safe action:** obtain original capture source-group/provenance information; review verified related work and define a defensible absolute safety metric. If the gate cannot be met, report the observed negative evidence as a scoped reproducibility/limitations study instead of fabricating a sustainable PPE system.
