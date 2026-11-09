"""Match target detections across real image-perturbation inference trials.

This module intentionally does NOT manufacture attributions or inference data.
"""
from dataclasses import dataclass
from math import isfinite
from typing import Optional, Sequence

@dataclass(frozen=True)
class Detection:
    class_name: str
    x: float  # box center, original-image pixel coordinates
    y: float
    width: float
    height: float
    score: float

    def __post_init__(self):
        if not self.class_name or not all(isfinite(t) for t in (self.x,self.y,self.width,self.height,self.score)):
            raise ValueError("invalid detection")
        if self.width <= 0 or self.height <= 0 or not 0 <= self.score <= 1:
            raise ValueError("invalid detection geometry or confidence")


def box_iou(a: Detection,b: Detection) -> float:
    """IoU on original image coordinates, not resized/normalized coordinates."""
    ax1,ay1,ax2,ay2=a.x-a.width/2,a.y-a.height/2,a.x+a.width/2,a.y+a.height/2
    bx1,by1,bx2,by2=b.x-b.width/2,b.y-b.height/2,b.x+b.width/2,b.y+b.height/2
    intersection=max(0,min(ax2,bx2)-max(ax1,bx1))*max(0,min(ay2,by2)-max(ay1,by1))
    union=a.width*a.height+b.width*b.height-intersection
    return intersection/union if union>0 else 0.0

@dataclass(frozen=True)
class DetectionMatch:
    status: str  # MATCHED, AMBIGUOUS, LOST
    score_before: float
    score_after: Optional[float]
    iou: Optional[float]


def match_target(reference:Detection, perturbed:Sequence[Detection], min_iou:float=0.5,
                 ambiguity_margin:float=0.03)->DetectionMatch:
    """Require same class and unique high-IoU match; LOST is not score zero.

    A lost matched detection must be reported separately, not silently included
    as an attribution-induced score drop; occlusion may change detection count.
    """
    if not 0 <= min_iou <= 1 or ambiguity_margin < 0:
        raise ValueError("invalid matching thresholds")
    candidates=sorted(((box_iou(reference,d),d) for d in perturbed if d.class_name==reference.class_name),key=lambda pair:pair[0],reverse=True)
    accepted=[(overlap,d) for overlap,d in candidates if overlap>=min_iou]
    if not accepted:
        return DetectionMatch("LOST",reference.score,None,None)
    if len(accepted)>1 and accepted[0][0]-accepted[1][0]<=ambiguity_margin:
        return DetectionMatch("AMBIGUOUS",reference.score,None,accepted[0][0])
    overlap,d=accepted[0]
    return DetectionMatch("MATCHED",reference.score,d.score,overlap)
