# V32 — Image-level detection and perturbation-XAI scope decision

**Date:** 22 November 2026  
**Decision:** AUTHOR-SELECTED PATH 1 — NARROW THE CURRENT PAPER TO PPE OBJECT DETECTION AND PERTURBATION-BASED EXPLANATION ANALYSIS  
**Canonical manuscript:** `MANUSCRIPT_MASTER.md` v0.32  
**Protocol:** `PROTOCOL_MASTER.md` v0.8

## 1. Author decision

The author selected the first proposed path: complete the current study by evaluating image-level PPE object detection and visual/black-box explanation behavior, without making worker-level Person–PPE compliance a required endpoint.

The manuscript is therefore **not** a study that certifies individual workers as compliant/non-compliant. It is an empirical study of an existing PPE detector and a selective, target-specific perturbation/explanation layer.

## 2. In-scope research questions

1. How does the unchanged 17-class RF-DETR Small model perform against the current author-curated image-level class/box annotations on the 459-image original-Source Validation cohort?
2. How do selected PPE detections respond to controlled Gaussian occlusion, black-fill deletion, target-only insertion and progressive grid-based perturbations?
3. Can selective policies prioritize image-level detections for additional explanation under matched XAI-call/target budgets, and what are their selection overlap, detection alignment and actual call counts?

## 3. Primary evidence and endpoints

- V26 image-level detection: M0=459, TP=3297, FP=806, FN=174, micro-F1=0.870610; M1=448 and M2=367 are source-overlap sensitivity cohorts, not independent-site cohorts.
- V27: 9/10 target detections lost after target-box Gaussian occlusion; mean target confidence drop 0.622325 and mean control-region drop 0.008304.
- V28: 10/10 target detections lost after black-fill deletion; 7/10 target-only insertions retained the target.
- V29: mean hosted request round-trip 1.5206 s across ten calls; this is not pure model inference latency.
- V30: eight development-exposed images, ten targets, 1,068 actual model calls, 640 target-cell outcomes, 60 progressive eleven-point curves and 60 independently audited AUCs. A5/A6 deletion/insertion mean AUCs are 0.496288/0.944195 and 0.397182/0.871354, respectively; six target slots overlap, so the comparison is descriptive only.

## 4. Explicitly out of scope for this manuscript

The following are not required to complete the current paper and must not be presented as measured outcomes:

- Complete worker-level Person–PPE gold or verified equipment ownership per worker.
- Task/site-specific PPE mandates, confirmed occupational violations or compliance labels.
- Worker-level false-clearance, safety-risk reduction or intervention efficacy.
- Actual completed human review or downstream protective action. `REVIEW` is a priority/request state only.
- Acquisition-independent or external site generalization. The corpus is an author-curated multi-project applied dataset; source overlap and historical development exposure remain disclosed.
- Process memory and physical energy/Joules, or claims of energy savings.
- Causal/external explanation faithfulness. Current perturbation curves measure detector response to controlled image changes, not independent explanation ground truth.

Existing Person–PPE pilot annotations and geometric links remain archived as exploratory engineering artifacts. Missing cells remain missing; they are not imputed, scored or used to claim worker compliance. The incomplete Train pilot does not block the current endpoint.

## 5. Remaining work within scope

1. Test robustness of perturbation-based explanation rankings to grid resolution, masking/background method, blur and target-selection choices.
2. Expand the A5/A6-style matched-budget image-target comparison on a prespecified development cohort; disclose shared targets and source exposure, and avoid superiority claims unless supported.
3. Reconcile detection/XAI tables and regenerate figures from archived numeric ledgers.
4. Verify citations/DOIs, complete limitations and data availability, and generate an editable Word export from the canonical manuscript.

## 6. Immutable constraints

The original RF-DETR Small model, images, labels and splits remain unchanged. No retraining, protected-Test tuning/access, repeated full-corpus image review, or invented human/worker labels are authorized by this scope decision. The source-risk M0/M1/M2 sensitivity analysis remains in place.

## 7. Consequence

The strict worker-safety readiness flag may remain `scoring_ready=false`; that flag describes an endpoint now explicitly outside scope. It is **not** a blocker to the V32 image-level detection/XAI manuscript. The paper must be titled, abstracted and discussed so that it does not imply energy-aware deployment, worker-level compliance or validated safety intervention.

