"""Named failure pattern library — inject into live digital twin for demo."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class FailurePattern:
    name: str
    pattern_id: str
    asset_type: str
    description: str
    signals: dict[str, float]   # signal_name -> multiplier vs. baseline
    health_penalty: float        # immediate health score reduction (0-100)
    rul_collapse_days: float     # RUL collapses to this value
    failure_mode: str
    time_to_catastrophic: str


FAILURE_PATTERNS: list[FailurePattern] = [
    FailurePattern(
        name="Bearing Spalling — Stage 2",
        pattern_id="bearing_spall_2",
        asset_type="bearing",
        description="Sub-surface fatigue cracks propagating. Kurtosis + impulse spikes.",
        signals={"kurtosis": 4.2, "vibration_rms": 2.8, "impulse_factor": 3.5},
        health_penalty=45,
        rul_collapse_days=4.0,
        failure_mode="shock",
        time_to_catastrophic="4-7 days",
    ),
    FailurePattern(
        name="Pump Cavitation — Progressive",
        pattern_id="pump_cavitation",
        asset_type="pump",
        description="Vapour bubble collapse eroding impeller. Pressure fluctuations + vibration.",
        signals={"pressure_inlet": 0.4, "vibration_rms": 3.1, "flow_rate": 0.65},
        health_penalty=35,
        rul_collapse_days=6.0,
        failure_mode="degradation",
        time_to_catastrophic="6-10 days",
    ),
    FailurePattern(
        name="Motor Winding Degradation",
        pattern_id="motor_winding",
        asset_type="motor",
        description="Insulation breakdown under thermal stress. Current imbalance rising.",
        signals={"motor_current": 1.8, "temperature_bearing": 1.5, "vibration_rms": 1.4},
        health_penalty=30,
        rul_collapse_days=9.0,
        failure_mode="degradation",
        time_to_catastrophic="9-14 days",
    ),
    FailurePattern(
        name="Compressor Surge Event",
        pattern_id="compressor_surge",
        asset_type="compressor",
        description="Cyclical flow reversal. Pressure ratio exceeds stability boundary.",
        signals={"pressure_ratio": 1.9, "discharge_temp": 1.7, "efficiency": 0.55},
        health_penalty=55,
        rul_collapse_days=2.0,
        failure_mode="shock",
        time_to_catastrophic="2-4 days — URGENT",
    ),
    FailurePattern(
        name="Valve Seat Wear — Chronic Leak",
        pattern_id="valve_seat_wear",
        asset_type="valve",
        description="Erosive wear from particulates. Pressure delta collapsing gradually.",
        signals={"pressure_delta": 0.3, "vibration_rms": 1.6, "flow_rate": 0.75},
        health_penalty=25,
        rul_collapse_days=12.0,
        failure_mode="wear",
        time_to_catastrophic="12-18 days",
    ),
]

PATTERNS_BY_ID:   dict[str, FailurePattern] = {p.pattern_id: p for p in FAILURE_PATTERNS}
PATTERNS_BY_TYPE: dict[str, list[FailurePattern]] = {
    t: [p for p in FAILURE_PATTERNS if p.asset_type == t]
    for t in ("pump", "compressor", "motor", "bearing", "valve")
}

# Cascade chains: which assets are downstream of a failing asset
ASSET_CASCADE: dict[str, list[tuple[str, str]]] = {
    "bearing":    [("motor",      "Bearing failure -> motor shaft imbalance"),
                   ("compressor", "Motor overload -> compressor loses drive")],
    "pump":       [("compressor", "Feed pressure drop -> compressor surge risk"),
                   ("valve",      "Pressure instability -> valve seat stress")],
    "motor":      [("compressor", "Drive loss -> compressor offline")],
    "compressor": [],
    "valve":      [("pump",       "Inlet starvation -> pump cavitation")],
}
