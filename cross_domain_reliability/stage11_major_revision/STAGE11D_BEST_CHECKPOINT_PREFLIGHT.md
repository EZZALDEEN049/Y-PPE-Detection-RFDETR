# Stage 11D — best.pt Preflight Verification

**Date:** 2026-10-09  
**Status:** CHECKPOINTS VERIFIED; held-out sensitivity inference still pending.

The six validation-selected `best.pt` checkpoints were verified in the existing completed Stage 5 run directories. No retraining is required.

| Run | Source | Seed | best.pt bytes | Validation epoch with maximum recorded mAP50:95 | Best validation mAP50:95 | Epoch 100 validation mAP50:95 |
|---|---|---:|---:|---:|---:|---:|
| Y_YOLO_s17 | Y-PPE | 17 | 40,534,380 | 54 | 0.27881 | 0.25961 |
| Y_YOLO_s42 | Y-PPE | 42 | 40,534,380 | 38 | 0.27847 | 0.24846 |
| Y_YOLO_s2026 | Y-PPE | 2026 | 40,534,444 | 35 | 0.27379 | 0.25060 |
| C_YOLO_s17 | Construction-PPE | 17 | 40,515,820 | 9 | 0.26288 | 0.23670 |
| C_YOLO_s42 | Construction-PPE | 42 | 40,515,820 | 12 | 0.26626 | 0.23474 |
| C_YOLO_s2026 | Construction-PPE | 2026 | 40,515,884 | 15 | 0.25313 | 0.22959 |

## Interpretation before held-out evaluation

The validation-selected checkpoints are materially earlier than epoch 100 in all six runs, especially for Construction-PPE. Therefore the reviewer-requested checkpoint-policy sensitivity is scientifically meaningful rather than a cosmetic re-evaluation.

These validation results **must not** be used as a substitute for the held-out Stage 11D results. They only verify that:
1. the six best.pt files exist;
2. validation selection differs from the primary final-epoch policy; and
3. Stage 11D remains necessary to determine whether the external-domain gap is robust to checkpoint policy.

No held-out best.pt result is inferred from validation performance.

## Drive checkpoint identities

- Y_YOLO_s17 best.pt — Drive ID `1XYuBUM4vmADHyYXTC5Y5ldptWoVnFuDo`
- Y_YOLO_s42 best.pt — Drive ID `1khxb0NtOoxzbjDUNXuchf26rwI6FabwE`
- Y_YOLO_s2026 best.pt — Drive ID `1x4N4rXHCf1kqjVg0Bu3ezowZS8StuS6f`
- C_YOLO_s17 best.pt — Drive ID `1cVbAMDpbA27thU-EBkTUBpYWsgqlOf37`
- C_YOLO_s42 best.pt — Drive ID `1p7Fqp0fL-EmYxwBRfu3gp-NhsR-ABZNM`
- C_YOLO_s2026 best.pt — Drive ID `1Jzjxmi_vXD2gk5_6y1HBnrbMZPcUilpo`

The held-out Stage 11D protocol remains exactly as frozen: same test sets, same evaluation thresholds, same image size, no TTA, no target adaptation, and no test-informed checkpoint selection.
