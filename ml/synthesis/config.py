"""Synthesis configuration — 30 assets × 20 signals × 3 failure modes × 500 cycles.

All values here match plant-config.yaml. Sync manually if yaml changes.
"""
from __future__ import annotations
from dataclasses import dataclass, field

# ─── Asset fleet ──────────────────────────────────────────────────────────────
ASSET_TYPES = ["pump", "compressor", "motor", "bearing", "valve"]
N_ASSETS_PER_TYPE = 6   # 6 × 5 = 30 total
N_CYCLES = 500
N_SIGNALS = 20
RANDOM_SEED = 42

# ─── Failure modes ────────────────────────────────────────────────────────────
FAILURE_MODES = ["degradation", "shock", "wear"]
# degradation: standard Weibull trajectory
# shock:       sudden health drop at random cycle in [150, 350]
# wear:        stepped degradation (staircase every ~50 cycles)


# ─── Signal definitions ───────────────────────────────────────────────────────
# Each signal: name, baseline_value, direction (+1 increases / -1 decreases with degradation),
#              noise_std (fraction of baseline), sensitivity (0–1, how fast it responds)
@dataclass(frozen=True)
class SignalSpec:
    name: str
    baseline: float      # value at health = 100
    direction: float     # +1 or -1
    noise_frac: float    # noise std as fraction of baseline
    sensitivity: float   # 0–1: how much signal changes per health unit


SIGNAL_SPECS: list[SignalSpec] = [
    SignalSpec("vibration_rms",        0.5,   +1, 0.05, 0.9),
    SignalSpec("temperature_bearing",  55.0,  +1, 0.02, 0.7),
    SignalSpec("pressure_delta",       3.5,   -1, 0.03, 0.6),
    SignalSpec("current_rms",          12.0,  +1, 0.02, 0.5),
    SignalSpec("acoustic_emission",    0.3,   +1, 0.08, 0.85),
    SignalSpec("oil_viscosity",        46.0,  -1, 0.02, 0.4),
    SignalSpec("oil_contamination",    2.0,   +1, 0.10, 0.6),
    SignalSpec("shaft_speed",          1480,  -1, 0.01, 0.3),
    SignalSpec("torque",               85.0,  +1, 0.03, 0.5),
    SignalSpec("displacement_pk_pk",   0.05,  +1, 0.07, 0.8),
    SignalSpec("kurtosis",             3.0,   +1, 0.06, 0.95),  # spikes near failure
    SignalSpec("crest_factor",         1.4,   +1, 0.04, 0.75),
    SignalSpec("skewness",             0.1,   +1, 0.15, 0.5),
    SignalSpec("high_freq_energy",     0.02,  +1, 0.12, 0.80),
    SignalSpec("low_freq_energy",      0.15,  -1, 0.06, 0.4),
    SignalSpec("voltage_rms",          380.0, -1, 0.005, 0.2),
    SignalSpec("power_factor",         0.92,  -1, 0.01, 0.3),
    SignalSpec("thd_pct",              2.5,   +1, 0.05, 0.45),
    SignalSpec("efficiency_pct",       92.0,  -1, 0.01, 0.65),
    SignalSpec("impulse_factor",       1.6,   +1, 0.05, 0.88),
]

assert len(SIGNAL_SPECS) == N_SIGNALS, f"Expected {N_SIGNALS} signals, got {len(SIGNAL_SPECS)}"


# ─── Operating condition ranges per asset type ────────────────────────────────
# Each asset instance gets fixed conditions drawn from these ranges at generation time.
OPERATING_CONDITIONS: dict[str, dict[str, tuple[float, float]]] = {
    "pump":       {"temp_celsius": (20.0, 45.0), "load_ratio": (0.7, 1.2)},
    "compressor": {"temp_celsius": (25.0, 55.0), "load_ratio": (0.8, 1.15)},
    "motor":      {"temp_celsius": (20.0, 50.0), "load_ratio": (0.6, 1.1)},
    "bearing":    {"temp_celsius": (15.0, 40.0), "load_ratio": (0.8, 1.3)},
    "valve":      {"temp_celsius": (10.0, 60.0), "load_ratio": (0.5, 1.0)},
}
