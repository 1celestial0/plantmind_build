# PlantMind × Götze Engine — Master Specification
**Version:** 2.0 Merged | **Date:** 2026-06-29  
**Workspace:** `C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live`  
**Replaces:** CONSOLIDATED-PROJECT-BLUEPRINT, IMPLEMENTATION-GUIDE-ULTRA (as primary), WIN-STRATEGY (as primary)

> Single document for CEO → engineer. Conflicts resolved per `CONFLICT-RESOLUTION.md` — **better option wins**.

---

# §1 Identity & story

**PlantMind** = Physics-Informed Engineering Intelligence. At peak asset stress, score every intervention → surface **ONE** best action → human approves → prove RED→GREEN → audit forever.

| Field | Value |
|---|---|
| Tagline | *Predict the failure. Decide the fix. Prove it.* |
| Event | LTTS Global EI Hackathon · **9 July 2026** · 24h · 4 members |
| Anchor | LTTS × Databricks partnership (11 June 2026) |
| Owner | Sourav Dutta, LTTS |

**Götze hook:** 2014 — analytics picked Götze; he scored the winner. PlantMind is that coach for a factory.

---

# §2 Two implementations, one product

| | v1 `src/legacy/demo-v1-metagpt/` | v2 `src/` |
|---|---|---|
| Status | ✅ Runnable | 🔲 Build P0–P6 |
| Model | 5-layer MetaGPT | 5-agent LangGraph |
| Score | G-score | **IIS (canonical)** |
| Health | RandomForest C-MAPSS | **Weibull (canonical)** |
| Hackathon | **Demo here if time short** | Production target |

---

# §3 Architecture (canonical = v2)

**Layer 0:** 7 interfaces (Ingestor, FeatureStore, AnomalyModel, PhysicsModel, KnowledgeRetriever, AgentOrchestrator, Governance, FeedbackLoop)

**Runtime:** DataSentinel → AssetHealthOracle → GötzeEngine → RootCauseAnalyst → ExecutiveSummarizer → Human Approve → Audit

**IIS (locked):**
```
IIS = 0.35·ΔP_failure + 0.25·ΔDowntimeCost + 0.20·Feasibility
    + 0.15·HistoricalSuccess − 0.05·SafetyRiskDelta
```

**Trigger:** health<40 OR rul_days<14 OR critical anomaly

---

# §4 Data flow

Sensors → Bronze/Silver/Gold → Weibull health → trigger → IIS → RAG → brief → dashboard → approve → audit

**Demo data:** 30 assets, 20 signals, 3 failure modes, 500 cycles + CMAPSS calibration

---

# §5 Model routing

| Task | Model | Rule |
|---|---|---|
| IIS/G-score math | Python deterministic | Never LLM |
| Narrative | Groq Llama 3.3 70B | Template fallback |
| Embeddings | MiniLM local | — |
| Health | scipy Weibull | Ships first |
| PINN | PyTorch | Stretch only |

Registry: `ops/MODEL-REGISTRY.md`

---

# §6 API & contracts

FastAPI routes: `/assets`, `/health`, `/evaluate`, `/decision`, `/approve`, `/audit`

Schemas: `src/contracts/` = LOCKED_STATE §4

Dashboard reads JSON only — never imports physics internals.

---

# §7 Team lanes

| Lane | Owner | Folder |
|---|---|---|
| 1 Backend | Sourav | `src/agents/`, `src/api/` |
| 2 Physics | Sourav | `src/physics/`, `ml/` |
| 3 UI | M2/M3 | `src/dashboard/` |
| 4 Databricks | Team | `deploy/databricks/` |
| 5 Demo | M4 | `ops/runbooks/` |

---

# §8 Demo

**Hero:** Scenario A — pump degrades → IIS winner → approve → audit  
**v1 run:** `streamlit run src\legacy\demo-v1-metagpt\app.py`  
**5-min script:** `docs/architecture/08_DEMO_SCENARIOS.md`

---

# §9 Governance & IP

Non-autonomous · Explainable · Logged · Patent-candidate pending prior-art

---

# §10 Build phases (P0–P6)

| Phase | Deliverable | Test gate |
|---|---|---|
| P0 | `src/contracts/` | pytest contracts |
| P1 | Weibull + synthetic | health<40 pump_07 |
| P2 | Agents 1-2 | anomaly + health JSON |
| P3 | IIS Götze | Scenario A winner |
| P4 | Agents 4-5 + API | POST /evaluate 200 |
| P5 | Dashboard + approve | audit on approve |
| P6 | E2E + freeze | tag v1.0-hackathon-submission |

Detail: former IMPLEMENTATION-GUIDE-ULTRA §Part 2 (kept in repo for step-by-step).

---

# §11 Integration test matrix

T01–T12: contracts, Weibull, sentinel, IIS, safety veto, API, approve, RAG, LLM fallback, v1 demo, scenarios B/D

Detail: `docs/CODEBASE-INVENTORY.md` + IMPLEMENTATION-GUIDE-ULTRA §Part 3

---

# §12 Code lineage

v1: ingestion → features → model → gotze_engine → pipeline → app.py  
v2: physics → agents → orchestrator → api → dashboard  
Migration map: `docs/CODEBASE-INVENTORY.md` §3

---

# §13 Win strategy (honest)

No 200% guarantee. Composite ~7.8/10 today; ~8.5/10 with polished v1 demo.

**Max win path:** Demo demo-v1-metagpt · Pitch v2 vision · Rehearse 10× · Backup video by July 8

Full analysis: `docs/WIN-STRATEGY-ASSESSMENT.md` (audit copy)

---

# §14 Portfolio & multi-CLI

```
Projects/
├── PlantMind_OS/     template
├── _archive/       frozen snapshots
└── PlantMind/      ACTIVE (this project)
```

CLIs: Claude, Grok, Gemini, Codex — see `ops/CLI-REGISTRY.md`  
New CLI: add row + `{TOOL}.md` pointing to `AI-OPERATING-SYSTEM.md`

---

# §15 Document map

See `docs/INDEX.md` for full registry. This file is the merge winner for handover content.