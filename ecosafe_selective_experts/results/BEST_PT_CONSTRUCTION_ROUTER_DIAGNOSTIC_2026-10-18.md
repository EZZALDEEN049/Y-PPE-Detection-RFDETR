# best.pt sensitivity — Construction development confidence-routing diagnostic

**Date:** 2026-10-18. **Status:** Exploratory, DEVELOPMENT-ONLY. No learned router, selected threshold, energy, latency or independent held-out test claim.

Six original best.pt models, three seed-matched expert pairs, 132 frozen Construction validation images with 98 annotated violations. The static operating detection threshold was 0.25; a second-expert cascade was evaluated with exactly the **same operational class-aware joint NMS fusion** as the always-both reference.

The primary-only routing score is `uncertainty=1-max(safety_class_confidence)` computed from low-confidence primary predictions (0.001); no safety prediction yields uncertainty 1. At exploratory score cutoff 0.50, run second expert if `uncertainty>=0.50`. Router sees **no ground truth or secondary outputs**. All safety TP and FP counts below use the one-to-one object-level GT matching IoU>=0.50 and a joint NMS IoU=0.70.

| Seed | Primary | Safety TP primary-only | Safety TP always-joint | Escalated images / 132 | Safety TP selective | Selective FP | Matched-invocation random-routing **expected** TP |
|---|---|---:|---:|---:|---:|---:|---:|
| 17 | Y-PPE | 8 | 20 | 92 | 11 | 90 | 16.36 |
| 17 | Construction | 13 | 20 | 131 | 19 | 106 | 19.95 |
| 42 | Y-PPE | 10 | 47 | 94 | 21 | 92 | 36.35 |
| 42 | Construction | 40 | 47 | 116 | 42 | 125 | 46.15 |
| 2026 | Y-PPE | 10 | 27 | 79 | 18 | 121 | 20.17 |
| 2026 | Construction | 21 | 27 | 116 | 24 | 110 | 26.27 |

The random-policy comparator is the mathematically expected TP count if the second expert were invoked with the **same per-image marginal probability** as observed under the heuristic, independently of content: `(1-r)*TP_primary+r*TP_always_joint`. It is NOT the result of multiple sampled random policies and provides **no statistical significance** by itself.

The fixed confidence heuristic produces fewer matched objects than this matched-rate expectation for **every** seed/direction in this diagnostic. The Construction-primary direction especially requires secondary calls on 88–99% of frames to approximate joint recall, which is already far below a defensible field-safety level. The proxy `1+secondary_rate` counts **expert executions**, not latency, power, CO2e or joules.

The finding is a **NO-GO for the specific confidence-only routing heuristic** under tested conditions. It does **not** exclude more informative or independently evaluated routing strategies, other checkpoint policies or thresholds. Its threshold was exploratory, and the same development data must not be mined retrospectively for a favorable post hoc submission claim. Do not use held-out test splits to select or repair a router. The associated best.pt Construction sensitivity is documented in `BEST_PT_CONSTRUCTION_THREE_SEEDS_VALIDATION_2026-10-18.md`.
