# EcoSafe-RFDETR Results Template

## Fixed-model Pilot
| Model | mAP50 | mAP50:95 | Violation Recall | J/frame | Latency ms | Memory | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
| Nano | TBD | TBD | TBD | TBD | TBD | TBD | |
| Medium | TBD | TBD | TBD | TBD | TBD | TBD | |
| Large | conditional | conditional | conditional | conditional | conditional | conditional | run only if justified |

## Pilot decision
GO / MODIFY / NO-GO: TBD

## Adaptive routing
| Router | Violation Recall | J/frame | Escalation Rate | Router Recall | Router FN | Notes |
|---|---:|---:|---:|---:|---:|---|
| Confidence | TBD | TBD | TBD | TBD | TBD | |
| Uncertainty | TBD | TBD | TBD | TBD | TBD | |
| EcoSafe | TBD | TBD | TBD | TBD | TBD | |

## External validation
Report controlled shift and cross-dataset results only after ontology mapping, overlap audit, and router freeze.

## Statistical reporting
- Bootstrap 95% confidence intervals
- Paired comparisons on common images
- Pareto source data for J/frame vs violation recall
- Non-inferiority only if delta was justified and frozen before final testing
