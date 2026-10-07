# Publication Tables — Stage 7

## Table 1. Cross-domain performance of YOLO11m across three seeds

| Train domain | Test condition | mAP50:95 (mean ± SD) | mAP50 (mean ± SD) | mAP75 (mean ± SD) | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Y-PPE | In-domain (Y-PPE) | 0.291 ± 0.007 | 0.551 ± 0.018 | 0.275 ± 0.009 | 0.881 | 0.516 | 0.651 |
| Y-PPE | Cross-domain (Construction-PPE) | 0.121 ± 0.003 | 0.293 ± 0.017 | 0.079 ± 0.001 | 0.711 | 0.382 | 0.497 |
| Construction-PPE | In-domain (Construction-PPE) | 0.252 ± 0.004 | 0.467 ± 0.002 | 0.241 ± 0.010 | 0.921 | 0.580 | 0.712 |
| Construction-PPE | Cross-domain (Y-PPE) | 0.082 ± 0.005 | 0.187 ± 0.011 | 0.057 ± 0.004 | 0.766 | 0.209 | 0.328 |

## Table 2. Domain-generalization gaps

| Direction | mAP50:95 absolute gap | Relative mAP50:95 drop | F1 absolute gap |
|---|---:|---:|---:|
| Y-PPE → Construction-PPE | 0.170 ± 0.009 | 58.4% | 0.154 ± 0.022 |
| Construction-PPE → Y-PPE | 0.170 ± 0.003 | 67.4% | 0.384 ± 0.017 |

## Table 3. Safety-violation recall at the frozen operating point

| Train/Test condition | no_helmet recall | no_gloves recall | no_boots recall |
|---|---:|---:|---:|
| Y-PPE → Y-PPE | 0.310 ± 0.109 | 0.303 ± 0.029 | 0.367 ± 0.033 |
| Y-PPE → Construction-PPE | 0.117 ± 0.031 | 0.039 ± 0.034 | 0.000 ± 0.000 |
| Construction-PPE → Construction-PPE | 0.027 ± 0.000 | 0.020 ± 0.000 | 0.000 ± 0.000 |
| Construction-PPE → Y-PPE | 0.024 ± 0.041 | 0.015 ± 0.007 | 0.000 ± 0.000 |

## Table 4. Consensus false-negative audit across all three seeds

| Transfer direction | Safety class | GT objects | Consensus FN | Consensus FN rate |
|---|---|---:|---:|---:|
| Y-PPE → Construction-PPE | no_helmet | 37 | 31 | 83.8% |
| Y-PPE → Construction-PPE | no_gloves | 51 | 47 | 92.2% |
| Y-PPE → Construction-PPE | no_boots | 15 | 15 | 100.0% |
| Construction-PPE → Y-PPE | no_helmet | 14 | 13 | 92.9% |
| Construction-PPE → Y-PPE | no_gloves | 88 | 85 | 96.6% |
| Construction-PPE → Y-PPE | no_boots | 30 | 30 | 100.0% |