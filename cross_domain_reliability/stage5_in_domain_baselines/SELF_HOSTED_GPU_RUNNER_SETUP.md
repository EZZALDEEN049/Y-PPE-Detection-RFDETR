# Stage 5 Dedicated GPU + GitHub Self-Hosted Runner Setup

**Purpose:** connect one dedicated NVIDIA GPU machine to this repository so Stage 5 can run under GitHub Actions while preserving the frozen experiment protocol.

## Recommended execution profile

Use one persistent/on-demand Linux x64 GPU machine with:

- exactly one visible NVIDIA GPU;
- at least 15 GB VRAM; 24 GB or more is preferred for headroom;
- NVIDIA driver installed and `nvidia-smi` working;
- Python 3.11 available;
- enough local disk for the two frozen derivatives, pretrained weights, checkpoints, logs, and artifacts;
- no spot/preemptible mode for the primary 100-epoch runs unless checkpoint-resume behavior is separately frozen before execution.

A RunPod GPU Pod is a suitable example, but any dedicated NVIDIA GPU VM/server that satisfies the same gates may be used.

## Security rule for this repository

This repository is public. A self-hosted runner attached to a public repository must not execute untrusted pull-request code. Stage 5 workflows are therefore manual `workflow_dispatch` workflows only. Do not enable automatic `pull_request` execution on the GPU runner.

Do not paste the runner registration token, Roboflow API key, provider credentials, SSH private keys, or other secrets into repository files, issues, logs, or chat messages.

## One-time GitHub runner registration

1. Create/start the GPU machine and open a shell on it.
2. Confirm `nvidia-smi` works.
3. In GitHub open this repository, then:
   `Settings -> Actions -> Runners -> New self-hosted runner`.
4. Select **Linux** and **x64**.
5. GitHub will display the current runner download/configuration commands and a short-lived registration token. Run exactly those commands on the GPU machine.
6. During configuration assign the custom labels:
   `gpu,stage5`
   in addition to the default `self-hosted`, `linux`, and `x64` labels.
7. Start the runner and keep the process/service active while Stage 5 workflows are running.
8. Back in GitHub, verify the runner appears **Idle** and has all labels:
   `self-hosted`, `linux`, `x64`, `gpu`, `stage5`.

## First scientific gate after registration

Run the manual workflow:

`.github/workflows/stage5-self-hosted-gpu-hardware-preflight.yml`

The workflow must pass before any package freeze or model training. It checks:

- exactly one NVIDIA GPU is visible;
- VRAM is at least 15,000 MiB;
- GPU model, UUID, driver, and total VRAM are recorded;
- runner identity is captured;
- no dataset is accessed;
- no model is trained;
- no validation or test image is touched.

The evidence artifact is named:

`stage5-self-hosted-gpu-hardware-preflight`

## What happens only after hardware PASS

The hardware evidence will be used to freeze, before the first full training run:

- exact Python/PyTorch/CUDA/Ultralytics/RF-DETR versions;
- physical batch size for YOLO11m;
- physical batch size and gradient accumulation for RF-DETR Small;
- worker count;
- mixed-precision policy;
- RF-DETR final raw-vs-EMA checkpoint policy;
- persistent output/checkpoint paths.

Only after that execution lock is committed may the 12-run baseline matrix begin.

## Frozen scientific controls that do not change with hardware

- datasets: Y-PPE-h9 and Construction-PPE-h9 frozen Stage 4 derivatives;
- input resolution: 640 x 640;
- epochs: 100;
- seeds: 17, 42, 2026;
- models: YOLO11m and RF-DETR Small;
- no offline augmentation;
- primary controlled comparison disables stochastic online augmentation;
- no early stopping;
- held-out test is not used for tuning/checkpoint selection;
- primary checkpoint policy is final epoch, subject only to the pre-frozen RF-DETR raw-vs-EMA weight interpretation.
