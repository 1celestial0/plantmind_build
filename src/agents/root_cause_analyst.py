"""RootCauseAnalyst — RAG over manuals/logs → cited causal chain.

STUB: returns template-based response. Wire Groq + ChromaDB in Lane 1 Phase 2.
Interface is final; swap body for real RAG call when ready.
"""
from __future__ import annotations

from dataclasses import dataclass

from src.rag.store import query_manuals


@dataclass
class RCAResult:
    asset_id: str
    causal_chain: list[str]    # ordered steps: root → symptom → consequence
    citations: list[str]       # source refs from RAG (doc name + page)
    confidence: float          # 0-1
    narrative: str


# Template causal chains per failure pattern
_CAUSAL_TEMPLATES: dict[str, list[str]] = {
    "vibration": [
        "Increased vibration RMS detected above 3-sigma",
        "Root cause: bearing wear causing imbalance",
        "Consequence: accelerated fatigue in shaft coupling",
        "Risk: seal failure within {rul:.0f} days if unaddressed",
    ],
    "temperature": [
        "Bearing temperature rising above baseline",
        "Root cause: lubrication degradation (viscosity drop)",
        "Consequence: increased friction → thermal runaway risk",
        "Risk: critical overheating within {rul:.0f} days if unaddressed",
    ],
    "pressure": [
        "Pressure delta declining below baseline",
        "Root cause: impeller wear or seal bypass",
        "Consequence: reduced efficiency → increased load on motor",
        "Risk: full impeller failure within {rul:.0f} days if unaddressed",
    ],
    "default": [
        "Multiple sensor anomalies detected",
        "Root cause: combined mechanical degradation (Weibull curve)",
        "Consequence: accelerated remaining useful life consumption",
        "Risk: asset failure within {rul:.0f} days if unaddressed",
    ],
}


def run(
    asset_id: str,
    asset_type: str,
    flagged_signals: list[str],
    rul_days: float,
    health_score: float,
) -> RCAResult:
    """
    Return cited causal chain for the observed anomalies.

    Production: replace body with Groq RAG call via src.rag.store.
    """
    rag_hits = query_manuals(asset_type, " ".join(flagged_signals[:3]))

    # Pick template based on dominant flagged signal
    template_key = "default"
    for sig in flagged_signals:
        if "vibr" in sig or "kurtosis" in sig or "crest" in sig or "impulse" in sig:
            template_key = "vibration"
            break
        if "temp" in sig:
            template_key = "temperature"
            break
        if "pressure" in sig or "flow" in sig or "efficiency" in sig:
            template_key = "pressure"
            break

    chain = [step.format(rul=rul_days) for step in _CAUSAL_TEMPLATES[template_key]]
    citations = [h["ref"] for h in rag_hits]

    narrative = " -> ".join(chain[:3])
    if citations:
        narrative += f" [Sources: {'; '.join(citations[:2])}]"

    confidence = min(0.90, 0.50 + 0.10 * len(flagged_signals) + 0.05 * (1 - health_score / 100))

    return RCAResult(
        asset_id=asset_id,
        causal_chain=chain,
        citations=citations,
        confidence=round(confidence, 2),
        narrative=narrative,
    )
