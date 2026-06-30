"""ExecutiveSummarizer — Groq-backed leadership brief with financial impact.

Falls back to enhanced templates if GROQ_API_KEY is not set.
"""
from __future__ import annotations
import json
import os

from src.contracts.ui import AssetHealthReport, ExecutiveBrief, GotzeDecision

# ── Groq client ───────────────────────────────────────────────────────────────
_GROQ = None
try:
    from groq import Groq
    if os.environ.get("GROQ_API_KEY"):
        _GROQ = Groq()
except Exception:
    pass


def _groq_brief(
    asset_id: str,
    health: float,
    rul: float,
    recommendation: str,
    downtime_saved: float,
) -> list[str] | None:
    prompt = f"""You are an executive summarizer for LTTS PlantMind industrial AI system.

Asset: {asset_id}
Health: {health:.1f}/100 (CRITICAL)
RUL: {rul:.1f} days remaining
GötzeEngine recommendation: {recommendation.replace('_', ' ')}
Financial saving if acted upon: ${downtime_saved:,.0f}

Generate exactly 2 critical alert strings for plant managers.
Each should be one crisp sentence. Be specific with numbers. No fluff.

Respond in JSON:
{{"alerts": ["alert 1 sentence", "alert 2 sentence"]}}"""

    try:
        resp = _GROQ.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=200,
            temperature=0.1,
        )
        data = json.loads(resp.choices[0].message.content)
        alerts = data.get("alerts", [])
        return [str(a) for a in alerts if a] or None
    except Exception:
        return None


def run(
    health_reports: list[AssetHealthReport],
    gotze_decision: GotzeDecision | None,
    downtime_cost_per_day: float = 15_000.0,
) -> ExecutiveBrief:
    worst_health = min((r.health_score for r in health_reports), default=100.0)
    critical_reports = [r for r in health_reports if r.health_score < 40 or r.rul_days < 14]

    pending = 1 if gotze_decision and gotze_decision.requires_human_approval else 0

    # Downtime saving calculation
    if gotze_decision and worst_health < 40:
        saved_days = 15.0 - 3.0   # unplanned 15d vs planned 3d
    elif gotze_decision:
        saved_days = 5.0
    else:
        saved_days = 0.0
    downtime_saved = round(saved_days * downtime_cost_per_day, 0)

    # Try Groq for richer alerts
    if _GROQ and critical_reports and gotze_decision:
        r = critical_reports[0]
        groq_alerts = _groq_brief(
            r.asset_id, r.health_score, r.rul_days,
            gotze_decision.top_intervention, downtime_saved,
        )
        if groq_alerts:
            return ExecutiveBrief(
                critical_alerts=groq_alerts,
                gotze_pending=pending,
                downtime_saved_estimate=downtime_saved,
            )

    # Enhanced template fallback
    alerts = []
    for r in critical_reports:
        action = gotze_decision.top_intervention.replace("_", " ") if gotze_decision else "immediate inspection"
        alerts.append(
            f"{r.asset_id}: health {r.health_score:.0f}/100, RUL {r.rul_days:.1f} d — "
            f"GötzeEngine recommends '{action}'. "
            f"Acting now saves ${downtime_saved:,.0f} vs. unplanned failure."
        )

    return ExecutiveBrief(
        critical_alerts=alerts,
        gotze_pending=pending,
        downtime_saved_estimate=downtime_saved,
    )
