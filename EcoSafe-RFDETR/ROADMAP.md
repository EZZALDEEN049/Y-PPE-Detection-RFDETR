# EcoSafe-RFDETR Roadmap

## Phase A — Project control [DONE]
- Dedicated branch created: ecosafe-rfdetr
- Draft pull request opened
- Project policy, protocol, configuration, manuscript skeleton, claims register and experiment registry versioned
- Raw data excluded from GitHub

## Phase B — Pilot-0 [NEXT]
- Provision a fixed NVIDIA GPU environment
- Record environment metadata
- Audit and lock the primary public dataset
- Train RF-DETR Nano and Medium
- Add Large only if needed
- Measure violation recall, latency and J/frame
- Build oracle escalation labels
- Decide GO / MODIFY / NO-GO

## Phase C — EcoSafe adaptive routing [BLOCKED BY PILOT]
- Calibrate detection confidence
- Build uncertainty signal
- Build lightweight domain-shift/OOD signal
- Define safety-relevance signal
- Train and evaluate cost-sensitive router
- Run threshold sensitivity and ablations

## Phase D — External validation [BLOCKED BY ROUTER FREEZE]
- Controlled domain-shift evaluation
- Cross-dataset overlap audit
- External construction-domain validation
- Bootstrap confidence intervals and Pareto analysis

## Phase E — Manuscript completion [BLOCKED BY RESULTS]
- Finalize Introduction and Related Work
- Align Methodology with executed code
- Populate Results only from versioned outputs
- Write Discussion, limitations and Conclusion
- Run final claim audit and submission checks
