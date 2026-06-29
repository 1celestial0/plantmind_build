---
tags: [ml, counterfactual, simulation]
created: 2026-06-20
---

# Surrogate Twin

## What It Is

A **surrogate twin** is a lightweight ML model that simulates how an engine's [[Remaining Useful Life]] would change if a specific maintenance action were applied at a specific cycle.

It's called "surrogate" because it *substitutes* for the real-world physical outcome (which we don't have) with a learned statistical model.

## How It Works in PlantMind

```python
# Current implementation: lookup table (sufficient for hackathon)
SURROGATE_GAIN_MAP = {
    "replace_bearing":   95.0,  # major repair → near-full life recovery
    "reduce_load":       40.0,  # operational change → partial recovery
    "flush_lubrication": 25.0,  # maintenance → moderate recovery
    "monitor_only":       5.0,  # no intervention → minimal benefit
}

# Production version: trained regression model per action
# Input:  (current_rul, action_params, engine_features)
# Output: predicted_rul_gain (how many cycles the action recovers)
```

## Why Not Use the Real Engine?

We don't have post-maintenance historical data in [[NASA C-MAPSS]]. The dataset shows run-to-failure; it doesn't show what happened after repairs. The surrogate twin is trained on domain knowledge + the structure of C-MAPSS degradation curves.

## The Production Version

In a real deployment (post-hackathon), the surrogate twin would be:
1. A regression model trained on historical repair outcomes per action type
2. One model per action × engine type combination
3. Input: `(current_sensor_readings, cycles_since_last_maintenance, operating_conditions)`
4. Output: `predicted_rul_after_action_distribution` (mean + uncertainty)

The uncertainty bound is what makes this different from a lookup table — a production twin would say "replace_bearing gives you 95 ± 12 cycles" not just "95."

## Connection to Patent Claims

The surrogate twin is the mechanism that makes [[Counterfactual Proof]] possible. Without it, you can't generate the trajectory comparison. This is cited in [[Patent 1 - Counterfactual Proof Engine]] claim step (b).

## WHAT / WHY / HOW / WHEN / WHY NOT

**WHAT:** A lightweight model that predicts RUL recovery for a given maintenance action.

**WHY:** To generate [[Counterfactual Proof]] — the "what would have happened" trajectory — without real post-repair data.

**HOW:** Currently a lookup table; production version is a per-action regression model on historical repair outcomes.

**WHEN:** Called by [[Layer 4 - Götze Engine]] for each action in the candidate set.

**WHY NOT:**
- Physics ODE model: correct but requires material constants (Young's modulus, fatigue coefficients) that C-MAPSS doesn't provide
- Exact replay of historical repairs: we don't have this data in C-MAPSS
- Single model for all actions: actions have fundamentally different RUL impact profiles; lumping them loses the per-action signal

## Connected Nodes

- Used by → [[Layer 4 - Götze Engine]]
- Output feeds → [[Götze Score]] (ΔHealth term)
- Enables → [[Counterfactual Proof]]
- Data source context → [[NASA C-MAPSS]]
- Referenced in → [[Patent 1 - Counterfactual Proof Engine]]
