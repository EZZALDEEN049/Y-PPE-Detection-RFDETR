# Stage 1 Pre-Execution Amendment — Cross-Domain PPE Reliability Study

**Date:** 2026-09-19  
**Status:** protocol clarification before any harmonized training or target-test exposure.  
**Purpose:** resolve methodological ambiguities identified during reviewer-style audit and Stage 2 data inspection. This amendment changes no empirical result because the new cross-domain experiments have not yet started.

## 1. Calibration support threshold

For classwise calibration analyses, a class is reported only when the evaluated calibration split produces at least **100 emitted detections, including at least 20 correct matched detections** after final post-processing. The primary calibration analysis remains global. Classwise results below this support threshold are marked insufficient-support rather than pooled or extrapolated.

A prediction is counted as correct for calibration only after one-to-one class-consistent matching at **IoU >= 0.50**. Unmatched detections and duplicate detections after final post-processing are incorrect. The primary reliability diagram uses **10 equal-frequency bins**. Platt scaling and isotonic regression are fit only on the designated target calibration/validation data; the target test split remains locked.

## 2. Brier-style correctness score

A Brier-style detection correctness score is **not part of the frozen primary metric set** because it was introduced during protocol drafting without prior justification. It may be reported later only as a clearly labeled exploratory analysis with a precise definition and appropriate citation; it cannot alter the primary conclusions.

## 3. Safety-weighted loss / cost ratios

No universal injury-cost ratio is assumed. Previously drafted fixed ratios such as 1:1, 2:1, 5:1, or 10:1 are not treated as factual safety costs. The primary safety reporting uses classwise, macro, and pooled violation false-negative rates (vFNR). If safety-weighted sensitivity analysis is retained, its weights must be declared before target-test evaluation and described explicitly as transparent sensitivity parameters rather than empirical injury probabilities.

## 4. Augmentation policy

The Y-PPE Roboflow Version 1 export contains training-only 3x Mosaic expansion and therefore is **not** accepted as the common raw training basis for the cross-dataset benchmark. Dataset cleaning, leakage assessment, split freezing, and harmonized class filtering are performed at source-image level before augmentation.

For the new harmonized baseline experiments, both Y-PPE and Construction-PPE will use the **same prespecified training-time augmentation/preprocessing policy for a given architecture**, or a no-offline-augmentation baseline if model-specific defaults make direct offline augmentation equivalence impractical. Historical Y-PPE Mosaic-expanded results remain contextual and are not reused as the harmonized baseline.

The exact common augmentation policy must be written into the run configuration before training and must not be changed in response to target-test performance.

## 5. Split independence and leakage gate

No model training for the new study is considered valid until both primary datasets pass Stage 2 or all detected issues are corrected and documented. Exact cross-split duplicates are prohibited. Perceptual near-duplicates are manually adjudicated. Frames from the same identifiable source video/project group must remain within a single split whenever grouping information is available.

The target test sets remain locked throughout calibration and adaptation. Progressive target adaptation subsets are nested within each seed and are drawn from target training/calibration data only.

## 6. Statistical comparison rule

Model comparisons evaluated on the same target images use paired resampling over target samples. Source-domain versus target-domain degradation is not treated as paired merely because the same model architecture is involved; it uses an independent-domain comparison unless a genuine pairing unit exists. Seed variability is reported separately from sample-resampling uncertainty.

## 7. Reliability language

The manuscript will not call performance “acceptable,” “reliable,” or “stable” based on an arbitrary universal threshold. If no application-specific stakeholder criterion is available before evaluation, results will be reported descriptively with confidence intervals, degradation magnitudes, calibration error, and safety-relevant false-negative metrics without a pass/fail deployment claim.

## 8. Harmonized baseline requirement

The historical 17-class Y-PPE results are contextual only. The empirical study requires new harmonized in-domain baselines using the frozen shared ontology before zero-shot transfer:

- Y-PPE harmonized -> Y-PPE test
- Construction-PPE harmonized -> Construction-PPE test
- Y-PPE harmonized -> Construction-PPE test (zero-shot)
- Construction-PPE harmonized -> Y-PPE test (zero-shot)

The same harmonized class semantics, split policy, and evaluation implementation are used for YOLOv11m and RF-DETR Small.

## 9. Amendment log rule

Any later protocol change made before training/test exposure must be appended with date, reason, and affected files. Changes prompted by target-test results are not permitted to be presented as preregistered decisions.
