# src/ — Application runtime

Modular monorepo. Lanes communicate through `contracts/` only.

| Folder | Purpose |
|---|---|
| `contracts/` | Pydantic schemas (= LOCKED_STATE §4) |
| `api/routes/` | FastAPI HTTP endpoints |
| `agents/` | 5 agents + orchestrator |
| `physics/` | Weibull, health, RUL |
| `pipeline/` | LangGraph / workflow wiring |
| `rag/` | ChromaDB + embeddings |
| `governance/` | Audit log, lineage |
| `dashboard/` | Streamlit app |

**v1 salvage:** `../../PlantMind/FORGE/src/` — migrate module by module per `MIGRATION-MAP.md`.