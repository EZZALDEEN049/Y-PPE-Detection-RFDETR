#!/usr/bin/env python3
"""Export deterministic per-detection and per-frame evidence from a frozen YOLO checkpoint."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np
from ultralytics import YOLO

SAFETY_CLASS_IDS = {6, 7, 8}


def finite(values):
    return [float(v) for v in values if math.isfinite(float(v))]


def q(values, quantile, default=0.0):
    vals = finite(values)
    return float(np.quantile(vals, quantile)) if vals else float(default)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--weights", required=True)
    p.add_argument("--source", required=True, help="Image directory, glob, txt list, or other Ultralytics source")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--test-domain", required=True, choices=["y", "c"])
    p.add_argument("--device", default="0")
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--conf", type=float, default=0.001)
    p.add_argument("--iou", type=float, default=0.70)
    args = p.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    det_path = out / f"{args.run_id}__TEST_{args.test_domain.upper()}__detections.csv"
    frame_path = out / f"{args.run_id}__TEST_{args.test_domain.upper()}__frames.csv"

    model = YOLO(args.weights)
    names = model.names

    det_fields = [
        "run_id", "test_domain", "image_path", "image_name", "class_id", "class_name",
        "confidence", "x1n", "y1n", "x2n", "y2n"
    ]
    frame_fields = [
        "run_id", "test_domain", "image_path", "image_name", "n_detections",
        "max_confidence", "mean_confidence", "min_confidence", "p10_confidence",
        "safety_max_confidence", "safety_detection_count"
    ]

    n_frames = 0
    n_dets = 0
    with det_path.open("w", newline="", encoding="utf-8") as fdet, frame_path.open(
        "w", newline="", encoding="utf-8"
    ) as fframe:
        dw = csv.DictWriter(fdet, fieldnames=det_fields)
        fw = csv.DictWriter(fframe, fieldnames=frame_fields)
        dw.writeheader()
        fw.writeheader()

        results = model.predict(
            source=args.source,
            imgsz=args.imgsz,
            conf=args.conf,
            iou=args.iou,
            device=args.device,
            stream=True,
            verbose=False,
            save=False,
        )

        for res in results:
            n_frames += 1
            image_path = str(Path(res.path))
            image_name = Path(res.path).name
            h, w = res.orig_shape
            confs = []
            safety_confs = []

            boxes = res.boxes
            if boxes is not None and len(boxes):
                xyxy = boxes.xyxy.detach().cpu().numpy()
                cls = boxes.cls.detach().cpu().numpy().astype(int)
                conf = boxes.conf.detach().cpu().numpy()

                for box, cid, score in zip(xyxy, cls, conf):
                    score = float(score)
                    confs.append(score)
                    if int(cid) in SAFETY_CLASS_IDS:
                        safety_confs.append(score)
                    x1, y1, x2, y2 = map(float, box.tolist())
                    dw.writerow({
                        "run_id": args.run_id,
                        "test_domain": args.test_domain,
                        "image_path": image_path,
                        "image_name": image_name,
                        "class_id": int(cid),
                        "class_name": names.get(int(cid), str(int(cid))) if isinstance(names, dict) else names[int(cid)],
                        "confidence": score,
                        "x1n": x1 / w,
                        "y1n": y1 / h,
                        "x2n": x2 / w,
                        "y2n": y2 / h,
                    })
                    n_dets += 1

            fw.writerow({
                "run_id": args.run_id,
                "test_domain": args.test_domain,
                "image_path": image_path,
                "image_name": image_name,
                "n_detections": len(confs),
                "max_confidence": max(confs) if confs else 0.0,
                "mean_confidence": float(np.mean(confs)) if confs else 0.0,
                "min_confidence": min(confs) if confs else 0.0,
                "p10_confidence": q(confs, 0.10),
                "safety_max_confidence": max(safety_confs) if safety_confs else 0.0,
                "safety_detection_count": len(safety_confs),
            })

    print(f"EXPORT_COMPLETE frames={n_frames} detections={n_dets}")
    print(det_path)
    print(frame_path)


if __name__ == "__main__":
    main()
