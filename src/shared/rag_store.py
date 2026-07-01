"""RAG store — ChromaDB interface for manual/log retrieval.

STUB: returns template citations. Wire real ChromaDB + embeddings in Lane 1 Phase 2.
Interface is final: query_manuals(asset_type, query_text, n_results) → list[dict].
Each result: {"ref": str, "excerpt": str, "score": float}
"""
from __future__ import annotations

# Placeholder corpus (10–20 docs planned per LOCKED_STATE §6)
_STUB_CORPUS: dict[str, list[dict[str, str]]] = {
    "pump": [
        {"ref": "PumpMaintManual_Rev4 §3.2", "excerpt": "Seal wear accelerates above 35°C differential; inspect every 90 days under high-load conditions."},
        {"ref": "FaultLog_2025_Q3 #PM-004", "excerpt": "Pump-07 seal failure traced to lubrication contamination; vibration RMS exceeded 3σ for 48 h prior."},
    ],
    "compressor": [
        {"ref": "CompressorSOP_Rev2 §5.1", "excerpt": "Valve wear is primary failure mode; schedule inspection when efficiency drops below 88%."},
        {"ref": "PRONOSTIA_BearingFaultAtlas §2", "excerpt": "Kurtosis > 5.5 indicates advanced spalling; bearing replacement should be immediate."},
    ],
    "motor": [
        {"ref": "MotorMaintGuide §4.3", "excerpt": "Winding insulation degrades when THD% exceeds 5%; derating required above 45°C ambient."},
        {"ref": "FaultLog_2025_Q4 #MT-011", "excerpt": "Motor-03 winding failure preceded by 6-day high-freq energy increase and power factor drop."},
    ],
    "bearing": [
        {"ref": "PRONOSTIA_BearingFaultAtlas §1", "excerpt": "Kurtosis spike > 4.0 is reliable indicator of inner-race defect (BPFI)."},
        {"ref": "BearingSelectGuide §2.4", "excerpt": "L10 life halves for every 10°C rise above rated temperature."},
    ],
    "valve": [
        {"ref": "ValveMaintSOP §3.1", "excerpt": "Seat erosion causes pressure delta decline; inspect when ΔP drops > 15% of rated."},
        {"ref": "FaultLog_2026_Q1 #VL-002", "excerpt": "Valve-02 seat failure; acoustic emission elevated 10 cycles before critical degradation."},
    ],
}

_DEFAULT_CORPUS = [
    {"ref": "CMAPSS_FaultModeAtlas §1", "excerpt": "Gradual degradation in turbofan/pump-type assets follows Weibull profile; Z-score threshold 3σ is industry standard."},
]


def query_manuals(
    asset_type: str,
    query_text: str,
    n_results: int = 2,
) -> list[dict[str, str | float]]:
    """
    Return top-n relevant manual excerpts for the asset type + query.

    Production: embed query_text with sentence-transformers all-MiniLM-L6-v2,
    search ChromaDB collection, return top-n hits with distance scores.
    """
    corpus = _STUB_CORPUS.get(asset_type, _DEFAULT_CORPUS)
    results = []
    for i, doc in enumerate(corpus[:n_results]):
        results.append({
            "ref": doc["ref"],
            "excerpt": doc["excerpt"],
            "score": round(0.92 - i * 0.07, 3),   # stub scores
        })
    return results
