"""GötzeEngine — scores candidate interventions via IIS → one best action.

REQUIRES human approval (LOCKED_STATE §1, §7).
IIS formula (LOCKED_STATE §2):
    IIS(i) = 0.35·ΔP_failure + 0.25·ΔDowntimeCost + 0.20·Feasibility
           + 0.15·HistoricalSuccess − 0.05·SafetyRiskDelta

Hard rule: SafetyRiskDelta ≥ SAFETY_VETO_CEILING → intervention vetoed.
Demo uses fixed IIS weights and fixed candidate scores.
"""
from __future__ import annotations

from dataclasses import dataclass

from src.contracts.ui import GotzeDecision

# Weights — LOCKED_STATE §2
_W = {
    "delta_p_failure": 0.35,
    "delta_downtime_cost": 0.25,
    "feasibility": 0.20,
    "historical_success": 0.15,
    "safety_risk_delta": -0.05,
}

SAFETY_VETO_CEILING = 0.80  # safety_risk_delta at or above this → vetoed


@dataclass(frozen=True)
class Intervention:
    name: str
    description: str
    delta_p_failure: float       # 0-1: reduction in failure probability
    delta_downtime_cost: float   # 0-1: net downtime cost saved (normalized)
    feasibility: float           # 0-1: operational feasibility right now
    historical_success: float    # 0-1: past success rate
    safety_risk_delta: float     # 0-1: added safety risk (higher = worse)

    @property
    def iis(self) -> float:
        return round(
            _W["delta_p_failure"] * self.delta_p_failure
            + _W["delta_downtime_cost"] * self.delta_downtime_cost
            + _W["feasibility"] * self.feasibility
            + _W["historical_success"] * self.historical_success
            + _W["safety_risk_delta"] * self.safety_risk_delta,
            4,
        )

    @property
    def vetoed(self) -> bool:
        return self.safety_risk_delta >= SAFETY_VETO_CEILING


# ── Candidate pool (fixed for demo) ──────────────────────────────────────────
CANDIDATES: list[Intervention] = [
    Intervention(
        name="reduce_load_20pct",
        description="Reduce operating load by 20 % for 48 h",
        delta_p_failure=0.45, delta_downtime_cost=0.55,
        feasibility=0.90, historical_success=0.78, safety_risk_delta=0.05,
    ),
    Intervention(
        name="lubrication_flush",
        description="Flush and replace lubrication system",
        delta_p_failure=0.62, delta_downtime_cost=0.70,
        feasibility=0.75, historical_success=0.85, safety_risk_delta=0.08,
    ),
    Intervention(
        name="bearing_inspection",
        description="Inspect and replace bearings beyond 60 % wear index",
        delta_p_failure=0.80, delta_downtime_cost=0.85,
        feasibility=0.60, historical_success=0.90, safety_risk_delta=0.12,
    ),
    Intervention(
        name="seal_replacement",
        description="Replace primary and secondary seals",
        delta_p_failure=0.55, delta_downtime_cost=0.60,
        feasibility=0.70, historical_success=0.82, safety_risk_delta=0.10,
    ),
    Intervention(
        name="temperature_derating",
        description="Reduce operating temperature 10 °C via cooling adjustment",
        delta_p_failure=0.38, delta_downtime_cost=0.42,
        feasibility=0.95, historical_success=0.70, safety_risk_delta=0.03,
    ),
    Intervention(
        name="predictive_shutdown",
        description="Schedule planned maintenance shutdown in 7 days",
        delta_p_failure=0.95, delta_downtime_cost=0.90,
        feasibility=0.85, historical_success=0.95, safety_risk_delta=0.15,
    ),
    Intervention(
        name="vibration_dampening",
        description="Install additional vibration dampening mounts",
        delta_p_failure=0.42, delta_downtime_cost=0.48,
        feasibility=0.80, historical_success=0.65, safety_risk_delta=0.06,
    ),
    Intervention(
        name="emergency_stop",
        description="Immediate emergency stop and full inspection",
        delta_p_failure=0.99, delta_downtime_cost=0.35,
        feasibility=1.00, historical_success=0.98, safety_risk_delta=0.02,
    ),
]


def run(
    asset_id: str,
    health_score: float,
    rul_days: float,
    flagged_signals: list[str] | None = None,
) -> GotzeDecision:
    """
    Score all non-vetoed candidates and return GötzeDecision with top action.

    health_score and rul_days slightly modulate feasibility for context-awareness.
    Always requires_human_approval = True (LOCKED_STATE §7).
    """
    flagged = flagged_signals or []

    # Context-aware feasibility nudge: if health is critically low, prefer fast actions
    urgency = max(0.0, (40.0 - health_score) / 40.0)  # 0 at h=40, 1 at h=0

    eligible = [c for c in CANDIDATES if not c.vetoed]

    scored: list[tuple[float, Intervention]] = []
    for cand in eligible:
        # Nudge feasibility up for interventions that are fast when urgency is high
        effective_feasibility = min(1.0, cand.feasibility + 0.05 * urgency * cand.delta_p_failure)
        adjusted_iis = round(
            _W["delta_p_failure"] * cand.delta_p_failure
            + _W["delta_downtime_cost"] * cand.delta_downtime_cost
            + _W["feasibility"] * effective_feasibility
            + _W["historical_success"] * cand.historical_success
            + _W["safety_risk_delta"] * cand.safety_risk_delta,
            4,
        )
        scored.append((adjusted_iis, cand))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_iis, top = scored[0]
    runner_iis, runner = scored[1]

    narrative = (
        f"GötzeEngine recommends '{top.name}' "
        f"(IIS {top_iis:.3f}). "
        f"{top.description}. "
        f"Runner-up: '{runner.name}' (IIS {runner_iis:.3f}, gap {top_iis - runner_iis:.3f}). "
        f"Health {health_score:.1f}/100, RUL {rul_days:.1f} d. "
        f"{'Flagged: ' + ', '.join(flagged[:3]) + '. ' if flagged else ''}"
        "Awaiting operator approval."
    )

    return GotzeDecision(
        top_intervention=top.name,
        iis_score=top_iis,
        runner_up=runner.name,
        iis_gap=round(top_iis - runner_iis, 4),
        narrative=narrative,
        confidence=round(top_iis, 3),
        requires_human_approval=True,
    )
