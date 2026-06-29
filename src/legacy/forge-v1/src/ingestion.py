"""
LAYER 1 — DATA INGESTION
=========================
Loads NASA C-MAPSS sensor data and computes RUL (Remaining Useful Life) labels.

REVERSE ENGINEER THIS FILE:
  Step 1 → Run standalone:       python -m src.ingestion
  Step 2 → Change clip_rul=50    What happens to training accuracy? Why?
  Step 3 → Remove .clip()        What does the RUL distribution look like now?
  Step 4 → Add a new sensor col  How does the pipeline downstream handle it?

KEY CONCEPT: RUL = max_cycle_for_this_engine − current_cycle
             If engine 1 runs 200 cycles total, at cycle 180 its RUL = 20.
             The model learns: "when sensors look like THIS, RUL ≈ 20."
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# C-MAPSS column schema  (26 cols: 1 id + 1 cycle + 3 settings + 21 sensors)
# ─────────────────────────────────────────────────────────────────────────────
CMAPSS_COLS = (
    ["engine_id", "cycle", "setting_1", "setting_2", "setting_3"]
    + [f"s{i}" for i in range(1, 22)]
)

# Sensors that actually carry degradation signal (others are noise)
# Source: NASA C-MAPSS paper — these 14 have high variance correlation with RUL
DEGRADING_SENSORS = ["s2", "s3", "s4", "s7", "s8", "s9",
                     "s11", "s12", "s13", "s14", "s15", "s17", "s20", "s21"]


def load_cmapss(filepath: str | Path, clip_rul: int = 130) -> pd.DataFrame:
    """
    Load a C-MAPSS training file and attach RUL labels.

    Args:
        filepath  : Path to train_FD001.txt  (whitespace-separated, no header)
        clip_rul  : Clip RUL at this value. Engines far from failure get
                    RUL=130, not 400+. Prevents model from chasing healthy noise.

    Returns:
        DataFrame with all 26 original columns + 'RUL' column.

    Download data from:
        https://www.kaggle.com/datasets/behrad3d/nasa-cmaps
    """
    df = pd.read_csv(
        filepath,
        sep=r"\s+",
        header=None,
        names=CMAPSS_COLS,
    )
    df["engine_id"] = df["engine_id"].astype(int)
    df["cycle"] = df["cycle"].astype(int)
    return _attach_rul(df, clip_rul)


def generate_synthetic_cmapss(
    n_engines: int = 30,
    max_life: int = 200,
    seed: int = 42,
    clip_rul: int = 130,
) -> pd.DataFrame:
    """
    Generate synthetic C-MAPSS-style data — NO DOWNLOAD NEEDED.

    Physics model:
      • Each engine gets a random lifespan (80 – max_life cycles).
      • 14 "degrading" sensors drift toward failure as cycle/lifespan → 1.
      • 7 "stable" sensors are pure Gaussian noise (realistic: some sensors
        don't correlate with wear at all — the model must learn to ignore them).

    Use this for:
      • Running the demo immediately (no file dependency)
      • Unit testing (deterministic with fixed seed)
      • Learning: tweak n_engines or max_life and see how model changes
    """
    np.random.seed(seed)
    rows = []

    for eng_id in range(1, n_engines + 1):
        lifespan = np.random.randint(80, max_life + 1)

        for cycle in range(1, lifespan + 1):
            health = cycle / lifespan          # 0.0 = brand new, 1.0 = about to fail
            noise  = np.random.normal(0, 0.02) # sensor measurement noise

            settings = [
                round(np.random.choice([0.0, 0.2, 0.84]), 2),  # setting_1
                round(np.random.choice([0.0, 0.7]),        2),  # setting_2
                round(np.random.choice([100.0]),            1),  # setting_3
            ]

            sensors = {}
            for i in range(1, 22):
                col = f"s{i}"
                if col in DEGRADING_SENSORS:
                    # Degrades: starts at 0.3, reaches ~0.95 near failure
                    base = 0.3 + 0.65 * health
                    sensors[col] = round(base + noise, 4)
                else:
                    # Stable: constant signal with noise
                    sensors[col] = round(0.5 + noise, 4)

            rows.append(
                [eng_id, cycle] + settings + [sensors[f"s{i}"] for i in range(1, 22)]
            )

    df = pd.DataFrame(rows, columns=CMAPSS_COLS)
    return _attach_rul(df, clip_rul)


# ─────────────────────────────────────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────────────────────────────────────

def _attach_rul(df: pd.DataFrame, clip_rul: int) -> pd.DataFrame:
    """Compute and clip RUL for each engine row."""
    max_cycles = df.groupby("engine_id")["cycle"].transform("max")
    df["RUL"] = (max_cycles - df["cycle"]).clip(upper=clip_rul)
    return df


def describe_dataset(df: pd.DataFrame) -> None:
    """Print a human-readable summary — good for sanity checking."""
    print("=" * 50)
    print("C-MAPSS DATASET SUMMARY")
    print("=" * 50)
    print(f"  Rows          : {len(df):,}")
    print(f"  Engines       : {df['engine_id'].nunique()}")
    print(f"  Avg lifespan  : {df.groupby('engine_id')['cycle'].max().mean():.0f} cycles")
    print(f"  RUL range     : {df['RUL'].min():.0f} – {df['RUL'].max():.0f}")
    print(f"  RED engines   : {(df.groupby('engine_id')['RUL'].min() < 30).sum()} "
          f"(RUL < 30 at some point)")
    print("=" * 50)


# ─────────────────────────────────────────────────────────────────────────────
# Standalone test — run: python -m src.ingestion
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing LAYER 1 — Data Ingestion")
    print("Using synthetic data (no download needed)\n")

    df = generate_synthetic_cmapss(n_engines=20, seed=42)
    describe_dataset(df)

    print(f"\nSample row (engine 1, cycle 10):")
    row = df[(df["engine_id"] == 1) & (df["cycle"] == 10)].iloc[0]
    print(f"  RUL={row['RUL']:.0f}  s2={row['s2']:.3f}  s7={row['s7']:.3f}")

    print("\n✅  Layer 1 — PASS")
