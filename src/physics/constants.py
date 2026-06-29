"""LOCKED_STATE §6a — physics constants. Change only via VAULT UPDATE."""
from __future__ import annotations

CYCLES_PER_DAY: float = 6.0
H_FAILURE_THRESHOLD: float = 20.0

# Arrhenius
BOLTZMANN_EV: float = 8.617_333e-5   # eV/K
ACTIVATION_ENERGY_EV: float = 0.15   # EA [ESTIMATE]
T_REF_K: float = 298.15              # 25 °C reference

# Load exponent (power law)
LOAD_EXPONENT: float = 2.0           # m [ESTIMATE]

# Corrected Weibull params per asset type.
# λ [ESTIMATE] — replace with calibrate_weibull.py MLE output when ready.
# Calibrated so H hits H_FAILURE_THRESHOLD within life_ref ± 15% cycles at S=1.
ASSET_PARAMS: dict[str, dict[str, float]] = {
    "pump":       {"lambda_": 1.49e-6, "beta": 2.3, "life_ref": 420.0},
    "compressor": {"lambda_": 1.83e-5, "beta": 1.9, "life_ref": 400.0},
    "motor":      {"lambda_": 5.98e-8, "beta": 2.8, "life_ref": 450.0},
    "bearing":    {"lambda_": 2.01e-9, "beta": 3.5, "life_ref": 350.0},
    "valve":      {"lambda_": 1.53e-4, "beta": 1.5, "life_ref": 480.0},
}

ASSET_TYPES: list[str] = list(ASSET_PARAMS.keys())
