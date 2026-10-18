# EcoSafe — independent verification of six frozen last.pt checkpoints

**Verification date:** 2026-10-17. **Status:** Complete for artifact existence, exact byte size and SHA-256; no inference or retraining from the four newly downloaded seeds implied.

The six original completed Stage 5 YOLO11m model files were retrieved from connected Stage5_Baselines Google Drive storage and independently hashed in local execution. They match the previously frozen `CHECKPOINT_LOCK.md` values.

| Run ID | Checked byte size | SHA-256 verification |
|---|---:|---|
| Y_YOLO_s17 | 40,534,380 | PASS — `b5c54704553a6bbc900b8ac37735ee1040025a3c685dcd3717c4490d107bbee5` |
| Y_YOLO_s42 | 40,534,380 | PASS — `3ec0b396ae344361a9e000683891aa88dd92ef9a6edff07829243f95bf6eaf64` |
| Y_YOLO_s2026 | 40,534,572 | PASS — `c1ab6209e26aa461ef2833889c85d8edb8ffac6de70348117b0923b80939c23e` |
| C_YOLO_s17 | 40,515,820 | PASS — `daef1d3841af76e0d3c801f8fd7a41d4713e465617b09b2e18d5fe67e5eb46c4` |
| C_YOLO_s42 | 40,515,820 | PASS — `868b533722848a6885909391daabf52d7bd189cca4fc1e8d82fbe0f4c03869a1` |
| C_YOLO_s2026 | 40,515,884 | PASS — `f1f160d2f1e84b8641872adb01d10b6c9d3b736a53b7ec5775333eef30f88bb1` |

The verification is a file-integrity check only: it does **not** show that all six have run successfully on both domains. The completed exploratory inference remains seed 17 on Construction validation. The Y-PPE validation seed-17 export and subsequent multi-seed experiments are independent milestones, with strict provenance and no held-out test exposure.

The immutable validation-only dataset ZIP had SHA-256 `5337fb80a7e74bbb56ebed497d56f129d5020efff1c36540d74095f2823ae1d7` and its two internal validation manifests matched the original frozen manifest fingerprints. Never upload binary weights or identifiable construction images to public GitHub.

**Research integrity:** no model re-training, new training seed, or CO2/energy benefit can be inferred from these checks.