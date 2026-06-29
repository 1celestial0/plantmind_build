"""DataSentinel — flags sensor anomalies via Z-score + Mahalanobis.

Flags only. Does not recommend actions. Output feeds trigger thresholds.
LOCKED_STATE §1: severity options are normal / warning / critical.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal

from ml.synthesis.config import SIGNAL_SPECS

# Keyed by signal name; built once from SIGNAL_SPECS baselines.
_BASELINES: dict[str, tuple[float, float]] = {
    s.name: (s.baseline, s.noise_frac * s.baseline) for s in SIGNAL_SPECS
}

Severity = Literal["normal", "warning", "critical"]

Z_WARN = 3.0
Z_CRIT = 4.5
MAHAL_CRIT = 5.0


@dataclass
class SentinelResult:
    asset_id: str
    severity: Severity
    flagged_signals: list[str]
    z_scores: dict[str, float]
    mahalanobis_distance: float
    message: str


def run(asset_id: str, signals: dict[str, float]) -> SentinelResult:
    """
    Compute per-signal Z-scores and diagonal Mahalanobis distance.

    Only checks signals that have a known baseline in SIGNAL_SPECS.
    Unknown signals are silently skipped.
    """
    z_scores: dict[str, float] = {}
    flagged: list[str] = []
    mahal_sq = 0.0
    n_used = 0

    for name, reading in signals.items():
        if name not in _BASELINES:
            continue
        mean, std = _BASELINES[name]
        if std == 0:
            continue
        z = (reading - mean) / std
        z_scores[name] = round(z, 3)
        mahal_sq += z * z
        n_used += 1
        if abs(z) >= Z_WARN:
            flagged.append(name)

    mahal = math.sqrt(mahal_sq / n_used) if n_used else 0.0

    # Severity decision
    has_crit_z = any(abs(z_scores.get(s, 0)) >= Z_CRIT for s in flagged)
    if has_crit_z or mahal >= MAHAL_CRIT:
        severity: Severity = "critical"
    elif flagged:
        severity = "warning"
    else:
        severity = "normal"

    msg = (
        f"{len(flagged)} signal(s) out of range — "
        f"Mahalanobis D={mahal:.2f}, severity={severity}."
        if flagged
        else f"All signals nominal (Mahalanobis D={mahal:.2f})."
    )

    return SentinelResult(
        asset_id=asset_id,
        severity=severity,
        flagged_signals=flagged,
        z_scores=z_scores,
        mahalanobis_distance=round(mahal, 3),
        message=msg,
    )
