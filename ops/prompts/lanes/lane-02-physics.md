# Lane 2 — Physics & ML Engine

Paste everything below the line into a **new chat** (Lane 2 only).

---

```
LANE 2 — Physics & ML Engine.

MISSION: Build the guaranteed-first physics core: synthetic data generator,
Weibull calibration from Kaggle (CMAPSS/PRONOSTIA), analytical health H(t) + RUL
with 95% CI, all behind PhysicsModelOutput (src/contracts/physics.py).
PINN is OPTIONAL stretch with invisible fallback to analytical model.

PRIMARY KB INPUTS: docs/architecture/07_ML_MODEL_AND_DATA.md, 04_DATA_FLOW.md,
LOCKED_STATE.md §6a (λ/β table, CYCLES_PER_DAY).

DO NOT: build agents, API, or UI. Expose ONE clean contract for Lane 1.

CONTRACT YOU OWN: PhysicsModelOutput →
{health_index, rul_estimate, confidence_interval, physics_explanation}.
Lane 1 depends on this exact shape — changes require 🔒 VAULT UPDATE.

CODE HOME: src/physics/, ml/synthesis/, ml/training/

FIRST ACTION: deliver generate_data.py (30 assets × 20 signals × 3 failure modes)
and physics/weibull.py (H(t), RUL, bootstrap CI) using LOCKED_STATE λ/β.
Park PINN until baseline validates.

Operate per AI-OPERATING-SYSTEM.md and confirmation-gate.md.
End each reply with ⏭️ NEXT ACTIONS.
```

**Source:** split from `ops/prompts/PLANTMIND_5_CHAT_PROMPTS.md` (Chat 2).