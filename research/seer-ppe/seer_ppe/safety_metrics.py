"""Safety metrics with explicit treatment of missed workers.

Reference GT objects only appear in this offline scoring module, never in runtime routing.
CI interpretation assumes independently sampled eligible units, which must be audited.
"""
from dataclasses import dataclass
from typing import Iterable
from scipy.stats import beta
from .routing import SafetyState


@dataclass(frozen=True)
class AdjudicatedCase:
    case_id: str
    true_violation: bool  # site/task PPE rule independently verified
    person_detected: bool
    state: SafetyState


def risk_counts(records: Iterable[AdjudicatedCase]) -> dict:
    cases = [r for r in records if r.true_violation]
    false_clear = sum(r.state == SafetyState.SUPPORTED_CLEAR for r in cases)
    # UC includes undetected people and erroneous NOT_REQUIRED judgments.
    uncontained = sum((r.state in {SafetyState.SUPPORTED_CLEAR, SafetyState.NOT_REQUIRED})
                      or (not r.person_detected) for r in cases)
    return {"verified_violations":len(cases), "false_clear":false_clear,
            "uncontained":uncontained,
            "false_clear_rate":(false_clear/len(cases) if cases else None),
            "uncontained_rate":(uncontained/len(cases) if cases else None)}


def clopper_pearson_upper(errors:int, n:int, alpha:float=0.05):
    """One-sided exact binomial upper confidence bound; n=0 -> None.

    Valid coverage requires independent Bernoulli trials and no post-hoc threshold
    selection using the same final-test observations.
    """
    if n < 0 or errors < 0 or errors > n or not 0 < alpha < 1:
        raise ValueError("invalid n/errors/alpha")
    if n == 0:
        return None
    if errors == n:
        return 1.0
    return float(beta.ppf(1-alpha, errors+1, n-errors))
