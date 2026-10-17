# EcoSafe validation decision gate — 2026-10-18

**Decision status: NO-GO for claiming safe, energy-efficient selective expert inference with the current original Stage 5 `last.pt` models at the development evaluation policy.** This is a decision about an **unsupported positive claim**, not a claim that the research is a failure or that selective inference is impossible.

## Evidence checklist — now complete for DEVELOPMENT

- [x] All six original model weights bytewise SHA-256 verified without retraining.
- [x] Two frozen validation domains tested, each with both experts in all three matched training seeds.
- [x] Y-PPE: 356 validation frames, 345 safety GT, 106/103/94 joint NMS TPs per seed; identical to the Y expert alone.
- [x] Construction: 132 validation frames, 98 safety GT, 13/13/14 joint NMS TPs; 67/68/74 joint FPs.
- [x] Development threshold sensitivity exposes the absolute recall–false-alert tension. Gains at alternative cutoffs are clearly labeled exploratory.
- [x] Maximum-cardinality object matching independently checked by NetworkX; 2,848 newly evaluated image-policy comparisons agree, plus archived seed17 comparison.
- [x] Primary-confidence-only cascade simulated against actual always-run-both NMS, not secondary-only prediction switching.
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

The two-domain observations are on separate frozen source distributions with different critical-class denominators and no verified independent site identifiers. Mean recall across the three repeated seeds is a *descriptive seed average on the same validation frames*, not a confidence interval for real-world worksites.

## Scientific next decision — choose explicitly before accessing held-out tests

1. **Preferred first:** reframe the paper as an evidence-driven *limits and failure-mode audit of safety-aware multi-expert inference*. This can preserve all completed work and negative outcomes; acceptance in a Q1 venue remains uncertain and requires a defensible method/reproducibility contribution.
2. **Allowed, separately labeled sensitivity:** evaluate the already-trained, validation-selected `best.pt` assets. Checkpoint choice changes the experimental policy and requires a fresh frozen declaration; do not overwrite the original last.pt baseline or optimize thresholds on held-out images.
3. **Prospective router hypothesis only if gates improve:** after observing a nontrivial object-level recovery ceiling and an agreed absolute safety criterion on development, fit a light primary-only router with cross-fitting, a matched-invocation random baseline and class/FP safeguards.
4. **No training of new detectors unless explicitly authorized** and scientifically necessary. No held-out test or energy benchmark is justified merely to rescue a weak development result.

**Test status:** untouched. **Energy/CO2 status:** unmeasured. **Original EcoSafe safety/sustainability positive claim:** unsupported / NO-GO.

Related reports: `results/Y_PPE_THREE_SEED_VALIDATION_2026-10-18.md`, `results/CONSTRUCTION_THREE_SEED_VALIDATION_2026-10-17.md`, `results/CONSTRUCTION_CONFIDENCE_SENSITIVITY_2026-10-17.md`, and the working manuscript.
