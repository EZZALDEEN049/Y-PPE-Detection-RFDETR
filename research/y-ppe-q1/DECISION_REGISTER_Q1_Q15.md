# Y-PPE Q1 research decision register — Q1 to Q15

**Last synchronized:** 22 November 2026  
**Canonical proposal:** v3.5.0  
**Scope:** decisions made in the researcher–assistant dialogue and recorded in the project workspace. Approval of a protocol is not evidence that its experiment has been executed.

| Question | Researcher choice | Recorded decision / interpretation | Status |
|---|---|---|---|
| Q1 | E initially | Researcher requested clarification before deciding; subsequent delegated resolution should be checked against the earliest archived decision record before reproducing its full wording. | Initial response recorded; full final wording not reconstructed in this checkpoint |
| Q2 | D | Decision was delegated to the assistant after the researcher requested the scientifically appropriate choice. The exact option text is not reproduced here because it is not present in the current authoritative summary. | Code recorded; exact wording requires archive reconciliation |
| Q3 | C | Combine historical assessment with a newly audited partition where admissible. Historical results remain historical; a new split is conditional on provenance evidence. | Approved |
| Q4 | C | Dual evaluation of reliability/errors: class-wise FNR and pooled missing-PPE FPPI as separate primary descriptive domains; conventional mAP/precision/recall/F1 as supporting metrics. | Approved |
| Q5 | D | A base operating rule selected from Validation, plus a separate sensitivity analysis. Thresholds must not be selected from Test. | Approved; no new admissible threshold values selected |
| Q6 | D | Require the strongest level of independence that can actually be demonstrated: image/file, scene/session, site, or external. Do not overstate the level. | Approved; highest source-family level remains unverified for the Q1 archive |
| Q7 | C | Statistical plan conditional on proven independence; paired/group bootstrap, 2,000 draws, seed 20261106, 95% pointwise intervals, explicit rare-class and valid-draw reporting. | Approved; real paired inference not completed |
| Q8 | D | Staged experimental design E0–E6, with acceptance gates before advancing. | Approved; experimental stages remain mostly unexecuted |
| Q9 | C | Staged repeated training with a documented resource budget; planned three independent full runs per model (seeds 11, 29, 47) where resources and data eligibility permit. | Approved prospectively; no new training runs |
| Q10 | C | Evidence-integrated originality criteria and Go/No-Go publication gates; a new model comparison alone is insufficient unless it produces defensible new inference. | Approved; Q1 publication gate not met |
| Q11 | D | Structured literature review with two novelty matrices: prior author publications and external literature. | Approved; exploratory corpus, not comprehensive systematic/PRISMA review |
| Q12 | A | Use existing labels without additional human annotation review at this stage. No new human visual tags or inter-rater agreement claims. | Approved; label validity remains a limitation |
| Q13 | E (delegation) | Assistant selected conservative C: keep unweighted class-wise FNR and pooled FPPI separate; do not assign unsupported safety weights. | Approved; no empirical safety weights |
| Q14 | D | Conditional within-Y-PPE subgroup robustness only when existing verified metadata or mechanically derived fields support a predeclared analysis. Primary candidate: apparent GT-box scale. | Conditional design approval; only retrospective RF-only exploratory diagnostic exists |
| Q15 | C | Retrieve both model tracks and verify checkpoint, training exposure, dataset identity, split membership and evaluation eligibility before deciding reuse versus retraining. | Researcher-approved; execution partially completed |

## Binding cross-question constraints

1. The source data and test annotations remain immutable under Q12 A.
2. Q5 thresholds are model-specific and must be selected from eligible Validation data only.
3. Q6 independence levels are evidence-based; matching image counts or split counts do not prove membership or source independence.
4. Q7 uncertainty resampling must use authenticated acquisition groups when available; image-only resampling is conditional/descriptive if source groups are unknown.
5. Q13 forbids unsupported numeric safety weights and blended risk scores.
6. Q14 subgroup analysis does not establish cross-site or external-domain generalization.
7. Historical thesis, conference, Roboflow, and SEER-PPE outputs must be labeled as historical/reused evidence, not new experiments.
8. Q15 retrieval or export readiness does not equal successful archive download, checkpoint access, matched inference, or a passed E1/E2 gate.

## Decision status

Q14 is the latest fully ratified methodological question. Q15 Option C is now ratified as the execution route, but the retrieval and eligibility work is incomplete. No Q16 should be asked until the current Q15 retrieval and data-identity gate has been advanced enough to identify a genuine unresolved decision.
