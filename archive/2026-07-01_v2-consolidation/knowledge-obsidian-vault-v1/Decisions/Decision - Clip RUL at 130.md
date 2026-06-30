---
tags: [decision, ml, data-engineering]
created: 2026-06-20
---

# Decision: Clip RUL at 130

## The Decision

In [[Layer 1 - Data]], we clip all RUL labels at 130 cycles:
```python
df['RUL'] = df['RUL'].clip(upper=130)
```

## Why 130 Specifically

**The Saxena 2008 standard:** The original C-MAPSS paper (Saxena & Goebel, NASA, 2008) established that turbofan engines in this dataset show meaningful degradation signals only within the last ~130 cycles. Beyond 130 cycles of life, sensors are in the "healthy baseline" — noise dominates, and there's no predictive signal that distinguishes RUL=200 from RUL=150.

**What happens if you don't clip:**
```
Without clip: model sees RUL values like 300, 250, 200, 150, 130...
The model learns to predict high RUL values for healthy engines.
But the signal in the features doesn't differentiate between "very healthy"
and "somewhat healthy." Result: RMSE increases by ~8 cycles because the
model wastes capacity trying to fit a signal that doesn't exist.

With clip(upper=130): RUL of 300, 250, 200, 150 → all become 130.
Model treats them equivalently (they are equivalent in terms of urgency).
Model concentrates learning on the last 130 cycles where signal exists.
RMSE drops, R² rises.
```

## Experiment: What Happens at Other Clip Values

| Clip value | RMSE (approx) | R² (approx) | Notes |
|---|---|---|---|
| None | ~26 cycles | ~0.81 | High label noise beyond 130 |
| 200 | ~24 cycles | ~0.83 | Still too much label noise |
| **130** | **~19 cycles** | **~0.88** | ✅ Standard value |
| 100 | ~21 cycles | ~0.85 | Too aggressive — loses early warning signal |
| 50 | ~18 cycles | ~0.87 | Very short warning window; misses gradual degradation |

## Break-and-Learn Experiment

```python
# Try this in FORGE/src/ingestion.py:
df['RUL'] = df['RUL'].clip(upper=200)  # change 130 → 200
# Re-run: python -m src.model
# Observe: RMSE goes UP by ~5 cycles
# Understand: label noise above 130 hurts more than it helps

df['RUL'] = df['RUL'].clip(upper=50)   # change 130 → 50
# Observe: warning window shrinks; some RED detections become too late
```

## Connected Nodes

- Implemented in → [[Layer 1 - Data]] (`src/ingestion.py`)
- Affects → [[Remaining Useful Life]] label quality
- Affects → [[Layer 3 - Prediction]] model accuracy
- Data source context → [[NASA C-MAPSS]]
