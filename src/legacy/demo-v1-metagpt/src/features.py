"""
LAYER 2 — FEATURE ENGINEERING
==============================
Converts raw sensor readings into predictive features using rolling statistics.

WHY ROLLING WINDOW?
  A single sensor reading at cycle 150 tells you little.
  The TREND over the last 30 cycles tells you everything.
  Rolling mean captures: "is this sensor creeping upward?"
  Rolling std captures:  "is this sensor becoming erratic?" (erratic = failing)

REVERSE ENGINEER THIS FILE:
  Step 1 → Run standalone:          python -m src.features
  Step 2 → Change window=10         Accuracy drops. Why? (too little history)
  Step 3 → Change window=60         What happens near the start of each engine?
  Step 4 → Remove rolling std       Does model accuracy change? By how much?
  Step 5 → Add rolling min/max      Does it improve R² score in model.py?
"""

import pandas as pd
import numpy as np
from src.ingestion import DEGRADING_SENSORS

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
WINDOW_SIZE = 30          # cycles of history per feature
MIN_PERIODS = 1           # allow partial windows at engine start (don't drop rows)


def engineer_features(df: pd.DataFrame, window: int = WINDOW_SIZE) -> pd.DataFrame:
    """
    Add rolling mean and std features for each degrading sensor.

    Per engine (groupby engine_id), for each degrading sensor:
      - {sensor}_mean_30  = rolling mean over last `window` cycles
      - {sensor}_std_30   = rolling std  over last `window` cycles (0 when < 2 obs)

    Args:
        df     : DataFrame from ingestion.py (must have engine_id, cycle, s1..s21)
        window : Number of cycles for rolling statistics

    Returns:
        Original DataFrame + 2 × len(DEGRADING_SENSORS) new feature columns.
        RUL column preserved for model training.
    """
    df = df.copy()

    for sensor in DEGRADING_SENSORS:
        grouped = df.groupby("engine_id")[sensor]

        df[f"{sensor}_mean_{window}"] = grouped.transform(
            lambda x: x.rolling(window, min_periods=MIN_PERIODS).mean()
        )
        df[f"{sensor}_std_{window}"] = grouped.transform(
            lambda x: x.rolling(window, min_periods=MIN_PERIODS).std().fillna(0)
        )

    return df


def get_feature_cols(window: int = WINDOW_SIZE) -> list[str]:
    """
    Return the list of feature column names produced by engineer_features().
    Use this everywhere you need X — single source of truth.

    Example:
        X = df[get_feature_cols()]
        y = df["RUL"]
    """
    cols = []
    for sensor in DEGRADING_SENSORS:
        cols.append(f"{sensor}_mean_{window}")
        cols.append(f"{sensor}_std_{window}")
    return cols


def get_latest_snapshot(df: pd.DataFrame, engine_id: int) -> pd.Series:
    """
    Return the most recent feature row for a given engine.
    Used at inference time: "what is this engine's health RIGHT NOW?"

    Args:
        df        : Feature-engineered DataFrame
        engine_id : Which engine to query

    Returns:
        Single row (pd.Series) with all feature columns for the latest cycle.
    """
    engine_rows = df[df["engine_id"] == engine_id]
    if engine_rows.empty:
        raise ValueError(f"Engine {engine_id} not found in dataset.")
    return engine_rows.sort_values("cycle").iloc[-1]


# ─────────────────────────────────────────────────────────────────────────────
# Standalone test — run: python -m src.features
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from src.ingestion import generate_synthetic_cmapss

    print("Testing LAYER 2 — Feature Engineering")
    print(f"  Window size : {WINDOW_SIZE} cycles")
    print(f"  Sensors     : {len(DEGRADING_SENSORS)} degrading sensors")
    print(f"  Features    : {len(get_feature_cols())} total (mean + std per sensor)\n")

    df_raw = generate_synthetic_cmapss(n_engines=5, seed=42)
    df_feat = engineer_features(df_raw)

    feat_cols = get_feature_cols()
    print(f"Raw columns   : {df_raw.shape[1]}")
    print(f"Feature cols  : {df_feat.shape[1]}  (+{len(feat_cols)} new)")

    # Show how s2_mean_30 increases as engine approaches failure
    eng1 = df_feat[df_feat["engine_id"] == 1][["cycle", "RUL", "s2_mean_30", "s2_std_30"]]
    print("\nEngine 1 — feature trend (every 20 cycles):")
    print(eng1[::20].to_string(index=False))

    print("\n✅  Layer 2 — PASS")
