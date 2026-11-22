# Y-PPE Research Tracker v2.6.0 — extracted workbook contents

**Original Library file:** `Y_PPE_Research_Tracker_v2.6.0.xlsx`  
**Extraction date:** 22 November 2026  
**Original workbook size:** 19,814 bytes  
**Format note:** This file preserves the extracted text of all ten workbook tabs. It is a searchable archival transcription, not a replacement for the original editable XLSX workbook.

<PARSED TEXT FOR SHEET: 1 / 10 TABS
TAB NAME: Overview>
index,Y-PPE Research Progress | Controlled Revision Tracker,Unnamed: 1
0,,
1,Canonical version,2.6.0
2,Review date,2026-11-06
3,Steps (total),9
4,Steps complete,1
5,Pending / conditional / protocol,8
6,Current independent research state,Validation-only Q5 threshold algorithm frozen prospectively; no real Y-PPE results
7,Total synthetic tests PASS,29
8,Actual Y-PPE images audited,0
9,Independent scene-level verification,BLOCKED
10,External-app steps this version,0
11,Frozen dependencies,8
12,Current model-performance results,NONE
13,"Synthetic tests verify code paths, not dataset independence. Roboflow metadata is confirmed, but no real image labels or model predictions were examined.",
<PARSED TEXT FOR SHEET: 2 / 10 TABS
TAB NAME: Roadmap>
index,Step,Work package,Status,Outcome currently available,Next gate / dependency,Master version,Last updated
0,1,Prior publications and overlap audit,Completed,11-topic overlap matrix,External related-work audit remains required,2.1.0,2026-11-04
1,2,Y-PPE provenance audit protocol,Protocol + tool drafted,Audit protocol v1.1; executable file-audit runner,Local Y-PPE images and verified capture-group log,2.3.0,2026-11-04
2,3,Dataset and taxonomy reconciliation,Software validated (synthetic only),Roboflow records; audit CLI; 5/5 synthetic tests PASS,Actual Y-PPE v3 archive; manual source/scene adjudication,2.3.0,2026-11-04
3,4,Freeze experimental and statistical plan,SAP v1.2 + validation-only threshold protocol; real analysis frozen,29/29 synthetic tests; 19-point validation micro-F1 selection policy,"Provenance groups, validated matches and validation predictions",2.6.0,2026-11-06
4,5,Train/evaluate matched detectors,FROZEN: model experiments,No new scores,"Safe partitions, checkpoints and environment",-,-
5,6,Uncertainty and error analysis,Paired error counts + threshold selector tested synthetically,"FNR, FPPI and model-specific validation cutoff selection; no actual thresholds","Matched validation predictions, then untouched admissible test",2.6.0,2026-11-06
6,7,Same-hardware inference profiling,FROZEN: hardware and checkpoints,No new benchmark,Hardware and controlled runtime,-,-
7,8,External novelty and Q1 journal fit,FROZEN: external literature and journal,Architecture source only,Structured literature matrix and new findings,-,-
8,9,Final article and internal peer review,FROZEN: results and ethics gates,Outline only,Passed evidence gates,-,-
<PARSED TEXT FOR SHEET: 3 / 10 TABS
TAB NAME: Audit_Issues>
index,Issue ID,Severity,Topic,Evidence / observation,Required verification,Current status
0,I01,High,Source independence,No file-level scene/group audit provided,Hash+phash+group provenance,Open
1,I02,High,Taxonomy inconsistency,Thesis No Safety Attire vs discussion of abaya,Inspect data.yaml and annotation IDs,Open
2,I03,High,Test reuse,234-image historical test used in past publications,Report prior exposure and define permissible new tests,Open
3,I04,Medium,Metric contexts,"F1 91.1% summary, 91.9% threshold-optimized",Recover evaluation settings and logs,Open
4,I05,High,Derivative version,"2,288/16,300 in proposal only","Verify bytes, removed images and label delta",Open
5,I06,Medium,Latency comparability,2025 paper >100 FPS vs 2026 lack of same-device benchmark,Benchmark on controlled hardware,Open
6,I07,Medium,Rare class support,No Hard Hat 22 / Face Masks 15 / Child 19 in old test,Bounded CIs and careful inference,Open
7,I08,High,Global novelty,Within-author overlap audited only,Search target-journal/2024-26 comparable methods,Open
8,I09,High,Dataset transfer blocked,Y-PPE v3 export is ready remotely; environment DNS prevented ZIP download,Use authorized local ZIP or secure mounted archive,Open
9,I10,Medium,Similarity false positives,"dHash is a screening candidate generator, not a proof of scene relatedness",Two-reviewer adjudication and threshold audit,Open
<PARSED TEXT FOR SHEET: 4 / 10 TABS
TAB NAME: Sources>
index,ID,Source,Year,Type,Primary relevant sections,Verification status
0,S1,Taiz University MSc thesis,2026,Thesis,Ch 3 §§3.2.2–3.2.6; Ch 4 Table 4.1; §4.3,Author supplied; raw files not checked
1,S2,X-RF-DETR Explainable & Trustworthy PPE,2025,Conference paper,Framework; 300 public-image exploratory case,Author supplied
2,S3,AI-Driven RF-DETR Decision System,2025,Conference paper,Y-PPE curation; RF-DETR; claims on T4 FPS,Author supplied
3,S4,PPE Detection in Yemeni Sites: YOLOv11m vs RF-DETRs,2026,Conference paper,"Tables I-II, VI-VIII; split/threshold limitations",Author supplied
4,S5,BIM-Integrated Explainable Vision,2026,Conference paper,"BIM, XAI, AHP-TOPSIS; analytical evaluation",Author supplied
5,S6,Preliminary Research Proposal V1.0,2026,Working proposal,Derivative candidate; E1–E8,User supplied; claims unverified
6,S7,"Robinson et al., RF-DETR ICLR 2026",2026,Peer-reviewed source,Architecture provenance / model name,Conference website checked 2026-11-04
7,S8,Roboflow ALTAYYAR public project/version/evals,2026,Live platform metadata,"v1, v2, v3; finished RF-DETR runs; v2 eval",Verified 2026-11-04; no raw bytes
<PARSED TEXT FOR SHEET: 5 / 10 TABS
TAB NAME: Versions>
index,Version,Date,Milestone,Major changes,Review disposition
0,2.1.0,2026-11-04,Research contribution boundary and audit protocol,RQ refinement; provenance group rules; novelty matrix; unresolved label and score context,"Major revision; protocol accepted, audit not run"
1,2.2.0,2026-11-04,Platform record and historical metric verification,3 project versions; v2 eval confirms rounded thesis results; download not completed,Source-of-results audit completed; image-level audit pending
2,2.3.0,2026-11-04,Offline audit tooling verified on synthetic fixtures,"YOLO file integrity, hashes, dHash candidates, reviewer templates, 5/5 unit tests",Instrument tests PASS; real-data and scene-independence gates BLOCKED
3,2.4.0,2026-11-06,Offline statistical-methods completion and external dependency freeze,"SAP, fixed estimands, paired bootstrap CLI, 15/15 synthetic unit tests, manuscript skeleton, 8 freeze gates",Offline preparation accepted conditionally; real experiments BLOCKED
4,2.5.0,2026-11-06,Researcher-approved Q3/Q4 metrics decision,Historical + new audited split conditional; FNR + FPPI co-primary descriptive axes; synthetic suite 19/19,Conditional method approval; real-world estimates frozen
5,2.6.0,2026-11-06,Q5 validation-only threshold protocol,19-point global per-model cutoff; pooled validation micro-F1; tie lower FPPI then higher confidence; 29/29 synthetic tests,Conditional methods approval; test access and numerical thresholds BLOCKED
<PARSED TEXT FOR SHEET: 6 / 10 TABS
TAB NAME: Tool_Validation>
index,Test ID,Synthetic test,Result,Actual Y-PPE used?,Scope of verification,Reference file,Date
0,T01,Cross-split exact duplicate + invalid labels,PASS,No,File hashes; class/box validation,tests/test_audit_y_ppe.py,2026-11-04
1,T02,Documented capture-group conflict,PASS,No,"Group conflict reporting, not source truth",tests/test_audit_y_ppe.py,2026-11-04
2,T03,Wrong expected file count,PASS,No,Expected-count mismatch gate,tests/test_audit_y_ppe.py,2026-11-04
3,T04,PNG re-encoding retains decoded pixel identity,PASS,No,Pixel hash differs from byte hash,tests/test_audit_y_ppe.py,2026-11-04
4,T05,ZIP path traversal rejected,PASS,No,Restricted archive extraction,tests/test_audit_y_ppe.py,2026-11-04
5,,,,,,,
6,Interpretation: 5/5 synthetic tests passed. No conclusion about Y-PPE image independence or detector performance.,,,,,,
7,T06,Seed reproducibility and complete pairing,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
8,T07,Duplicate image/class/model row rejected,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
9,T08,Group bootstrap requires documented groups,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
10,T09,Incomplete rectangular table rejected,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
11,T10,Inconsistent grouping rejected,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
12,T11,Nonnegative count/GT identity validated,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
13,T12,No-GT denominator encoded null,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
14,T13,Group-aware model pairing preserved,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
15,T14,Model GT discrepancies rejected,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
16,T15,Unknown model rejected,PASS,No,Synthetic tests only; not real Y-PPE measurements,tests/test_paired_error_analysis.py,2026-11-06
17,T16,FPPI exact denominator and paired difference,PASS,No,FNR/FPPI synthetic matched counts,tests/test_paired_error_analysis.py,2026-11-06
18,T17,Cluster-resampling FPPI normalizes by actual images,PASS,No,Group bootstrap synthetic only,tests/test_paired_error_analysis.py,2026-11-06
19,T18,Sparse class leads to undefined macro FNR,PASS,No,Avoid zero-imputation in synthetic test,tests/test_paired_error_analysis.py,2026-11-06
20,T19,Declared violation list must be complete,PASS,No,No silent drop of a primary class,tests/test_paired_error_analysis.py,2026-11-06
21,TOTAL,19/19 synthetic tests passed,PASS,No,No Y-PPE images or model predictions verified,tests/,2026-11-06
22,T20,Complete 19-point validation grid accepted,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
23,T21,Max pooled validation micro-F1 selects correct threshold,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
24,T22,Reject any test split row,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
25,T23,Reject incomplete image/class/model/threshold grid,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
26,T24,Reject ground-truth drift across candidates/models,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
27,T25,Reject duplicate validation count row,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
28,T26,Reject impossible GT / TP + FN mismatch,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
29,T27,Reject candidate outside fixed grid,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
30,T28,Reject absent positive validation support,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
31,T29,F1+FPPI tie selects higher confidence threshold,PASS,No,Validation-only selection logic; synthetic fixture only,tests/test_select_validation_threshold.py,2026-11-06
32,TOTAL,29/29 synthetic tests passed,PASS,No,Not a Y-PPE dataset or model performance result,tests/,2026-11-06
<PARSED TEXT FOR SHEET: 7 / 10 TABS
TAB NAME: Frozen_Dependencies>
index,Gate,Paused operation,Needed material,Status,Resume when
0,D01,Image/label file audit,Local authorized image+YOLO annotation files,FROZEN,Archive and checksum manifest available
1,D02,Scene/session/site independent splits,"Verified source/session/group IDs, human review",FROZEN,Documented capture groups validated
2,D03,Derivative version diff,"2,288 image derivative and removals log",FROZEN,All before/after image and label changes reconciled
3,D04,New model training/evaluation,New splits/checkpoints/predictions,FROZEN,"No test leakage, matched evaluator"
4,D05,Expert safety weights,"Expert input, worker-level task rules",FROZEN,Documented cost justification and ground truth
5,D06,Fixed-hardware benchmarks,"Real device, weights, power meter for energy",FROZEN,Controlled repeated measurement logs
6,D07,Journal/novelty verification,Fresh external literature + index status,FROZEN,Search evidence and selected journal confirmed
7,D08,Submission readiness,"Empirical contribution, ethics, reuse disclosures",FROZEN,All scientific and publishing gates passed
<PARSED TEXT FOR SHEET: 8 / 10 TABS
TAB NAME: Statistical_Plan>
index,Item,Accepted rule,Boundary / interpretation
0,Primary estimand,Classwise FNR_c = FN_c/(TP_c+FN_c),Co-primary descriptive domain 1: missed annotated missing-PPE instances
1,Paired contrast,Paired ΔFNR_c and ΔFPPI (RF-DETR minus YOLOv11m),Signs interpreted per metric at fixed validation-selected operating points
2,Confidence,"95% percentile bootstrap; 2,000 draws",No equivalence claim if CI spans zero
3,Sampling unit,Documented capture group if known; else image,Image intervals descriptive and possibly too narrow
4,Validation,Threshold policy frozen on validation only,No test-tuned operating point
5,Sparse classes,Numerator/denominator + valid replicate counts,"No-GT means NA, not zero"
6,AP/mAP,Separate COCO-compatible raw prediction evaluator,NOT computed by paired_error_analysis.py
7,Multiplicity,No six unqualified confirmatory tests,Exploratory unless formal correction preregistered
8,Software validation,19/19 tests on synthetic fixtures,Software validation; no Y-PPE experiments
9,Final status,Dual FNR+FPPI plan conditionally approved,No absolute safer-model or incident-risk claim
10,Co-primary FPPI_V,Σ FP in six missing-PPE classes / all evaluated images,"False object predictions per image, not binary FPR or unique safety alerts"
11,Optional macro FNR,Mean six class FNRs if each class has GT>0,Undefined if any prespecified class has no reference support
12,Threshold selection,Use validation only; prospective rule now detailed in Q5 rows below,"No numeric budget, threshold or superiority margin approved yet"
13,Q5 primary cutoff selector,Max pooled six-class validation micro-F1 over 19 candidates; lower FPPI tie-break then higher threshold,No test-split rows used; actual cutoff values NOT yet calculated
14,Q5 sensitivity plot,Predeclared test FNR–FPPI curves on fixed threshold grid,"Exploratory only, never selects/reselects primary threshold"
<PARSED TEXT FOR SHEET: 9 / 10 TABS
TAB NAME: Interactive_Decisions>
index,Question,Adopted choice,Scientific decision,Evidence status,Next prerequisite
0,Q1,E — explanation requested,No research theme selection inferred from Q1 alone,Discussion only,External novelty evidence
1,Q2,D — supervisor recommendation,Object level primary; worker-level conditional,Protocol only,Verified person–PPE associations
2,Q3,C — researcher approved,Historical metrics + new audited group split if feasible,Protocol approved; new evaluation frozen,"Provenance, data and retraining resources"
3,Q4,C — researcher approved,"Class FNR + class-labelled FPPI, descriptive co-primary",Protocol v1.1; 19/19 synthetic tests,Matched predictions and validation-locked thresholds
4,Q5,D — researcher approved,Validation-only global per-model cutoff by pooled micro-F1 on 0.05–0.95 grid; test curves exploratory only,Protocol v1.0; 29/29 synthetic-only tests,Real validation predictions plus frozen source-safe split
<PARSED TEXT FOR SHEET: 10 / 10 TABS
TAB NAME: Q5_Threshold>
index,Q5 OPERATING POLICY,Rule,Evidence status,Reviewer restriction
0,Approval,D — researcher-approved,Confirmed choice,Method only
1,Candidate thresholds,"0.05, 0.10, ..., 0.95 (19 points)",Prespecified algorithm,Not real observed values
2,Global policy,One cutoff per model,Prespecified,"Identical selection method, numbers may differ"
3,Selection objective,Maximum micro-F1 for six absent-PPE classes,Validation only,Not safety-optimal utility
4,Tie break 1,Lower violation FPPI,Validation only,Do not peek at test
5,Tie break 2,Higher confidence threshold,Validation only,Only after F1 and FPPI tie
6,Matching,Class-consistent 1:1 boxes; IoU >= 0.50,Upstream required,Matcher not implemented by selector
7,Test FNR,At frozen per-model cutoffs,FROZEN,Requires test predictions
8,Test FPPI,At frozen per-model cutoffs,FROZEN,Requires same test images
9,Sensitivity,FNR–FPPI curves on test for 19 points,Exploratory only,No post-hoc threshold tuning
10,Calibration,Not inferred from threshold sweep,Not performed,Separate methodology required
11,Prior test,Published 234-image test exposed,Historical,Not independent unseen
12,Code tests,10 new + 19 prior = 29 PASS,Synthetic only,Not Y-PPE evidence
13,Primary freeze gate,Validation runs and source-separated split,Pending,No real threshold selection yet
