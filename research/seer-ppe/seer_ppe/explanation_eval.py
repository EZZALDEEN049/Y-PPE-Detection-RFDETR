"""Scoring and localization utilities, not an implemented RF-DETR XAI generator."""
import numpy as np


def attribution_fraction_in_mask(attribution, target_mask):
    """Fraction of positive |attribution| inside a validated target ROI.
    This is a localization metric only and DOES NOT by itself prove faithfulness.
    """
    a=np.asarray(attribution,dtype=float)
    mask=np.asarray(target_mask,dtype=bool)
    if a.shape != mask.shape or a.ndim != 2 or not np.isfinite(a).all():
        raise ValueError("shape/missing/finite attribution problem")
    mass=np.abs(a)
    if np.sum(mass) == 0:
        return None
    return float(np.sum(mass[mask]) / np.sum(mass))


def target_score_drop(original_score, perturbed_score):
    """Matched, same-target score change for *real* perturbation trials.
    Matching detection class, identity and IoU is a separate required step.
    """
    if not all(0<=x<=1 for x in (original_score,perturbed_score)):
        raise ValueError("probability scores must lie in [0,1]")
    return float(original_score-perturbed_score)
