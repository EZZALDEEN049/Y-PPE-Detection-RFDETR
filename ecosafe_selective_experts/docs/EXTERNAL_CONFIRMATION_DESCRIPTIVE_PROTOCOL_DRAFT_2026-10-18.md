# EcoSafe — prospective external-cohort evaluation design (NOT activated)

**Written:** 2026-10-18. **Status:** planned DESCRIPTIVE study; no external images obtained, no external ground truths exposed, no prospective test run or independently approved safety threshold. This file is not evidence of an independent study, an institutional preregistration, or a deployable routing algorithm.

## 0. Historical constraints, before any external data

The six frozen original YOLO11m weights were already measured on the original Stage 5/6 test splits in the **earlier cross-domain reliability manuscript**, including `last.pt` and a separate `best.pt` checkpoint sensitivity. EcoSafe's joint NMS and primary-only escalation diagnostics are **validation-only** thus far; **old Stage 6 test cannot be described as a newly unseen confirmatory cohort**. Earlier Stage 4.5 also used source test annotation metadata for deterministic pretraining label-completeness filtering. Source/provenance disclosure: `docs/HISTORICAL_STAGE6_TEST_REUSE_AND_INDEPENDENCE_2026-10-18.md`.

## 1. Independent cohort gate — do not run detector before every criterion is addressed

- Research permission and non-public storage arrangement from the actual data owner.
- Original new images/GT boxes with *exact* per-class definitions and verified one-to-one geometry mappings to `no_helmet`, `no_gloves`, `no_boots`; `no_shoes` is NOT automatically `no_boots`. Do NOT evaluate missing target classes as if they were negative GT.
- Independently verifiable site/camera/video/session/family source groups and non-overlap with Roboflow ALTAYYAR Version 2, Ultralytics Construction-PPE v1.0.0 and the images scored in Stage 6; if unknown, report **no independent-site confirmation**.
- Exact/decoded-pixel hash and perceptual candidate audit, with ambiguous cases resolved by authorized steward; no cherry-picked exclusions after seeing predictions.
- Per-class support on genuinely distinct groups; aggregate and per-class support set out *before* inference; a few sites or low boots GT counts may permit only descriptive analysis.
- The existing `scripts/15_external_cohort_preflight.py` verifies asserted metadata but **cannot independently certify the truth of signed site keys**, license or label definitions. Its output is only an eligibility-preflight report, not test authorization.

## 2. Descriptive policy registry — default proposal, awaiting approval

The proposed fixed reference grid **copies the historically specified primary operating point** to avoid external-score tuning. This is not an optimization of external results.

- Input 640, fixed object match class-aware max cardinality **IoU>=0.50**, detector export confidence floor **0.001**, model NMS IoU **0.70**.
- Main operating cutoff **confidence >=0.25**; joint class-aware NMS **IoU=0.70**.
- Both experts for each of three seeds **17, 42, 2026**; two source directions (Y-trained primary and Construction-trained primary). **Primary** is prespecified by source training domain, not chosen from results on the independent cohort; both primary directions are reported even if one is weak.
- Two checkpoint policies **`last.pt`** (original Stage 5 primary) and **`best.pt`** (original source-validation-selected sensitivity) must be reported separately, with their exact model SHA-256 and source-selection optimism disclosed. Never select the better checkpoint/seed based on new test.
- For each seed/checkpoint/primary direction, predefine four evaluation output policies: primary-only; other expert only; always-run-both plus class-aware NMS; evaluation-only concatenation matching oracle. Do NOT describe an oracle as a runnable ensemble or use GT for deciding invocations.
- **No learned/router hypothesis is confirmed or preselected** by this document: existing confidence-only heuristics are negative exploratory examples. Any prospective learned router would require a separate explicit lock and development-only cross-fitting before data access, or be absent from external claims.
- If any external class is semantically incompatible with the frozen Stage 5 ontology, abort full three-class evaluation; a helmet-only or glove-only sensitivity would be a **new explicitly limited question**, not a substitute for missing labels.

## 3. Prespecified outputs and uncertainty

For **every** seed, checkpoint and policy, compute only on the fixed and fully reported qualifying external cohort:
1. n images, n positive frames, original verified independent source-site groups; exactly recorded class GT support.
2. Per safety class: TP, FP, FN, fixed cutoff recall/FNR; pooled safety micro-recall with explicit numerator/denominator; predicted-box FP **per image**.
3. For joint versus each primary: within-image paired `DeltaTP`, `DeltaFP`, counts of frames with `DeltaTP>0,=0,<0`; raw concatenation GT oracle ceiling. For `DeltaTP=0`, `DeltaFP/DeltaTP` is **undefined**, never presented as 0.
4. Relative FP change, incremental **false detections per additional GT match**, and number of detections (not real field alarm counts) at the fixed cutoff.
5. Checkpoint variant by source/domain/seed with every row, not only mean or best-performing seed.
6. If properly recorded independently sampled source groups are adequately numerous, report a prespecified paired **group-cluster** bootstrap (5,000 replications) with all frames and model policies resampled together. If grouping is unverified or has very few independent groups, report **descriptive only**, no site-independent confidence interval or post hoc p-value.
7. Expert invocation fractions are counts only, NOT time/energy. Energy, latency, RAM, emissions may be reported only after separate matched actual device instrumentation; no energy reduction inferred from oracle or simulated policy.

The paper has **no externally approved safety loss/false-alert cost criterion**. Thus even a statistically measurable fusion gain cannot establish operationally *adequate safety* or a safe–energy tradeoff by itself.

## 4. Stop/abort conditions — preserve results, don't rescue with hidden tweaks

- If annotation schema conflates wearing no shoes with absence of safety boots, do not relabel without independent semantic review before scoring.
- If candidate images derive from Stage 5/6 sources or access permissions are not obtained, stop. A reused Stage 6 analysis must be labeled SECONDARY and never FIRST independent confirmation.
- If missing labels for a safety class, abstain from a three-class violation recall and never count unlabelled true violations as model false positives.
- If source groups are few or uncertain, do not compute misleading site-level CIs.
- If the predetermined grid shows no useful performance, report its negative outcome; never retune `conf`, seed, checkpoint or NMS against external GT and then call it an independent result.
- Keep RAW images, image names, source IDs, weights, test GT and per-image predictions private. Commit **aggregate-only** outputs after license check.

## 5. Current decision and dependencies

**Blocked:** original image/GT access and permissions; no-boots semantic alignment; original capture source-group attestations and support; academic/safety-authority acceptance criterion; hardware power meter and repeat traces if claiming sustainability. An email draft requesting the 2026 Scientific Reports external cohort was created **in the researcher's Gmail drafts but NOT SENT** on 2026-10-18. No dataset access or author agreement is implied.

**Related:** `docs/EXTERNAL_TEST_CANDIDATES_AND_ELIGIBILITY_2026-10-18.md`, `docs/UNSENT_EXTERNAL_VALIDATION_DATA_REQUEST_2026-10-18.md`, `docs/STATISTICAL_AND_SOURCE_GROUP_ANALYSIS_PLAN_2026-10-18.md`, `docs/PROSPECTIVE_TEST_FREEZE_GATE_DRAFT_2026-10-18.md`. These are transparent pre-analysis design documents, not authorization to publish operational safety or emissions claims.
