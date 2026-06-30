"""RootCauseAnalyst — Groq LLM-backed causal chain with RAG citations.

Falls back to enhanced templates if GROQ_API_KEY is not set.
"""
from __future__ import annotations
import json
import os
from dataclasses import dataclass

from src.rag.store import query_manuals

# ── Groq client (optional) ────────────────────────────────────────────────────
_GROQ = None
try:
    from groq import Groq
    if os.environ.get("GROQ_API_KEY"):
        _GROQ = Groq()
except Exception:
    pass


@dataclass
class RCAResult:
    asset_id: str
    causal_chain: list[str]
    citations: list[str]
    confidence: float
    narrative: str


# ── enhanced templates (fallback) ─────────────────────────────────────────────
_TEMPLATES: dict[str, dict] = {
    "vibration": {
        "root_cause": "Sub-surface fatigue causing bearing imbalance — vibration RMS exceeded 3-sigma",
        "chain": [
            "Vibration RMS and kurtosis elevated above 3-sigma threshold",
            "Root cause: micro-crack propagation in bearing races (Hertzian fatigue)",
            "Consequence: shaft imbalance -> seal wear -> lubricant contamination",
        ],
    },
    "temperature": {
        "root_cause": "Lubrication viscosity breakdown causing thermal runaway risk",
        "chain": [
            "Bearing temperature rising above baseline — viscosity index depleted",
            "Root cause: oxidative degradation of lubricant film",
            "Consequence: asperity contact -> boundary lubrication -> seizure risk",
        ],
    },
    "pressure": {
        "root_cause": "Impeller wear or seal bypass causing efficiency loss",
        "chain": [
            "Pressure delta and flow rate declining below operational band",
            "Root cause: erosive wear on impeller vanes or bypass around worn seal",
            "Consequence: reduced hydraulic efficiency -> motor overload -> thermal trip",
        ],
    },
    "electrical": {
        "root_cause": "Winding insulation degradation causing current imbalance",
        "chain": [
            "Motor current elevated with phase imbalance signature",
            "Root cause: insulation breakdown from thermal cycling (Arrhenius mechanism)",
            "Consequence: partial discharge -> ground fault -> motor failure",
        ],
    },
    "default": {
        "root_cause": "Multi-mode degradation — Weibull model confirms accelerated wear",
        "chain": [
            "Multiple signal anomalies across sensor suite — composite Z-score elevated",
            "Root cause: compound mechanical degradation exceeding Weibull life model",
            "Consequence: accelerated RUL consumption -> imminent failure if unaddressed",
        ],
    },
}


def _template_key(flagged: list[str]) -> str:
    for sig in flagged:
        s = sig.lower()
        if any(x in s for x in ("vibr", "kurtosis", "crest", "impulse")):
            return "vibration"
        if "temp" in s:
            return "temperature"
        if any(x in s for x in ("pressure", "flow", "efficiency")):
            return "pressure"
        if any(x in s for x in ("current", "motor", "winding")):
            return "electrical"
    return "default"


def _groq_rca(asset_type: str, asset_id: str, health: float, cycle: int,
              flagged: list[str], rul: float, citations: list[str]) -> tuple[str, str, float] | tuple[None, None, None]:
    prompt = f"""You are a senior industrial maintenance engineer providing a root cause analysis for LTTS PlantMind.

Asset: {asset_type} (ID: {asset_id})
Health score: {health:.1f}/100 (CRITICAL — below failure threshold)
Operating cycle: {cycle}
Remaining useful life: {rul:.1f} days
Flagged sensor signals: {', '.join(flagged) if flagged else 'none'}
Maintenance manual references: {', '.join(citations) if citations else 'generic'}

Respond in JSON only:
{{
  "root_cause": "one sentence — specific physical failure mechanism for {asset_type}",
  "causal_chain": "signal anomaly -> physical mechanism -> consequence (use -> separator)",
  "confidence": 0.85
}}

Be specific: name the signals, describe the physics of {asset_type} failure. No generic text."""

    try:
        resp = _GROQ.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=350,
            temperature=0.15,
        )
        data = json.loads(resp.choices[0].message.content)
        return (
            str(data.get("root_cause", "")),
            str(data.get("causal_chain", "")),
            float(data.get("confidence", 0.80)),
        )
    except Exception:
        return None, None, None


def run(
    asset_id: str,
    asset_type: str,
    flagged_signals: list[str],
    rul_days: float,
    health_score: float,
    cycle: int = 0,
) -> RCAResult:
    rag_hits   = query_manuals(asset_type, " ".join(flagged_signals[:3]))
    citations  = [h["ref"] for h in rag_hits]
    confidence = min(0.92, 0.52 + 0.10 * len(flagged_signals) + 0.05 * (1 - health_score / 100))

    # Try Groq first
    if _GROQ:
        root, chain_str, conf = _groq_rca(asset_type, asset_id, health_score,
                                           cycle, flagged_signals, rul_days, citations)
        if root and chain_str:
            chain = chain_str.split(" -> ")
            narrative = chain_str
            if citations:
                narrative += f" [Sources: {'; '.join(citations[:2])}]"
            return RCAResult(
                asset_id=asset_id,
                causal_chain=chain,
                citations=citations,
                confidence=round(conf, 2),
                narrative=narrative,
            )

    # Enhanced template fallback
    key   = _template_key(flagged_signals)
    tmpl  = _TEMPLATES[key]
    chain = tmpl["chain"]
    chain[-1] = chain[-1].replace("{rul}", f"{rul_days:.0f}")

    narrative = " -> ".join(chain[:3])
    if citations:
        narrative += f" [Sources: {'; '.join(citations[:2])}]"

    return RCAResult(
        asset_id=asset_id,
        causal_chain=chain,
        citations=citations,
        confidence=round(confidence, 2),
        narrative=narrative,
    )
