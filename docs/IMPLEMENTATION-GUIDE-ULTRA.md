# PlantMind × Götze Engine
# Ultra Implementation Guide — Build, Integrate, Test
**Version:** 1.0 | **Date:** 29 June 2026  
**Audience:** Technical members, TL, Delivery Manager, reviewers  
**Workspace:** `C:\Users\hp\Claude\Projects\PlantMind-Live` (ONLY folder to work in)

---

# PART 0 — WHAT IS THIS PROJECT? (Read this first)

## In one sentence

**PlantMind converts industrial sensor data into ONE ranked, explainable, human-approved maintenance action — and proves that action would rescue the asset — using physics-informed health scoring and a deterministic Intervention Impact Score (IIS).**

## What it is NOT

| Not this | Why |
|---|---|
| A chatbot | It decides and proves — narrative is secondary |
| A dashboard-only tool | Visualization serves the decision loop |
| A pure ML prediction app | Prediction is input; **decision** is the product |
| Three separate projects | One product, two implementation generations (v1 + v2) |

## The product in 30 seconds (for any stakeholder)

```
Sensors in → Health scored (Weibull) → Anomaly flagged → Götze Engine ranks all fixes
→ ONE best action shown → Human approves → Audit logged forever → Demo proves RED→GREEN
```

## Two implementations — one product

| | **v1 Reference** (`src/legacy/forge-v1/`) | **v2 Target** (`src/` — build here) |
|---|---|---|
| **Status** | ✅ Built, runnable | 🔲 Scaffolded |
| **Architecture** | 5-layer MetaGPT pipeline | 5-agent LangGraph sequence |
| **Scoring** | G-score (4 terms) | IIS (5 terms) — canonical |
| **Health** | RandomForest on C-MAPSS cycles | Weibull on multi-asset plant |
| **Demo** | Streamlit 4 tabs + RED→GREEN | Streamlit + FastAPI + approve button |
| **Hackathon role** | **Ship this if time runs out** | **Migrate toward this post-demo** |

**Rule for the team:** v2 spec in `LOCKED_STATE.md` is the product truth. v1 is the insurance policy.

---

# PART 1 — CODEBASE LINEAGE MAP

## 1.1 Folder topology (after merge)

```
PlantMind-Live/                          ← WORK HERE ONLY
├── LOCKED_STATE.md                      ← Locked decisions (agents, IIS, contracts)
├── ROADMAP.md                           ← What to do next
├── 00-START-HERE.md                     ← Human entry point
├── AI-OPERATING-SYSTEM.md               ← Claude + Grok + Gemini rules
│
├── src/
│   ├── contracts/                       ← Pydantic schemas (API between all modules)
│   ├── agents/                          ← 5 agents + orchestrator (BUILD)
│   ├── physics/                         ← Weibull, synthetic data interface (BUILD)
│   ├── api/routes/                      ← FastAPI endpoints (BUILD)
│   ├── pipeline/                        ← LangGraph workflow (BUILD)
│   ├── governance/                      ← Audit log, hash chain (BUILD)
│   ├── rag/                             ← ChromaDB retrieval (BUILD)
│   ├── dashboard/                       ← Streamlit v2 (BUILD)
│   └── legacy/forge-v1/                 ← v1 COMPLETE — do not delete
│       ├── app.py                       ← Streamlit demo
│       ├── src/pipeline.py              ← MetaGPT orchestrator
│       ├── src/gotze_engine.py          ← G-score engine
│       ├── src/ingestion.py             ← C-MAPSS load
│       ├── src/features.py              ← Rolling windows
│       ├── src/model.py                 ← RandomForest RUL
│       └── src/roles/                     ← Data/ML/Proof engineers
│
├── ml/
│   ├── synthesis/                       ← generate_data.py (BUILD)
│   ├── data/raw/                        ← CMAPSS, PRONOSTIA downloads
│   └── training/notebooks/              ← calibrate_weibull.py (BUILD)
│
├── docs/
│   ├── architecture/                      ← 01-10 vault KB (spec source)
│   ├── research/                        ← Pain register, competitive map
│   └── CONFLICT-RESOLUTION.md           ← v1 vs v2 decisions
│
└── ops/
    ├── MODEL-REGISTRY.md                ← All LLM/API routing
    ├── ROUTING.md                       ← Which folder for which task
    └── prompts/lanes/                   ← One prompt per build lane
```

## 1.2 Message / data lineage (v1 built)

```
train_FD001.txt
    → ingestion.py (RUL labels, clean)
    → features.py (30-cycle rolling window, 13 sensors)
    → model.py (RandomForest → RUL per engine)
    → messages.EngineHealth (frozen dataclass)
    → gotze_engine.py (G-score → winner + proof)
    → messages.EngineDecision
    → proof_engineer.py (Plotly RED→GREEN data)
    → app.py (4 Streamlit tabs)
```

**Key files and contracts (v1):**

| File | Input type | Output type |
|---|---|---|
| `ingestion.py` | CSV path | DataFrame + RUL column |
| `features.py` | DataFrame | Feature matrix |
| `model.py` | Features | RUL float |
| `messages.py` | — | SensorReading, EngineFeatures, EngineHealth, EngineDecision |
| `gotze_engine.py` | EngineHealth | GotzeResult / EngineDecision |
| `pipeline.py` | engine_id: int | {decision, proof_chart, agent_trace} |

## 1.3 Message / data lineage (v2 target)

```
synthetic CSV / Kaggle seed
    → ingest/ (Bronze validate)
    → features/ (Silver + physics features)
    → physics/weibull.py (PhysicsModelInterface)
    → agents/data_sentinel.py → DataQualityReport
    → agents/asset_health_oracle.py → AssetHealthReport
    → [TRIGGER] → agents/gotze_engine.py → GötzeDecision (IIS)
    → agents/root_cause_analyst.py → CausalChain
    → agents/executive_summarizer.py → ExecutiveBrief
    → api/routes/*.py (JSON to dashboard)
    → dashboard/app.py (render + approve button)
    → governance/audit.py (AuditRecord hash chain)
```

**Contracts live in `src/contracts/` — must match LOCKED_STATE §4 exactly.**

## 1.4 v1 → v2 migration map

| v1 module | v2 destination | Migration action |
|---|---|---|
| `forge-v1/src/ingestion.py` | `ml/data/` + `src/physics/` | Extract C-MAPSS loader; add synthetic generator |
| `forge-v1/src/features.py` | `src/physics/features.py` | Port rolling window; add physics features |
| `forge-v1/src/model.py` | `ml/training/` (fallback) | Keep RF as C-MAPSS path only |
| `forge-v1/src/gotze_engine.py` | `src/agents/gotze_engine.py` | **Rewrite** G-score → IIS |
| `forge-v1/src/pipeline.py` | `src/pipeline/orchestrator.py` | **Rewrite** MetaGPT → LangGraph |
| `forge-v1/app.py` | `src/dashboard/app.py` | Reskin; add approve + IIS panel |
| `forge-v1/src/messages.py` | `src/contracts/messages.py` | Extend to v2 contract shapes |

---

# PART 2 — PHASE-BY-PHASE BUILD PLAN

## Overview

| Phase | Name | Days | Owner | Delivers | Demo gate |
|---|---|---|---|---|---|
| **P0** | Environment + contracts | 0.5 | Sourav | Schemas, requirements, git | Team can `pip install` |
| **P1** | Physics + synthetic data | 1 | Lane 2 | Weibull + 30 assets | Health score on 1 asset |
| **P2** | Agents 1–2 | 1 | Lane 1 | Sentinel + Oracle | Anomaly + health on dashboard |
| **P3** | Götze + IIS | 1 | Lane 1 | Agent 3 + scoring | ONE action appears |
| **P4** | RAG + summary + API | 1 | Lane 1 | Agents 4–5 + FastAPI | Full JSON to UI |
| **P5** | Dashboard + approve | 1 | Lane 3 | Streamlit v2 | Human approve works |
| **P6** | Integration + demo freeze | 0.5 | Lane 5 | E2E tests, backup video | H16 equivalent |

**Parallel hackathon path:** If P1–P6 cannot finish, **demo from forge-v1** (P0 only + rehearsal).

---

## P0 — Environment & Contracts (Day 0, ~4 hours)

### WHAT
Scaffold runnable project: dependencies, Pydantic contracts, folder wiring, git branch strategy.

### WHY
Without frozen contracts, Lane 1/2/3 will build incompatible modules. This is the API between all codebases.

### HOW

```powershell
cd "C:\Users\hp\Claude\Projects\PlantMind-Live"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt   # create from stack in LOCKED_STATE §5
```

**Create `src/contracts/` files:**

| File | Models |
|---|---|
| `physics.py` | PhysicsModelOutput |
| `agents.py` | DataQualityReport, AssetHealthReport, GötzeDecision, CausalChain, ExecutiveBrief |
| `governance.py` | AuditRecord |
| `state.py` | PlantMindState (orchestrator shared state) |

### WHO
Lane 1 (Sourav)

### INPUTS
- `LOCKED_STATE.md` §4
- `docs/architecture/06_AGENTS.md`

### OUTPUTS
- `src/contracts/*.py` with unit tests in `tests/test_contracts.py`
- `requirements.txt`
- `plant_config.yaml` with Weibull λ, β per asset (from LOCKED_STATE §6a)

### TEST GATE
```powershell
pytest tests/test_contracts.py -v
# All models serialize/deserialize JSON matching LOCKED_STATE shapes
```

### DEPENDS ON
Nothing.

---

## P1 — Physics & Synthetic Data (Day 1, ~8 hours)

### WHAT
Weibull health model, synthetic plant generator, Kaggle calibration script.

### WHY
AssetHealthOracle needs deterministic, explainable health+RUL. Synthetic data lets you inject failures on stage (Scenario A–D).

### HOW

| File to create | Purpose |
|---|---|
| `ml/synthesis/generate_data.py` | 30 assets × 20 signals × 500 cycles |
| `src/physics/weibull.py` | H(t), RUL_days, bootstrap CI |
| `src/physics/interface.py` | PhysicsModelInterface implementation |
| `ml/training/calibrate_weibull.py` | MLE on CMAPSS/PRONOSTIA → update plant_config.yaml |

**Weibull (canonical):**
```
H(t) = 100 · exp(−λ · S · t^β)
RUL_days = invert(H, threshold=20) / CYCLES_PER_DAY
```

### WHO
Lane 2 (Sourav)

### INPUTS
- Kaggle CMAPSS (download to `ml/data/raw/`)
- LOCKED_STATE §6a constants

### OUTPUTS
- `ml/data/processed/synthetic_plant.csv`
- `plant_config.yaml` with calibrated λ, β
- `PhysicsModelInterface` callable returning contract JSON

### TEST GATE
```powershell
python -m src.physics.weibull --asset pump_07 --cycles 400
# Expect: health < 40, rul_days < 14 at end of gradual_wear scenario
```

### DEPENDS ON
P0 contracts

---

## P2 — Agents 1–2: Sentinel + Oracle (Day 2, ~8 hours)

### WHAT
DataSentinel (anomaly) and AssetHealthOracle (health+RUL) as callable agent modules.

### WHY
These feed the Götze trigger. Without them, GötzeEngine has nothing to score.

### HOW

| File | Agent | Engine |
|---|---|---|
| `src/agents/data_sentinel.py` | DataSentinel | Z-score + Mahalanobis |
| `src/agents/asset_health_oracle.py` | AssetHealthOracle | Calls PhysicsModelInterface |

**Rules (hard):**
- Sentinel: flags only, never modifies data
- Oracle: always returns ci_95 with rul_days

### WHO
Lane 1 (Sourav)

### INPUTS
- P1 PhysicsModelInterface
- P0 contracts
- Sensor window from synthetic CSV

### OUTPUTS
- `DataQualityReport`, `AssetHealthReport` JSON
- Unit tests with known anomaly injection

### TEST GATE
```powershell
pytest tests/test_agents_1_2.py -v
# Inject z-score>3 on bearing_3 → severity=critical
# pump_07 at cycle 400 → health<40
```

### DEPENDS ON
P0, P1

---

## P3 — Götze Engine + IIS (Day 3, ~8 hours)

### WHAT
GötzeEngine: score all candidate interventions, return ONE winner with IIS breakdown.

### WHY
**This is the product.** Everything else exists to feed this moment.

### HOW

| File | Purpose |
|---|---|
| `src/agents/gotze_engine.py` | IIS calculator + intervention catalog |
| `src/agents/_llm.py` | Groq narrative adapter (registry ID: narrative-primary) |
| `src/agents/interventions.yaml` | Candidate actions per asset type |

**IIS (canonical — do not change weights without vault update):**
```
IIS = 0.35·ΔP + 0.25·ΔCost + 0.20·Feasibility + 0.15·History − 0.05·SafetyRisk
```

**v1 reference:** See `src/legacy/forge-v1/src/gotze_engine.py` for G-score pattern — same structure, different terms.

### WHO
Lane 1 (Sourav)

### INPUTS
- AssetHealthReport from P2
- plant_config.yaml (weights, safety ceiling)
- Candidate interventions list

### OUTPUTS
- `GötzeDecision` with runner_up, iis_gap, requires_human_approval=True

### TEST GATE
```powershell
pytest tests/test_gotze_iis.py -v
# pump_07 stressed → winner = reduce_load_now (not emergency_stop)
# safety veto → next-best surfaces
```

### DEPENDS ON
P0, P2

---

## P4 — Agents 4–5 + FastAPI (Day 4, ~8 hours)

### WHAT
RootCauseAnalyst (RAG), ExecutiveSummarizer, FastAPI routes, audit writer stub.

### WHY
Closes the agentic story for judges: citations + leadership brief + machine-readable API for UI.

### HOW

| File | Purpose |
|---|---|
| `src/rag/seed_corpus.py` | Load 10–20 SOPs into ChromaDB |
| `src/rag/retriever.py` | MiniLM embeddings + top-k |
| `src/agents/root_cause_analyst.py` | RAG + causal chain |
| `src/agents/executive_summarizer.py` | 3-bullet brief |
| `src/api/main.py` | FastAPI app |
| `src/api/routes/assets.py` | /assets, /health, /evaluate |
| `src/api/routes/decisions.py` | /decision, /approve |
| `src/governance/audit.py` | Append-only AuditRecord + hash chain |
| `src/pipeline/orchestrator.py` | LangGraph sequence |

### WHO
Lane 1 (Sourav) + Lane 4 for Databricks narrative docs

### INPUTS
- P0–P3 outputs
- ChromaDB corpus
- MODEL-REGISTRY for LLM routing

### OUTPUTS
- `POST /api/v1/assets/{id}/evaluate` returns full pipeline JSON
- Audit log entry per agent hop

### TEST GATE
```powershell
uvicorn src.api.main:app --reload
curl http://localhost:8000/api/v1/assets/pump_07/evaluate
# Returns: sentinel + health + gotze + rca + brief + audit_ids
```

### DEPENDS ON
P0–P3

---

## P5 — Dashboard + Human Approve (Day 5, ~8 hours)

### WHAT
Streamlit v2: plant overview, ONE-best-action panel, IIS breakdown, approve/reject, audit viewer.

### WHY
Judges see and touch the product. Approve button proves governance.

### HOW

| File | Purpose |
|---|---|
| `src/dashboard/app.py` | Main Streamlit app |
| `src/dashboard/components/iis_panel.py` | Winner + runner-up + gap |
| `src/dashboard/components/audit_view.py` | Timeline + lineage |
| `src/dashboard/components/proof_chart.py` | Port RED→GREEN from forge-v1 |

**Rule:** Dashboard imports **only** `requests` to API or reads JSON files — never `src/physics` or `src/agents` directly.

### WHO
Lane 3 (Member 2/3)

### INPUTS
- FastAPI running (P4)
- UI contract shapes from LOCKED_STATE §4

### OUTPUTS
- Runnable `streamlit run src/dashboard/app.py`
- Approve button → POST /approve → audit updates

### TEST GATE
- Manual: Scenario A end-to-end in UI
- Approve → audit shows decision=approved
- Reject → audit shows decision=rejected + reason

### DEPENDS ON
P4

---

## P6 — Integration, Test, Demo Freeze (Day 6, ~4 hours)

### WHAT
E2E tests, scenario injector, backup video, git tag, rehearsed 5-min script.

### WHY
Hackathon is won on stage, not in docs.

### HOW

| Task | Command / file |
|---|---|
| E2E test | `tests/test_e2e_scenario_a.py` |
| Scenario injector | `src/dashboard/scenario_injector.py` |
| Demo script | `ops/runbooks/demo.md` |
| Backup video | Record Streamlit run |
| Freeze | `git tag v1.0-hackathon-submission` |

### TEST MATRIX (full)

| Test ID | What | Pass criteria |
|---|---|---|
| T01 | Contracts serialize | pytest test_contracts |
| T02 | Weibull health | pump_07 health<40 at cycle 400 |
| T03 | Sentinel flags | z>3 → critical |
| T04 | IIS winner | correct action for Scenario A |
| T05 | Safety veto | unsafe action blocked |
| T06 | API evaluate | 200 + full JSON |
| T07 | Approve flow | audit record written |
| T08 | RAG citation | ≥1 citation or "uncertain" |
| T09 | Groq fallback | templates work when API down |
| T10 | v1 fallback demo | forge-v1 app.py starts |
| T11 | Scenario B | emergency_stop wins |
| T12 | Scenario D | sensor dropout flagged as data issue |

### DEPENDS ON
P0–P5 (or forge-v1 for T10 only)

---

# PART 3 — INTEGRATION GUIDE FOR TEAM MEMBERS

## 3.1 Lane assignments (who builds what)

| Lane | Member | Folders they OWN (write) | Folders they READ only |
|---|---|---|---|
| 1 | Sourav | `src/agents/`, `src/api/`, `src/pipeline/`, `src/governance/` | `src/contracts/`, `src/physics/` |
| 2 | Sourav | `src/physics/`, `ml/` | `src/contracts/` |
| 3 | Member 2/3 | `src/dashboard/`, `docs/design/` | `src/contracts/` (JSON shapes) |
| 4 | Sourav/team | `deploy/databricks/` | `docs/architecture/`, contracts |
| 5 | Member 4 | `ops/runbooks/`, tests E2E | all docs, no src internals |

## 3.2 PR / merge rules

- Branch: `feature/lane{N}-{description}`
- Commit: `feat(agents): add DataSentinel v1`
- **Never merge** if contracts changed without LOCKED_STATE vault update
- **Never import** across lanes except via `src/contracts/`

## 3.3 Daily standup script (15 min)

1. What phase gate did you pass yesterday?
2. What contract do you consume / produce today?
3. Any vault update needed?
4. Blocker?

---

# PART 4 — HACKATHON DECISION TREE

```
START
  │
  ├─ Is it July 8+ ?
  │     YES → Demo from forge-v1 ONLY. Freeze. Rehearse.
  │     NO  ↓
  │
  ├─ Is P3 (IIS) done?
  │     NO  → Continue v2 build OR demo prep on forge-v1 in parallel
  │     YES ↓
  │
  ├─ Is P5 (approve UI) done?
  │     NO  → Demo forge-v1 + narrate v2 governance as "next sprint"
  │     YES → Demo v2 as primary, forge-v1 as fallback video
  │
  END
```

---

# PART 5 — QUICK REFERENCE COMMANDS

```powershell
# Session start (any AI tool)
cd "C:\Users\hp\Claude\Projects\PlantMind-Live"
.\scripts\start-session.ps1

# v1 demo (insurance)
streamlit run src\legacy\forge-v1\app.py

# v2 API (when built)
uvicorn src.api.main:app --reload

# v2 dashboard (when built)
streamlit run src\dashboard\app.py

# Tests
pytest tests/ -v

# Close session
# Tell any AI: "close session" → updates ROADMAP + Chat Context + git
```

---

*End of Ultra Implementation Guide v1.0*