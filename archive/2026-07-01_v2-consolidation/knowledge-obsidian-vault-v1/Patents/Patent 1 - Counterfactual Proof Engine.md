---
tags: [patent, core-ip, strongest]
created: 2026-06-20
---

# Patent 1 — Counterfactual Proof Engine
## Status: STRONGEST CLAIM · File first

## What It Covers

A method for generating proof-of-efficacy for industrial maintenance decisions. Specifically, the idea that you don't just *recommend* the fix — you *prove* it works by showing the counterfactual trajectory (what WOULD have happened if you'd applied the action at this cycle).

## The 5 Steps (claim structure)

1. Receive sensor data indicating RUL < critical threshold
2. Simulate counterfactual health trajectory for each action via [[Surrogate Twin]]
3. Compute deterministic multi-objective [[Götze Score]] for each action
4. Select highest-scoring action
5. Generate visualization of actual trajectory vs. counterfactual rescued trajectory → [[RED-GREEN Transition]]

## Prior Art Gap

- **LIME/SHAP:** explain model *predictions*, not action *outcomes*. Different claim space.
- **Prescriptive maintenance:** proposes actions without proof
- **Digital twins:** simulate the asset, don't rank or prove maintenance actions
- **All three miss:** the *unified method* of score + select + prove in one flow

## Key Evidence of Reduction to Practice

Working implementation: `FORGE/src/gotze_engine.py` → `GotzeEngine.diagnose()`
Demo output: `EngineDecision.summary()` shows before/after RUL with GREEN/RED status
The RED→GREEN chart in Streamlit is step (e) of the claim.

## Connected Nodes

- Implemented in → [[Layer 4 - Götze Engine]]
- Proof mechanism → [[Counterfactual Proof]]
- Scoring mechanism → [[Götze Score]]
- Visualization → [[RED-GREEN Transition]]
- Simulation → [[Surrogate Twin]]
- Full claim document → `FORGE/PATENT_IDEAS.md`
