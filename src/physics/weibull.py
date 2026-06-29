"""Weibull health model + RUL solver — LOCKED_STATE §6a.

H(t) = 100 · exp(−λ · S · t^β)

To find t_fail where H(t_fail) = H_FAILURE_THRESHOLD:
    t_fail = (ln(100 / H_THRESHOLD) / (λ · S)) ^ (1 / β)

RUL_cycles = max(0, t_fail − t_current)
RUL_days   = RUL_cycles / CYCLES_PER_DAY

95% CI: parametric bootstrap on λ (log-normal, σ = 10% by default).
"""
from __future__ import annotations
import math
from typing import NamedTuple

import numpy as np

from .constants import CYCLES_PER_DAY, H_FAILURE_THRESHOLD


class WeibullRUL(NamedTuple):
    health: float        # 0–100
    rul_days: float
    ci_low_days: float   # 2.5th percentile
    ci_high_days: float  # 97.5th percentile


def health_at(cycle: float, lambda_: float, beta: float, s: float = 1.0) -> float:
    """H(t) — clamped to [0, 100]."""
    raw = 100.0 * math.exp(-lambda_ * s * (cycle**beta))
    return max(0.0, min(100.0, raw))


def _t_fail(lambda_: float, beta: float, s: float) -> float:
    """Analytical solution for cycle at which H = H_FAILURE_THRESHOLD."""
    return (math.log(100.0 / H_FAILURE_THRESHOLD) / (lambda_ * s)) ** (1.0 / beta)


def compute_rul(
    cycle: float,
    lambda_: float,
    beta: float,
    s: float = 1.0,
    n_bootstrap: int = 500,
    lambda_sigma_frac: float = 0.10,
    rng: np.random.Generator | None = None,
) -> WeibullRUL:
    """
    Compute health + RUL + 95% CI for a given operating cycle.

    Args:
        cycle: current operating cycle count
        lambda_: Weibull scale parameter (from ASSET_PARAMS)
        beta: Weibull shape parameter (from ASSET_PARAMS)
        s: composite stress factor (default 1.0 = reference conditions)
        n_bootstrap: number of λ samples for CI
        lambda_sigma_frac: fractional σ for log-normal λ bootstrap
        rng: optional numpy Generator for reproducibility
    """
    rng = rng or np.random.default_rng(42)

    h = health_at(cycle, lambda_, beta, s)
    t_f = _t_fail(lambda_, beta, s)
    rul_days = max(0.0, t_f - cycle) / CYCLES_PER_DAY

    # Bootstrap CI: sample λ from LogNormal(μ=ln(λ), σ=lambda_sigma_frac)
    lambda_samples = rng.lognormal(
        mean=math.log(lambda_),
        sigma=lambda_sigma_frac,
        size=n_bootstrap,
    )
    t_fail_samples = np.array([_t_fail(lam, beta, s) for lam in lambda_samples])
    rul_day_samples = np.maximum(0.0, t_fail_samples - cycle) / CYCLES_PER_DAY

    return WeibullRUL(
        health=round(h, 2),
        rul_days=round(rul_days, 2),
        ci_low_days=round(float(np.percentile(rul_day_samples, 2.5)), 2),
        ci_high_days=round(float(np.percentile(rul_day_samples, 97.5)), 2),
    )
