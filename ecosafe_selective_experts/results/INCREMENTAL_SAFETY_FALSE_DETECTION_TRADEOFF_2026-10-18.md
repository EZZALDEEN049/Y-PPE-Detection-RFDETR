# EcoSafe incremental true-positive / false-detection burden (development validation)

**Calculated:** 2026-10-18. **Input:** previously archived locked aggregate `EcoSafe_last_vs_best_all_2domains_3seeds_validation.json` (two domains, three seeds, both original checkpoint variants); NO new model inference, no held-out test scores, no power meter. The private data were not required to produce the table.

Operational policy compared: **same class-aware joint NMS of both experts** versus the in-domain model (Y primary on Y-PPE, C primary on Construction) at fixed confidence 0.25 and GT class-aware IoU>=0.50.

`DeltaTP = matched_TP(joint)-matched_TP(in_domain_primary)`; `DeltaFP = unmatched_critical_detections(joint)-unmatched_critical_detections(primary)`. The **incremental false detections per extra true positive** is `DeltaFP/DeltaTP` when DeltaTP>0; if DeltaTP=0 it is undefined, NOT zero or infinity-valued evidence. These counts are **object-detection evaluation conventions**, not measured alarms delivered to employees or real-world false-positive operating costs.

| Validation domain | Seed | last.pt incremental TP / FP | best.pt incremental TP / FP | best.pt extra FP per extra TP |
|---|---:|---|---|---:|
| Y-PPE (345 critical GT / 356 images), Y primary | 17 | +0 / +2 | +2 / +4 | **2.00** |
| Y-PPE, Y primary | 42 | +0 / +2 | +3 / +16 | **5.33** |
| Y-PPE, Y primary | 2026 | +0 / +0 | +1 / +15 | **15.00** |
| Construction-PPE (98 critical GT / 132 images), C primary | 17 | +5 / +59 | +7 / +88 | **12.57** |
| Construction-PPE, C primary | 42 | +8 / +58 | +7 / +78 | **11.14** |
| Construction-PPE, C primary | 2026 | +7 / +68 | +6 / +112 | **18.67** |

The **checkpoint-policy effect is not a clean independent causal test**: `best.pt` was originally selected using source-domain validation feedback; the same frames are used in this development audit. The FP/TP quantities cannot establish a predeclared operational cost ratio, because no safety-domain authority has defined the different harms and review costs of missed violations versus false alerts.

**New bounded insight:** Even on the source domain where both experts show greater violation complementarity, the fixed-rule `best.pt` merger adds 11–19 unmatched detection boxes per extra matched GT violation versus using Construction alone. On the Y-PPE source, the extra matching benefit is 1–3 objects and the added false-detection cost varies substantially. A count-only improvement is therefore an incomplete evaluation of a safety monitoring cascade.

No group-independent confidence interval, energy consumption, carbon savings, safe-alarm rate, or operational deployment guarantee follows. The proposed independent evaluation must predeclare its safety objective and include both per-class missed violations and false-alarm burden, reporting absolute numbers and original sample support.
