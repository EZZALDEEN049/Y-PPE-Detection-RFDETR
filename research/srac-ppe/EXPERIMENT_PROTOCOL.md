# SRAC-PPE experimental protocol — preregistration candidate v0.2

**Authored:** 2026-10-29. **Status:** DRAFT, NOT FROZEN; no target-site model results yet.  
**Primary detector:** pre-existing, frozen Roboflow `softyyemen/altayyar-0oflt-lafos-qqauz/2` (RF-DETR Small; 17 original classes).  
**Primary endpoint:** whether an automated **CLEAR** incorrectly clears a **true worker who must wear a helmet but is not wearing one**.

## A. Data integrity and decision ontology
1. Preserve acquisition-group identifiers (site, camera, video/source, timestamp/scene family); random frame-level splitting is prohibited.
2. Distinguish true field safety violations from object-level `no_helmet` marks. Ground truth requires worker localization, helmet requirement applicable to that task/location, actual wearing state, head visibility, annotator verdict, and `indeterminate` where unresolvable.
3. Annotate **all** ground-truth workers, even when the detector misses them. Match detected persons to GT by a prespecified method and report unmatched GT workers.
4. Record the original 17-class frozen-model outputs and the independent nine-class harmonized benchmark ontology separately. A nine-class dataset does not imply the 17-class model has been retrained.
5. A frozen reference archive is not an independent test of the frozen detector until original model-training provenance and scene-level overlap have been ruled out.

## B. Experimental partitioning (at the acquisition-group level)
- **Detector train**: historical/immutable; new paper does not retrain its main detector.
- **Score-fit**: may fit or calibrate a worker-level violation score; no leakage into risk calibration.
- **Risk-calibration**: independent *true violation* acquisition clusters; used solely for prespecified confidence-bound threshold selection.
- **Final test**: entirely disjoint clusters/sites as applicable, with complete GT worker inventory and no method tuning.
- If target dataset is from a single site, claim *target-site conditional evaluation*, not generalization across construction sites.
- If an external dataset has unknown actual site IDs, claim *cross-dataset* only.
- Repeated workers/frames within a cluster do not constitute independent calibration trials. Enforce one prespecified violation sampling unit per independent cluster, or use a separately justified cluster-valid inference procedure.

## B2. Strict anti-leakage interface contract (critical prerequisite)
**Do not permit deployment-time decisions to read hidden evaluation labels.** The current prototype's boolean `ppe_required` serves double duty in decision routing and ground-truth risk denominators. This is valid only if it is supplied from a *prospectively available, independently documented safety policy*, not copied from an after-the-fact human annotation of whether the pictured worker was violating a rule.

The next schema revision must separate:
1. `policy_helmet_requirement` in {REQUIRED, NOT_REQUIRED, UNKNOWN}, available at runtime from a frozen site/task policy authority;
2. `gt_helmet_requirement` in {REQUIRED, NOT_REQUIRED, UNKNOWN}, independently adjudicated for offline risk denominators;
3. `gt_helmet_wearing`, `gt_state`, and `worker_gt_id`, **offline-only**;
4. `detection/association/evidence/score`, runtime-only model outputs.

The runtime decision must depend only on (1) and (4), never on (2) or (3). UNKNOWN policy must route to REVIEW, never CLEAR. Offline risk evaluation uses independent (2) and (3); policy-rule disagreements must be reported as an additional failure mechanism. No result from the current combined-boolean CSV interface should be characterized as prospective deployment performance without independent provenance proof of its policy fields.

## C. Frozen decision policy
Outputs: **CLEAR**, **ALERT**, **REVIEW** for detected workers; **UNDETECTED** only in GT-based offline accounting.  
Non-required PPE is **NOT_REQUIRED**; unknown mandate, conflicting evidence, insufficient visibility, or uncalibrated score must not be automatically CLEAR.

Write `Y=1` for adjudicated true helmet-rule violation and `A=1` for helmet required.
- `R_FC(t) = P[decision_t = CLEAR | Y=1, A=1]`
- `R_UC(t) = P[decision_t in {CLEAR, UNDETECTED, NOT_REQUIRED} | Y=1, A=1]`

Caveat: `R_UC` measures *not automatically contained by the decision-routing interface*, not observed injury/hazard outcome. In the strict, revised policy/GT interface, an erroneous policy decision `NOT_REQUIRED` for a true helmet-rule violation is counted as uncontained; otherwise policy classification errors could artificially reduce risk. The offline evaluator knows which workers the detector missed; a deployed system may not.

Prespecify clear-threshold grid (candidate): `[.02,.05,.10,.15,.20,.30,.40,.50,.60]`; alert threshold `.80`. The score must be a separately fitted, independently assessed worker-level signal, **not** raw Roboflow confidence or the uncalibrated `no-helmet confidence minus helmet confidence`. Freeze evidence gate, class association and mapping before risk calibration.

## D. Simultaneous one-sided risk bounds
For each threshold t in a fixed M-element grid and risk r in {FC, UC}, count the errors `k_{r,t}` among `n_+` independently sampled adjudicated violations. Compute `U_{r,t} = BetaQuantile(1-δ/(2M); k_{r,t}+1, n_+-k_{r,t})` when k<n, and 1 otherwise.

Feasibility conditions:
- `U_FC(t) <= α_FC` and `U_UC(t) <= α_UC`.
- Proposed research targets: `α_FC=.05`, `α_UC=.15`, `δ=.05`. These are not regulatory thresholds.
- Select among feasible thresholds on *calibration-only* CLEAR utility; otherwise disable automatic CLEAR and state **NO FEASIBLE THRESHOLD**. Do not choose the protocol or grid after reviewing calibration outcomes.
- Bonferroni over 2M guarantees simultaneous confidence for this **fixed finite family** under the stated sampling assumptions; it is **not** a novel theorem nor a shift-robust guarantee.

### Planning-only sample feasibility (exact binomial; 2 risks x 9 thresholds)
Minimum independent true violation cases necessary for a certified upper bound at these parameters **if the observed risk error counts equal k**:

| k observed errors | FC upper <= 5% | UC upper <= 15% |
|---:|---:|---:|
| 0 | 115 | 37 |
| 1 | 159 | 51 |
| 2 | 196 | 63 |
| 3 | 231 | 74 |
| 5 | 296 | 95 |
| 10 | 443 | 144 |

The rows are mathematical feasibility conditions, not an experimental performance curve. Actual `k_FC` and `k_UC` need not be equal.

## E. Comparisons and fair tuning
- B0: fixed raw confidence or heuristic without selective abstention.
- B1: fixed confidence with REVIEW option.
- B2: calibrated score (e.g., temperature/Platt) with review budget; calibration fitted *only* on score-fit split.
- B3: matched-review selective threshold chosen *only* on calibration/split data; **never** tune review-rate match using final-test labels.
- B4: proposed risk-bounded decision policy using exactly the same frozen detections and worker matching.
- Ablations: evidence gate removed; detector missed-worker term excluded; score calibration removed; source-vs-target calibration; 1 vs 9 prespecified CLEAR thresholds; different label budgets.

All baselines must be evaluated at comparable human-review budgets. Distinguish fairness in reviewing detected workers from safety on undetected GT workers.

## F. Metrics and statistics
Primary: FC and UC risk on independent GT workers; CLEAR coverage; REVIEW rate; detection miss frequency. Secondary: false alert rate, violation recall, risk–coverage profiles, Brier/ECE **only for properly defined worker probabilities**, per-site breakdown, latency of **real measured** pipeline.

Report 95% uncertainty intervals for empirical test estimates, unit of independence, and paired/cluster-aware comparisons. For tiny samples report counts and `not estimable` rather than unsupported percentages or guarantees. Describe abstention, uncertain mandates, and detector misses.

## G. Research question gates
RQ1: Does site/dataset shift change worker-level risk? Requires external site provenance.  
RQ2: Is FC reduced at matched review burden? Requires paired independent test annotations.  
RQ3: How many violation labels support target-site risk calibration? Computational bound verified; empirical curve pending.  
RQ4: Which frozen components matter? Requires ablation on actual model predictions.

## H. Blocked but not preventing other work
No independent inference response/verified frozen weights; incomplete worker-level PPE-required labels; incomplete cross-site provenance; external construction dataset access in runtime. Continue literature/ontology/mathematical/reproducibility work without treating these as completed.
