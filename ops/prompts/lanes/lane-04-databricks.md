# Lane 4 — Databricks Parallel Port

Paste everything below the line into a **new chat** (Lane 4 only).

---

```
LANE 4 — Databricks Parallel Port.

MISSION: Mirror the local build on Databricks-native services (Auto Loader + DLT,
Feature Store, MLflow, Unity Catalog, Vector Search, Mosaic AI Agents) by REUSING
Layer-0 contracts — maximum shared codebase, minimum rewrite.

PRIMARY KB INPUTS: docs/research/DATABRICKS_MAP_2026_30th_June.md,
docs/architecture/03_ARCHITECTURE.md, LOCKED_STATE.md.

DO NOT: invent new contracts. Bind the SAME interfaces to Databricks services.
Flag GA-status caveats. Mark non-free-tier-testable items.

CODE HOME: deploy/databricks/

FIRST ACTION: reusable-vs-Databricks-specific boundary map + parallel runbook skeleton
with contract→service mapping table (see DATABRICKS_MAP Part B). Then notebooks.

Operate per AI-OPERATING-SYSTEM.md and confirmation-gate.md.
End each reply with ⏭️ NEXT ACTIONS.
```

**Source:** split from `ops/prompts/PLANTMIND_5_CHAT_PROMPTS.md` (Chat 4).