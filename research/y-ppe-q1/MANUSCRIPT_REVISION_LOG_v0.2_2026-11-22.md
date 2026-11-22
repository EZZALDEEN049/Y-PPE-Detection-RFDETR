# Manuscript v0.2 revision record

**Date:** 22 November 2026  
**Canonical proposal:** v3.5.0  
**Decision register:** Q1–Q15; Q14 D; Q15 C  
**Publication status:** NO-GO

## Artifacts created

- `Y_PPE_Q1_First_Manuscript_Draft_v0.2.docx` — revised working manuscript (approximately 6,355 words including tables; 7 tables).
- `Y_PPE_v0.1_Internal_Peer_Review_Report.docx` — internal scientific review report.
- This repository folder stores the review and change record; the Word files were delivered as conversation attachments and are not committed as binary files in this update.

## Changes from v0.1

1. Subtitle now identifies both RF-DETR Small and YOLOv11m.
2. E1 status updated to a partial 2,093-image Train/Validation source-integrity screen:
   - 760,500 cross-split comparisons;
   - zero exact SHA-256 matches;
   - zero decoded-RGB exact matches;
   - zero missing files and decode errors;
   - 46 dHash near-pair candidates involving 31 Validation IDs;
   - original Test bytes not audited.
3. Explicitly states that the above is not proof of scene/session/site independence and does not establish exact membership across the two model-linked Roboflow projects.
4. Keeps the 459-row SEER-PPE RF-only Validation diagnostic out of Y-PPE Q1 results because the crosswalk is provisional and paired YOLO predictions are absent.
5. Adds the prior paper's full Validation/Test comparison table and flags unresolved provenance of its Test-specific “optimal confidence” values.
6. Documents that the prior YOLOv11m/RF-DETRs training setup used 300 versus 40 epochs, managed cloud resources, and non-fixed seeds; it was not a fixed-resource comparison.
7. Expands Q9 training budget, Q7 uncertainty, Q14 FPPI boundaries, and evaluator-freeze requirements.
8. Adds the nearest 2026 external literature and narrows the novelty statement.
9. Completes bibliographic details where verifiable and adds YOLO11 software and recent external references.
10. Retains E1 not passed, E2 not passed, E3 not started, and publication NO-GO.

## Gate status unchanged

| Gate | Status |
|---|---|
| E0 | Partially complete |
| E1 | Not passed |
| E2 | Not passed |
| E3 | Not started for an admissible common test |
| E4/Q14 | Separate SEER-PPE RF-only exploratory diagnostic; not transferable |
| E5 | Deferred |
| E6 | Not started |
| Q1 publication | NO-GO |

## Progress estimate

The weighted project estimate is adjusted conservatively from 47.25% to **47.75% (48% rounded)** because manuscript preparation and internal review advanced. No empirical gate was passed; the percentage is project-management progress, not probability of acceptance or scientific validation.
