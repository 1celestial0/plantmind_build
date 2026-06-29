"""
# ── LAYER 1: DataEngineerRole (MetaGPT Level 2) ──

WHAT  : MetaGPT-aligned role that owns all Layer 1 responsibilities:
        loading, cleaning, labeling, and packaging C-MAPSS data as SensorReading messages.
WHY   : Separating data concerns from feature/model concerns follows MetaGPT's SOP pattern.
        Each role is independently testable and replaceable.
HOW   : Loads C-MAPSS, computes RUL labels, validates data quality, emits SensorReading.
WHEN  : Called at pipeline start. Re-run when new data arrives.
WHY NOT: Could merge with FeatureEngineerRole — but separate roles mean:
         (1) swapping datasets only requires changing this file,
         (2) feature logic stays clean without data loading concerns.

Reference: MetaGPT Level 2 adoption — typed messages, role boundaries, no MetaGPT runtime.
"""

from __future__ import annotations
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional

from FORGE.src.messages import SensorReading


# ══════════════════════════════════════════════════════════════
# CONSTANTS — no magic numbers
# ══════════════════════════════════════════════════════════════

# WHAT: Sensor column names as defined by Saxena & Goebel (2008)
# WHY NOT: Hardcoding index positions breaks if column order changes
SENSOR_COLS = [f's{i}' for i in range(1, 22)]          # s1..s21
SETTING_COLS = ['op_setting_1', 'op_setting_2', 'op_setting_3']
INDEX_COLS = ['engine_id', 'cycle']

# WHAT: C-MAPSS column names in order (no header in source file)
CMAPSS_COLUMNS = INDEX_COLS + SETTING_COLS + SENSOR_COLS

# WHAT: RUL clipping threshold from Saxena (2008)
# WHY: Beyond 130 cycles, sensors are in healthy baseline — no discriminative signal
# WHY NOT: Clip at max_cycle or higher — would inflate RMSE on easy early cycles
RUL_CLIP: int = 130

# WHAT: Sensors known to degrade in FD001 (verified empirically + literature)
# WHY NOT: Use all 21 — 7 are near-constant in FD001, adding noise
DEGRADING_SENSORS = ['s2', 's3', 's4', 's7', 's9', 's11',
                     's12', 's13', 's14', 's15', 's17', 's20', 's21']
# NOTE: s11 added here but verify on your data — borderline degrader in FD001
# Total: 13 sensors (literature confirms ~14 but s11 is marginal)


class DataEngineerRole:
    """
    WHAT  : The data engineering agent in PlantMind's MetaGPT-style pipeline.
    WHY   : Owns all data I/O and quality assurance — downstream roles trust this output.
    HOW   : load() → validate() → label() → emit SensorReading messages.
    WHEN  : Instantiated once per pipeline run, or once per streaming batch.
    WHY NOT: Singleton — allows multiple instances for parallel engine fleets.
    """

    def __init__(self, data_path: str = "data/CMaps/train_FD001.txt"):
        # WHAT: Path to C-MAPSS training file
        # WHY NOT: Hardcode in method — allows injection for testing with synthetic data
        self.data_path = Path(data_path)
        self._df: Optional[pd.DataFrame] = None

    def load_and_prepare(self) -> pd.DataFrame:
        """
        WHAT  : Load C-MAPSS FD001, compute RUL labels, validate quality.
        WHY   : Single entry point guarantees every caller gets validated data.
        HOW   : pandas read_csv → RUL = max_cycle - cycle → clip at 130 → validate.
        WHEN  : Call once at pipeline start. Returns cached df on repeat calls.
        WHY NOT: Could lazy-load per engine — but full dataset fits in RAM (<10 MB).
        """
        if self._df is not None:
            return self._df  # Cached

        # ── Load raw data ──
        df = pd.read_csv(
            self.data_path,
            sep=r'\s+',          # C-MAPSS uses space-separated values
            header=None,
            names=CMAPSS_COLUMNS
        )

        # ── Compute RUL labels (standard Saxena 2008 method) ──
        max_cycles = df.groupby('engine_id')['cycle'].max().rename('max_cycle')
        df = df.merge(max_cycles, on='engine_id')
        df['RUL'] = (df['max_cycle'] - df['cycle']).clip(upper=RUL_CLIP)
        df.drop(columns=['max_cycle'], inplace=True)

        # ── Remove constant sensors (FD001 specific) ──
        # WHY: s1, s5, s6, s10, s16, s18, s19 have near-zero variance in FD001
        constant_threshold = 0.001
        for col in SENSOR_COLS:
            if df[col].std() < constant_threshold:
                df.drop(columns=[col], inplace=True)

        # ── Validate ──
        assert df['RUL'].max() == RUL_CLIP, f"RUL clip failed: max={df['RUL'].max()}"
        assert (df['RUL'] < 0).sum() == 0, "Negative RUL detected"
        assert df.isnull().sum().sum() == 0, "Null values detected post-cleaning"

        self._df = df
        return df

    def get_latest_reading(self, engine_id: int) -> SensorReading:
        """
        WHAT  : Get the most recent SensorReading for a given engine.
        WHY   : Layer 2 (FeatureEngineerRole) needs per-engine readings.
        HOW   : Filter by engine_id, take max cycle, package as SensorReading.
        WHEN  : Called per engine during inference.
        WHY NOT: Return whole dataframe — breaks encapsulation; FeatureEngineerRole
                 should not access raw data directly.
        """
        df = self.load_and_prepare()
        engine_df = df[df['engine_id'] == engine_id]
        if engine_df.empty:
            raise ValueError(f"Engine {engine_id} not found in dataset")

        latest = engine_df.loc[engine_df['cycle'].idxmax()]
        sensor_values = {
            col: float(latest[col])
            for col in latest.index
            if col.startswith('s')
        }

        return SensorReading(
            engine_id=int(latest['engine_id']),
            cycle=int(latest['cycle']),
            predicted_rul=float(latest['RUL']),   # Ground truth RUL for training
            op_setting_1=float(latest.get('op_setting_1', 0)),
            op_setting_2=float(latest.get('op_setting_2', 0)),
            op_setting_3=float(latest.get('op_setting_3', 0)),
            sensor_values=sensor_values,
        )

    def get_all_readings(self) -> list[SensorReading]:
        """
        WHAT  : Get latest SensorReading for every engine in the dataset.
        WHY   : Needed for batch evaluation (fleet-level dashboard).
        HOW   : Calls get_latest_reading() for each engine_id.
        WHEN  : Used for demo fleet view in Streamlit.
        WHY NOT: Return DataFrame — breaks role contract.
        """
        df = self.load_and_prepare()
        engine_ids = df['engine_id'].unique().tolist()
        return [self.get_latest_reading(eid) for eid in engine_ids]

    def get_engine_history(self, engine_id: int) -> pd.DataFrame:
        """
        WHAT  : Full cycle history for one engine (for trajectory visualization).
        WHY   : Layer 5 (proof chart) needs full degradation history, not just latest.
        HOW   : Filter and sort by cycle.
        WHEN  : Called by ProofEngineerRole for RED→GREEN chart data.
        WHY NOT: Return SensorReading list — need native pandas for Plotly charting.
        """
        df = self.load_and_prepare()
        return df[df['engine_id'] == engine_id].sort_values('cycle').copy()
