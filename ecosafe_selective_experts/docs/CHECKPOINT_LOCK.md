# Primary Checkpoint Lock

These SHA-256 values were computed from the immutable Stage 5 final-epoch `last.pt` files retrieved from connected external storage. Large binary checkpoints remain outside the public Git repository.

| Run ID | Bytes | SHA-256 |
|---|---:|---|
| Y_YOLO_s17 | 40,534,380 | `b5c54704553a6bbc900b8ac37735ee1040025a3c685dcd3717c4490d107bbee5` |
| Y_YOLO_s42 | 40,534,380 | `3ec0b396ae344361a9e000683891aa88dd92ef9a6edff07829243f95bf6eaf64` |
| Y_YOLO_s2026 | 40,534,572 | `c1ab6209e26aa461ef2833889c85d8edb8ffac6de70348117b0923b80939c23e` |
| C_YOLO_s17 | 40,515,820 | `daef1d3841af76e0d3c801f8fd7a41d4713e465617b09b2e18d5fe67e5eb46c4` |
| C_YOLO_s42 | 40,515,820 | `868b533722848a6885909391daabf52d7bd189cca4fc1e8d82fbe0f4c03869a1` |
| C_YOLO_s2026 | 40,515,884 | `f1f160d2f1e84b8641872adb01d10b6c9d3b736a53b7ec5775333eef30f88bb1` |

## Policy

- These six hashes define the primary detector evidence for the selective-expert study.
- No detector retraining or silent checkpoint substitution is allowed.
- If a file fails its hash check, execution must stop.
- Validation-selected `best.pt` checkpoints are sensitivity assets, not replacements for the primary `last.pt` policy.
