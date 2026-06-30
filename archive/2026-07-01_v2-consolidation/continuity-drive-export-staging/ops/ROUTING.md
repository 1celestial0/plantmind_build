# Task Routing — where every kind of work goes

> If you're unsure where to work, find your row. If two rows match, pick the **leftmost folder** (docs before code).

---

## Master routing table

| Work type | Primary folder | Supporting folders | Prompt / skill |
|---|---|---|---|
| **Session start** | `00-START-HERE.md` | `LOCKED_STATE`, `Chat Context`, `ROADMAP` | project-continuity `start` |
| **Session close** | `ROADMAP.md` | `Chat Context/` | project-continuity `close` |
| **Locked decision change** | `LOCKED_STATE.md` | `src/contracts/` | 🔒 VAULT UPDATE protocol |
| **Backlog / next steps** | `ROADMAP.md` | — | — |
| **Project story / pitch** | `docs/dna/` | `ops/runbooks/demo.md` | Lane 5 |
| **Architecture design** | `docs/architecture/` | `LOCKED_STATE` | Lane 4 for Databricks |
| **UI mockups** | `docs/design/` | `src/dashboard/` | Lane 3 |
| **Industry research** | `docs/research/` | `ops/prompts/research/` | Master research prompt |
| **Pain / competitive / ROI** | `docs/research/` | — | Phase 1–5 artifacts |
| **Lane chat prompts** | `ops/prompts/lanes/` | `LOCKED_STATE` | One lane per chat |
| **Agent workflow design** | `ops/workflows/` | `src/pipeline/` | LangGraph/CrewAI |
| **Hooks / loops / feedback** | `ops/workflows/` | `src/governance/` | FeedbackLoopInterface |
| **Model API config** | `ops/MODEL-REGISTRY.md` | `src/api/` or agent files | — |
| **Project-local skills** | `ops/skills/` | — | `/skill-name` |
| **FastAPI routes** | `src/api/routes/` | `src/contracts/` | Lane 1 |
| **Agent implementation** | `src/agents/` | `src/pipeline/` | Lane 1 |
| **Physics / Weibull** | `src/physics/` | `ml/synthesis/` | Lane 2 |
| **RAG / ChromaDB** | `src/rag/` | `ml/data/` | Lane 1 + 2 |
| **Audit / governance** | `src/governance/` | `src/contracts/` | Lane 1 |
| **Orchestrator** | `src/pipeline/` | `ops/workflows/` | Lane 1 |
| **Streamlit / dashboard** | `src/dashboard/` | `src/api/` (JSON only) | Lane 3 |
| **Raw datasets** | `ml/data/raw/` | — | Lane 2 |
| **Synthetic data gen** | `ml/synthesis/` | `src/physics/` | Lane 2 |
| **Training notebooks** | `ml/training/notebooks/` | `ml/models/` | Lane 2 |
| **Saved models** | `ml/models/` | `mlflow` (future) | Lane 2 |
| **Local deploy** | `deploy/local/` | `requirements.txt` | — |
| **Databricks deploy** | `deploy/databricks/` | `docs/architecture/` | Lane 4 |
| **Demo rehearsal** | `ops/runbooks/demo.md` | `src/dashboard/` | Lane 5 |
| **Obsidian / KB graph** | `knowledge/` | `docs/` | — |
| **v1 salvage / reference** | `../PlantMind/FORGE/` | read-only until migrated | — |

---

## Lane → folder map

| Lane | Name | Write folders | Read folders |
|---|---|---|---|
| **1** | Backend & Agents | `src/agents/`, `src/api/`, `src/pipeline/`, `src/governance/` | `LOCKED_STATE`, `docs/architecture/05-06` |
| **2** | Physics & ML | `src/physics/`, `ml/synthesis/`, `ml/training/`, `ml/data/` | `LOCKED_STATE §6a`, `docs/architecture/07` |
| **3** | Dashboard & UI | `src/dashboard/`, `docs/design/` | `src/contracts/` (JSON shapes only) |
| **4** | Databricks Port | `deploy/databricks/` | `docs/architecture/`, `docs/research/` |
| **5** | Demo & Pitch | `ops/runbooks/`, `docs/dna/` | All docs, no `src/` internals |

---

## API routing pattern (future-proof)

```
HTTP Request
    → src/api/routes/{module}.py
    → src/agents/ or src/physics/ (business logic)
    → src/contracts/ (validate I/O)
    → src/governance/ (audit write)
    → Response JSON (matches LOCKED_STATE UI contract)
```

Dashboard **never** imports physics internals — only calls API or reads contract JSON.

---

## Anti-patterns (what causes drift)

| Don't | Do instead |
|---|---|
| Work in `_archive/` for new code | Work in `PlantMind/src/` |
| Keep next steps in Chat Context | Keep next steps only in `ROADMAP.md` |
| Add model API keys in code | Register in `ops/MODEL-REGISTRY.md` + `.env` |
| Change schemas without vault update | Update `LOCKED_STATE` + `src/contracts/` together |
| One chat across all lanes | One chat = one lane |