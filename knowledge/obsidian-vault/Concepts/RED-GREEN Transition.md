---
tags: [demo, visualization, proof]
created: 2026-06-20
---

# RED → GREEN Transition

## The "Money Shot"

The RED→GREEN transition is the most important visual in the PlantMind demo. It shows on a single chart:

- **RED line (left):** The engine's actual degradation curve → crashes to failure at cycle ~45
- **GREEN line (right):** The counterfactual curve after the Götze winner is applied → engine survives to cycle 80+
- **Yellow dashed line:** The failure threshold (RUL = 30 cycles)

This is called the "money shot" because it proves, in 2 seconds, what PlantMind does differently from every competitor: not just predict failure, but RESCUE the asset.

## What Makes It Honest

**What's real:**
- The C-MAPSS data (real NASA dataset)
- The RUL prediction (real ML model output)
- The Götze formula computation (real deterministic math)
- The counterfactual trajectory shape (from [[Surrogate Twin]])

**What's simulated (and we say so):**
- The specific numeric values of the GREEN curve use the surrogate twin's lookup table, not a trained regression model. In a real deployment, the surrogate would be trained on thousands of historical repairs.

Saying "pre-run for demo speed, surrogate trained on domain knowledge" is the correct honest framing. Judges respect it.

## Chart Specification (for Streamlit/Plotly)

```python
# Two lines on the same axes:
# x-axis: engine cycle number
# y-axis: RUL (or health score, 0–100)

# Red trace: actual degradation from current cycle to failure
cycles_fail   = np.arange(current_cycle, current_cycle + current_rul)
rul_fail      = np.linspace(current_rul, 0, len(cycles_fail))

# Green trace: counterfactual after winner action
new_rul       = current_rul + winner.rul_gain
cycles_rescue = np.arange(current_cycle, current_cycle + new_rul)
rul_rescue    = np.linspace(new_rul, 0, len(cycles_rescue))

# Threshold line
plt.axhline(30, color='orange', linestyle='--', label='Failure threshold')
```

## WHAT / WHY / HOW / WHEN / WHY NOT

**WHAT:** A two-line Plotly chart: failing trajectory (red) vs. rescued trajectory (green).

**WHY:** Abstract numbers ("score = 0.89") don't resonate in a 5-minute demo. A chart where one line falls and one rises tells the entire PlantMind story visually and instantly.

**HOW:** Two lineplots on a shared axis. Red = actual degradation curve. Green = surrogate twin projection after action. Yellow dashed = failure threshold at RUL=30.

**WHEN:** Displayed in [[Layer 5 - Proof and Learn]] (Streamlit dashboard), after the Götze engine picks a winner.

**WHY NOT:**
- Bar chart of scores: shows comparative ranking but not the temporal rescue story
- Pie chart: wrong data type entirely
- Static image: defeats the purpose of live computation

## Connected Nodes

- Generated from → [[Counterfactual Proof]]
- Requires → [[Surrogate Twin]] for the GREEN trajectory
- Displayed in → [[Layer 5 - Proof and Learn]]
- Is the visual output of → [[Layer 4 - Götze Engine]]
- Referenced in → [[Patent 1 - Counterfactual Proof Engine]] claim step (e)
