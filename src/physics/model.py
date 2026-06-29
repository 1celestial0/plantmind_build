"""Public Lane 2 interface.

Usage:
    from src.physics import compute_health

    out = compute_health("pump", cycle=300, temp_celsius=35.0, load_ratio=1.1)
    # → PhysicsModelOutput (Lane 1 consumes this contract)
"""
from __future__ import annotations

import numpy as np

from src.contracts.physics import PhysicsModelOutput
from .constants import ASSET_PARAMS
from .stress import composite_stress
from .weibull import compute_rul


def compute_health(
    asset_type: str,
    cycle: float,
    temp_celsius: float = 25.0,
    load_ratio: float = 1.0,
    rng: np.random.Generator | None = None,
) -> PhysicsModelOutput:
    """
    Compute asset health snapshot for Lane 1 consumption.

    Args:
        asset_type: one of ASSET_TYPES ("pump", "compressor", "motor", "bearing", "valve")
        cycle: current operating cycle count
        temp_celsius: operating temperature in °C (default 25 = reference)
        load_ratio: fraction of rated load (default 1.0 = rated)
        rng: optional Generator for reproducible CI bootstrap

    Returns:
        PhysicsModelOutput (LOCKED_STATE §4)

    Raises:
        KeyError: unknown asset_type
        ValueError: invalid load_ratio
    """
    if asset_type not in ASSET_PARAMS:
        raise KeyError(f"Unknown asset_type '{asset_type}'. Valid: {list(ASSET_PARAMS)}")

    params = ASSET_PARAMS[asset_type]
    s = composite_stress(temp_celsius, load_ratio)
    result = compute_rul(
        cycle=cycle,
        lambda_=params["lambda_"],
        beta=params["beta"],
        s=s,
        rng=rng,
    )

    explanation = (
        f"{asset_type.capitalize()} — cycle {cycle:.0f}: "
        f"health {result.health:.1f}/100, "
        f"RUL {result.rul_days:.1f} days "
        f"(95% CI [{result.ci_low_days:.1f}–{result.ci_high_days:.1f} d]). "
        f"Operating stress S={s:.3f} "
        f"(T={temp_celsius:.1f}°C, load={load_ratio:.2f}×rated). "
        f"Weibull λ={params['lambda_']:.2e}, β={params['beta']}."
    )

    return PhysicsModelOutput(
        health_index=result.health,
        rul_estimate=result.rul_days,
        confidence_interval=(result.ci_low_days, result.ci_high_days),
        physics_explanation=explanation,
    )
