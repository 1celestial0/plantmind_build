"""MLE calibration of Weibull λ from failure-cycle observations.

Per LOCKED_STATE §6a: "replace with calibrate_weibull.py MLE output when ready."
Run this when you have real or CMAPSS-derived failure cycles.

Usage:
    python -m ml.synthesis.calibrate_weibull \
        --asset-type pump \
        --failure-cycles 410 425 398 440 415 \
        --beta 2.3

Output: prints updated λ and 95% CI, ready to paste into constants.py.
"""
from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import chi2

from src.physics.constants import ASSET_PARAMS


def _neg_log_likelihood(lambda_: float, cycles: np.ndarray, beta: float, s: float = 1.0) -> float:
    """Negative log-likelihood for Weibull failure times (complete data)."""
    n = len(cycles)
    # Weibull PDF: f(t) = λβ·S·t^(β-1)·exp(-λ·S·t^β)
    # log L = n·ln(λ) + n·ln(β) + n·ln(S) + (β-1)·Σln(t) - λ·S·Σt^β
    ll = (
        n * math.log(lambda_)
        + n * math.log(beta)
        + n * math.log(s)
        + (beta - 1) * np.sum(np.log(cycles))
        - lambda_ * s * np.sum(cycles**beta)
    )
    return -ll


def mle_lambda(
    failure_cycles: list[float],
    beta: float,
    s: float = 1.0,
) -> dict[str, float]:
    """
    MLE estimate of λ with 95% CI from profile likelihood.

    Returns dict with keys: lambda_mle, ci_low, ci_high.
    """
    t = np.asarray(failure_cycles, dtype=float)
    n = len(t)

    # Closed-form MLE: λ̂ = n / (S · Σt^β)
    lambda_mle = float(n / (s * np.sum(t**beta)))

    # 95% CI via chi-squared (exact for complete data)
    # 2n·λ̂·S·Σt^β / λ ~ chi2(2n) — simplifies to chi2(2n) / (2 * Σt^β * S)
    total = s * np.sum(t**beta)
    ci_low = float(chi2.ppf(0.025, df=2 * n) / (2 * total))
    ci_high = float(chi2.ppf(0.975, df=2 * n) / (2 * total))

    return {"lambda_mle": lambda_mle, "ci_low": ci_low, "ci_high": ci_high}


def main() -> None:
    parser = argparse.ArgumentParser(description="MLE calibrate Weibull λ")
    parser.add_argument("--asset-type", required=True, choices=list(ASSET_PARAMS))
    parser.add_argument(
        "--failure-cycles",
        nargs="+",
        type=float,
        required=True,
        help="Observed cycles at failure",
    )
    parser.add_argument(
        "--beta",
        type=float,
        default=None,
        help="β to use (default: locked value for asset type)",
    )
    parser.add_argument("--stress", type=float, default=1.0, help="Composite stress S")
    args = parser.parse_args()

    beta = args.beta or ASSET_PARAMS[args.asset_type]["beta"]
    result = mle_lambda(args.failure_cycles, beta, args.stress)

    locked_lambda = ASSET_PARAMS[args.asset_type]["lambda_"]
    print(f"\nAsset: {args.asset_type}  β={beta}  S={args.stress}")
    print(f"  n observations    : {len(args.failure_cycles)}")
    print(f"  failure cycles    : {args.failure_cycles}")
    print(f"  λ̂  (MLE)          : {result['lambda_mle']:.4e}")
    print(f"  95% CI            : [{result['ci_low']:.4e}, {result['ci_high']:.4e}]")
    print(f"  Locked λ (current): {locked_lambda:.4e}")
    print()
    print("Paste into src/physics/constants.py ASSET_PARAMS and log a VAULT UPDATE.")


if __name__ == "__main__":
    main()
