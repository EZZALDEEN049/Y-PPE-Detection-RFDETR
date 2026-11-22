# Y-PPE thesis-to-Q1 research track

**Canonical proposal:** Version 3.5.0 (22 November 2026), maintained in the research project workspace.  
**GitHub role:** public-safe progress, decision, and evidence checkpoint; not a mirror of the unpublished full manuscript or raw data.  
**Current estimated progress toward a defensible Q1 empirical submission:** **47%** (weighted milestone estimate; see checkpoint for calculation and limitations).  
**Current status:** protocol development substantially advanced; Q15 model/data retrieval is partially executed; the paired evaluation and publication gates remain unmet.

## Start here

- [Progress checkpoint — 22 November 2026](PROGRESS_CHECKPOINT_2026-11-22.md)
- [Decision register Q1–Q15](DECISION_REGISTER_Q1_Q15.md)
- [Roboflow and SEER-PPE evidence audit](ROBOFLOW_SEER_EVIDENCE_AUDIT_2026-11-22.md)
- [Machine-readable project state](PROJECT_STATE_2026-11-22.json)
- [Repository-level YOLOv11m vs RF-DETR comparison protocol](../../docs/comparison_protocol.md)

## Scope separation

This folder tracks the **Y-PPE thesis-to-Q1 comparative reassessment** titled *From Aggregate Accuracy to Safety-Relevant Reliability*. It is distinct from:
- research/seer-ppe/: the separate SEER-PPE study and its source/prediction audits.
- research/srac-ppe/: the separate SRAC-PPE worker-level risk-adaptive research track.
- cross_domain_reliability/: the separate cross-domain study workspace.

Evidence may be reused across tracks only after exact dataset/model/version identity and admissible scope are established. A successful audit in one track does not automatically establish a gate in another.

## Research guardrails

1. Historical thesis/paper/platform metrics are not new experimental results.
2. Matching dataset counts and preprocessing do not prove identical split membership.
3. Source-image identity, scene/session independence, site independence, and external independence are different claims.
4. Q5 thresholds must be selected on eligible validation data only.
5. Q14 subgroup analysis is conditional on pre-existing verified metadata or mechanically derived GT-box scale; no new human visual labels are authorized under Q12 Option A.
6. A paired RF-DETR/YOLOv11m result requires both models' predictions on the same admissible images, using the same reference annotations and frozen matching rules.
7. Do not publish API keys, temporary export URLs, raw private images, or model-weight binaries in this public repository.
