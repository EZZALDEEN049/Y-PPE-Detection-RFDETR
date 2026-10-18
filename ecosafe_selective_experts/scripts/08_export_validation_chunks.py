#!/usr/bin/env python3
"""Frozen-checkpoint validation-only inference exporter, resumable in small chunks.

Reads immutable Stage 5 validation files and exact last.pt checkpoints.
No retraining, no test inference, no automatic upload; results stay private.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile

CHECKPOINTS = {
    "Y_YOLO_s17": ("b5c54704553a6bbc900b8ac37735ee1040025a3c685dcd3717c4490d107bbee5", 40534380),
    "Y_YOLO_s42": ("3ec0b396ae344361a9e000683891aa88dd92ef9a6edff07829243f95bf6eaf64", 40534380),
    "Y_YOLO_s2026": ("c1ab6209e26aa461ef2833889c85d8edb8ffac6de70348117b0923b80939c23e", 40534572),
    "C_YOLO_s17": ("daef1d3841af76e0d3c801f8fd7a41d4713e465617b09b2e18d5fe67e5eb46c4", 40515820),
    "C_YOLO_s42": ("868b533722848a6885909391daabf52d7bd189cca4fc1e8d82fbe0f4c03869a1", 40515820),
    "C_YOLO_s2026": ("f1f160d2f1e84b8641872adb01d10b6c9d3b736a53b7ec5775333eef30f88bb1", 40515884),
}
DOMAINS = {
    "y": ("Y-PPE-h9-v2", 356, "82c08766d5c5e50e93d41d21c4751fd686a3932ea6a8cb24ffd2838d9e30fba8"),
    "c": ("Construction-PPE-h9-v2", 132, "59469299ba67355dbcb0e725851f73d244a7ad6e93522d44601be3c8323d3c14"),
}
CLASSES = ("person", "helmet", "gloves", "vest", "boots", "goggles",
           "no_helmet", "no_gloves", "no_boots")
FIELDNAMES = ("image_name", "class_id", "confidence", "x1n", "y1n", "x2n", "y2n")


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def plan(validation_root: Path, domain: str, checkpoint: Path, model_id: str, chunk_size: int, chunk_index: int):
    if model_id not in CHECKPOINTS or domain not in DOMAINS:
        raise ValueError("Unknown frozen checkpoint or domain.")
    if not 1 <= chunk_size <= 32 or chunk_index < 0:
        raise ValueError("Chunk size must be 1..32; index must be >=0.")
    if checkpoint.name != "last.pt":
        raise ValueError("Frozen primary analysis requires last.pt, not best.pt.")
    expected_hash, expected_size = CHECKPOINTS[model_id]
    if not checkpoint.is_file() or checkpoint.stat().st_size != expected_size or sha256(checkpoint) != expected_hash:
        raise ValueError("FROZEN_CHECKPOINT_LOCK_FAILED")
    ds, expected_n, manifest_sha = DOMAINS[domain]
    dataset_root = validation_root / ds
    manifest = dataset_root / "manifest.jsonl"
    if not manifest.is_file() or sha256(manifest) != manifest_sha:
        raise ValueError("FROZEN_DATASET_MANIFEST_LOCK_FAILED")
    images = dataset_root / "images" / "val"
    labels = dataset_root / "labels" / "val"
    if not images.is_dir() or not labels.is_dir():
        raise ValueError("Expected validation-only image/label directories.")
    files = sorted(
        (p for p in images.iterdir() if p.is_file() and p.suffix.lower() in (".jpg",".jpeg",".png")),
        key=lambda x: x.name
    )
    if len(files) != expected_n or len({p.stem for p in files}) != expected_n:
        raise ValueError("Unexpected image count or ambiguous stems.")
    if any(not (labels / (p.stem + ".txt")).is_file() for p in files):
        raise ValueError("Validation labels missing.")
    offset = chunk_index * chunk_size
    if offset >= len(files):
        raise ValueError("Chunk index outside validation image partition.")
    selected = files[offset:offset + chunk_size]
    return {
        "model_id": model_id, "domain": domain, "expected_total_validation_images": expected_n,
        "chunk_index": chunk_index, "chunk_size": chunk_size,
        "start": offset, "end_exclusive": offset + len(selected),
        "expected_checkpoint_sha256": expected_hash, "frozen_manifest_sha256": manifest_sha,
        "images": selected
    }


def validate_detections(rows):
    for rec in rows:
        if not isinstance(rec["class_id"], int) or rec["class_id"] not in range(len(CLASSES)):
            raise ValueError("Detector class index invalid.")
        vals = [float(rec[x]) for x in ("confidence", "x1n", "y1n", "x2n", "y2n")]
        if not all(math.isfinite(x) for x in vals):
            raise ValueError("Non-finite detector value.")
        if not 0 <= vals[0] <= 1 or not (0 <= vals[1] < vals[3] <= 1 and 0 <= vals[2] < vals[4] <= 1):
            raise ValueError("Detector bounding box/confidence out of range.")


def write_private_result(out_dir: Path, spec: dict, frame_rows: list, detection_rows: list, runtime_version: str):
    """Atomic, overwrite-protected chunk. FRAME rows cover zero-detection images."""
    expected = [p.name for p in spec["images"]]
    observed = [x["image_name"] for x in frame_rows]
    if expected != observed:
        raise ValueError("Missing/reordered/duplicated inference frame.")
    if sum(int(x["n_detections"]) for x in frame_rows) != len(detection_rows):
        raise ValueError("Frame/detection counts disagree.")
    if any(r["image_name"] not in set(expected) for r in detection_rows):
        raise ValueError("Detection from unexpected image.")
    validate_detections(detection_rows)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f'{spec["model_id"]}__VAL_{spec["domain"].upper()}__chunk_{spec["chunk_index"]:03d}'
    targets = [out_dir/(stem+"_frames.csv"),out_dir/(stem+"_detections.csv"),out_dir/(stem+"_manifest.json")]
    if any(p.exists() for p in targets):
        raise FileExistsError("Refusing to overwrite previously exported inference chunks.")
    metadata = {
        key: spec[key] for key in (
            "model_id","domain","expected_total_validation_images","chunk_index","chunk_size",
            "start","end_exclusive","expected_checkpoint_sha256","frozen_manifest_sha256"
        )
    }
    metadata.update({
        "split": "validation_only", "model_retraining": False, "heldout_test_accessed": False,
        "imgsz": 640, "inference_confidence": 0.001, "nms_iou": 0.70,
        "runtime_ultralytics_version": runtime_version,
        "frames_exported": len(frame_rows), "raw_detections_exported": len(detection_rows),
        "latency_or_energy_benchmark": False,
        "scope": "private_model_predictions_not_for_public_repository",
    })
    temporaries = []
    try:
        for target, payload, fields in (
            (targets[0], frame_rows, ["image_name","n_detections"]),
            (targets[1], detection_rows, list(FIELDNAMES)),
        ):
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", dir=out_dir, delete=False) as handle:
                temporaries.append(Path(handle.name))
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(payload)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=out_dir, delete=False) as handle:
            temporaries.append(Path(handle.name))
            json.dump(metadata, handle, indent=2)
            handle.write("\n")
        for src, dst in zip(temporaries, targets):
            os.replace(src, dst)
    finally:
        for tmp in temporaries:
            tmp.unlink(missing_ok=True)
    return metadata


def infer(spec, checkpoint, device="cpu", threads=2):
    import torch
    import ultralytics
    from ultralytics import YOLO
    if ultralytics.__version__ != "8.4.156":
        raise ValueError("Frozen export tested only with Ultralytics 8.4.156.")
    torch.set_num_threads(threads)
    model = YOLO(str(checkpoint))
    if [model.names[i] for i in range(9)] != list(CLASSES):
        raise ValueError("Checkpoint class ontology does not match frozen class order.")
    image_list = [str(p) for p in spec["images"]]
    frames = []
    dets = []
    for idx, response in enumerate(model.predict(
        source=image_list, imgsz=640, conf=0.001, iou=0.70,
        device=device, batch=1, stream=True, verbose=False, save=False
    )):
        path_name = Path(response.path).name
        if idx >= len(spec["images"]) or path_name != spec["images"][idx].name:
            raise ValueError("Unmatched source image in model output.")
        height, width = response.orig_shape
        if height <= 0 or width <= 0:
            raise ValueError("Invalid inference input shape.")
        count = 0
        for xyxy, cls, conf in zip(
            response.boxes.xyxy.cpu().numpy(),
            response.boxes.cls.cpu().numpy(),
            response.boxes.conf.cpu().numpy()
        ):
            x1, y1, x2, y2 = map(float, xyxy)
            dets.append({
                "image_name": path_name, "class_id": int(cls), "confidence": float(conf),
                "x1n": x1/width, "y1n": y1/height, "x2n": x2/width, "y2n": y2/height
            })
            count += 1
        frames.append({"image_name": path_name, "n_detections": count})
    return frames, dets, ultralytics.__version__


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--validation-root", type=Path, required=True)
    ap.add_argument("--checkpoint", type=Path, required=True)
    ap.add_argument("--model-id", choices=tuple(CHECKPOINTS), required=True)
    ap.add_argument("--domain", choices=tuple(DOMAINS), required=True)
    ap.add_argument("--chunk-index", type=int, required=True)
    ap.add_argument("--chunk-size", type=int, default=16)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--cpu-threads", type=int, default=2)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if args.cpu_threads < 1 or args.cpu_threads > 16:
        ap.error("CPU threads must be in 1..16")
    try:
        spec = plan(args.validation_root, args.domain, args.checkpoint, args.model_id,
                    args.chunk_size, args.chunk_index)
        if args.dry_run:
            print(json.dumps({k: v for k, v in spec.items() if k != "images"}, indent=2))
            return
        # Never touch the test set or train/reselect a checkpoint.
        frames, dets, version = infer(spec, args.checkpoint, args.device, args.cpu_threads)
        manifest = write_private_result(args.out_dir, spec, frames, dets, version)
        print(json.dumps({
            "model_id": manifest["model_id"], "domain": manifest["domain"],
            "chunk_index": manifest["chunk_index"], "frames": manifest["frames_exported"],
            "raw_detections": manifest["raw_detections_exported"],
            "validation_only": True, "energy_measured": False
        }))
    except (OSError, ValueError) as exc:
        # Don't print private paths or class/image IDs in error messages.
        raise SystemExit("VALIDATION_EXPORT_BLOCKED: " + type(exc).__name__)


if __name__ == "__main__":
    main()
