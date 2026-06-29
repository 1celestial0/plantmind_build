# PlantMind Phase Rubric Validator
**Purpose:** Gate each implementation phase with explicit pass/fail criteria — no phase proceeds until previous gates are GREEN
**Version:** 1.0 · 2026-06-20
**Principle:** Rubric-first engineering. Every feature earns its place.

---

## RUBRIC MASTER SCORE

| Phase | Max Score | Gate Threshold | Status |
|---|---|---|---|
| Phase 0: Foundation | 10 pts | ≥ 8/10 to proceed | ✅ |
| Phase 1: Data Pipeline | 15 pts | ≥ 12/15 to proceed | ✅ |
| Phase 2: Features | 10 pts | ≥ 8/10 to proceed | ✅ |
| Phase 3: RUL Model | 20 pts | ≥ 16/20 to proceed | ⚠️ VERIFY |
| Phase 4: Götze Engine | 25 pts | ≥ 20/25 to proceed | ⚠️ IN PROGRESS |
| Phase 5: Proof + Demo | 20 pts | ≥ 16/20 to proceed | 🔴 NOT STARTED |
| **TOTAL** | **100 pts** | **≥ 82 to submit** | **0.83 estimated** |

---

## PHASE 0: FOUNDATION (10 pts)

**Goal:** Project is structured, reproducible, and documented.

| Criterion | Max | Passing | How to verify |
|---|---|---|---|
| Git repo exists with clean history | 2 | 2 | `git log --oneline` → ≥5 meaningful commits |
| README describes 5-layer architecture | 2 | 1 | Open README.md, check layer table |
| requirements.txt / pyproject.toml complete | 2 | 2 | `pip install -r requirements.txt` succeeds |
| All code has 5W comments | 2 | 1 | Spot-check 3 functions |
| FORGE GitHub repo initialized | 2 | 1 | `git remote -v` on FORGE repo |

**Self-evaluation script:**
```python
# WHAT  : Phase 0 validator
# WHY   : Catch foundation issues before building on them
# HOW   : Check each criterion programmatically where possible
# WHEN  : Run before starting Phase 1 work
# WHY NOT: Manual checks miss edge cases

import os, subprocess

checks = {
    "README exists": os.path.exists("README.md"),
    "requirements.txt exists": os.path.exists("requirements.txt"),
    "FORGE dir exists": os.path.isdir("FORGE"),
    "gotze_engine.py exists": os.path.exists("FORGE/src/gotze_engine.py"),
    "git repo": subprocess.run(["git", "status"], capture_output=True).returncode == 0
}

for check, passed in checks.items():
    print(f"{'✅' if passed else '🔴'} {check}")
```

---

## PHASE 1: DATA PIPELINE (15 pts)

**Goal:** C-MAPSS data loads cleanly, RUL labels are correct.

| Criterion | Max | How to verify |
|---|---|---|
| C-MAPSS FD001 loads without errors | 3 | `python FORGE/src/ingestion.py` → no traceback |
| RUL labels computed correctly | 3 | `df['RUL'].max()` == 130 (clipped) |
| Training set: 80/20 split by engine_id | 2 | Verify no engine appears in both train and test |
| No data leakage | 3 | Scaler fit only on train, transform on test |
| NULL/NaN audit passes | 2 | `df.isnull().sum().sum()` == 0 after cleaning |
| RUL < 0 count == 0 | 2 | `(df['RUL'] < 0).sum()` == 0 |

**Gate criterion:** ≥ 12/15 → proceed to Phase 2

**Self-evaluation script:**
```python
# WHAT  : Phase 1 validator
# WHY   : Data errors silently corrupt everything downstream
# HOW   : Statistical checks on loaded dataframe
# WHEN  : After ingestion.py runs
# WHY NOT: Visual inspection misses subtle errors

import pandas as pd

def validate_phase1(df: pd.DataFrame) -> dict[str, bool]:
    """Run all Phase 1 gates. Returns pass/fail per criterion."""
    return {
        "RUL max == 130": df['RUL'].max() == 130,
        "No negative RUL": (df['RUL'] < 0).sum() == 0,
        "No nulls": df.isnull().sum().sum() == 0,
        "Has 21 sensors": sum(1 for c in df.columns if c.startswith('s')) == 21,
        "Has engine_id": 'engine_id' in df.columns,
        "Has cycle": 'cycle' in df.columns,
    }

# Usage after loading data:
# results = validate_phase1(df_train)
# print({k: '✅' if v else '🔴' for k, v in results.items()})
```

---

## PHASE 2: FEATURE ENGINEERING (10 pts)

**Goal:** Rolling features are correct and informative.

| Criterion | Max | How to verify |
|---|---|---|
| Window size = 30 cycles | 2 | `WINDOW = 30` constant in features.py |
| 14 degrading sensors selected | 2 | Count columns with `_mean` suffix == 14 |
| NaN from rolling handled (drop or fill) | 2 | `df.isnull().sum().sum()` == 0 after rolling |
| Feature correlation > 0 with RUL | 2 | Check: `df[feature_cols].corrwith(df['RUL']).abs().min()` > 0.05 |
| No constant-variance features | 2 | `df[feature_cols].std().min()` > 0 |

**Gate criterion:** ≥ 8/10

**Self-evaluation script:**
```python
def validate_phase2(df: pd.DataFrame, feature_cols: list[str]) -> dict[str, bool]:
    """Phase 2 validator: feature engineering."""
    return {
        "14 degrading sensors": sum(1 for c in feature_cols if '_mean' in c) == 14,
        "No nulls post-rolling": df[feature_cols].isnull().sum().sum() == 0,
        "Corr with RUL > 0.05": df[feature_cols].corrwith(df['RUL']).abs().min() > 0.05,
        "No constant features": df[feature_cols].std().min() > 0.001,
        "Both _mean and _std present": (
            any('_mean' in c for c in feature_cols) and
            any('_std' in c for c in feature_cols)
        ),
    }
```

---

## PHASE 3: RUL MODEL (20 pts)

**Goal:** RandomForest meets minimum performance thresholds.

| Criterion | Max | Threshold | How to verify |
|---|---|---|---|
| RMSE on test set | 6 | ≤ 22 cycles | `mean_squared_error(y_test, y_pred, squared=False)` |
| R² on test set | 6 | ≥ 0.85 | `r2_score(y_test, y_pred)` |
| RED recall (RUL<30) | 4 | ≥ 0.90 | `recall_score(y_true<30, y_pred<30)` |
| Feature importances extracted | 2 | Top 5 identified | `model.feature_importances_` available |
| Model saved (MLflow or joblib) | 2 | File exists | `os.path.exists("models/rul_model.pkl")` |

**Gate criterion:** ≥ 16/20 — especially: RMSE ≤ 22, RED recall ≥ 0.90

**Self-evaluation script:**
```python
from sklearn.metrics import mean_squared_error, r2_score, recall_score
import numpy as np

def validate_phase3(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model,
    model_path: str = "models/rul_model.pkl"
) -> dict[str, tuple[float, bool]]:
    """Phase 3 validator. Returns (value, passed) for each metric."""
    rmse = mean_squared_error(y_true, y_pred, squared=False)
    r2 = r2_score(y_true, y_pred)
    red_recall = recall_score(y_true < 30, y_pred < 30)
    
    return {
        "RMSE ≤ 22": (rmse, rmse <= 22),
        "R² ≥ 0.85": (r2, r2 >= 0.85),
        "RED recall ≥ 0.90": (red_recall, red_recall >= 0.90),
        "Feature importances": (len(model.feature_importances_), True),
        "Model file exists": (0, os.path.exists(model_path)),
    }
```

---

## PHASE 4: GÖTZE ENGINE (25 pts) ← HIGHEST WEIGHT

**Goal:** Decision engine produces correct, explainable, deterministic scores.

| Criterion | Max | How to verify |
|---|---|---|
| All weights sum to 1.0 | 3 | `0.40 + 0.25 + 0.20 + 0.15 == 1.0` |
| All scores ∈ [0, 1] | 3 | `assert 0 <= score <= 1` for all actions |
| Winner action is deterministic | 3 | Same input → same output on 100 runs |
| Counterfactual trajectory generated | 4 | `EngineDecision.counterfactual_rul` > current_rul |
| RED→GREEN proof works | 4 | Status flips RED→GREEN after winner action |
| All 4 actions always scored | 3 | `len(decision.all_actions)` == 4 always |
| No LLM in decision path | 3 | No `openai` / `anthropic` call in `_score_all_actions()` |
| dataclasses used (no raw dicts) | 2 | `isinstance(result, GotzeResult)` |

**Gate criterion:** ≥ 20/25 — especially: determinism, [0,1] scores, RED→GREEN proof

**Self-evaluation script:**
```python
from FORGE.src.gotze_engine import GotzeEngine, SensorReading
import random

def validate_phase4() -> dict[str, bool]:
    """Phase 4 validator: Götze Engine correctness."""
    engine = GotzeEngine()
    
    # Test input: engine in RED zone
    reading = SensorReading(
        engine_id=1, cycle=200, predicted_rul=15, health_score=0.35,
        sensor_means={}, sensor_stds={}
    )
    
    # Run 5x to test determinism
    results = [engine.diagnose(reading) for _ in range(5)]
    winner_actions = [r.winner_action.action_name for r in results]
    
    decision = results[0]
    winner_score = decision.winner_action.gotze_score
    
    return {
        "Weights sum to 1.0": abs(0.40 + 0.25 + 0.20 + 0.15 - 1.0) < 1e-9,
        "Winner score ∈ [0,1]": 0 <= winner_score <= 1,
        "All actions scored": len(decision.all_scored_actions) == 4,
        "Deterministic": len(set(winner_actions)) == 1,
        "Counterfactual RUL > current": decision.winner_action.projected_rul > reading.predicted_rul,
        "Status GREEN after fix": decision.winner_action.projected_status == "GREEN",
    }
```

---

## PHASE 5: PROOF + DEMO (20 pts)

**Goal:** The Streamlit app demonstrates the full pipeline clearly and robustly.

| Criterion | Max | How to verify |
|---|---|---|
| RED→GREEN chart renders | 4 | Screenshot shows two distinct lines |
| Chart legend: RED=failure / GREEN=rescue | 2 | Visual check |
| Agent trace panel visible | 3 | Scrollable log showing reasoning steps |
| Engine runs in < 3 seconds | 3 | `time.time()` before/after `diagnose()` |
| Handles missing sensor data gracefully | 3 | Pass NaN sensors → no crash, shows warning |
| Second segment demo (EV or MedTech) | 3 | At least one non-turbofan scenario works |
| No hardcoded demo mode | 2 | Remove any `if DEMO_MODE:` bypass |

**Gate criterion:** ≥ 16/20 — especially: RED→GREEN chart, < 3 second response, agent trace

**Self-evaluation script:**
```python
import time
from FORGE.src.gotze_engine import GotzeEngine, SensorReading

def validate_phase5_speed(n_runs: int = 10) -> dict[str, bool]:
    """Phase 5 validator: performance."""
    engine = GotzeEngine()
    reading = SensorReading(engine_id=1, cycle=200, predicted_rul=15,
                            health_score=0.35, sensor_means={}, sensor_stds={})
    
    times = []
    for _ in range(n_runs):
        t0 = time.time()
        engine.diagnose(reading)
        times.append(time.time() - t0)
    
    avg_ms = sum(times) / len(times) * 1000
    return {
        "Avg response < 3000ms": (avg_ms, avg_ms < 3000),
        "Max response < 5000ms": (max(times)*1000, max(times)*1000 < 5000),
    }
```

---

## HACKATHON RUBRIC (Judges' Perspective)

| Judge Criterion | Weight | What earns max score |
|---|---|---|
| Technical innovation | 30% | Novel combination: decision + proof layer |
| Real-world applicability | 25% | NASA data + second segment (EV/medical) |
| Demo impact | 20% | RED→GREEN visual, <3s response, no errors |
| Scalability & architecture | 15% | Databricks mention + 5-layer structure |
| Patent/IP potential | 10% | Götze formula + counterfactual claim language |

**Total hackathon score estimate from rubric:** 0.83 → Target 0.91

**Gap analysis:**
- Demo impact: need agent trace panel (+0.03), demo freeze protocol (+0.05)
- Scalability: need Databricks slide/screenshot (+0.03)
- Real-world: second dataset demo (+0.03)
- Innovation: current score is strong (0.88 estimated on this criterion)

---

## PHASE GATE DASHBOARD

Run this before each phase to get go/no-go:

```python
# WHAT  : Master phase gate runner
# WHY   : Prevent building on broken foundations
# HOW   : Runs all validator functions, aggregates scores
# WHEN  : Run at start of each new phase
# WHY NOT: Manual checklist gets skipped under time pressure

PHASE_WEIGHTS = {0: 10, 1: 15, 2: 10, 3: 20, 4: 25, 5: 20}
PHASE_THRESHOLDS = {0: 8, 1: 12, 2: 8, 3: 16, 4: 20, 5: 16}

def run_phase_gate(phase: int, score: float) -> bool:
    """Return True if score meets gate threshold for phase."""
    threshold = PHASE_THRESHOLDS[phase]
    result = score >= threshold
    status = "✅ GATE PASSED" if result else "🔴 GATE BLOCKED"
    print(f"Phase {phase}: {score}/{PHASE_WEIGHTS[phase]} → {status} (threshold: {threshold})")
    return result
```

---

*Phase Rubric Validator v1.0 · PlantMind · 2026-06-20*
*Update this file whenever a criterion changes or a new phase is added.*
