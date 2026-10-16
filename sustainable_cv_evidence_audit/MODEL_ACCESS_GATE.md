# Stage 3 preflight: availability of the already-trained models

**Status:** model/version identifiers documented; no independent local model
download or fine-tuned-weight execution demonstrated in this workstream.

## Trained-model tracks

- YOLO11m: altayyar-0oflt-lafos-qqauz-ty5nh/1
  https://universe.roboflow.com/master-fylfq/altayyar-0oflt-lafos-qqauz-ty5nh
- RF-DETR Small: altayyar-0oflt-lafos-qqauz/2
  https://universe.roboflow.com/softyyemen/altayyar-0oflt-lafos-qqauz

Do not replace the model IDs with stock COCO-pretrained YOLO or RF-DETR weights.
Those are NOT the same Y-PPE fine-tuned models and would answer a different
research question. Never start retraining without first evaluating the existing
options and documenting the methodological change.

## Official platform paths to investigate

Roboflow Inference documentation supports self-hosted execution of supported
fine-tuned models. A workspace/account and model-specific access rights may be
required, and local compatibility can vary with architecture/device/runtime.
Official overview:
https://inference.roboflow.com/quickstart/roboflow_ecosystem/

Official model-weight export guidance and supported-model compatibility
must be checked for the specific trained versions; an available generic
download button or generic RF-DETR pretrained checkpoint is not evidence
that these specific trained weights are accessible.

https://docs.roboflow.com/
https://rfdetr.roboflow.com/

## Gate 1 — identity, rights, access

Record privately per track:
- exact project, workspace, model ID and dataset version;
- permission to run research inference and to use model weights;
- evidence of access to actual fine-tuned model artifacts OR successful
  self-hosted Inference model download on the intended device;
- immutable model checkpoint hash if an actual file is available;
- exact class order/ontology and preprocessing as deployed;
- tool versions, model runtime/backend, device and resolution;
- controlled inference output on a non-sensitive test image.

Only when BOTH models pass on the SAME target hardware can a matched local
inference comparison be prepared. A hosted web/API call does not establish
local model compute time, local power use or true offline capability.

## Gate 2 — no-training measurement plan (future)

- Independent source-disjoint common held-out images, lawful to evaluate.
- Model loading and initialization measured separately from warm steady-state.
- Batch size 1 and matched input resolution as primary edge use case.
- Repeated interleaved inference with fixed ordering/randomized blocks,
  fixed concurrent load, warm-up and OS power profile.
- Median and p95 per-image end-to-end and model-only latency where possible.
- Peak RAM and, if applicable, VRAM by the same documented tools.
- Watts/Joules using calibrated system/instrument measurement. Report
  idle baseline and component/system boundary, runs, units and uncertainty.
- Only estimate CO2e if emission factor, location, measurement time and
  system boundary are documented.
- Paired, image-level accuracy/false-negative comparison only after the
  common test/label/evaluator protocol is frozen.

## Security and integrity

Never commit a Roboflow API key, private Roboflow response, downloaded
weights, or personally identifiable worksite images. Store credentials only
as local environment variables or an appropriate secret manager; do not
paste them in issues, logs or chat. The current GitHub CPU tests are a
software preflight, not an experiment measuring performance.
