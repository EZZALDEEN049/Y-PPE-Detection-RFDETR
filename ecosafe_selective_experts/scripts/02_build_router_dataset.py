#!/usr/bin/env python3
"""Build development-only selective-routing labels from frozen expert predictions.

The script does not train a router and must not be pointed at a held-out test split
when its output will be used for model/threshold selection.

Predictions are exported at low confidence for reproducibility, then filtered here
at a frozen operating-confidence threshold before safety TP/FN matching.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

SAFETY_CLASS_IDS = {6, 7, 8}


def iou(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    aa = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    bb = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    den = aa + bb - inter
    return inter / den if den > 0 else 0.0


def read_detections(path, operating_conf):
    by_image = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            confidence = float(r["confidence"])
            if confidence < operating_conf:
                continue
            by_image[r["image_name"]].append({
                "class_id": int(r["class_id"]),
                "confidence": confidence,
                "box": tuple(float(r[k]) for k in ("x1n", "y1n", "x2n", "y2n")),
            })
    return by_image


def read_frames(path):
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[r["image_name"]] = r
    return out


def read_gt(label_path):
    gt = []
    if not label_path.exists():
        return gt
    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) < 5:
            continue
        cid = int(float(parts[0]))
        cx, cy, w, h = map(float, parts[1:5])
        gt.append({
            "class_id": cid,
            "box": (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2),
        })
    return gt


def safety_counts(gt, pred, threshold):
    """Global greedy, class-aware one-to-one matching sorted by IoU."""
    gt_s = [g for g in gt if g["class_id"] in SAFETY_CLASS_IDS]
    pred_s = [p for p in pred if p["class_id"] in SAFETY_CLASS_IDS]

    candidates = []
    for gi, g in enumerate(gt_s):
        for pi, p in enumerate(pred_s):
            if p["class_id"] != g["class_id"]:
                continue
            overlap = iou(g["box"], p["box"])
            if overlap >= threshold:
                candidates.append((overlap, gi, pi))

    candidates.sort(reverse=True)
    used_gt, used_pred = set(), set()
    for _, gi, pi in candidates:
        if gi in used_gt or pi in used_pred:
            continue
        used_gt.add(gi)
        used_pred.add(pi)

    tp = len(used_gt)
    fn = len(gt_s) - tp
    fp = len(pred_s) - len(used_pred)
    return fn, tp, fp, len(gt_s)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--primary-detections", required=True)
    p.add_argument("--primary-frames", required=True)
    p.add_argument("--secondary-detections", required=True)
    p.add_argument("--labels-dir", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--operating-conf", type=float, default=0.25)
    p.add_argument("--match-iou", type=float, default=0.50)
    args = p.parse_args()

    primary = read_detections(args.primary_detections, args.operating_conf)
    secondary = read_detections(args.secondary_detections, args.operating_conf)
    frames = read_frames(args.primary_frames)
    labels_dir = Path(args.labels_dir)

    fields = [
        "image_name", "n_detections", "max_confidence", "mean_confidence",
        "min_confidence", "p10_confidence", "safety_max_confidence",
        "safety_detection_count", "gt_safety_objects", "primary_safety_tp",
        "primary_safety_fp", "primary_safety_fn", "secondary_safety_tp",
        "secondary_safety_fp", "secondary_safety_fn", "recovery_count",
        "second_expert_recovers_primary_safety_fn"
    ]

    rows = []
    for image_name, fr in sorted(frames.items()):
        stem = Path(image_name).stem
        gt = read_gt(labels_dir / f"{stem}.txt")
        p_fn, p_tp, p_fp, n_gt = safety_counts(
            gt, primary.get(image_name, []), args.match_iou
        )
        s_fn, s_tp, s_fp, _ = safety_counts(
            gt, secondary.get(image_name, []), args.match_iou
        )
        recovery = max(0, p_fn - s_fn)
        rows.append({
            "image_name": image_name,
            "n_detections": fr["n_detections"],
            "max_confidence": fr["max_confidence"],
            "mean_confidence": fr["mean_confidence"],
            "min_confidence": fr["min_confidence"],
            "p10_confidence": fr["p10_confidence"],
            "safety_max_confidence": fr["safety_max_confidence"],
            "safety_detection_count": fr["safety_detection_count"],
            "gt_safety_objects": n_gt,
            "primary_safety_tp": p_tp,
            "primary_safety_fp": p_fp,
            "primary_safety_fn": p_fn,
            "secondary_safety_tp": s_tp,
            "secondary_safety_fp": s_fp,
            "secondary_safety_fn": s_fn,
            "recovery_count": recovery,
            "second_expert_recovers_primary_safety_fn": int(recovery > 0),
        })

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    positive = sum(int(r["second_expert_recovers_primary_safety_fn"]) for r in rows)
    print(
        f"ROUTER_DATASET_COMPLETE frames={len(rows)} recovery_positive={positive} "
        f"operating_conf={args.operating_conf:.3f} match_iou={args.match_iou:.3f}"
    )
    print(out)


if __name__ == "__main__":
    main()
