# Y-PPE thesis-to-Q1 research track

**Canonical proposal:** Version 3.5.0 (22 November 2026), maintained in the research project workspace.  
**GitHub role:** public-safe progress, decision, and evidence checkpoint; not a mirror of the unpublished full manuscript or raw data.  
**Current estimated progress toward a defensible Q1 empirical submission:** **49%** (weighted milestone estimate; see checkpoint for calculation and limitations).  
**Current status:** protocol development substantially advanced; Q15 model/data retrieval and current-version metadata parity are partially advanced; E1/E2/E3 and publication gates remain unmet.

## Start here

- [Progress checkpoint — 22 November 2026](PROGRESS_CHECKPOINT_2026-11-22.md)
- [Decision register Q1–Q15](DECISION_REGISTER_Q1_Q15.md)
- [Roboflow and SEER-PPE evidence audit](ROBOFLOW_SEER_EVIDENCE_AUDIT_2026-11-22.md)
- [Machine-readable project state](PROJECT_STATE_2026-11-22.json)
- [Internal peer review of manuscript v0.1](MANUSCRIPT_PEER_REVIEW_v0.1_2026-11-22.md)
- [Manuscript v0.2 revision log](MANUSCRIPT_REVISION_LOG_v0.2_2026-11-22.md)
- [Latest session handoff — complete E1/E2 status v0.4](SESSION_HANDOFF_2026-11-22_v0.4.md)
- [Historical COCO export retrieval status](E1_HISTORICAL_COCO_EXPORT_RETRIEVAL_2026-11-22.md)
- [Previous session handoff — E1 continuation v0.3](SESSION_HANDOFF_2026-11-22_v0.3.md)
- [Current Roboflow dataset parity](Y_PPE_CURRENT_DATASET_PARITY_2026-11-22.json)
- [SEER V13 source-overlap transfer to Y-PPE](Y_PPE_SEER_V13_SOURCE_OVERLAP_TRANSFER_2026-11-22.json)
- [Previous session handoff — manuscript v0.2 and icon](SESSION_HANDOFF_2026-11-22_v0.2.md)
- [Research icon (SVG)](assets/Y_PPE_Research_Icon.svg)
- [Repository-level YOLOv11m vs RF-DETR comparison protocol](../../docs/comparison_protocol.md)

## Latest saved session

The latest session consolidated all verified evidence into `SESSION_HANDOFF_2026-11-22_v0.4.md`. Both exact historical COCO exports (YOLO v1 and RF-DETR v2) are ready on Roboflow, but the archive download was blocked by the active environment's DNS/network restriction. No ZIP hashes or archive inspection have been completed. E1 and E2 remain NOT PASSED; E3 remains NOT STARTED; publication remains NO-GO. Temporary signed URLs, credentials, raw data, model weights and unpublished DOCX binaries are intentionally not committed.

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
