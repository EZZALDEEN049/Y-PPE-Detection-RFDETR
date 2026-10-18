# EcoSafe manuscript / figure submission dossier — DRAFT, not submission-ready

**Compiled 2026-10-18.** This file is a checkable inventory of existing valid results and future author decisions. It is **not** a publisher-format final manuscript, editor acceptance, verified new independent cohort or measured sustainability contribution.

## Current evidence-bearing figures

| Identifier | GitHub vector image | Safe figure-caption claim | Important nonclaim |
|---|---|---|---|
| Figure 1 | `figures/FIG1_CHECKPOINT_RECALL_FP_2026-10-18.svg` | Paired seed-level last.pt-versus-best.pt joint-safety recall and **false detection boxes per 100 validation frames** on Y-PPE/Construction-PPE | No population-independent CI; validation-selected best.pt may be optimistic; not field alerts or energy |
| Figure 2 | `figures/FIG2_INCREMENTAL_FP_PER_RECOVERED_GT_2026-10-18.svg` | For best.pt, source-aligned joint vs primary marginal FPs / marginal matched TP at fixed 0.25 | Ratio undefined when delta TP=0; not human alarm cost or a safety-utility threshold |

Source of Figure 1 points: hash-locked three-seed primary and sensitivity aggregate reports `results/Y_PPE_THREE_SEED_VALIDATION_2026-10-18.md`, `results/CONSTRUCTION_THREE_SEED_VALIDATION_2026-10-17.md`, `results/BEST_PT_Y_PPE_THREE_SEEDS_VALIDATION_2026-10-18.md`, `results/BEST_PT_CONSTRUCTION_THREE_SEEDS_VALIDATION_2026-10-18.md`. Figure 2 numbers are in `results/INCREMENTAL_SAFETY_FALSE_DETECTION_TRADEOFF_2026-10-18.md`. Both graphs depict original **development validation**, not Stage 6 reused tests or a new external set.

## Paper framing decision (scientifically mandatory)

The existing title *When Does a Second Detector Help? Checkpoint-Sensitive Safety-Object Complementarity under PPE Domain Shift* describes an empirical **limitations/failure-mode audit**. Do **NOT** present EcoSafe as a demonstrated field-safe, energy-saving selective PPE system. The tested primary-only confidence escalator does not show such a result, and even always-fuse baselines miss most violation GT objects.

## Standard end-matter drafts and required author decisions

**Data availability — author review required before submission:** The nine-class derivatives originate from Roboflow ALTAYYAR Version 2 and Ultralytics Construction-PPE v1.0.0. Rebuild instructions, correction manifests, source links and frozen fingerprint registries are in `docs/DATASET_SOURCE_LINEAGE_AND_TEST_SELECTION_2026-10-18.md`. Source access may require the dataset owner's credentials/permissions. Source original photographs, unapproved worker images, raw test labels and checkpoints are NOT openly redistributed by this PR. Public reproducibility currently includes source link/versions, code, SHA checks, methodological results and aggregate-only tables. The final manuscript must accurately specify which derived material can be shared under BOTH upstream datasets' actual terms.

**Ethics/privacy — author/steward decision pending:** The researcher states routine academic image use is authorized; no institution-specific ethics determination, worker consent record or blanket right to republish source photos is supplied here. Do not invent approval/waiver ID or falsely claim all personally identifying subjects consented. If only aggregate results and non-image charts are published, distinguish them from publishing raw photographs.

**Conflicts of interest — author statement pending:** Do not populate "none" until all authors declare.

**Funding — author statement pending:** Do not populate "no funding" without a confirmation.

**Author contributions — pending:** Cite only real contributors and actual duties; do not generate imagined author names/roles.

**Code availability — verified:** Research code is in `research/ecosafe-object-level-safety-gate-2026-10`, PR#16, with original Stage 5/6 repository histories. Tests are synthetic and do not validate empirical performance. Pin a **commit SHA/tag after research freeze**, not a moving branch alias.

**Figures and formatting — ongoing:** Figures 1/2 are non-identifying SVGs. Verify journal accepts SVG or convert to editor-accepted TIFF/EPS/PDF under exact target journal specification; do not claim a format or permissions review already completed. Captions must include conf 0.25, GT IoU>=0.50, NMS IoU 0.70 and n=356/132.

**Statistics — conditional:** Descriptive repeated seeds on same images do not give independent-site replication. Group-cluster uncertainty and external confirmation need original worksite/site IDs. Construction `no_boots` GT=4 in validation and cannot support precise rare-class safety claims.

**Energy and sustainability — NOT MEASURED:** Postprocessing tool `scripts/14_audit_measured_wall_power.py` exists, but no external power meter trace, calibrated wall joules, end-to-end p95, router/model wakeup cost, or CO2e record has been supplied. If submitted without measurements, **remove all affirmative energy/carbon conclusions** and retain any computational-call counts only as nonenergy diagnostics.

**Original held-out Stage 6 already used:** The older cross-domain reliability manuscript on the same models/images reports single-expert last.pt and best.pt test performance. The EcoSafe joint/router development analysis cannot claim its original test split is a first unseen test; seek a genuinely fresh source-independent cohort, or transparently acknowledge secondary use.

## Acceptance blockers by evidence type

| Blocker | Needed artifact / decision | Current status |
|---|---|---|
| New genuinely independent test | Approved external image/GT cohort, reviewed no-boots definition, group and exact-overlap audit, policies locked before scoring | **BLOCKED; no external dataset obtained** |
| Adequate PPE safety operating standard | Safety expert's minimum class-specific recall and false-detection burden limits | **BLOCKED; undefined** |
| Physical energy | Real instrumented full-system same-hardware traces and warm/cold run repetitions | **BLOCKED; unmeasured** |
| New methodological novelty | Strong independent scholarly review against established cascades, calibration, PPE generalization | **Partly screened; not certified** |
| Publisher format/author declarations | Choice of journal, final reference list, data/ethics/rights and conflicts/funding declarations | **Pending authors** |
| Scientific negative result reporting | Full last/best 3 seeds, two domains, object-level oracle, false-detection burden and transparency | **Documented on validation** |

**Operational next step:** review and (if authorized) SEND the prepared Gmail draft to the corresponding author of Scientific Reports 2026, or obtain another original external source meeting the strict ontology/site identity requirements; independently arrange access to power instrumentation if a sustainability claim is indispensable. This file does not send anything or authorize score-based test selection.
