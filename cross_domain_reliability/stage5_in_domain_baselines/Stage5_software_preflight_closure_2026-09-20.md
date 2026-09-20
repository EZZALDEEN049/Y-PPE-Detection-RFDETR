# Stage 5 Software/API Preflight — Closure

**Date:** 2026-09-20  
**Status:** SOFTWARE/API PREFLIGHT PASSED. GPU EXECUTION GATE REMAINS OPEN.  
**Successful GitHub Actions run:** `35477445347` (`Stage 5 Baseline Training Preflight #1`)  
**Head commit used by the run:** `c634f538d9095a389231731a295eda9746acbd5e`

## What was verified

The preflight completed successfully without model training and without held-out test evaluation.

Verified items:

- all Stage 5 training/materialization/layout-adapter scripts compiled;
- the frozen 12-run matrix contains 2 datasets x 2 architectures x 3 seeds;
- seeds are fixed to `17, 42, 2026`;
- controlled input resolution is fixed to `640`;
- both Stage 4 dataset fingerprints are checked in the experiment matrix;
- RF-DETR Small structural block size is 32, so 640 is a valid controlled resolution;
- expected current RF-DETR training configuration fields are available;
- expected Ultralytics training/augmentation configuration fields are available;
- the Stage-4-to-RF-DETR layout adapter preserves the synthetic manifest fingerprint and is accepted by the installed RF-DETR YOLO dataset validator;
- no dataset content or split membership was changed by the adapter.

## Candidate software stack observed in the successful CI preflight

- Python: `3.11.16`
- PyTorch: `2.14.0+cu130`
- CUDA runtime bundled with PyTorch: `13.0`
- torchvision: `0.29.0`
- Ultralytics: `8.4.156`
- RF-DETR package installed by pip: `1.10.1`
- PyYAML: `6.0.3`
- NumPy after dependency resolution: `2.3.5`

The RF-DETR package did not expose a useful `__version__` attribute in the Python namespace, so the package version is taken from the successful pip installation record (`rfdetr-1.10.1`).

## Important limitation of this preflight

The GitHub-hosted `ubuntu-latest` runner used for this preflight reported:

`torch.cuda.is_available() == False`

Therefore this run validates software/API compatibility only. It does **not** validate real NVIDIA GPU execution, VRAM sufficiency, mixed precision behavior, achievable physical batch size, gradient accumulation, throughput, or RF-DETR final raw-vs-EMA evaluation policy.

No full Stage 5 baseline training may begin until those GPU-dependent parameters are measured and frozen before inspecting any held-out test result.

## Next gate

Run `gpu_preflight.py` on the intended NVIDIA GPU execution environment. The resulting JSON must be archived before the first full baseline run. After GPU preflight, freeze per architecture:

- GPU model and VRAM;
- NVIDIA driver;
- CUDA availability/runtime;
- physical batch size;
- gradient accumulation;
- effective batch size;
- worker count;
- AMP/bfloat16 policy;
- RF-DETR final raw-vs-EMA primary evaluation policy;
- final software versions used for all 12 Stage 5 runs.

The same locked execution policy must then be used across Y-PPE-h9 and Construction-PPE-h9 for a given architecture.
