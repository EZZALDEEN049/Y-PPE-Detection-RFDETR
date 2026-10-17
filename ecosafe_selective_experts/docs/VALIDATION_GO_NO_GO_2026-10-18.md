# EcoSafe validation decision gate — 2026-10-18

**Decision status: NO-GO for claiming safe, energy-efficient selective expert inference under BOTH the original Stage 5 last.pt policy AND the newly completed best.pt checkpoint sensitivity at the fixed development operating point.** This is a decision about an **unsupported positive claim**, not a claim that the research is a failure or that selective inference is impossible.

## Evidence checklist — now complete for DEVELOPMENT

- [x] All six original last.pt AND separately selected best.pt model weights bytewise SHA-256 verified without detector retraining.
- [x] Both immutable validation domains tested, each with both experts in all three matched training seeds under BOTH checkpoint policies (24 model-domain inference cells in total).
- [x] Y-PPE: 356 validation frames, 345 safety GT, 106/103/94 joint NMS TPs per seed; identical to the Y expert alone.
- [x] Construction: 132 validation frames, 98 safety GT, 13/13/14 joint NMS TPs; 67/68/74 joint FPs.
- [x] Development threshold sensitivity exposes the absolute recall–false-alert tension. Gains at alternative cutoffs are clearly labeled exploratory.
- [x] Maximum-cardinality object matching independently checked by NetworkX; 2,848 newly evaluated image-policy comparisons agree, plus archived seed17 comparison.
- [x] Primary-confidence-only cascade simulated against actual always-run-both NMS, not secondary-only prediction switching.
- [x] best.pt source-domain checkpoint-policy sensitivity completed on both domains, all seeds, and kept separate from primary last.pt results; all 11,712 independent matching checks agreed at two cutoffs.
- [x] best.pt exploratory routing compared against rate-matched random expected outcomes (not a sampled significance test).
- [x] GT-privileged opportunity and primary-only rank feature comparison completed with full private chunk data locks and 56-test CPU CI; source-validation selection bias clearly marked.
- [x] Development-only exact-hash and 64-bit dHash sensitivity audit completed; *independent capture groups remain unverified*.
- [ ] An **independently justified absolute operational safety recall / permissible miss and FP cost** is documented. A relative non-inferiority to very low always-both recall is not enough.
- [ ] Verified independent source/site grouping and population-level statistical uncertainty.
- [ ] A robust, prespecified router significantly reduces secondary invocations while satisfying *both* absolute safety and acceptable FP burden on development data.
- [ ] A locked protocol tested once on untouched, site-independent held-out images, with paired uncertainty.
- [ ] Instrumented per-image energy, inference latency, memory and router overhead on fixed hardware; defensible carbon accounting if CO2e is claimed.
- [ ] Public manuscript permissions, literature novelty verification, reporting and ethics/data-rights checklist closed.

## Interpretation by domain

| Domain | Current joint baseline (three seeds) | Marginal safety detection over best single | Development decision |
|---|---|---|---|
| Y-PPE validation, 345 safety GT | 106 / 103 / 94 TP | 0 / 0 / 0 | **Do not invoke second expert for a claimed recall gain at confidence 0.25.** Additional calls may only add false alarms. |
| Construction-PPE validation, 98 safety GT | 13 / 13 / 14 TP; FP 67 / 68 / 74 | +5 / +4 / +6 TP | **Not safety adequate;** the observed recall gains are too small and false alarms too large to justify a field-ready cascade claim. |

## best.pt checkpoint-policy sensitivity — now completed

Each original validation-selected best.pt source checkpoint was separately locked, never retrained, and evaluated on the same frozen development images. This is a **selection-biased** experiment on the in-domain source validation for each selected checkpoint, not an unbiased confirmatory test. The original last.pt primary results remain unchanged.

| Domain | best.pt joint NMS TP by seeds 17 / 42 / 2026 | best.pt joint FP | Added safety TPs beyond corresponding better best.pt single expert |
|---|---|---|---|
| Y-PPE (345 GT) | 113 / 122 / 134 | 54 / 74 / 108 | +2 / +3 / +1 |
| Construction (98 GT) | 20 / 47 / 27 | 110 / 157 / 148 | +7 / +7 / +6 |

At confidence 0.25 the highest observed best.pt fused critical-object recall was **134/345=38.84% on Y-PPE** and **47/98=47.96% on Construction**, with large false-detection burdens. Lowering confidence to 0.05 raises some TP counts but increases false detections substantially (e.g. 60 TP with 559 FP on Construction seed42). The validated oracle gains on Y that were absent under last.pt reappear (only 1–3 objects/seed) under best.pt; therefore the zero-complementarity statement is specific to the last.pt checkpoint policy and fixed threshold, **not invariant across checkpoints**.

Exploratory best.pt confidence-only Y-primary cascade on Y validation invokes the second expert in **279/356, 281/356 and 270/356** frames for seeds 17, 42, 2026 to recover only +1, +1 and +0 critical GT objects beyond primary-only. On Construction validation, six seed/direction confidence-only heuristic policies at cutoff 0.50 produced fewer matched objects than a **same-call-rate randomized routing expectation**; the comparator is mathematical, not sampled or a significance test. Neither observation establishes safety-aware compute reduction or energy benefits.

**NO-GO remains for deployable PPE safety, operational energy/carbon savings, and a claim that the present selective router is superior.** A revised paper focused on checkpoint-selection sensitivity, domain-conditional safety failure modes and the limits of confidence-only cascades is scientifically possible if a novelty assessment and an independently pre-locked final test justify its claims.

The two-domain observations are on separate frozen source distributions with different critical-class denominators and no verified independent site identifiers. Mean recall across the three repeated seeds is a *descriptive seed average on the same validation frames*, not a confidence interval for real-world worksites.

## Additional GT-privileged routing-value gate (2026-10-18)

A separate verified **retrospective** frame-level audit of the frozen best.pt predictions is now available in `results/BEST_PT_PRIVILEGED_ROUTING_OPPORTUNITY_2026-10-18.md`. For Construction-PPE validation with Construction as primary, only **7/132, 8/132 and 6/132** frames actually gained safety TPs under secondary invocation across seeds 17/42/2026; corresponding fixed-policy joint NMS matched **20, 47 and 27** GT objects. The privileged frame oracle's exact-GT selection could match **20, 48 and 27** at substantially fewer theoretical calls and fewer FPs, but this policy requires knowing the true labels at decision time and is **NOT OPERATIONAL OR DEPLOYABLE**.

The original safety-only confidence uncertainty feature has retrospective AUC **0.063, 0.053 and 0.085** for recognizing positive-gain frames on Construction. Confidence uncertainty over all object classes improves the descriptive AUC to **0.865, 0.753 and 0.858**, but the positive support is just 6–8 frames per seed, the best.pt checkpoints were already source-validation-selected, and **no calibrated independent router** exists. These results establish a *candidate ranking hypothesis*, not a safety, energy or deployment finding.

Y-PPE validation with Y as primary presents only **2/356, 3/356 and 1/356** positive-benefit frames on the best.pt sensitivity. With such rare positives, even a high ROC AUC would not, on its own, justify a practical router or an efficiency claim.

An independent validation data audit (`results/FROZEN_STAGE5_VALIDATION_SIMILARITY_PREFLIGHT_2026-10-18.md`) found **zero identical exported image SHA groups** among validation images within/across either nine-class domain and zero exact train↔val SHA overlap within the original frozen manifests. Small candidate dHash near-similarity groups exist and remain unadjudicated. No independent site/camera/video capture IDs are established. This is **not proof of source-group independence** or independent test validity.

**Publication decision unchanged:** GO for a scoped methodological **failure-mode and value-of-information audit** if related-work novelty is defensible, with clearly described GT oracle and selection bias. **NO-GO** for claiming a safe/sustainable selective PPE monitoring system; do not access final test merely to rescue a weak experimental claim. Prospectively predeclare a new target and threshold policy *without accessing test* if the research scope is deliberately changed.

## Scientific next decision — choose explicitly before accessing held-out tests

1. **Preferred first:** reframe the paper as an evidence-driven *limits and failure-mode audit of safety-aware multi-expert inference*. This can preserve all completed work and negative outcomes; acceptance in a Q1 venue remains uncertain and requires a defensible method/reproducibility contribution.
2. **Completed, separately labeled sensitivity:** six original validation-selected best.pt assets were independently verified and fully evaluated on both validation domains. Checkpoint choice materially changes observed performance, but the results are selection-biased diagnostics. Do not promote best.pt to an unbiased new primary baseline or optimize thresholds on held-out images.
3. **Prospective router hypothesis only if gates improve:** after observing a nontrivial object-level recovery ceiling and an agreed absolute safety criterion on development, fit a light primary-only router with cross-fitting, a matched-invocation random baseline and class/FP safeguards.
4. **No training of new detectors unless explicitly authorized** and scientifically necessary. No held-out test or energy benchmark is justified merely to rescue a weak development result.

**Test status:** untouched. **Energy/CO2 status:** unmeasured. **Original EcoSafe safety/sustainability positive claim:** unsupported / NO-GO.

Related reports: `results/Y_PPE_THREE_SEED_VALIDATION_2026-10-18.md`, `results/CONSTRUCTION_THREE_SEED_VALIDATION_2026-10-17.md`, `results/BEST_PT_Y_PPE_THREE_SEEDS_VALIDATION_2026-10-18.md`, `results/BEST_PT_CONSTRUCTION_THREE_SEEDS_VALIDATION_2026-10-18.md`, `results/BEST_PT_CONSTRUCTION_ROUTER_DIAGNOSTIC_2026-10-18.md`, and the updated working manuscript.
