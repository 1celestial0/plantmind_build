# Lane 1 — Backend Core & Agents

Paste everything below the line into a **new chat** (Lane 1 only).

---

```
LANE 1 — Backend Core & Agents.

MISSION: Build the runnable Python backend — the shared PlantMindState, the
LangGraph/CrewAI orchestrator, the 5 agents (DataSentinel, AssetHealthOracle,
GötzeEngine, RootCauseAnalyst, ExecutiveSummarizer), the IIS scorer, FastAPI
endpoints, and the SQLite audit writer.

PRIMARY KB INPUTS: docs/architecture/06_AGENTS.md, 05_RUNTIME_AND_AGENTIC_WORKFLOW.md,
03_ARCHITECTURE.md, LOCKED_STATE.md, src/contracts/.

DO NOT: implement physics internals (Lane 2 owns PhysicsModelInterface) or build
UI (Lane 3). Call physics via its contract; expose clean JSON for the UI.

CONTRACTS YOU OWN: UI JSON (GötzeDecision + AssetHealthReport + ExecutiveBrief)
and AuditRecord writer. Changes → 🔒 VAULT UPDATE.
CONTRACTS YOU CONSUME: PhysicsModelOutput from src/contracts/physics.py.

CODE HOME: src/agents/, src/api/, src/pipeline/, src/shared/

FIRST ACTION: scaffold PlantMindState + orchestrator skeleton + 5 agent stubs with
correct signatures and graceful-failure wrappers. Import contracts from src/contracts/.
Real, runnable files — then fill agents one by one.

Operate per AI-OPERATING-SYSTEM.md and confirmation-gate.md.
End each reply with ⏭️ NEXT ACTIONS (pick one concrete step).
```

**Source:** split from `ops/prompts/PLANTMIND_5_CHAT_PROMPTS.md` (Chat 1).