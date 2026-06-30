# PlantMind × Götze Engine

> **Config-driven, physics-informed, agentic decision fabric for industrial assets.**
> Turns existing plant data into trusted, ranked, human-approved, audited engineering actions — without rip-and-replace.

**🔒 Source of truth:** [`PROJECT-DNA.md`](PROJECT-DNA.md) (apex constitution) → [`LOCKED_STATE.md`](LOCKED_STATE.md) (technical vault). Read those first. Every other doc is derived and conforms to them.

## Two pillars
1. **Closed decision loop** — physics health → IIS scoring → one approved, audited action.
2. **Config-driven modularity** — a declarative Plant Config Manifest composes the whole stack; a new plant/asset/use-case is a config change, not a code deploy.

## The 6 agents
DataSentinel → AssetHealthOracle → **GötzeEngine ⭐** → RootCauseAnalyst → ExecutiveSummarizer → **MaintenanceScheduler ⭐**

## Repo map
| Path | What |
|---|---|
| `PROJECT-DNA.md` / `LOCKED_STATE.md` | Source of truth |
| `00-START-HERE.md` | Operating manual + session lifecycle SOP |
| `ROADMAP.md` | Top-20 backlog |
| `src/` | App code (contracts · physics · agents · pipeline · api · governance · rag · dashboard) |
| `ml/` | Synthesis · training · feedback |
| `team-share/` | Onboarding pack (verified-correct docs) |
| `knowledge/` | Living Obsidian vaults (truth mirror + code lineage) |
| `archive/` | Quarantined v1/legacy — historical only |

## Run (local)
```powershell
streamlit run src\dashboard\app.py
uvicorn src.api.main:app --reload
```

## Status
Product idea **LOCKED** (PROJECT-DNA v1.0, 2026-07-01). Building toward the LTTS EI Hackathon (2026-07-09). Private / internal — hackathon IP.

Stack: Python 3.11 · FastAPI · Pydantic v2 · CrewAI + LangGraph · Groq · ChromaDB · scikit-learn/scipy · Streamlit + Plotly · SQLite. Production path: Databricks (Layer 1).
