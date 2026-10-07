# Reproducibility Manifest

## Datasets
Y-PPE-h9-v2
- train: 1,236
- validation: 356
- test: 186
- retained instances: 9,471
- SHA-256 fingerprint: 82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8

Construction-PPE-h9-v2
- train: 1,046
- validation: 132
- test: 138
- retained instances: 9,514
- SHA-256 fingerprint: 59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14

## Shared class order
person, helmet, gloves, vest, boots, goggles, no_helmet, no_gloves, no_boots

## Training
- model: YOLO11m
- pretrained checkpoint: yolo11m.pt
- epochs: 100
- image size: 640
- batch: 8
- workers: 2
- seeds: 17, 42, 2026
- AMP: enabled
- online stochastic augmentation: disabled
- early stopping: disabled
- primary checkpoint: last.pt
- hardware: NVIDIA Tesla T4
- Python: 3.13.15
- PyTorch: 2.11.0+cu128
- CUDA runtime: 12.8
- Ultralytics: 8.4.156

## Held-out evaluation
- AP confidence floor: 0.001
- fixed operating confidence: 0.25
- NMS IoU: 0.70
- class-matched IoU: 0.50
- image size: 640
- no test-time augmentation
- six completed models x two test domains = 12 evaluation cells

## Integrity
No target-domain fine-tuning, checkpoint reselection, or test-informed threshold tuning was performed after held-out evaluation began.
