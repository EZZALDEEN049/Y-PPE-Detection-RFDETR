"""Model-agnostic black-box occlusion attribution; requires a real, local detector.

This is *not* a completed SEER-PPE experiment. It does not manufacture scores,
interpret matched-target loss as a zero score, or infer the task PPE rule.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Sequence
import numpy as np
from .detection_match import Detection, match_target

@dataclass(frozen=True)
class OcclusionTrial:
    row: int
    col: int
    status: str
    matched_score_drop: float | None
    matched_iou: float | None


def occlusion_explain(
    rgb_image: np.ndarray,
    reference: Detection,
    predict: Callable[[np.ndarray], Sequence[Detection]],
    *,
    rows: int = 4,
    cols: int = 4,
    minimum_iou: float = 0.5,
    fill_value: int = 127,
) -> tuple[np.ndarray, list[OcclusionTrial]]:
    """Score-drop map for a *fixed matched detection* across rectangular deletions.

    Caller supplies a real prediction function that accepts HÃWÃ3 uint8 and
    returns detections on the same image coordinate system. Explanations are
    validated separately by an independent worker/PPE target annotation.

    Zero attribution for LOST would be scientifically misleading, so cells that
    cannot be target-matched are NaN. Their count is reported separately.
    """
    x = np.asarray(rgb_image)
    if x.ndim != 3 or x.shape[2] != 3 or x.dtype != np.uint8:
        raise ValueError('uint8 HxWx3 image required')
    h,w=x.shape[:2]
    if rows < 1 or cols < 1 or h < rows or w < cols:
        raise ValueError('invalid occlusion grid')
    if not 0 <= fill_value <= 255:
        raise ValueError('invalid fill')
    m=np.full((rows,cols),np.nan,dtype=np.float64)
    trials=[]
    for i in range(rows):
        for j in range(cols):
            top=i*h//rows;bottom=(i+1)*h//rows
            left=j*w//cols;right=(j+1)*w//cols
            altered=x.copy();altered[top:bottom,left:right,:]=fill_value
            result=match_target(reference,predict(altered),min_iou=minimum_iou)
            drop=reference.score-result.score_after if result.status=='MATCHED' else None
            if drop is not None:m[i,j]=drop
            trials.append(OcclusionTrial(i,j,result.status,drop,result.iou))
    return m,trials
