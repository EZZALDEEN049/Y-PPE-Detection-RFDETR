"""Progressive, target-matched black-box XAI utilities for SEER-PPE V30.

The module is inference-backend agnostic. A caller supplies a real predictor
that maps an RGB uint8 image to Detection objects. A lost target has a defined
target score of zero; an ambiguous match is missing and blocks curve AUC.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Callable, Iterable, Literal, Sequence

import numpy as np
from PIL import Image, ImageFilter

from .detection_match import Detection, match_target

Direction = Literal["deletion", "insertion"]


@dataclass(frozen=True)
class OcclusionCell:
    row: int
    col: int
    status: str
    score_after: float | None
    score_drop: float | None
    matched_iou: float | None
    area_fraction: float


@dataclass(frozen=True)
class CurvePoint:
    direction: str
    ordering: str
    requested_fraction: float
    modified_fraction: float
    target_confidence: float | None
    normalized_score: float | None
    match_status: str
    matched_iou: float | None


def _validate_image(image: np.ndarray) -> np.ndarray:
    x = np.asarray(image)
    if x.ndim != 3 or x.shape[2] != 3 or x.dtype != np.uint8:
        raise ValueError("uint8 RGB image with shape HxWx3 required")
    if x.shape[0] < 1 or x.shape[1] < 1:
        raise ValueError("empty image")
    return x


def cell_bounds(height: int, width: int, rows: int, cols: int, row: int, col: int):
    if rows < 1 or cols < 1 or height < rows or width < cols:
        raise ValueError("invalid grid dimensions")
    if not (0 <= row < rows and 0 <= col < cols):
        raise ValueError("cell index outside grid")
    return row * height // rows, (row + 1) * height // rows, col * width // cols, (col + 1) * width // cols


def target_score(reference: Detection, predictions: Sequence[Detection], *,
                 minimum_iou: float = 0.50, ambiguity_margin: float = 0.03
                 ) -> tuple[float | None, str, float | None]:
    """Return fixed-target score, match status and IoU.

    A same-class unique match contributes its confidence. A LOST target has a
    target score of zero by definition (the target detection is absent).
    An AMBIGUOUS match is not assigned an arbitrary score and returns None.
    """
    result = match_target(reference, predictions, min_iou=minimum_iou,
                          ambiguity_margin=ambiguity_margin)
    if result.status == "MATCHED":
        return float(result.score_after), result.status, result.iou
    if result.status == "LOST":
        return 0.0, result.status, None
    return None, result.status, result.iou


def occlusion_importance_map(image: np.ndarray, reference: Detection,
                             predict: Callable[[np.ndarray], Sequence[Detection]], *,
                             rows: int = 8, cols: int = 8, fill_value: int = 127,
                             minimum_iou: float = 0.50,
                             ambiguity_margin: float = 0.03
                             ) -> tuple[np.ndarray, list[OcclusionCell]]:
    """Create a coarse grid importance map from single-cell occlusion drops.

    Positive values indicate a reduction in the frozen target's confidence.
    Negative values are retained but not prioritized. Lost targets score zero;
    ambiguous matches remain NaN and must not be silently imputed.
    """
    x = _validate_image(image)
    h, w = x.shape[:2]
    if rows < 1 or cols < 1 or h < rows or w < cols:
        raise ValueError("invalid occlusion grid")
    if not 0 <= fill_value <= 255:
        raise ValueError("fill_value must be an integer in [0,255]")
    importance = np.full((rows, cols), np.nan, dtype=np.float64)
    trials: list[OcclusionCell] = []
    for row in range(rows):
        for col in range(cols):
            top, bottom, left, right = cell_bounds(h, w, rows, cols, row, col)
            altered = x.copy()
            altered[top:bottom, left:right, :] = fill_value
            score_after, status, iou = target_score(
                reference, predict(altered), minimum_iou=minimum_iou,
                ambiguity_margin=ambiguity_margin)
            drop = None if score_after is None else float(reference.score - score_after)
            if drop is not None:
                importance[row, col] = drop
            area_fraction = ((bottom - top) * (right - left)) / float(h * w)
            trials.append(OcclusionCell(row, col, status, score_after, drop, iou, area_fraction))
    return importance, trials


def rank_grid_cells(importance: np.ndarray) -> list[tuple[int, int]]:
    """Rank cells by positive score drop; ties are resolved row-major."""
    a = np.asarray(importance, dtype=float)
    if a.ndim != 2 or not np.isfinite(a).all():
        raise ValueError("importance map must be finite; ambiguous cells block ranking")
    positive = np.maximum(a, 0.0)
    if float(positive.sum()) <= 0:
        raise ValueError("importance map has no positive target-score drop")
    cells = [(r, c) for r in range(a.shape[0]) for c in range(a.shape[1])]
    return sorted(cells, key=lambda cell: (-positive[cell], cell[0], cell[1]))


def stable_random_order(target_id: str, rows: int = 8, cols: int = 8) -> list[tuple[int, int]]:
    """Return a reproducible random cell order keyed by the frozen target ID."""
    if not target_id:
        raise ValueError("target_id is required for deterministic random control")
    seed = int.from_bytes(sha256(target_id.encode("utf-8")).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    cells = [(r, c) for r in range(rows) for c in range(cols)]
    return [cells[int(i)] for i in rng.permutation(len(cells))]


def gaussian_blur_baseline(image: np.ndarray, sigma: float | None = None) -> tuple[np.ndarray, float]:
    """Build a fixed blurred baseline; default sigma is 1% of the short edge."""
    x = _validate_image(image)
    if sigma is None:
        sigma = max(3.0, round(0.01 * min(x.shape[0], x.shape[1]), 3))
    if not np.isfinite(sigma) or sigma <= 0:
        raise ValueError("sigma must be a positive finite value")
    blurred = np.asarray(Image.fromarray(x).filter(ImageFilter.GaussianBlur(radius=float(sigma))),
                         dtype=np.uint8)
    return blurred, float(sigma)


def _selected_area_fraction(height: int, width: int, rows: int, cols: int,
                            selected: Iterable[tuple[int, int]]) -> float:
    area = 0
    for row, col in selected:
        top, bottom, left, right = cell_bounds(height, width, rows, cols, row, col)
        area += (bottom - top) * (right - left)
    return area / float(height * width)


def _alter_by_cells(image: np.ndarray, baseline: np.ndarray,
                    selected: Sequence[tuple[int, int]], *, rows: int, cols: int,
                    direction: Direction) -> np.ndarray:
    x = _validate_image(image)
    b = _validate_image(baseline)
    if x.shape != b.shape:
        raise ValueError("image and blurred baseline shapes must match")
    altered = x.copy() if direction == "deletion" else b.copy()
    source = b if direction == "deletion" else x
    for row, col in selected:
        top, bottom, left, right = cell_bounds(x.shape[0], x.shape[1], rows, cols, row, col)
        altered[top:bottom, left:right, :] = source[top:bottom, left:right, :]
    return altered


def progressive_curve(image: np.ndarray, blurred_baseline: np.ndarray,
                      reference: Detection,
                      predict: Callable[[np.ndarray], Sequence[Detection]],
                      order: Sequence[tuple[int, int]], *,
                      direction: Direction, ordering_name: str,
                      blurred_score: float, rows: int = 8, cols: int = 8,
                      step_percent: int = 10, minimum_iou: float = 0.50,
                      ambiguity_margin: float = 0.03
                      ) -> tuple[list[CurvePoint], float | None]:
    """Evaluate a curve with shared, precomputed original/blurred endpoints.

    The predictor is called only for intermediate points. The original-image
    endpoint is the verified reference confidence and the fully blurred
    endpoint is supplied once per image, shared across targets in that image.
    """
    x = _validate_image(image)
    b = _validate_image(blurred_baseline)
    if x.shape != b.shape:
        raise ValueError("image and blurred baseline shapes must match")
    if direction not in ("deletion", "insertion"):
        raise ValueError("direction must be deletion or insertion")
    expected = rows * cols
    valid_cells = {(r, c) for r in range(rows) for c in range(cols)}
    if len(order) != expected or len(set(order)) != expected or set(order) != valid_cells:
        raise ValueError("order must contain every grid cell exactly once")
    if step_percent < 1 or 100 % step_percent != 0:
        raise ValueError("step_percent must divide 100")
    if reference.score <= 0 or not 0 <= blurred_score <= 1:
        raise ValueError("invalid endpoint score")
    points: list[CurvePoint] = []
    for percent in range(0, 101, step_percent):
        count = int(round((percent / 100.0) * expected))
        selected = list(order[:count])
        fraction = _selected_area_fraction(x.shape[0], x.shape[1], rows, cols, selected)
        if percent == 0:
            score, status, iou = ((reference.score, "BASELINE", 1.0)
                                  if direction == "deletion"
                                  else (blurred_score, "BLURRED_ENDPOINT", None))
        elif percent == 100:
            score, status, iou = ((blurred_score, "BLURRED_ENDPOINT", None)
                                  if direction == "deletion"
                                  else (reference.score, "BASELINE", 1.0))
        else:
            altered = _alter_by_cells(x, b, selected, rows=rows, cols=cols,
                                      direction=direction)
            score, status, iou = target_score(
                reference, predict(altered), minimum_iou=minimum_iou,
                ambiguity_margin=ambiguity_margin)
        normalized = None if score is None else float(np.clip(score / reference.score, 0.0, 1.0))
        points.append(CurvePoint(direction, ordering_name, percent / 100.0,
                                  float(fraction), None if score is None else float(score),
                                  normalized, status, iou))
    return points, curve_auc(points)


def curve_auc(points: Sequence[CurvePoint]) -> float | None:
    """Trapezoidal AUC over actual modified pixel fraction; ambiguity blocks it."""
    if len(points) < 2 or any(p.normalized_score is None for p in points):
        return None
    x = np.asarray([p.modified_fraction for p in points], dtype=float)
    y = np.asarray([p.normalized_score for p in points], dtype=float)
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        return None
    if abs(x[0]) > 1e-9 or abs(x[-1] - 1.0) > 1e-9 or np.any(np.diff(x) <= 0):
        return None
    return float(np.sum((y[:-1] + y[1:]) * np.diff(x) / 2.0))
