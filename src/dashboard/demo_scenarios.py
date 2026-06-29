"""Pre-wired sensor readings for demo scenarios A–E (from ops/testing/scenarios.json)."""
from __future__ import annotations

from src.pipeline.schemas import SensorReading

SCENARIOS: dict[str, dict] = {
    "A": {
        "label": "A — Gradual pump wear (hero demo)",
        "description": "pump_07 at cycle 340: advanced degradation, 3 signals critical. GötzeEngine fires.",
        "reading": SensorReading(
            asset_id="pump_07",
            asset_type="pump",
            cycle=340.0,
            signals={
                "vibration_rms": 2.8,
                "kurtosis": 8.5,
                "temperature_bearing": 78.0,
                "efficiency_pct": 74.0,
                "oil_contamination": 8.5,
                "pressure_delta": 1.8,
                "crest_factor": 3.2,
            },
            temp_celsius=38.0,
            load_ratio=1.15,
        ),
    },
    "B": {
        "label": "B — Sudden bearing impact",
        "description": "bearing_03 at cycle 200: shock event — kurtosis spike + impulse factor critical.",
        "reading": SensorReading(
            asset_id="bearing_03",
            asset_type="bearing",
            cycle=200.0,
            signals={
                "vibration_rms": 4.2,
                "kurtosis": 12.8,
                "impulse_factor": 7.1,
                "crest_factor": 4.8,
                "high_freq_energy": 0.18,
                "temperature_bearing": 68.0,
            },
            temp_celsius=35.0,
            load_ratio=1.1,
        ),
    },
    "C": {
        "label": "C — Intermittent valve fault",
        "description": "valve_11 at cycle 250: pressure delta dropping, acoustic emission elevated.",
        "reading": SensorReading(
            asset_id="valve_11",
            asset_type="valve",
            cycle=250.0,
            signals={
                "pressure_delta": 1.4,
                "acoustic_emission": 1.9,
                "efficiency_pct": 81.0,
                "displacement_pk_pk": 0.12,
            },
            temp_celsius=30.0,
            load_ratio=0.85,
        ),
    },
    "D": {
        "label": "D — Sensor dropout (data quality edge)",
        "description": "motor_02 at cycle 100: vibration + temp sensors report 0 (dropout). Machine is healthy.",
        "reading": SensorReading(
            asset_id="motor_02",
            asset_type="motor",
            cycle=100.0,
            signals={
                "vibration_rms": 0.0,        # dropout — flags sentinel but machine is fine
                "temperature_bearing": 0.0,  # dropout
                "current_rms": 12.1,
                "power_factor": 0.91,
            },
            temp_celsius=25.0,
            load_ratio=1.0,
        ),
    },
    "E": {
        "label": "E — Conflicting signals (multivariate edge)",
        "description": "comp_04 at cycle 150: high temp stress but efficiency and vibration normal.",
        "reading": SensorReading(
            asset_id="comp_04",
            asset_type="compressor",
            cycle=150.0,
            signals={
                "vibration_rms": 0.3,
                "temperature_bearing": 80.0,   # anomalous
                "pressure_delta": 4.2,
                "efficiency_pct": 95.0,         # contradicts high temp
                "shaft_speed": 1475.0,
            },
            temp_celsius=45.0,
            load_ratio=0.9,
        ),
    },
}
