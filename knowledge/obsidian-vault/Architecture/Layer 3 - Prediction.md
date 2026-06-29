---
tags: [architecture, ml, layer-3]
created: 2026-06-20
---

# Layer 3 — RUL Prediction Model

## What This Layer Does

Takes the rolling window feature matrix (from [[Layer 2 - Features]]) and outputs a predicted [[Remaining Useful Life]] for every engine at every cycle. Engines with predicted RUL < 30 are flagged RED (see [[Asset Health]]).

## File: `FORGE/src/model.py`

### Key components

| Component | Detail |
|---|---|
| Model | `RandomForestRegressor(n_estimators=200, max_depth=15)` |
| Target | `RUL` column (clipped at 130, see [[Decision - Clip RUL at 130]]) |
| Features | All `_mean` and `_std` columns from [[Layer 2 - Features]] |
| RED threshold | `RUL < 30` cycles |
| Expected RMSE | ~18–22 cycles on C-MAPSS FD001 |
| Expected R² | ~0.87–0.91 |

## The RED Threshold

```python
RED_THRESHOLD = 30  # Why 30: see [[Decision - RED Threshold 30]]

# At every cycle, for every engine:
engine_health = "RED" if predicted_rul < RED_THRESHOLD else "GREEN"
```

## WHAT / WHY / HOW / WHEN / WHY NOT

**WHAT:** RandomForest regression model that predicts remaining useful life per engine per cycle.

**WHY:** We need a number (RUL) to trigger the Götze engine. Without prediction, we have no "RED" engines to diagnose.

**HOW:** (1) Train RF on 80% of C-MAPSS FD001. (2) At inference: pass feature row through RF, get predicted RUL. (3) Compare to threshold (30 cycles) → RED or GREEN.

**WHEN:** Called by `run_demo.py` after [[Layer 2 - Features]] produces the feature matrix.

**WHY NOT:** See [[Decision - RandomForest over LSTM]].

## Connected Nodes

- Receives input from → [[Layer 2 - Features]]
- Predicts → [[Remaining Useful Life]]
- Classifies → [[Asset Health]] (RED/GREEN)
- RED engines go to → [[Layer 4 - Götze Engine]]
- Model tracked in → [[MLflow]]
- Run on → [[Databricks]] (for demo; also runs locally)
- Rationale → [[Decision - RandomForest over LSTM]]
