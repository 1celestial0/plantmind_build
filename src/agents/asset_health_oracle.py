"""AssetHealthOracle — health 0–100 + RUL + CI via Weibull physics.

Reports only. Consumes PhysicsModelInterface (LOCKED_STATE §4).
LOCKED_STATE trigger: health < 40 OR rul_days < 14 → GötzeEngine.
"""
from __future__ import annotations

import numpy as np

from src.contracts.ui import AssetHealthReport
from src.physics import compute_health


def run(
    asset_id: str,
    asset_type: str,
    cycle: float,
    temp_celsius: float = 25.0,
    load_ratio: float = 1.0,
    rng: np.random.Generator | None = None,
) -> AssetHealthReport:
    """
    Produce a health report for one asset at a given cycle.

    Raises KeyError for unknown asset_type.
    """
    physics_out = compute_health(
        asset_type=asset_type,
        cycle=cycle,
        temp_celsius=temp_celsius,
        load_ratio=load_ratio,
        rng=rng,
    )

    return AssetHealthReport(
        asset_id=asset_id,
        health_score=physics_out.health_index,
        rul_days=physics_out.rul_estimate,
        ci_95=physics_out.confidence_interval,
        physics_text=physics_out.physics_explanation,
    )


def should_trigger_gotze(report: AssetHealthReport) -> bool:
    """LOCKED_STATE §3 trigger check."""
    return report.health_score < 40.0 or report.rul_days < 14.0
