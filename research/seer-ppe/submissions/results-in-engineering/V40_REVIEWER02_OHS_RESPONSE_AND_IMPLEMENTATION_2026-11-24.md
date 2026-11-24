# V40 — Colleague reviewer 2: occupational safety and PPE review response
Date: 2026-11-24. Reviewer assessment: 75/100, Major Revision (colleague review, not journal decision). No new inference, training, dataset modifications, final package, or Zenodo deposit.

## Decisions and implementation
| Issue | Decision | Implemented action | Remaining limitation |
|:--|:--|:--|:--|
| 5.1 Class performance | Accept and verify | Recomputed all 17 class F1 values directly from archived M0 class counts. Added macro-F1 and illustrative lower-precision categories to Results 3.1, with negative-label interpretation. | Detection metrics against current single-curator annotations only; not worker-level safety accuracy. |
| 5.2 Occupational-safety claims | Accept | Added conceptual workflow in Discussion 4.1, explicit distinction between target eligibility, consistency diagnostics and qualified human assessment. No automatic clearance, sanction, validated operating cutoff or field deployment claim. | Person–equipment association, task-specific rules, human assessment and safety outcomes not validated. |
| 5.2 Proposed schematic | Accept, with transparent drafting attribution | Saved editable vector SVG Figure_4_Proposed_Workflow.svg and linked it as Figure 4; caption and general AI disclosure record ChatGPT (GPT-6.2) assistance. | Author must independently review and approve the artwork and scientific meaning; final visual, dimensions, export and caption QA pending. Do not claim author-only creation. |
| 5.3 Potential minors | Accept | Confirmed Child reference count and number of images, added context in S2 and manuscript ethics statement, expanded institutional determination request to cover historical research use, legal-representative permission, assent and safeguards as applicable. | 31 boxes in 22 images are not 31 unique children or verified ages, employment or child labor. No approval, exemption, legal-representative permission or institutional rights independently verified. |
| 5.3 Publication and data rights | Accept | Retain author permission attestation separately from documented research-use, publication, organization/project and redistribution permissions. Proposed public archive excludes raw field photos, source-identifying records, personal data and consent records. | Determine actual permissions and institutional requirements; review derived-data disclosure risk and licenses. Author retains documents privately. |

## Numerical check
Source: research/seer-ppe/V26_VALID_CURRENT_SOURCE_459_NUMERIC_SUMMARY.json (blob 662689a45f7276e8a48284175f9fc14dd207cee5), cohorts.M0.per_class. Sum across all 17 categories gives GT 3471, predictions 4103, TP 3297, FP 806, FN 174. Micro-F1 2*3297/(2*3297+806+174)=0.8706099815. Unweighted mean of exact per-class F1=0.8678108196461584. Hard Hat F1=0.9378109452736318; No Safety Boots F1=0.776255707762557. Goggles F1=366/(366+33+6)=0.9037037037037037 (90.37%, not 90.41% in the colleague report); Safety Vests=0.9041095890410958 (90.41%). S2 original numeric rows are correct and unchanged. Child: 31 GT boxes, 22 images with GT, 37 predictions, 29 TP, 8 FP, 2 FN, F1=0.8529411764705882. Child is outside V38-B's eleven selected target categories; that does not mean the images contain no minors. No raw photos accessed for this review.

## Workflow and policies
Figure 4 source: artwork-publication/Figure_4_Proposed_Workflow.svg (blob 10ef9c77dfcaa1266190505a9b80a2f0327360ef). It depicts a proposed process, not a validated decision system. No image pixels or empirical data used in the diagram. The only empirically studied component shown is the matched-target perturbation diagnostic, subject to the eligibility and experimental limitations in Methods. Elsevier June 2026 AI policy permits assistance with explanatory flowcharts, with human oversight and caption/general disclosure. https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals . Research ethics and vulnerable-population safeguards: https://www.elsevier.com/about/policies-and-standards/research-ethics . No assertion that a general image publication permission substitutes for required research-use, guardian or organizational permissions.

## Changed files
- Main manuscript 6d222ce8bba8f97538d05da4268613bd8eef21ff
- S2 42f977a7d4e7e654bcb763d1df2bcc00d9ef4f11
- Ethics route 4f509c8ca9376ca2c513db7ab269333ba3860a6b
- Matrix 5041eb51038245b86861a6a6c970fa072fd412d2
- SVG 87962610884a0e51d4450136502c6db3ba6c1d3e
Original numeric table rows identical. Final package generator must be updated to include four main figures, ten supplementary figures, SVG-to-PDF/raster export, exactly one caption for Figure 4, and final author review. Earlier V40 ZIP is superseded for manuscript content. No new final package requested or created. Keep institutional ethics and rights holds open until evidence is available.
