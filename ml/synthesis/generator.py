"""Physics-seeded synthetic sensor data generator.

Produces:
    ml/data/synthetic/
        assets_manifest.csv   — one row per asset (id, type, failure_mode, λ, β, temp, load)
        sensor_data.parquet   — N_ASSETS × N_CYCLES rows, N_SIGNALS + meta columns
        sensor_data.csv       — same data as CSV (for quick inspection)

Usage:
    python -m ml.synthesis.generator
    python -m ml.synthesis.generator --cycles 200 --seed 0 --out ml/data/synthetic
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np
import pandas as pd

from src.physics.constants import ASSET_PARAMS, CYCLES_PER_DAY, H_FAILURE_THRESHOLD
from src.physics.stress import composite_stress
from src.physics.weibull import health_at
from .config import (
    ASSET_TYPES,
    FAILURE_MODES,
    N_ASSETS_PER_TYPE,
    N_CYCLES,
    OPERATING_CONDITIONS,
    RANDOM_SEED,
    SIGNAL_SPECS,
)


def _signal_value(
    spec,
    health: float,
    rng: np.random.Generator,
) -> float:
    """Generate one signal reading given current health."""
    # degradation_fraction: how far health has fallen (0 at H=100, 1 at H=0)
    degraded = (100.0 - health) / 100.0
    # scale shift: sensitivity × direction × degraded × baseline
    shift = spec.sensitivity * spec.direction * degraded * spec.baseline
    noise = rng.normal(0, spec.noise_frac * spec.baseline)
    return round(spec.baseline + shift + noise, 6)


def _kurtosis_spike(cycle: float, n_cycles: int, base_health: float) -> float:
    """Extra kurtosis boost in final 10% of life to simulate impulsive faults."""
    if base_health < 30.0:
        return float(rng_global.exponential(2.0))
    return 0.0


def _apply_failure_mode(
    health_trace: np.ndarray,
    mode: str,
    rng: np.random.Generator,
) -> np.ndarray:
    """Modify a standard health trace to reflect a failure mode."""
    n = len(health_trace)
    if mode == "degradation":
        return health_trace  # standard Weibull

    if mode == "shock":
        shock_cycle = rng.integers(int(n * 0.3), int(n * 0.7))
        drop = rng.uniform(15.0, 35.0)
        modified = health_trace.copy()
        modified[shock_cycle:] = np.maximum(0.0, modified[shock_cycle:] - drop)
        return modified

    if mode == "wear":
        step_interval = rng.integers(40, 70)
        modified = health_trace.copy()
        steps = np.arange(0, n, step_interval)
        for s in steps[1:]:
            drop = rng.uniform(3.0, 8.0)
            modified[s:] = np.maximum(0.0, modified[s:] - drop)
        return modified

    raise ValueError(f"Unknown failure mode: {mode}")


rng_global = np.random.default_rng(RANDOM_SEED)


def build_asset_manifest(
    n_assets_per_type: int = N_ASSETS_PER_TYPE,
    n_cycles: int = N_CYCLES,
    rng: np.random.Generator | None = None,
) -> pd.DataFrame:
    """Generate fleet metadata — one row per asset."""
    rng = rng or np.random.default_rng(RANDOM_SEED)
    rows = []
    asset_id = 0
    for asset_type in ASSET_TYPES:
        temp_range = OPERATING_CONDITIONS[asset_type]["temp_celsius"]
        load_range = OPERATING_CONDITIONS[asset_type]["load_ratio"]
        params = ASSET_PARAMS[asset_type]
        for i in range(n_assets_per_type):
            temp = float(rng.uniform(*temp_range))
            load = float(rng.uniform(*load_range))
            failure_mode = FAILURE_MODES[i % len(FAILURE_MODES)]
            rows.append(
                {
                    "asset_id": f"{asset_type}_{i:02d}",
                    "asset_type": asset_type,
                    "failure_mode": failure_mode,
                    "temp_celsius": round(temp, 2),
                    "load_ratio": round(load, 3),
                    "lambda_": params["lambda_"],
                    "beta": params["beta"],
                    "life_ref_cycles": params["life_ref"],
                    "cycles_per_day": CYCLES_PER_DAY,
                    "h_failure_threshold": H_FAILURE_THRESHOLD,
                }
            )
            asset_id += 1
    return pd.DataFrame(rows)


def generate_sensor_data(
    manifest: pd.DataFrame,
    n_cycles: int = N_CYCLES,
    rng: np.random.Generator | None = None,
) -> pd.DataFrame:
    """Generate sensor readings for all assets across all cycles."""
    rng = rng or np.random.default_rng(RANDOM_SEED + 1)
    all_rows = []
    signal_names = [s.name for s in SIGNAL_SPECS]

    for _, asset in manifest.iterrows():
        s_factor = composite_stress(asset["temp_celsius"], asset["load_ratio"])
        lam = asset["lambda_"]
        beta = asset["beta"]

        # Base health trace from Weibull
        health_trace = np.array(
            [health_at(float(c), lam, beta, s_factor) for c in range(n_cycles)]
        )
        # Apply failure mode modification
        health_trace = _apply_failure_mode(health_trace, asset["failure_mode"], rng)

        for cycle_idx, health in enumerate(health_trace):
            row: dict = {
                "asset_id": asset["asset_id"],
                "asset_type": asset["asset_type"],
                "failure_mode": asset["failure_mode"],
                "cycle": cycle_idx,
                "day": round(cycle_idx / CYCLES_PER_DAY, 2),
                "health_true": round(float(health), 2),
                "rul_days_true": round(
                    max(0.0, _t_fail_safe(lam, beta, s_factor) - cycle_idx) / CYCLES_PER_DAY,
                    2,
                ),
            }
            for spec in SIGNAL_SPECS:
                val = _signal_value(spec, float(health), rng)
                # Extra kurtosis spike near end-of-life
                if spec.name == "kurtosis" and health < 30.0:
                    val += float(rng.exponential(1.5))
                row[spec.name] = round(val, 6)
            all_rows.append(row)

    meta_cols = ["asset_id", "asset_type", "failure_mode", "cycle", "day",
                 "health_true", "rul_days_true"]
    return pd.DataFrame(all_rows, columns=meta_cols + signal_names)


def _t_fail_safe(lam: float, beta: float, s: float) -> float:
    try:
        return (math.log(100.0 / H_FAILURE_THRESHOLD) / (lam * s)) ** (1.0 / beta)
    except (ZeroDivisionError, ValueError):
        return float("inf")


def run(
    n_assets_per_type: int = N_ASSETS_PER_TYPE,
    n_cycles: int = N_CYCLES,
    seed: int = RANDOM_SEED,
    out_dir: str = "ml/data/synthetic",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate and save all synthetic data. Returns (manifest, sensor_df)."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    rng_m = np.random.default_rng(seed)
    rng_s = np.random.default_rng(seed + 1)

    manifest = build_asset_manifest(n_assets_per_type, n_cycles, rng_m)
    sensor_df = generate_sensor_data(manifest, n_cycles, rng_s)

    manifest.to_csv(out / "assets_manifest.csv", index=False)
    sensor_df.to_parquet(out / "sensor_data.parquet", index=False)
    sensor_df.to_csv(out / "sensor_data.csv", index=False)

    print(f"Saved {len(manifest)} assets × {n_cycles} cycles = {len(sensor_df)} rows")
    print(f"Output: {out.resolve()}")
    return manifest, sensor_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PlantMind synthetic sensor data")
    parser.add_argument("--assets-per-type", type=int, default=N_ASSETS_PER_TYPE)
    parser.add_argument("--cycles", type=int, default=N_CYCLES)
    parser.add_argument("--seed", type=int, default=RANDOM_SEED)
    parser.add_argument("--out", type=str, default="ml/data/synthetic")
    args = parser.parse_args()
    run(args.assets_per_type, args.cycles, args.seed, args.out)
