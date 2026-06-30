---
tags: [ml, prediction, concept]
created: 2026-06-20
---

# Remaining Useful Life (RUL)

## Definition

**RUL** = the number of operational cycles remaining before an asset (turbofan engine) reaches functional failure.

```
RUL at cycle t = max_cycle_for_this_engine - t

Example:
  Engine 1 runs to cycle 300 (then fails)
  At cycle 50: RUL = 300 - 50 = 250 (plenty of life left)
  At cycle 280: RUL = 300 - 280 = 20 (CRITICAL — RED)
```

## The Label Problem

C-MAPSS provides run-to-failure data. The RUL label is computed from the data, not measured. This means:
- We know exactly when the engine failed (end of the file)
- Working backwards gives us the RUL at every cycle

**Clipping at 130:** See [[Decision - Clip RUL at 130]]. Beyond 130 cycles of life, the sensor readings are in the "healthy baseline" region — they don't discriminate between healthy states. Including them as high RUL values misleads the regression model.

## How PlantMind Uses RUL

1. [[Layer 3 - Prediction]] predicts RUL from sensor features
2. If predicted RUL < 30 → engine status = RED (see [[Asset Health]])
3. [[Layer 4 - Götze Engine]] takes RED engines and computes what action recovers the most RUL (ΔHealth term in [[Götze Score]])

## WHAT / WHY / HOW / WHEN / WHY NOT

**WHAT:** A scalar (number of cycles) representing how much operational life remains before failure.

**WHY:** Maintenance engineers need a number, not just "high risk." RUL = "you have 20 cycles → about 20 hours" is actionable. "Anomaly score = 0.87" is not.

**HOW:** Regression problem. Features (rolling sensor statistics from [[Layer 2 - Features]]) → ML model → RUL prediction. See [[Layer 3 - Prediction]].

**WHEN:** Predicted at every cycle for every engine in the dataset.

**WHY NOT:**
- Binary classification (fail/not-fail): loses the time dimension — doesn't tell you HOW SOON
- Anomaly score: not interpretable in engineering units
- Physics-based RUL (Arrhenius model): requires material constants we don't have

## Connected Nodes

- Data source → [[NASA C-MAPSS]]
- Computed in → [[Layer 1 - Data]]
- Predicted by → [[Layer 3 - Prediction]]
- Triggers → [[Asset Health]] classification
- Recovery estimated by → [[Surrogate Twin]] (ΔHealth in [[Götze Score]])
- Label design → [[Decision - Clip RUL at 130]]
