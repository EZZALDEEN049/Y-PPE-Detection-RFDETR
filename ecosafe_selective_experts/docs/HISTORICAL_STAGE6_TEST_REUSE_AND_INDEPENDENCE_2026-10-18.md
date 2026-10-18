# EcoSafe — Historical test-data exposure and independence audit (2026-10-18)

**Purpose:** avoid false novelty/first-time held-out-test claims arising from reuse of Stage 5 checkpoints and datasets already evaluated in a DIFFERENT paper. This is a public, aggregate evidence-based protocol note; it uses no new test images, individual test labels or additional detector scoring.

## Three different uses of "test" that MUST NOT be conflated

1. **Historical Stage 4.5 preprocessing BEFORE Stage 5 model training:** Native source annotation metadata and geometry from train/validation/**test** were used to deterministically exclude harmonized-empty/critically unmatched images. No test image pixels were opened for qualitative threshold design and no model predictions influenced membership. Filtered 48 Y-PPE test images from the 234 clean-source images and 3 Construction-PPE test images from 141; final Stage 5 tests are **186 and 138 images**. This is annotation-informed definition of the benchmark population.
2. **Historical Stage 6 of the separate cross-domain reliability study:** The *same six final-epoch YOLO11m checkpoints* were evaluated on **BOTH Stage 5 frozen test splits**, 12 cells (6 models × 2 target domains), under an already frozen Stage 6 protocol. Aggregate performance was reported in `paper_draft/MANUSCRIPT_STAGE12_Q1_COMMITTEE_FINAL.md`. A subsequent, separately labeled, validation-selected **best.pt sensitivity was ALSO evaluated on test and summarized in that earlier manuscript**. The baseline test results thus **already exist and are available to the project research team**. It is FALSE to call either target test split globally "never model-evaluated," regardless of what EcoSafe code has done.
3. **Current EcoSafe research on primary/secondary fusion and selective escalation:** All **new paired joint NMS, GT-privileged per-frame recovery, router-signal diagnostics and confidence-threshold exploration** documented in PR#16 were run on the immutable **validation-only** source datasets (Y 356; Construction 132). There is **no newly reported EcoSafe joint-fusion/router test outcome in this branch**. This is true but is NOT equivalent to an as-yet-unseen test domain, because earlier Stage 6 models/test performance are part of the existing project knowledge.

## Chronological and scientific consequences

- Historical Stage 4.5: *annotation-dependent sampling* narrows original test population before training. Scope claims conditional on included harmonizable images. Training-source split dependence was pre-audited but no full original worksite mapping.
- Historical Stage 6: *model-prediction test evaluation* already produced paired in-domain/cross-domain expert performance for last.pt and later best.pt. Any new EcoSafe paper sharing authors/checkpoints/datasets must **cite the earlier paper** and must not relabel the existing held-out results as fresh independent confirmation.
- Current EcoSafe: the new **joint fusion** and **conditional router** policies were explored ONLY on validation; they have not yet been prospectively confirmed anywhere, and their source-validation-selected checkpoint sensitivity can be optimistic.

The prior manuscript reported last.pt seed-mean mAP50:95: Y in-domain **0.291 ± 0.007** vs Y→Construction **0.121 ± 0.003** and Construction in-domain **0.252 ± 0.004** vs Construction→Y **0.082 ± 0.005**. These are **earlier paper results**, not newly obtained EcoSafe independent test evidence or comparable to the new object-level fixed-confidence recall.

## Go/no-go decision for future verification

**Preferred independent confirmatory evidence** for a *NEW* safe-routing claim: acquire a fresh, rights-cleared, source-group-independent evaluation sample (worksite/camera/time holdout) not previously used for any model/route/policy selection and not present in the original Stage 5/Stage 6 paper; freeze every model/routing threshold, exact source/ontology and statistics **before** looking at it.

**If a new independent sample is unavailable:** One may transparently report additional test-policy outcomes on the EXISTING Stage 6 test images as a **secondary/reused-benchmark analysis**, ONLY after predeclaring the new analysis and maintaining test-policy discipline. It cannot honestly be presented as the study's first untouched independent test, nor used for confirmatory cross-site or previously unseen-population inference; reuse, related manuscripts and historical known performance must be explicitly disclosed. Do not mine these results to select a confidence threshold or seed.

**Current operational decision:** NO-GO for a claim of field-ready safety, new independently confirmed selective inference, lower joules or carbon. All real-energy and original-capture site-group gates remain unmet.

## Existing independently recorded evidence

- `cross_domain_reliability/stage4_5_label_completeness/Stage4_5_label_completeness_protocol_2026-09-20.md`
- `cross_domain_reliability/stage4_5_label_completeness/Stage4_5_conservative_adjudication_decision_2026-09-20.md`
- `cross_domain_reliability/stage6_heldout_evaluation/STAGE6_PROTOCOL_FROZEN.md`
- `cross_domain_reliability/stage6_heldout_evaluation/README.md`
- `paper_draft/MANUSCRIPT_STAGE12_Q1_COMMITTEE_FINAL.md`
- `ecosafe_selective_experts/docs/DATASET_SOURCE_LINEAGE_AND_TEST_SELECTION_2026-10-18.md`

**Privacy and reproducibility:** No private test identifiers/filenames, test predictions, original worker images or raw weights are uploaded in this evidence note. Original test metadata processing and prior published Stage 6 results are fully disclosed; no fresh test outcome was computed here.
