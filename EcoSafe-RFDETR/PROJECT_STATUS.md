# EcoSafe-RFDETR Status

## Completed before GPU execution
- Research problem, gap, innovation, RQs and hypotheses
- Adaptive architecture and safety-energy objective
- Public dataset strategy and data-lock protocol
- Dataset audit + deduplication utilities
- YOLO-to-COCO and VOC-to-COCO conversion
- RF-DETR training launcher
- Per-image inference extraction
- NVML energy benchmark
- Per-class TP/FP/FN matching
- Oracle escalation labels
- Pilot GO/MODIFY/NO-GO logic
- Post-hoc confidence calibration utility
- Logistic routing utility

## Empirical work still requires an NVIDIA GPU
RF-DETR fine-tuning, real J/frame measurement, router training on real outputs, external evaluation, and final Results/Discussion must be run on the independent GPU environment.
