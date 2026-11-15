# SRAC-PPE public progress update — 15 November 2026

**Repository:** [EZZALDEEN049/Y-PPE-Detection-RFDETR](https://github.com/EZZALDEEN049/Y-PPE-Detection-RFDETR)  
**Project folder:** `research/srac-ppe/`  
**Status:** exploratory cross-dataset image-level inference completed; independent worker-level risk evaluation remains pending.  
**Publication status:** working research only; NOT submission-ready.

## 1. Executive state

This update records a real hosted-inference feasibility probe using the frozen author Roboflow RF-DETR Small model. It advances the project beyond the earlier six-image smoke test, but it does **not** validate worker-level PPE compliance, risk calibration, false-clearance control, or cross-site generalization.

The public GitHub folder is a status/reproducibility ledger. The full unpublished manuscript, worker imagery, per-image identifiers, raw identity-linked annotations, model weights, and credentials are intentionally not committed.

## 2. Verified model and dataset used in the probe

- **Detector:** `altayyar-0oflt-lafos-qqauz/2`, RF-DETR Small, original 17-class model.
- **Hosted inference settings:** confidence threshold 0.25; overlap threshold 0.50.
- **External public dataset:** [Construction-PPE on Roboflow Universe](https://universe.roboflow.com/disitech-0pg5l/construction-ppe-unha4-5njlk).
- **Dataset image counts observed during this audit:** 1,416 total; train 1,132; validation 143; test 141.
- **GT/model class mapping used for this image-level probe:** dataset `Person` / `no_helmet` / `helmet`; detector `Persons` / `No Hard Hat` / `Hard Hat`.

The dataset is external to the model's Roboflow project, but the model's complete training-source provenance and possible source-image overlap with this dataset were **not independently audited**. Therefore, this is a cross-dataset probe, not verified cross-site evaluation or proof of domain-shift robustness.

## 3. Prespecified image-level sample construction

The test partition was queried in full:

- Positive stratum: all 24 test images whose dataset annotation metadata contained at least one `Person` and one `no_helmet`.
- Comparison stratum: 24 images sampled from the 103 test images containing `Person` and `helmet`, with no `no_helmet` annotation. The 24 were selected by ascending FNV-1a 32-bit hash of `SRAC20261110:` concatenated with the provider image ID.
- Total: 48 distinct test images; all 48 hosted inference requests returned predictions.

The selection is deliberately stratified by existing image-level labels. It is not a prevalence-representative worker sample. Image identifiers are omitted from this public report in accordance with the repository's public-data policy.

## 4. Observed image-level outcomes

Outcome: whether an image contained at least one predicted `No Hard Hat` box. This is **not** a per-worker recall, IoU metric, PPE-rule violation rate, or false-clearance estimate.

| Analysis cutoff | GT stratum | Images | Images with at least one `No Hard Hat` prediction | Descriptive rate |
|---|---|---:|---:|---:|
| 0.25 (hosted inference cutoff) | `Person + no_helmet` | 24 | 22 | 91.7% |
| 0.25 (hosted inference cutoff) | `Person + helmet`, no `no_helmet` label | 24 | 1 | 4.2% |
| 0.50 (post-hoc box-score filter) | `Person + no_helmet` | 24 | 20 | 83.3% |
| 0.50 (post-hoc box-score filter) | `Person + helmet`, no `no_helmet` label | 24 | 1 | 4.2% |
| 0.75 (post-hoc box-score filter) | `Person + no_helmet` | 24 | 15 | 62.5% |
| 0.75 (post-hoc box-score filter) | `Person + helmet`, no `no_helmet` label | 24 | 1 | 4.2% |

For the base 0.25 cutoff, nominal two-sided exact Clopper–Pearson 95% intervals are:

- 22/24 positive-stratum image hits: **73.0%–99.0%**.
- 1/24 comparison-stratum label discordances: **0.1%–21.1%**.

These are nominal image-level intervals under an unverified independence assumption. They are not simultaneous intervals, not worker-level uncertainty intervals, and not population precision/false-positive estimates. The two higher cutoffs were applied post hoc to boxes returned by the original 0.25 hosted calls; they were not new inference runs and must not be used as prospective threshold optimization or final risk-calibration thresholds.

The comparison result is called **label discordance**, not a verified false-positive rate: an image may contain an unannotated bareheaded person.

## 5. Targeted failure and ontology review

A machine-assisted visual review of three discordant examples suggested:

1. Two images in the `no_helmet`-positive stratum were not construction work scenes (a child playing soccer and a stage performer wearing a casual cap). These are possible context/construct-validity contaminants; the visual review is not expert human adjudication.
2. One comparison image with a predicted `No Hard Hat` box appeared to contain a helmet-wearing person and a second bareheaded person. This suggests possible incomplete absence-class annotation rather than a confirmed detector false alarm. It remains unadjudicated.

Consequently, an object-class `no_helmet` label does not establish that the pictured person is a worker, that a helmet is required by the task/site, or that an occupational safety violation occurred. Conversely, the absence of a `no_helmet` annotation does not prove that every person is helmet-compliant.

## 6. Predicted worker–equipment association diagnostic

A small geometry-only screen was run on three multi-person images:

- 10 predicted `Hard Hat` / `No Hard Hat` head-evidence boxes.
- 9 boxes had their centres inside the top 40% of exactly one predicted person rectangle.
- 1 box fell inside two candidate person rectangles (ambiguous).
- 0 boxes were unmatched by this simple containment rule.

This is a feasibility diagnostic over model predictions, not validated identity matching. It did not use independent worker ground truth, did not prove one-to-one assignment, and is not an association accuracy estimate. Ambiguous association must route to `REVIEW`; robust evaluation requires all-worker ground truth, explicit one-to-one matching, and duplicate-detection handling.

A previous smoke test also exposed near-duplicate person boxes. Deduplication and association need to be tested against independent GT before worker-level metrics are reported.

## 7. Risk estimands clarified

Keep these quantities distinct:

- **False-clearance risk:** `R_FC(t) = P(D_t = CLEAR | Y = 1, PPE required)`. This is the probability of clearing a truly violating worker.
- **Uncontained-violation risk:** `R_UC(t) = P(D_t in {CLEAR, UNDETECTED, erroneous NOT_REQUIRED} | Y = 1, PPE required)`. This also counts missed workers and erroneous policy exemptions.
- **Accepted-CLEAR violation proportion:** `R_AC(t) = P(Y = 1 | D_t = CLEAR)`. This is the fraction of cleared workers who are true violators.

An upper bound on `R_FC` does **not** imply the same bound on `R_AC`; the latter depends on violation prevalence and the composition of all CLEAR decisions. `R_AC` requires a representative all-worker target-test sample with complete worker inventory and independent PPE-requirement/wearing labels. The present 24+24 stratified image sample cannot estimate it.

## 8. Statistical and software status

- The repository's candidate protocol currently specifies two risk families across a fixed nine-threshold grid, with illustrative targets `alpha_FC=0.05`, `alpha_UC=0.15`, and `delta=0.05`. Its committed planning calculator records 115 independent violation cases for zero observed FC errors and 159 for one observed FC error under that candidate simultaneous-bound procedure. These are mathematical feasibility counts, **not empirical performance or a guarantee**.
- A separate 661-case planning scenario was mentioned in a prior conversation under hypothetical true-risk/power assumptions. It was not reproduced with the committed calculator in this synchronization and is **not adopted** as the protocol sample size.
- Existing repository history records 24/24 tests for the research-only policy/GT-separation prototype. A later 25/25 count was reported in conversation, but the corresponding test source/log was not available for independent rerun in this synchronization; do not silently replace the repository's reproducible test record.
- No model retraining, score fitting, probability calibration, risk-threshold selection, risk-calibration, or independent final test was performed in this probe.

## 9. Manuscript artifact reconciliation

A local working DOCX is present in the project workspace under the filename `SRAC_PPE_Research_Manuscript_Working_v5_2026-11-10.docx`. Its document metadata title identifies it as v5, while the visible title page labels it **Manuscript v4.0**. The title-page status paragraph still mentions six smoke tests, while Section 6.1 documents the 48-image probe. Reconcile the version label and status paragraph before freezing the next manuscript revision.

The local document is not uploaded to this public repository. The public repository's policy against publishing the full unpublished manuscript and field imagery remains in force.

## 10. Remaining critical gates

1. Obtain a permissioned independent construction-site dataset with site/camera/acquisition-group provenance.
2. Audit overlap between the detector's training sources and all external evaluation images.
3. Have qualified human annotators adjudicate all workers, head visibility, helmet wearing, applicable task/site rules, and uncertain cases; include workers missed by the detector.
4. Freeze one-to-one worker–equipment association, deduplication, and visibility rules before calibration.
5. Separate score-fit, target risk-calibration, and final-test acquisition groups.
6. Estimate `R_FC` and `R_UC` on independent true-violation units; estimate `R_AC` only on a representative all-worker sample.
7. Compare strong baselines at matched human-review budgets and report uncertainty, coverage, review burden, violation recall, calibration, and failure cases.
8. Reassess the novelty claim against the closest PPE association, detector calibration, selective review, and risk-control literature.
9. Reconcile the local DOCX version metadata and ensure all manuscript tables describe the same verified experiment.

## 11. Synchronization and integrity note

This report and the aggregate CSV are public-safe status artifacts. No per-image IDs, private images, worker identities, raw annotations, API credentials, or model weights are committed. The full unpublished manuscript remains outside this public repository. No GitHub/Drive binary manuscript upload was performed.
