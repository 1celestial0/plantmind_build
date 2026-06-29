---
tags: [architecture, core-ip, layer-4]
created: 2026-06-20
---

# Layer 4 — Götze Decision Engine

## What This Layer Does

Takes every RED engine (from [[Layer 3 - Prediction]]) and outputs:
1. Root cause — which subsystem is responsible
2. Action menu — 3–4 candidate maintenance actions
3. [[Götze Score]] for each action — the deterministic ranking
4. [[Counterfactual Proof]] — visual proof the winner works

**This is the core IP of PlantMind.**

## File: `FORGE/src/gotze_engine.py`

### Key classes

| Class | Role |
|---|---|
| `MaintenanceAction` | Data class: one candidate action (cost, downtime, safety) |
| `GotzeResult` | Data class: scored result for one action |
| `EngineDecision` | Data class: full decision record for one RED engine |
| `GotzeEngine` | The engine: diagnose() → root cause + scored actions |

### The Pipeline

```
RED engine (current_rul < 30)
    → _identify_root_cause(rul) → str
    → _score_all_actions(rul)   → list[GotzeResult]
    → EngineDecision (winner = argmax(gotze_score))
    → EngineDecision.is_rescued = (current_rul + winner.rul_gain) > 30
```

### Design Rule (never break)

```
AI does uncertain work:      diagnose root cause, generate action options
Deterministic rules decide:  Götze Score picks the winner, not the AI
```

## WHAT / WHY / HOW / WHEN / WHY NOT

**WHAT:** Layer 4 of the 5-layer PlantMind architecture. The decision + proof layer.

**WHY:** Every competitor predicts failure. Nobody decides the fix AND proves it. This layer is PlantMind's differentiator.

**HOW:** (1) Rule-based root cause (LLM in production). (2) 4 candidate actions from library. (3) Götze formula scores each on 4 objectives. (4) argmax picks winner. (5) Counterfactual proof generated from [[Surrogate Twin]].

**WHEN:** Called by `run_demo.py` for each engine flagged RED by [[Layer 3 - Prediction]].

**WHY NOT:**
- Fully LLM-driven: LLM can't produce a formula that a patent office can examine
- Pure optimization: needs repair history data C-MAPSS doesn't provide
- Rule-only (no surrogate twin): can't generate counterfactual trajectories

## Connected Nodes

- Receives input from → [[Layer 3 - Prediction]]
- Computes → [[Götze Score]]
- Generates → [[Counterfactual Proof]]
- Uses → [[Surrogate Twin]]
- Sends output to → [[Layer 5 - Proof and Learn]]
- Protected by → [[Patent 1 - Counterfactual Proof Engine]]
- Protected by → [[Patent 2 - Götze Scoring Method]]
