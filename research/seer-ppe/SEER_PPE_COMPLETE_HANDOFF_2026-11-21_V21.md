# SEER-PPE — Comprehensive GitHub handoff and research-state archive (V21)
# الورقة الشاملة لرسالة الماجستير — سجل التسليم والاستئناف

**Handoff date:** 21 November 2026.  
**Snapshot type:** Final *handoff/continuation snapshot* of work completed through manuscript **v0.20** (including A–D Train V16/V17, source/annotation V18/V19 and historical Valid V20).  
**Important:** This is **NOT the final publishable research paper**. Claims of statistically established SEER-PPE safety improvements, independently verified validation, XAI fidelity, and measured energy are **not yet supported**.  
**Repository:** https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR (verified public).  
**Canonical continually updated paper:** [MANUSCRIPT_MASTER.md](MANUSCRIPT_MASTER.md).  
**Snapshot owner:** The same project repository; source code, checkpoints, scripts, metrics and protocols remain linked below.  
**Author:** Ezzaldeen Al-Tayar — Faculty of Engineering and Information Technology, Taiz University, Taiz, Yemen — azzaltayyar@gmail.com.

---

## 1. رسالة إلى ChatGPT في أي حساب آخر / Instructions to the next assistant

> أعمل على رسالة ماجستير / ورقة SEER-PPE في المستودع العام \`EZZALDEEN049/Y-PPE-Detection-RFDETR\`. اقرأ هذا الملف أولًا، ثم \`research/seer-ppe/MANUSCRIPT_MASTER.md\`، و\`research/seer-ppe/DUAL_TRACK_CHECKPOINT_2026-11-21_V20.md\`، و\`research/seer-ppe/HISTORICAL_VALID_INTERNAL_METRICS_V20.json\`. افحص حالة GitHub الحالية قبل أي تعديل. **لا تبدأ البحث من الصفر ولا تطلب مراجعة بشرية ثانية أو إعادة فحص الصور**؛ أنا الباحث الذي جمعها وراجع وسومها. احتفظ بالنموذج الأصلي \`altayyar-0oflt-lafos-qqauz/2\` وبالتقسيمات والصور والوسوم دون تعديل. نتائج V20 تاريخية داخلية وليست إثباتًا لتفوق SEER-PPE. أكمل بدءًا من V21/V22 مع توثيق كل خطوة جديدة وحفظها في GitHub، دون استخدام Test للتطوير أو اختلاق توقيعات أو نتائج. اشرح أولًا ما وجدته بالفعل في الملفات ثم نفّذ الخطوة البحثية التالية.

**For a different ChatGPT account:** A new account or conversation does not automatically inherit private conversation context, connected Roboflow/GitHub permissions, private files or memories. The **public repository and this handoff are the portable context**. For writing to GitHub or accessing private Roboflow resources, connect the relevant accounts/plugins explicitly in that ChatGPT account; read-only public repository access does not grant write permission.

## 2. Research target and boundary

**Title:** *SEER-PPE: Safety-Constrained, Energy-Aware, and Evidence-Grounded Explainable Vision for Occupational Safety Monitoring.*

The research asks whether a safety-constrained post-detection evidence/routing policy can achieve reliable person–PPE decisions, principled uncertainty/abstention and faithful selective explanations with a better **measured** computational/review budget than a comparably guarded selective competitor. The baseline detector is the **already trained original RF-DETR Small 17-class** model. This is not a proposal to retrain the original model or a claim that the original detector's prior mAP is a new SEER result.

**Evidence layers must remain distinct:**
1. Object detection from original bounding-box labels (author-curated and already visually checked).
2. Individual person-to-PPE ownership, visibility and detector misses (only where recorded).
3. Applicable occupational task/site PPE mandate (not implied by the detector's negative-class name).
4. SEER-PPE policy safety/abstention decisions and actual human review action.
5. Instance-specific XAI faithfulness, workload, timing and *physically measured* energy if available.
6. Independent acquisition source/site groups and evaluation exposure.

Do not combine these into one unverified "PPE compliance" number.

## 3. Author's explicit non-reinspection instruction

The author personally selected, gathered, annotated, classified and inspected the images before/during/after the project, and has confirmed the general review was completed. The author explicitly rejects requirements to repeat all visual inspections or recruit a second reviewer. **Existing original labels are an acceptable single-curator reference for scoped internal object-detection analysis.** See [V18 explicit author-reference decision](AUTHOR_CURATOR_REFERENCE_POLICY_2026-11-21_V18.md).

Do not interpret this instruction as fabricated individual person–PPE entries, acquisition/site/session independence, employer PPE mandates, second-rater inter-annotator agreement or an independent blind test. Where prior Person–PPE fields were not documented, use \`NOT_RECORDED\` rather than inventing \`PRESENT\`, \`ABSENT\` or human-approved \`UNKNOWN\`. Focus on programmatic, already available annotation and source-record evidence.

## 4. Dataset and model identity — verified prior project records

| Dataset / split | Train | Valid | Test | Total |
|---|---:|---:|---:|---:|
| Original 17-class Y-PPE source images | 1,625 | 468 | 234 | **2,327** |
| Clean17 corrected derivative | 1,595 | 459 | 234 | **2,288** |

Original dataset had **16,520** object annotations. Clean17 recorded **16,300**. The original trained model's Roboflow **version 2** uses 5,577 generated/versioned images (Train 4,875 after train-only augmentation; 468 Valid; 234 Test) and model ID **\`altayyar-0oflt-lafos-qqauz/2\`**. Project \`softyyemen/altayyar-0oflt-lafos-qqauz\`. **Roboflow project version 3** is the unaugmented source corpus; do not silently treat it as a newly trained checkpoint. A separate historical 9-class local checkpoint is **not** the original 17-class RF-DETR Small model.

Prior model mAP figures cited in older work are **historical previous-research results**, not performance gains from SEER-PPE. The historical Test split was used/exposed during previous development. In this continuation **do not inspect Test images, query Test per-image outcomes, or tune against Test**; it cannot be called freshly unseen/external.

The Clean17 ZIP was previously archived privately and checked by SHA-256; its private binary bytes, Roboflow tokens and any short-lived media URLs **are not copied into this public handoff**. The GitHub repo contains the nonsecret research manifests and scripts.

## 5. What was actually executed — chronological, no inflated claims

### V06–V15: source integrity and provenance investigation

- Original Train+Valid **2,093/2,093** Source images retrieved/decoded for read-only pixel fingerprint audit; no missing images, no decode failures and **zero exact original Train↔Valid raw-byte or EXIF-normalized RGB cross-split matches** across 760,500 comparisons. **46** dHash-close candidate pairs (distance ≤8) touched **31** Valid original images. Exact-byte mismatch is not proof of independent acquisition.
- A 99-Valid-source risk queue and **280** actual original Train–Valid candidate-pair similarity inspections are archived. **12 high-similarity technical edges** form **8 graph components**; these are candidate same-frame/scene links, not site-family certifications.
- Original-to-Clean17 **459/459** Valid photo-content technical correspondence verified; **9** originals omitted from corrected Valid. Existing source risks: **5** previous research holds, **6** additional technical overlap quarantines, **81** other possible cross-split source-family candidates and **367** unflagged-but-uncertified.
- The strict independently certified source / individual worker-safety validation workflow has **0 independently signed Valid source families** and **0 complete signed Valid person-level reference cases**. Its file [VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json](VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json) remains **\`NOT_FROZEN\` and \`scoring_ready=false\`**. This does not invalidate existing author-curated object-detection boxes for a **different, narrow historical internal** endpoint.
- Source and gate details: [full pixel audit](SOURCE_ORIGINAL_FULL_AUDIT_2026-11-21_V01.md), [99 source comparisons](ORIGINAL_99_VALID_SOURCE_FAMILY_PAIRS_2026-11-21_V14.json), [Valid 459 technical correspondence](ORIGINAL_CLEAN17_VALID_IMAGE_CONTENT_V13.json), [V15 eligibility report](VALIDATION_459_SIGNED_SOURCE_COHORT_READINESS_V15.json).

### V16–V17: real *Train-only* model calls and conservative policy offline tracing

- Original fixed RF-DETR Small read-only inference on **four permitted original Train images A/B/C/D**: **51 detections**, comprising **7 Person boxes**, **38 typed PPE cues** and **6 context boxes**. No Valid/Test new inference in these steps.
- V17 executed a deterministic **offline paired A0/A5 routing trace** on the same saved detections: **34 tentative single-person geometric proposals**, **4 ambiguous/unassigned** typed PPE cues and **38 review suggestions that were NOT dispatched**. No actual XAI, reviews, verified worker clearances or power/energy metering. A0 raw detector boxes are not a worker-compliance decision policy.
- Earlier human-entered Train person/PPE review had **19 accepted person/item links** and **38/42** originally anticipated visual-state cells; four B cells remain unrecorded and D absence-of-people is not automatically certified just because the detector returned no Person box. These are not Validation human gold.
- Original detection evidence: [V16 actual Train predictions](ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json), [V17 paired trace](PAIRED_TRAIN_DETECTOR_POLICY_TRACE_V17.json), [V17 checkpoint](DUAL_TRACK_CHECKPOINT_2026-11-21_V17.md). [V17 successful CI](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44851631822).

### V18–V19: author-curated original boxes and actual numeric *Train* matching

- Live read-only Roboflow original annotations for A/B/C/D returned **48 saved boxes** (A 5, B 15, C 27, D 1). **7 B boxes** carry historical \`labeledByModel=RFBoxPrompt/v1\` provenance markers; author curation is accepted, but independent manual-from-scratch labeling cannot be claimed.
- Class-matched greedy one-to-one bbox matching at **IoU ≥0.50** on the 51 previously saved original-model predictions produced **TP=47, FP=4, FN=1; Precision=0.921569, Recall=0.979167, F1=0.949495**. These are **four in-training images and exploratory diagnostic metrics**, never independent validation, verified occupational-compliance scores or an A5 performance improvement.
- Historical hosted confidence floor was **0.20**. The computed truncated AP50 and AP50–95 above-floor proxies are **not canonical COCO mAP**.
- Excluding entire B image with model-assisted source labels: 3 Train images, 33 annotated boxes, 35 predictions; TP32/FP3/FN1, P0.914286/R0.969697/F10.941176.
- Computational original Valid sensitivity cohorts were fixed: **M0 459**, **M1 448** (remove 5 old holds and 6 technical quarantines), **M2 367** (also remove 81 other flagged possible-source images). Even M2 is not independently certified.
- Evidence: [Train numeric result](TRAIN_SOURCE_LABEL_DETECTION_NUMERIC_PREFLIGHT_V19.json), [source overlap cohorts](VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json), [V19 checkpoint](DUAL_TRACK_CHECKPOINT_2026-11-21_V19.md). [V19 successful CI](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44853282012).

### V20: frozen *historical internal* original-model Valid reaggregation

- Before reading V20 individual outcomes, an internal-only Valid analysis protocol was committed: [V20 frozen internal protocol](VALID_HISTORICAL_INTERNAL_OBJECT_EVAL_PROTOCOL_FROZEN_V20.md).
- Roboflow's **preexisting September 2025 model Eval** \`KyzP9neuyNTN5eQpGCAY\`, dataset/model **v2** and **\`split=valid\` at confidence 0.20** returned **468 saved original Valid image-level TP/FP/FN records**. Its native image IDs matched all **468/468** Source IDs. Exactly **459/459** mapped to corrected Clean17 Valid; nine non-retained originals excluded from M0/M1/M2. **No new inference** and **no Test data access** in V20.
- Read-only API on the **current** saved author-curated annotations for these **459** Valid sources returned **3,471 object boxes**, **729 annotated with model-assisted provenance**. The **historical Eval's** \`TP+FN\` referenced **3,455** objects; **446** image counts agreed, while **13** images disagreed by **16** labels in total. Historic version-2 prediction/GT geometry is **not accessible** through the legacy evaluation endpoint, so these metrics **were not recomputed against current bbox-level labels**. The 13 discrepancies are recorded and must never be silently ignored.

| V20 saved historic RF-DETR Valid-only cohort | Images | TP | FP | FN | Micro Precision | Micro Recall | Micro F1 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **M0** — 459 original IDs retained in Clean17 | **459** | 3252 | 642 | 203 | 0.835131 | 0.941245 | **0.885018** |
| **M1** — exclude 5 holds + 6 technical quarantines | **448** | 3217 | 639 | 200 | 0.834284 | 0.941469 | **0.884642** |
| **M2** — additionally exclude 81 flagged possible families | **367** | 2851 | 589 | 183 | 0.828779 | 0.939684 | **0.880754** |

M1/M2 relative F1 changes are approximately **−0.0376** and **−0.4264 percentage points** vs M0. Because these sets differ, this is only descriptive **source-risk sensitivity**, not causal source-leakage estimation, statistical superiority, fresh current-label evaluation or SEER-PPE-vs-baseline comparison.

Saved input/output: [historical V2 per-image counters](HISTORICAL_V2_VALID_PER_IMAGE_COUNTERS_V20.json), [read-only current labels, batch 1](V20_VALID_SOURCE_ANNOTATION_COUNTS_PART1_PRIVATE_WORKING.json) + [batch 2](V20_VALID_SOURCE_ANNOTATION_COUNTS_PART2_PRIVATE_WORKING.json), [V20 calculated cohort metrics](HISTORICAL_VALID_INTERNAL_METRICS_V20.json), [V20 checkpoint](DUAL_TRACK_CHECKPOINT_2026-11-21_V20.md), [deterministic Node script](tools/compile_historical_valid_internal_metrics_v20.mjs), [V20 successful CI](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions/runs/44856892166).

## 6. Current manuscript state and remaining work

**Canonical writing state:** [MANUSCRIPT_MASTER.md](MANUSCRIPT_MASTER.md), **working manuscript v0.20**, including article title, author, Taiz University affiliation, abstract, introduction, related work, materials/methods, descriptive Results, discussion, limitations, bibliographic foundations and Appendices A–M. This is a long cumulative draft; some early sections use outdated "pending" wording despite later V16–V20 appendix evidence. Treat **the latest dated appended evidence/checkpoints as the precise record**; reconcile textual inconsistencies by editorial review rather than invent data or silently replacing historical source statements. The related-work/novelty collision matrix and journal formatting still need work.

**Author's previous rough project estimates** were ~60% overall research progress and ~35% publication readiness; these are **subjective planning estimates, not a formal measured milestone or an assurance of acceptance**. Progress should be revised from documented actual experiments, not by the number of words appended.

**Still genuinely unfinished:**
1. If claiming metrics against **current** Valid boxes (rather than historical V2 annotations), freeze the original-model inference configuration, obtain **new read-only original-model bbox predictions** on already-author-curated original Valid Source IDs and compute same-class IoU/TP/FP/FN against the saved present labels for M0/M1/M2; log runtime/provider conditions and avoid revisiting Test. Confirm preprocessing and exact image mapping, and show effects of the 13 mismatched reference versions.
2. Execute real **SEER-PPE A5 post-detection policy** and preselected **strong matched-safety/matched-review-budget selective comparator** (e.g. A2) on the same approved images, rather than relying on the existing V17 abstention-only dry run. Define meaningful false-clearance and worker safety endpoints **only** when worker coverage, visual PPE status and applicable site/task mandates are genuinely available; otherwise report \`NOT_ESTIMABLE\` and use scoped detection/abstention/compute analyses.
3. Obtain real target-matched explanation perturbation outputs and **faithfulness** measures if XAI claims are to be made. Log actual inference/XAI count and latency/memory; claim electrical Joules **only if directly measured** on disclosed instrumentation.
4. Fix endpoint, cohort, threshold, hazard mandate policy and statistical comparison before final assessment. Historical Test was development-exposed; do not claim unseen or external generalization.
5. Update Results §4 and Discussion/Conclusion in the manuscript to consolidate genuine V19/V20 evidence without calling historical counter summaries a SEER effect. Complete literature review 2024–2026, novelty matrix, references, figures/tables, reproducibility and journal-format copyedit.
6. Strict source-family-certified worker-level comparison remains blocked by independent acquisition and per-person evidence. **Do not demand a second reviewer or repeat image review just to proceed with original author-labeled object detection.** Either narrow safety claims appropriately or provide genuine already-existing site/task evidence.

## 7. Research verification and safety rules for the next assistant

- **Read before write:** the root START HERE, this handoff, current \`MANUSCRIPT_MASTER.md\`, latest \`DUAL_TRACK_CHECKPOINT\` and current GitHub Actions statuses. Check git SHA and the public repository branch first.
- Preserve **original fixed 17-class RF-DETR Small**, original Roboflow images/splits/annotations, author decisions, real vs synthetic vs historical evaluation labels; **do not retrain**.
- Do **not** call previous Test unseen; do not access it for iterative development.
- The author has finished the broad image selection/classification/checking process. **No request to repeat all image review, obtain a second annotator or prove that the author photographed the files.**
- **Separate the legacy strict worker-safety gate** \`NOT_FROZEN\`/\`scoring_ready=false\` from the finished limited historical Valid internal object-detection reaggregation.
- The historical Eval's 13/459 GT count discrepancies and 729 assisted-label provenance markers are **not errors to silently fix**. V20 values are model-provider 2025 historic counters.
- Protect private Roboflow keys, privileged media URLs, private full-image archives, private communication and any credentials. GitHub handoff is public and contains **research summaries and nonsecret references only**, not the full ChatGPT dialogue or hidden attachments.
- For future new version V22+, create an explicit dated checkpoint and update README/master and deterministic tests. Distinguish completed CI from peer-reviewed scientific validation.

## 8. Canonical file map (clickable in GitHub)

| Purpose | Relative link |
|---|---|
| **Main full research manuscript, v0.20** | [MANUSCRIPT_MASTER.md](MANUSCRIPT_MASTER.md) |
| Research directory index | [README.md](README.md) |
| Single-curator accepted reference policy | [AUTHOR_CURATOR_REFERENCE_POLICY_2026-11-21_V18.md](AUTHOR_CURATOR_REFERENCE_POLICY_2026-11-21_V18.md) |
| Overall master protocol / study question | [PROTOCOL_MASTER.md](PROTOCOL_MASTER.md) |
| Last full verified checkpoint | [DUAL_TRACK_CHECKPOINT_2026-11-21_V20.md](DUAL_TRACK_CHECKPOINT_2026-11-21_V20.md) |
| Machine-readable last checkpoint | [DUAL_TRACK_CHECKPOINT_2026-11-21_V20.json](DUAL_TRACK_CHECKPOINT_2026-11-21_V20.json) |
| **All historic Valid per-image metrics and source risk cases** | [HISTORICAL_VALID_INTERNAL_METRICS_V20.json](HISTORICAL_VALID_INTERNAL_METRICS_V20.json) |
| Historical internal-only frozen method | [VALID_HISTORICAL_INTERNAL_OBJECT_EVAL_PROTOCOL_FROZEN_V20.md](VALID_HISTORICAL_INTERNAL_OBJECT_EVAL_PROTOCOL_FROZEN_V20.md) |
| V19 actual Train bbox metrics | [TRAIN_SOURCE_LABEL_DETECTION_NUMERIC_PREFLIGHT_V19.json](TRAIN_SOURCE_LABEL_DETECTION_NUMERIC_PREFLIGHT_V19.json) |
| Source-risk cohorts (459/448/367) | [VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json](VALIDATION_SOURCE_OVERLAP_NUMERIC_SENSITIVITY_V19.json) |
| A0/A5 dry run (Train only) | [PAIRED_TRAIN_DETECTOR_POLICY_TRACE_V17.json](PAIRED_TRAIN_DETECTOR_POLICY_TRACE_V17.json) |
| V16 original four Train real predictions | [ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json](ROBOFLOW_TRAIN_ONLY_REAL_MODEL_PREFLIGHT_2026-11-21_V16.json) |
| strict worker safety gate status | [VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json](VALIDATION_PERSON_PPE_SCORING_FREEZE_2026-11-21_V11.json) |
| V20 deterministic reproducibility script | [tools/compile_historical_valid_internal_metrics_v20.mjs](tools/compile_historical_valid_internal_metrics_v20.mjs) |
| V19 Train label matching script | [tools/score_original_train_boxes_v19.mjs](tools/score_original_train_boxes_v19.mjs) |
| V19 risk sensitivity script | [tools/compute_validation_source_sensitivity_v19.mjs](tools/compute_validation_source_sensitivity_v19.mjs) |
| Latest full GitHub source/reference CI | [GitHub Actions](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR/actions) |

## 9. Version meaning and access from another account

- **V21** in this filename means the **handoff/snapshot record created after the confirmed v0.20 work**, *not* a new V21 RF-DETR/SEER scientific evaluation. All V20 results and no-test restrictions are unchanged.
- Continue active development on \`main\`; the archive branch made for this handoff is a stable **historical snapshot**, not a promise that it will auto-update. Fetch \`main\` for current future progress.
- A fresh ChatGPT chat should use the public START_HERE URL to retrieve this context; if a GitHub plugin is linked in that chat, use it to read and then commit future research modifications. The other account **cannot import this chat's private memory or connector authorization** by visiting a link.
- The handoff preserves the research narrative, experiments, scripts and evidence pointers, **not** the literal entire private ChatGPT conversation transcript.

**Final handoff integrity note:** No new metric, retraining, source-review signature, Test inference, worker compliance result, XAI faithfulness or electrical-energy measurement was performed by producing this archival document.
