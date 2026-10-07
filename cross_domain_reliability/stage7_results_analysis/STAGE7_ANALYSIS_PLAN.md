# Stage 7 — Analysis Plan

## Objective
Convert the frozen Stage 6 held-out outputs into publication-ready evidence for the revised YOLO-only cross-domain reliability paper.

## Locked evidence base
- Six completed YOLO11m Stage 5 runs.
- Final-epoch `last.pt` checkpoint only.
- Three seeds per source domain: 17, 42, 2026.
- Two frozen held-out test domains.
- Exactly 12 Stage 6 evaluation cells.
- No new training or test-informed threshold/model selection.

## Analysis blocks
1. Primary cross-domain performance: mAP50:95, mAP50, mAP75.
2. Fixed operating-point reliability: Precision, Recall, F1.
3. Seed robustness: mean, SD, and paired seed-level gaps.
4. Safety-critical reliability: no_helmet, no_gloves, no_boots recall/FNR.
5. Per-class AP50:95 profile.
6. Dataset diagnostic audit to investigate plausible mechanisms.
7. Qualitative failure review after the quantitative audit.

## Statistical position
The current three-seed analysis is descriptive. Mean ± SD and paired seed-level gaps are the primary uncertainty summaries. No causal explanation or strong inferential claim should be made from three seeds alone.

## Publication claim permitted at this stage
The frozen evidence supports the claim that substantial cross-domain degradation occurs in both transfer directions and that safety-critical violation detection is particularly fragile. The evidence does not yet support a causal explanation for that degradation.
