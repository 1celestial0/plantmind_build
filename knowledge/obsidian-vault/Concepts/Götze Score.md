---
tags: [core-ip, formula, decision-engine]
created: 2026-06-20
---

# Götze Score

## The Formula

```
G = w₁·ΔHealth + w₂·(1−NormCost) + w₃·(1−NormTime) + w₄·Safety

Default weights:
  w₁ = 0.40  (health gain is primary objective)
  w₂ = 0.25  (cost matters, but less than life extension)
  w₃ = 0.20  (downtime matters)
  w₄ = 0.15  (safety is a floor constraint)

Constraint: w₁ + w₂ + w₃ + w₄ = 1.0 (exactly)
Output range: G ∈ [0, 1] for all valid inputs
```

## What Each Term Means

| Term | Formula | Meaning |
|---|---|---|
| ΔHealth | `min(rul_gain / 130.0, 1.0)` | How much RUL the action recovers, normalised |
| (1−NormCost) | `1 - (cost_usd / max_cost_in_set)` | Cheapest action scores 1.0, most expensive scores 0 |
| (1−NormTime) | `1 - (downtime_hr / max_downtime_in_set)` | Fastest action scores 1.0 |
| Safety | `action.safety_score` | Pre-assigned [0,1]; 0=risky, 1=fully safe |

## Why This Design is Novel

Most maintenance systems either:
- Let an LLM pick the best action (not auditable)
- Optimize a single objective like cost (misses tradeoffs)

Götze Score is **multi-objective + deterministic + explainable**. When a judge asks "why action 2?" the answer is always a number. No black box.

## WHAT / WHY / HOW / WHEN / WHY NOT

**WHAT:** A weighted sum that ranks maintenance actions on 4 objectives simultaneously.

**WHY:** Industrial decisions need to be auditable. A plant manager must justify every maintenance choice to regulators. LLM outputs can't be put in a court document. Götze Score can.

**HOW:** Normalize each objective to [0,1], multiply by weight, sum. The `assert weights.sum() == 1.0` guarantees scores stay in [0,1].

**WHEN:** Called by [[Layer 4 - Götze Engine]] for every RED engine (see [[Asset Health]]).

**WHY NOT:**
- Genetic algorithm: correct approach in production, but needs 100+ historical repairs per action to optimize the Pareto front. C-MAPSS doesn't provide repair history.
- Softmax normalization: squashes differences, makes all actions look similar. We need clear differentiation.
- Equal weights (0.25 each): tried it — monitor_only action scores too high because it's cheap and fast, even though it gives nearly zero RUL gain.

## Connected Nodes

- Powers → [[Counterfactual Proof]]
- Computed in → [[Layer 4 - Götze Engine]]
- Protected by → [[Patent 1 - Counterfactual Proof Engine]]
- Protected by → [[Patent 2 - Götze Scoring Method]]
- Design rationale → [[Decision - Deterministic over LLM Scoring]]
- Source: `FORGE/src/gotze_engine.py` → `GotzeEngine._score_all_actions()`
