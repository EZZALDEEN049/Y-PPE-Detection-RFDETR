"""Conservative two-stage PPE evidence routing.

Experimental policy only. The confidence values are not safety-certified.
This module never consults offline ground truth to make a runtime decision.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Route(str, Enum):
    BASIC = "BASIC"
    EXPLAIN = "EXPLAIN"
    REVIEW = "REVIEW"


class SafetyState(str, Enum):
    SUPPORTED_CLEAR = "SUPPORTED_CLEAR"
    POTENTIAL_ALERT = "POTENTIAL_ALERT"
    NOT_REQUIRED = "NOT_REQUIRED"
    UNCERTAIN_REVIEW = "UNCERTAIN_REVIEW"


@dataclass(frozen=True)
class RuntimeEvidence:
    """No field here may be populated using retrospective test GT.

    ppe_required: an independent, runtime-visible verified site/task rule;
       None means no rule was established.
    ppe_worn: inference from detector + person-PPE association (not GT).
    visible_person: whether a runtime candidate worker is detected/confirmed;
       False is NOT proof that the scene is worker-free.
    association_status: 'unique', 'ambiguous', or 'none'.
    explicit_non_ppe: a detected non-PPE class; NOT automatically legal violation.
    """
    case_id: str
    ppe_required: Optional[bool]
    visible_person: bool
    ppe_worn: Optional[bool]
    confidence: Optional[float]
    association_status: str
    visibility: str
    explicit_non_ppe: bool = False

    def __post_init__(self):
        if not self.case_id:
            raise ValueError("case_id required")
        if self.confidence is not None and not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be in [0,1]")
        if self.association_status not in {"unique", "ambiguous", "none"}:
            raise ValueError("invalid association status")
        if self.visibility not in {"clear", "partial", "occluded", "unknown"}:
            raise ValueError("invalid visibility")


@dataclass(frozen=True)
class ExperimentalPolicy:
    """Values are only demonstrations; tune on calibration partition, never test."""
    clear_min_confidence: float = 0.90
    alert_min_confidence: float = 0.90
    explanation_min_confidence: float = 0.55

    def __post_init__(self):
        values = (self.clear_min_confidence, self.alert_min_confidence,
                  self.explanation_min_confidence)
        if any(not 0 <= c <= 1 for c in values):
            raise ValueError("thresholds must be in [0,1]")


@dataclass(frozen=True)
class RouteDecision:
    case_id: str
    route: Route
    safety_state: SafetyState
    reason: str


def route_case(evidence: RuntimeEvidence, policy: ExperimentalPolicy) -> RouteDecision:
    """Route after a detector has already run; saves XAI, not detection, energy."""
    e = evidence
    if e.ppe_required is None:
        return RouteDecision(e.case_id, Route.REVIEW, SafetyState.UNCERTAIN_REVIEW,
                             "unknown_task_site_ppe_requirement")
    if e.ppe_required is False:
        return RouteDecision(e.case_id, Route.BASIC, SafetyState.NOT_REQUIRED,
                             "verified_runtime_policy_exception_not_gt")
    if not e.visible_person:
        return RouteDecision(e.case_id, Route.REVIEW, SafetyState.UNCERTAIN_REVIEW,
                             "person_not_detected_cannot_assert_absence")
    if e.association_status != "unique" or e.visibility in {"occluded", "unknown"}:
        return RouteDecision(e.case_id, Route.REVIEW, SafetyState.UNCERTAIN_REVIEW,
                             "association_or_visibility_uncertain")
    conf = e.confidence
    if e.ppe_worn is True and conf is not None and conf >= policy.clear_min_confidence and e.visibility == "clear":
        return RouteDecision(e.case_id, Route.BASIC, SafetyState.SUPPORTED_CLEAR,
                             "strong_unique_visual_ppe_evidence_not_certification")
    if e.ppe_worn is False and e.explicit_non_ppe and conf is not None and conf >= policy.alert_min_confidence and e.visibility == "clear":
        return RouteDecision(e.case_id, Route.BASIC, SafetyState.POTENTIAL_ALERT,
                             "explicit_non_ppe_observation_requires_context")
    if conf is not None and conf >= policy.explanation_min_confidence and e.visibility in {"clear", "partial"}:
        return RouteDecision(e.case_id, Route.EXPLAIN, SafetyState.UNCERTAIN_REVIEW,
                             "explanation_requested_no_automatic_clear")
    return RouteDecision(e.case_id, Route.REVIEW, SafetyState.UNCERTAIN_REVIEW,
                         "insufficient_visual_evidence")
