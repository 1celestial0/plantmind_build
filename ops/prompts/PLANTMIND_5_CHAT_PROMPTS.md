# PlantMind × Götze Engine — 5 PARALLEL CHAT PROMPTS
> Open 5 chats in the project. Paste one prompt per chat. Each is self-propagating: it ends every reply with `⏭️ NEXT ACTIONS` so you always know the next move. All inherit the project custom instruction (lane discipline, vault updates, no-fabrication).

**The 5 lanes (non-overlapping):**
1. Backend Core & Agents — the brain
2. Physics & ML Engine — the doctor's brain
3. Dashboard, UI & Mockups — the face
4. Databricks Parallel Port — the production twin
5. Demo, Pitch, Governance & ROI — win the room

---

## ═══ CHAT 1 — BACKEND CORE & AGENTS (The Brain) ═══

```
LANE 1 — Backend Core & Agents.

MISSION: Build the runnable Python backend — the shared PlantMindState, the
LangGraph/CrewAI orchestrator, the 5 agents (DataSentinel, AssetHealthOracle,
GötzeEngine, RootCauseAnalyst, ExecutiveSummarizer), the IIS scorer, FastAPI
endpoints, and the SQLite audit writer.

PRIMARY KB INPUTS: 06_AGENTS, 05_RUNTIME_AND_AGENTIC_WORKFLOW, 03_ARCHITECTURE, LOCKED_STATE.

DO NOT: implement physics internals (Lane 2 owns PhysicsModelInterface) or build
UI (Lane 3). Call physics via its contract; expose clean JSON for the UI.

CONTRACTS YOU OWN: the UI-consumed JSON (GötzeDecision + AssetHealthReport +
ExecutiveBrief) and the AuditRecord writer. If you change either, emit a VAULT UPDATE.
CONTRACTS YOU CONSUME: PhysicsModelInterface (from Lane 2).

FIRST ACTION: produce the repo scaffold + PlantMindState (Pydantic v2) + the
orchestrator skeleton + 5 agent stubs with correct signatures and graceful-failure
wrappers. Real, runnable files. Then we fill agents one by one.

Operate per the project custom instruction.
```

---

## ═══ CHAT 2 — PHYSICS & ML ENGINE (The Doctor's Brain) ═══

```
LANE 2 — Physics & ML Engine.

MISSION: Build the guaranteed-first physics core: synthetic data generator,
Weibull calibration from Kaggle (CMAPSS/PRONOSTIA), analytical health H(t) + RUL
with 95% CI, all behind a clean PhysicsModelInterface. PINN is an OPTIONAL stretch
with a no-visible-difference fallback to the analytical model.

PRIMARY KB INPUTS: 07_ML_MODEL_AND_DATA, 04_DATA_FLOW, LOCKED_STATE.

DO NOT: build agents, API, or UI. Expose ONE clean contract for Lane 1 to call.

CONTRACT YOU OWN: PhysicsModelInterface →
{health_index, rul_estimate, confidence_interval, physics_explanation}.
Lane 1 depends on this exact shape — changes require a VAULT UPDATE.

FIRST ACTION: deliver generate_data.py (30 assets × 20 signals × 3 failure modes)
and physics/weibull.py (H(t), RUL, bootstrap CI) wired behind PhysicsModelInterface,
using pre-calibrated λ/β. Keep the PINN explicitly parked until the baseline is solid.

Operate per the project custom instruction.
```

---

## ═══ CHAT 3 — DASHBOARD, UI & MOCKUPS (The Face) ═══

```
LANE 3 — Dashboard, UI & Mockups.

MISSION: Design then build what judges see — Streamlit + Plotly: live plant overview,
sensor/health charts, the ONE-best-action panel (IIS + runner-up + reason), and the
audit/lineage/integrity views. Mockups first so the team aligns visually, then live
screens wired to Lane 1's JSON.

PRIMARY KB INPUTS: 08_DEMO_SCENARIOS, 09_LOGGING_AND_AUDIT, 05_RUNTIME, LOCKED_STATE.

DO NOT: build backend logic or physics. Render from the JSON contract only.

CONTRACT YOU CONSUME: the UI JSON (GötzeDecision + AssetHealthReport + ExecutiveBrief).
If you need a field that isn't there, specify it precisely and emit a VAULT UPDATE so
Lane 1 adds it.

FIRST ACTION: text/wireframe mockups of the 3 key screens (Plant Overview, Decision/
One-Best-Action, Audit & Lineage) with exact layout, components, and which JSON field
feeds each element. Then we build the Streamlit shell.

Operate per the project custom instruction.
```

---

## ═══ CHAT 4 — DATABRICKS PARALLEL PORT (The Production Twin) ═══

```
LANE 4 — Databricks Parallel Port.

MISSION: Using the Databricks KB, mirror the local build on Databricks-native services
(Auto Loader + DLT for Bronze/Silver/Gold, Feature Store, MLflow, Unity Catalog,
Vector Search, Mosaic AI Agents) by REUSING the Layer-0 contracts — maximum shared
codebase, minimum rewrite. Produce a runbook + notebooks that stay 1:1 with the local
flow.

PRIMARY KB INPUTS: PlantMind-Databricks KB, 03_ARCHITECTURE, 07_ML_MODEL_AND_DATA, LOCKED_STATE.

DO NOT: invent new contracts. Bind the SAME Layer-0 interfaces to Databricks services.
Flag every GA-status caveat. Mark anything not free-tier-testable.

FIRST ACTION: produce the reusable-vs-Databricks-specific code boundary map (which
modules port unchanged, which get a thin Databricks adapter) + the parallel runbook
skeleton with the contract→service mapping table. Then notebook-by-notebook.

Operate per the project custom instruction.
```

---

## ═══ CHAT 5 — DEMO, PITCH, GOVERNANCE & ROI (Win the Room) ═══

```
LANE 5 — Demo, Pitch, Governance & ROI.

MISSION: Package the win — the scenario injector spec, the rehearsed 5-minute script
with a judge-question bank, the interactive ROI calculator, the governance/audit
narrative, and the honest novelty/prior-art note. You stress-test and sell; you do not
build core code.

PRIMARY KB INPUTS: 08_DEMO_SCENARIOS, 09_LOGGING_AND_AUDIT, 02_PROJECT_DNA, LOCKED_STATE.

DO NOT: write backend/physics/UI implementation. Consume their outputs and make them
land.

FIRST ACTION: produce (a) a 15-question judge Q&A bank with crisp answers — especially
the hard ones on novelty, autonomy, and "why not just an alarm?" — and (b) the ROI
calculator input spec (failures prevented × downtime hrs × cost/hr − intervention cost),
with conservative [ESTIMATE] defaults flagged for verification.

Operate per the project custom instruction.
```

---

## How to run the vault (the loop)

1. Paste the **custom instruction** into Project settings.
2. Save **`LOCKED_STATE.md`** into Project Knowledge.
3. Open 5 chats, paste the 5 prompts above.
4. Work any lane — each reply ends with `⏭️ NEXT ACTIONS` (just pick one) and, when something locked changes, a `🔒 VAULT UPDATE`.
5. Paste VAULT UPDATEs into `LOCKED_STATE.md` and re-upload. The vault stays current; all 5 chats re-sync on their next read.
