# Y-PPE research results — complete repository inventory

**Last consolidated:** 22 November 2026  
**Canonical proposal:** v3.5.0  
**Repository:** `EZZALDEEN049/Y-PPE-Detection-RFDETR`  
**Branch:** `main`

## 1. Purpose and preservation rule

This inventory identifies the Y-PPE thesis-to-Q1 research artifacts currently preserved in the repository, the additional source documents copied from the connected Library, and the evidence that remains unavailable. It distinguishes the current Q1 reassessment from earlier Y-PPE dataset-audit work and from other research tracks.

## 2. Canonical research source documents newly archived

| Artifact | Repository path | Status / role |
|---|---|---|
| Master proposal v3.5.0 | `source_documents/MASTER_PROPOSAL_v3.5.0.md` | Canonical proposal text copied from the current Library source; working proposal, not completed article |
| Journal manuscript scaffold v0.1 | `source_documents/JOURNAL_MANUSCRIPT_SCAFFOLD_v0.1.md` | Methods-only manuscript scaffold; results section intentionally not written |
| Research tracker v2.6.0 | `source_documents/Y_PPE_Research_Tracker_v2.6.0_EXTRACTED.md` | Searchable extraction of all 10 workbook tabs — Overview, Roadmap, Audit_Issues, Sources, Versions, Tool_Validation, Frozen_Dependencies, Statistical_Plan, Interactive_Decisions, Q5_Threshold; original XLSX remains in Library |

## 3. Current Q1 reassessment and evidence records

- `README.md` — start page and research guardrails.
- `PROJECT_STATE_2026-11-22.json` — machine-readable project status and next actions.
- `PROGRESS_CHECKPOINT_2026-11-22.md` — weighted progress and chronological checkpoint.
- `DECISION_REGISTER_Q1_Q15.md` — researcher-approved decisions and constraints.
- `ROBOFLOW_SEER_EVIDENCE_AUDIT_2026-11-22.md` — version chronology, current dataset parity, and SEER-PPE V13 source-overlap mapping.
- `Y_PPE_CURRENT_DATASET_PARITY_2026-11-22.json` — duplicate-aware current-version metadata comparison and sampled annotation geometry checks.
- `Y_PPE_SEER_V13_SOURCE_OVERLAP_TRANSFER_2026-11-22.json` — machine-readable source-ID, filename/split and overlap evidence transfer.
- `E1_HISTORICAL_COCO_EXPORT_RETRIEVAL_2026-11-22.md` — exact historical COCO export readiness and download limitation.
- `SESSION_HANDOFF_2026-11-22_v0.2.md`, `v0.3.md`, `v0.4.md` — chronological resumption records; v0.4 is the latest.
- `MANUSCRIPT_PEER_REVIEW_v0.1_2026-11-22.md` — internal review findings.
- `MANUSCRIPT_REVISION_LOG_v0.2_2026-11-22.md` — revision record.
- `assets/Y_PPE_Research_Icon.svg` — research icon.

## 4. Earlier Y-PPE data-audit evidence preserved elsewhere in this repository

The following records are retained under `cross_domain_reliability/stage2_data_audit/results/` and should be read as earlier dataset-stage audits, not as proof that the current Q1 E1 gate has passed:

- `Y-PPE_v1_audit_2026-09-19.md`
- `Y-PPE_v1_correction_plan_2026-09-19.md`
- `Y-PPE_v1_near_box_adjudication_2026-09-19.md`
- `Y-PPE_v1_visual_adjudication_2026-09-19.md`
- `Y-PPE_v2_stage2_audit_and_correction_2026-09-19.md`
- `Y-PPE_v2_conservative_file_correction_manifest_2026-09-19.csv`
- `Y-PPE_v2_near_box_removal_manifest_2026-09-19.csv`
- `Y-PPE_v2_clean_stage2_closure_2026-09-20.md`

The executable audit scripts, configuration, and workflow are in the same `stage2_data_audit/` directory. Their scope and source versions must not be conflated with the historical model-training archives required for the current E1 gate.

## 5. Current scientific state — unchanged by archiving

- Weighted project-management estimate: **48.75% (49% rounded)**. This is not a publication probability or an empirical validity score.
- E1: **NOT PASSED**.
- E2: **NOT PASSED**.
- E3: **NOT STARTED** for a new admissible paired comparison.
- Publication decision: **NO-GO**.
- Research Hold: no new training, performance comparison, or superiority claim before E1 and E2 pass.

## 6. Explicitly not yet archived as raw binaries

1. The 5,081-word manuscript draft v0.1 DOCX previously described in conversation was not found as an accessible Library/Project file in this verification pass. The repository contains the manuscript scaffold, internal peer review and revision log, but these are **not** a substitute for that full DOCX. It has not been recreated or falsely represented as archived.
2. The original `MASTER_PROPOSAL_v3.5.0.docx` and `Y_PPE_Research_Tracker_v2.6.0.xlsx` binaries remain in the connected Library. Their proposal text and workbook-tab contents are now archived in searchable Markdown transcriptions under `source_documents/`; the binary originals were not uploaded to GitHub.
3. The historical COCO ZIP archives for YOLOv11m project v1 and RF-DETR Small project v2 have not been downloaded. Roboflow export readiness is not equivalent to archive possession. No archive SHA-256, archive integrity, or historical split-byte audit exists yet.
4. Model checkpoint binaries and temporary signed export URLs are intentionally not committed.
5. Raw private images, credentials, API keys, and restricted source material are not included.

## 7. Next required inputs

- Upload the historical YOLOv11m v1 COCO ZIP.
- Upload the historical RF-DETR Small v2 COCO ZIP.
- If the full 5,081-word manuscript v0.1 DOCX is to be versioned, attach that exact original file; do not reconstruct it from the scaffold.
- After the two COCO archives arrive, compute archive and per-image SHA-256, inspect split membership and raw bytes, audit Test images, and resolve source-family/site/session evidence before E1 can be reconsidered.

## 8. Entry point

Start with `README.md` and then open `SESSION_HANDOFF_2026-11-22_v0.5.md`. Use `SESSION_HANDOFF_2026-11-22_v0.4.md` for the detailed E1/E2 evidence record. This inventory is the complete repository map as verified on 22 November 2026.
