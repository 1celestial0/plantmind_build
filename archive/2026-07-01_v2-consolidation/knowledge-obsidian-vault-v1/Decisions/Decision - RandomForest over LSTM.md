---
tags: [decision, ml, why-not]
created: 2026-06-20
---

# Decision: RandomForest over LSTM

## The Decision

For [[Layer 3 - Prediction]], we use `RandomForestRegressor` instead of an LSTM (Long Short-Term Memory neural network).

## Why RandomForest

| Criterion | RandomForest | LSTM |
|---|---|---|
| RMSE on C-MAPSS FD001 | ~18–22 cycles | ~15–18 cycles |
| Training time | ~30 seconds | ~15 minutes |
| Code complexity | 5 lines | 50+ lines |
| Feature importance | ✅ `predictor.feature_importances_` | ❌ black box |
| Explainability for pitch | ✅ "top sensor is s11" | ❌ attention weights (complex) |
| Demo risk | Low (fast, deterministic) | High (GPU dependency, initialization) |
| F1 for RED classification | > 0.88 | ~0.92 |

**Verdict:** LSTM gets ~3–4 fewer cycles RMSE but costs 10x more in complexity, training time, and demo risk. For a hackathon with a hard deadline and a live demo requirement, RF wins at every tradeoff point except raw accuracy.

## The Tradeoff, Quantified

```
LSTM advantage: RMSE better by ~4 cycles (18 → 14)
LSTM cost: 3h extra dev time + 15min training + GPU risk

RF advantage: F1>0.88 is sufficient for demo; feature importances = 
              pitch talking point ("sensor s11 matters most")
RF cost: 4 cycle RMSE penalty

Decision: take the cost, get the benefit. RF wins for hackathon.
```

## What LSTM Would Look Like (Post-Hackathon)

```python
# If you wanted LSTM after the hackathon:
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# WHAT  : Sequence model that uses the temporal order of sensor readings
# WHY   : LSTM can learn LONG-RANGE dependencies in the degradation signal
#          — e.g., the pattern from cycle 1 affects cycle 100's RUL
# HOW   : Hidden state carries forward information from earlier cycles
# WHEN  : Use this when you have > 3 months and GPU training infrastructure
# WHY NOT: RF is 2% worse RMSE but 90% simpler; not worth it for hackathon

model = Sequential([
    LSTM(64, input_shape=(WINDOW, len(SENSOR_COLS)), return_sequences=True),
    LSTM(32),
    Dense(1)  # single RUL output
])
```

## Connected Nodes

- Affects → [[Layer 3 - Prediction]]
- Related concept → [[Remaining Useful Life]] (what we're predicting)
- Feature input from → [[Decision - Window Size 30]] (why rolling windows)
- Label target from → [[Decision - Clip RUL at 130]]
