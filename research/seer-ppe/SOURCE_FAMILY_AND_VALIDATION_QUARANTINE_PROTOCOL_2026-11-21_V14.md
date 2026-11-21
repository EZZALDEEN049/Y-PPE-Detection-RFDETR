# SEER-PPE V14 — conservative Validation source-quarantine and signed-eligibility handoff

**21 November 2026.** The real [V14 original media run](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44845378772) compared all **99** flagged original Valid sources against **280** unique original Train candidates (50 V13 comparisons plus 230 additional), with **304/304** source SHA-256 verifications and **no Test photo access**. It detected **12** high same-frame alignment *technical* pairs involving **9 distinct original Valid sources**; two of these were previously held but present in Clean17, **six** additional clean-retained images are unsigned high-risk candidates, and one original Valid source was already excluded by Clean17. The other 90 flagged Valid originals lack high same-frame alignment among compared candidates but are **not independently sourced by default**.

## Conservative readiness classes for the 459 Clean17 Valid candidates

| Administrative status (not GT label) | Original Valid sources in corrected Clean17 |
|---|---:|
| `RETAIN_PREEXISTING_RESEARCH_HOLD` | **5** |
| `TECHNICAL_OVERLAP_QUARANTINE_PENDING_REVIEW` | **6** |
| `SOURCE_FAMILY_REVIEW_PENDING` | **81** |
| `NO_SCREEN_FLAG_INDEPENDENCE_UNCERTIFIED` | **367** |
| **Total** | **459** |

The full [Source-ID eligibility matrix](VALIDATION_TECHNICAL_QUARANTINE_V14.json) contains 459 rows, each linked to the actual SHA-verified original→Clean17 file correspondence. The [six-personalized evidence handoff packet](VALIDATION_P0_HIGH_OVERLAP_HUMAN_REVIEW_V14.json) cites the strongest original Train image candidate, measured SSIM and number of matching candidate pairs for each new technical quarantine. These six **are not six newly signed research holds**, and no new human source-family verdict has been entered. A strong same-frame optical match is a serious source-dependence risk for a site-independent evaluation; equally, a weak SSIM does not establish source independence.

All five original research holds are retained regardless of whether their particular V14 candidate comparisons have high alignment; the two held School 22 May – Aseefrah images remain held because named-site evidence is logically distinct from same-frame pixel matching. Other flagged cases remain pending; unflagged images still need family/acquisition signoff. A human decision requires original site/scene provenance and training-family crosscheck, not just user-level general visual approval.

## Before freezing a scientific Validation experiment

A future freeze may only select individually signed independent-source images not on a research hold or unresolved high-image technical quarantine, with separately documented human person/gear ground truth and task applicability, fixed predictor and thresholds, paired baseline-versus-SEER evaluation plan, audited per-image inference outputs and family-cluster-aware statistics. This V14 artifact is *source-eligibility triage*, not an empirical model evaluation. No image classification, original RF-DETR weight, Roboflow annotation, split, case reference or protected Test was modified; no mAP, F1, compliance false-clearance, explanation fidelity or electrical-energy result is asserted. **`scoring_ready=false`.**
