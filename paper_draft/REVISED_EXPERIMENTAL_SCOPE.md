# Revised Experimental Scope

The initial Stage 5 plan considered two datasets, two detector architectures, and three seeds per setting. Only the six YOLO11m runs were completed reliably and are included in the final held-out analysis. Incomplete RF-DETR runs are excluded from all reported results.

The final study therefore uses a YOLO11m-only, multi-seed, bidirectional cross-domain reliability design with two harmonized PPE datasets and three seeds per source domain. Each completed final-epoch checkpoint is evaluated in-domain and on the alternate held-out domain, producing 12 frozen evaluation cells.

A manuscript-safe transparency statement is:

> The initial experimental plan included a second detector architecture; however, incomplete runs were excluded before the final held-out analysis. The reported study therefore focuses on the six fully completed YOLO11m runs and evaluates cross-domain reliability across two datasets and three random seeds per source domain.

This design supports claims about reproducible cross-domain degradation, seed robustness, safety-class failure, and dataset-side associations with class support and object scale. It does not support claims about architecture superiority, architecture-independent generalization, or a single confirmed causal mechanism for the observed failures.