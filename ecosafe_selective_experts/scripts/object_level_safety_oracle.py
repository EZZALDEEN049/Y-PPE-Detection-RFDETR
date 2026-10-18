#!/usr/bin/env python3
"""CPU-only object-level safety complementarity preflight.

This is a maximum-cardinality, class-aware *oracle* for concatenating two
detector outputs. No retraining, no real predictions, and NO production fusion
or NMS claim. Used to test whether the old FN-count-difference recovery target
can be misleading. Frozen violation class IDs: 6, 7, 8.
"""
from __future__ import annotations
import math
from typing import Iterable

SAFETY = {6, 7, 8}


def _box(item: dict) -> tuple[float, float, float, float]:
    try:
        b = tuple(float(x) for x in item["box"])
        cid = item["class_id"]
    except (KeyError, ValueError, TypeError) as exc:
        raise ValueError("Each detection needs numeric box and integer class_id") from exc
    if type(cid) is not int or cid < 0 or len(b) != 4 or not all(math.isfinite(v) for v in b):
        raise ValueError("Bad class ID or box")
    if not (0 <= b[0] < b[2] <= 1 and 0 <= b[1] < b[3] <= 1):
        raise ValueError("Boxes must use normalized xyxy in [0,1] with positive area")
    return b


def iou(a, b) -> float:
    ax1, ay1, ax2, ay2 = _box({"class_id": 0, "box": a})
    bx1, by1, bx2, by2 = _box({"class_id": 0, "box": b})
    w = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    h = max(0.0, min(ay2, by2) - max(ay1, by1))
    overlap = w * h
    area_a = (ax2 - ax1) * (ay2 - ay1)
    area_b = (bx2 - bx1) * (by2 - by1)
    denom = area_a + area_b - overlap
    return overlap / denom if denom else 0.0


def matched_gt_indices(gt: Iterable[dict], preds: Iterable[dict], threshold=0.50) -> set[int]:
    """Deterministic maximum-cardinality bipartite matching of safety objects.

    GT and prediction class IDs must agree and IoU must exceed threshold.
    This avoids greedily selecting a large IoU edge that blocks two recoveries.
    """
    if not (0 < threshold <= 1):
        raise ValueError("IoU threshold must be in (0,1]")
    g = list(gt)
    p = list(preds)
    for item in g + p:
        _box(item)
    neighbors = []
    for gi, obj in enumerate(g):
        if obj["class_id"] not in SAFETY:
            neighbors.append([])
            continue
        adj = []
        for pi, det in enumerate(p):
            if det["class_id"] != obj["class_id"]:
                continue
            overlap = iou(obj["box"], det["box"])
            if overlap >= threshold:
                adj.append((pi, overlap))
        neighbors.append([pi for pi, _ in sorted(adj, key=lambda e: (-e[1], e[0]))])

    matched_prediction_to_gt = {}
    def visit(gi, seen):
        for pi in neighbors[gi]:
            if pi in seen:
                continue
            seen.add(pi)
            if pi not in matched_prediction_to_gt or visit(matched_prediction_to_gt[pi], seen):
                matched_prediction_to_gt[pi] = gi
                return True
        return False

    for gi in range(len(g)):
        visit(gi, set())
    return set(matched_prediction_to_gt.values())


def frame_oracle(gt: Iterable[dict], primary: Iterable[dict], secondary: Iterable[dict], threshold=0.50) -> dict:
    """Returns safety FN/TP and object-level recovery, not a deployed fusion score."""
    g, p, s = list(gt), list(primary), list(secondary)
    total = sum(x.get("class_id") in SAFETY for x in g)
    gp = matched_gt_indices(g, p, threshold)
    gs = matched_gt_indices(g, s, threshold)
    gu = matched_gt_indices(g, p + s, threshold)
    pfn, sfn, ufn = (total - len(a) for a in (gp, gs, gu))
    assert ufn <= pfn and ufn <= sfn, "Maximum matching monotonicity violation"
    return {
        "gt_safety_objects": total,
        "primary_tp": len(gp), "primary_fn": pfn,
        "secondary_tp": len(gs), "secondary_fn": sfn,
        "concat_oracle_tp": len(gu), "concat_oracle_fn": ufn,
        "object_recovery_vs_primary_count": pfn - ufn,
        "secondary_exclusively_recovers_primary_missed_objects": len(gs - gp),
        "legacy_recovery_by_fn_count_difference": max(0, pfn - sfn),
        "routing_recovery_positive": int(ufn < pfn),
        "comparison_policy": "concat_predictions_maximum_cardinality_matching_oracle",
        "actual_merged_operational_predictions_evaluated": False,
    }
