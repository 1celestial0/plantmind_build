"""ExecutiveSummarizer — 3-bullet leadership brief.

STUB: template-based. Wire Groq Llama 3.2 3B in Lane 1 Phase 2.
Interface is final; swap body for LLM call when ready.
"""
from __future__ import annotations

from src.contracts.ui import AssetHealthReport, ExecutiveBrief, GotzeDecision


def run(
    health_reports: list[AssetHealthReport],
    gotze_decision: GotzeDecision | None,
    downtime_cost_per_day: float = 15_000.0,
) -> ExecutiveBrief:
    """
    Produce a 3-field ExecutiveBrief from pipeline outputs.

    Production: replace body with Groq Llama 3.2 3B summarization call.
    """
    critical = [
        f"{r.asset_id}: health {r.health_score:.0f}/100, RUL {r.rul_days:.1f} d"
        for r in health_reports
        if r.health_score < 40 or r.rul_days < 14
    ]

    pending = 1 if gotze_decision and gotze_decision.requires_human_approval else 0

    # Downtime saved: planned maintenance avoids unplanned failure cost.
    # Assume unplanned failure costs 5x planned maintenance window (3 days).
    # With intervention: pay 3 days planned. Without: pay 15 days unplanned.
    worst_health = min((r.health_score for r in health_reports), default=100.0)
    if gotze_decision and worst_health < 40:
        unplanned_days = 15.0
        planned_days = 3.0
        saved_days = unplanned_days - planned_days
    elif gotze_decision:
        saved_days = 5.0
    else:
        saved_days = 0.0
    downtime_saved = round(saved_days * downtime_cost_per_day, 0)

    return ExecutiveBrief(
        critical_alerts=critical,
        gotze_pending=pending,
        downtime_saved_estimate=downtime_saved,
    )
