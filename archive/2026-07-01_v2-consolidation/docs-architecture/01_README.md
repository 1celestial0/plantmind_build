# PlantMind × Götze Engine

> **Engineering Intelligence for industrial assets.** It watches machines, spots trouble early, estimates how bad and how soon — then surfaces the **one best action** a human should take, with a reason. Human approves. Everything is logged.

- **Owner:** Sourav Dutta — Senior Data Engineer, LTTS (L&T Technology Services)
- **Event:** LTTS Global Engineering Intelligence Hackathon — **July 9, 2026** (24h, OpenHack, 4 members)
- **Strategic anchor:** LTTS × Databricks announced an Industrial AI / Engineering Intelligence partnership on **June 11, 2026** — 28 days before this hackathon. PlantMind is the reference implementation of that vision.

---

## The one-sentence pitch

> In 2014, analytics told Germany's coach the single best substitution was Götze; he came on and scored the World Cup winner. **PlantMind is that coach for a factory** — at the moment of maximum asset stress, it scores every possible human intervention and surfaces the ONE optimal action with physics-grounded reasoning.

---

## What this actually does (no jargon)

1. **Watches** sensor data from machines (pumps, motors, compressors, bearings, valves).
2. **Scores health** of each machine (0–100) and estimates **days-to-failure** (this is "RUL" — Remaining Useful Life).
3. **Recommends the single best action** to take right now, ranked by an **Intervention Impact Score (IIS)** — and explains why.
4. A human **approves** before anything happens. Nothing is autonomous.
5. **Logs everything** — immutable audit trail of every decision.

---

## Jargon decoder (read this once)

| Term | Plain meaning |
|---|---|
| **RUL** | Remaining Useful Life — "days left before this part fails." A battery % for machines. |
| **Weibull** | A 70-year-old trusted reliability formula for how machines fail over time. The industry-standard "how machines die" curve. |
| **ODE** | An equation for how fast something changes. "Weibull ODE" = the failure curve written as a rate-of-decay. |
| **PINN** | Physics-Informed Neural Network — an AI model with the physics rule baked in, so its predictions can't violate engineering reality. |
| **IIS** | Intervention Impact Score — *our invention.* Scores every candidate action so the engine picks the top one. The real differentiator. |
| **Agent** | A small AI program that does one job. We have 5 (see `06_AGENTS.md`). |
| **RAG** | Letting the AI search a document library (manuals, fault logs) and cite from it. |
| **CMAPSS / PRONOSTIA** | Free public failure datasets (NASA engines, bearings) used to train/test. |

---

## Repo map (read in this order)

| # | File | What it gives you |
|---|---|---|
| 01 | `01_README.md` | This file — the overview |
| 02 | `02_PROJECT_DNA.md` | The 10-minute canonical read: what, why it wins, build map, demo story |
| 03 | `03_ARCHITECTURE.md` | Two-layer architecture + tool/model lineage |
| 04 | `04_DATA_FLOW.md` | End-to-end data flow diagram |
| 05 | `05_RUNTIME_AND_AGENTIC_WORKFLOW.md` | How the 5 agents fire in sequence at runtime |
| 06 | `06_AGENTS.md` | Each agent: instruction + rule + engine |
| 07 | `07_ML_MODEL_AND_DATA.md` | What ML to build (honest version) + how to get/make data |
| 08 | `08_DEMO_SCENARIOS.md` | How to show real failures live + the 5-minute script |
| 09 | `09_LOGGING_AND_AUDIT.md` | How everything gets logged and shown in-app |
| 10 | `10_BUILD_PLAN.md` | Realistic 24h plan, team split, repo strategy, phases |

**Staged for the build chat:** full Python codebase · Databricks parallel runbook · UI mockups · interactive ROI calculator.

---

## Stack at a glance (hackathon / local, all open or free-tier)

- **Backend:** Python 3.11 · FastAPI · Pydantic v2
- **Agents:** CrewAI + LangGraph
- **LLM (runtime narrative):** Groq — Llama 3.3 70B (free tier)
- **Embeddings:** sentence-transformers `all-MiniLM-L6-v2` (local, free)
- **Vector DB:** ChromaDB (local)
- **Physics/ML:** scikit-learn · scipy (Weibull) · PyTorch (optional PINN)
- **Dashboard:** Streamlit + Plotly
- **Storage:** SQLite (hackathon) → Delta Lake (production narrative)

> ⚠️ Verify current model availability, free-tier limits, and library versions at build time — these move fast.

---

## Golden rules (non-negotiable)

1. **Non-autonomous.** Every agent flags, scores, or reports. A human approves all actions.
2. **Explainable.** Every recommendation carries a reason and, where possible, a citation.
3. **Logged.** Every decision is immutably recorded.
4. **Demo-first.** What wins is the *story + a working demo of the one-best-action moment* — not unbuilt physics.
