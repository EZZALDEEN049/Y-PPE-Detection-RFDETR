"""Exact risk-calibration sample-budget planning; NOT a model validation result.

No scipy required. Numerically checked against scipy.stats.beta.ppf for the
research protocol alpha_FC=.05, alpha_UC=.15, delta=.05, M=9.
Assumes independent adjudicated site-level violations; not video frames.
"""
import argparse
import json
import math


def binomial_cdf(k, n, p):
    """P(Binomial(n,p) <= k) via log-sum-exp."""
    if not (0 < p < 1) or n < 0 or k < 0:
        raise ValueError("Invalid binomial arguments")
    if k >= n:
        return 1.0
    logs = [
        math.lgamma(n + 1) - math.lgamma(i + 1) -
        math.lgamma(n - i + 1) + i * math.log(p) +
        (n - i) * math.log1p(-p)
        for i in range(k + 1)
    ]
    high = max(logs)
    return math.exp(high) * sum(math.exp(v - high) for v in logs)


def minimum_n(k, alpha, delta=0.05, grid_size=9, risks=2, cap=10000):
    """Minimum independent violation count to certify upper_CP(k,n)<=alpha.

    For a one-sided CP upper limit, this is equivalent to
    P[Binom(n,alpha)<=k] <= delta/(grid_size*risks).
    """
    if not (0 < alpha < 1 and 0 < delta < 1 and grid_size >= 1 and risks >= 1):
        raise ValueError("Invalid protocol parameters")
    tail = delta / (grid_size * risks)
    for n in range(k + 1, cap + 1):
        if binomial_cdf(k, n, alpha) <= tail:
            return n
    raise ValueError("Exceeds cap: raise cap after checking sample feasibility")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha-fc", type=float, default=0.05)
    parser.add_argument("--alpha-uc", type=float, default=0.15)
    parser.add_argument("--delta", type=float, default=0.05)
    parser.add_argument("--grid-size", type=int, default=9)
    args = parser.parse_args()
    output = {
        "source": "Exact binomial feasibility, two risk families and fixed grid",
        "not_empirical_performance": True,
        "delta": args.delta,
        "grid_size": args.grid_size,
        "tail_per_risk_threshold": args.delta/(2*args.grid_size),
        "minimum_violation_cases_by_observed_errors": {
            str(k): {
                "FC": minimum_n(k, args.alpha_fc, args.delta, args.grid_size),
                "UC": minimum_n(k, args.alpha_uc, args.delta, args.grid_size),
            }
            for k in (0, 1, 2, 3, 5, 10)
        }
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
