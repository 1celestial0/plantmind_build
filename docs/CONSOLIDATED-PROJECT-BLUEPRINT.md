# PlantMind × Götze Engine
## Complete Project Blueprint — Consolidated Specification
**Version:** 1.0 Consolidated | **Date:** 29 June 2026  
**Owner:** Sourav Dutta, Senior Data Engineer, LTTS  
**Event:** LTTS Global Engineering Intelligence Hackathon — 9 July 2026  
**Workspace:** `C:\Users\hp\Claude\Projects\PlantMind-Live`

---

## Document purpose and audience

| Audience | Read these sections |
|---|---|
| **CEO / Executive** | §1 Executive Summary, §2 Why We Win, §12 ROI, §16 Status |
| **Delivery Manager** | §10 Build Plan, §15 Governance, §16 Roadmap, §17 Team |
| **Technical Lead** | §4–§9 Architecture, Data Flow, Agents, Models |
| **Peers / Engineers** | §5–§8, §11 Stack, Appendix contracts |
| **Judges / Handover** | §1–§3, §9 Demo, §13 Research |

---

# §1 Executive Summary

**PlantMind** is a Physics-Informed Engineering Intelligence framework that converts industrial sensor and maintenance data into **one explainable, human-approved corrective action** — at the moment of maximum asset stress.

**The Götze analogy:** In 2014, analytics told Germany's coach the single best substitution was Mario Götze. He scored the World Cup winner. PlantMind is that coach for a factory.

| Field | Value |
|---|---|
| **Product** | PlantMind × Götze Engine |
| **Tagline** | *Predict the failure. Decide the fix. Prove it.* |
| **Strategic anchor** | LTTS × Databricks Industrial AI partnership (announced 11 June 2026) |
| **Differentiator** | Everyone predicts failure. PlantMind **decides the optimal fix** and **proves it** with counterfactual simulation and immutable audit. |
| **IP wedge** | Closed decision loop: physics-grounded health → IIS scoring → one approved action → audit — patent-candidate, pending prior-art review. |
| **Team** | 4 members · 24-hour OpenHack · Demo target: 5 July rehearsal, freeze 8 July |

**Consolidated status:** v1 reference implementation (FORGE) is **built and runnable**. v2 target architecture (5 agents, IIS, Weibull, FastAPI) is **specified and locked**; migration into `src/` is in progress.

---

# §2 Problem validation and market context

## 2.1 The pain

| Metric | Value | Source |
|---|---|---|
| Global unplanned downtime cost | ~$50B/yr (US manufacturing) | Industry reports |
| Fortune 500 downtime loss | ~$1.4T/yr (~11% revenue) | Siemens 2024 |
| Cost per hour (large plant) | $50K–$500K/hr | Sector-dependent |
| Failures caught before occurrence | Only 20–30% | Standard PdM |
| Alarm flood (vs. manageable <150/day) | 300–2,000/operator/day | EEMUA 191 |
| Industrial data analyzed | <1% | Dark data studies |

## 2.2 The gap PlantMind fills

**Every major vendor predicts.** Almost none closes the loop to: *"Here is the single best action, ranked, with reasoning, human-approved, and logged."*

## 2.3 LTTS alignment

PlantMind maps 1:1 to five joint LTTS–Databricks solution areas:

| Joint area | PlantMind component |
|---|---|
| Predictive Asset Reliability | AssetHealthOracle |
| Energy & Emissions Optimization | IIS downtime-cost term |
| OEE & Production Intelligence | Downtime-cost scoring |
| Quality Intelligence | DataSentinel |
| Sustainability Analytics | ExecutiveSummarizer ROI roll-up |

---

# §3 Consolidated vision (post-merge)

PlantMind has **three complementary views** of one product — not three products:

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 0 — Framework (LTTS IP)                                   │
│  7 tool-agnostic interface contracts — portable to any cloud       │
├─────────────────────────────────────────────────────────────────┤
│  LAYER 1 — Reference implementation                              │
│  Local hackathon build + Databricks production narrative         │
├─────────────────────────────────────────────────────────────────┤
│  RUNTIME — 5 specialist agents (LangGraph sequence)              │
│  Sentinel → Oracle → Götze → RootCause → Summarizer → Human     │
├─────────────────────────────────────────────────────────────────┤
│  v1 REFERENCE (forge-v1) — Runnable proof of decision + chart    │
│  5-layer MetaGPT pipeline · G-score · C-MAPSS · Streamlit        │
└─────────────────────────────────────────────────────────────────┘
```

---

# §4 System architecture

## 4.1 Two-layer framework (Layer 0 + Layer 1)

**Layer 0 — Framework (tool-agnostic LTTS IP)**

| Contract | Responsibility |
|---|---|
| IngestorInterface | Sensor/maintenance ingest + validation |
| FeatureStoreInterface | Point-in-time features incl. physics |
| AnomalyModelInterface | Per-asset/window anomaly detection |
| PhysicsModelInterface | Health + RUL callable contract |
| KnowledgeRetrieverInterface | RAG over manuals/logs |
| AgentOrchestratorInterface | Agent trigger, routing, audit |
| GovernanceInterface | Lineage, policy, audit, explainability |
| FeedbackLoopInterface | Outcomes → recalibration (production) |

**Layer 1 — Bindings**

| Contract | Hackathon (local) | Production (Databricks) |
|---|---|---|
| Ingestor | Python + Pydantic / SQLite | Auto Loader + DLT |
| FeatureStore | pandas | Databricks Feature Store |
| AnomalyModel | Z-score + Mahalanobis | MLflow serving |
| PhysicsModel | scipy Weibull (+ optional PINN) | Python wheel on cluster |
| KnowledgeRetriever | ChromaDB + MiniLM | Vector Search |
| Orchestrator | CrewAI + LangGraph | Mosaic AI Agents |
| Governance | SQLite + hash-chain audit | Unity Catalog |
| FeedbackLoop | SQLite outcomes | Delta + Workflows |

## 4.2 Logical architecture diagram

```
[Sensors] [Maintenance logs] [Manuals/SOPs]
        │         │              │
        ▼         ▼              ▼
   ┌──────── INGEST / BRONZE-SILVER-GOLD ────────┐
   │  Validate → Features → Physics features      │
   └──────────────────┬──────────────────────────┘
                      ▼
            ┌─────────────────┐
            │ AssetHealthOracle│  Weibull H(t), RUL days, CI
            └────────┬────────┘
                     │ [TRIGGER: health<40 OR rul<14d OR critical]
                     ▼
            ┌─────────────────┐
            │  GötzeEngine ⭐  │  IIS → ONE best action
            └────────┬────────┘
                     ▼
            ┌─────────────────┐
            │ RootCauseAnalyst │  RAG + citations
            └────────┬────────┘
                     ▼
            ┌─────────────────┐
            │ExecutiveSummarizer│  3-bullet brief
            └────────┬────────┘
                     ▼
              [Streamlit Dashboard]
                     ▼
              {Human Approve?}
                     ▼
              [Immutable Audit Log]
```

## 4.3 Module folder map (PlantMind-Live)

| Module | Path |
|---|---|
| Contracts | `src/contracts/` |
| Agents | `src/agents/` |
| Physics | `src/physics/` |
| API | `src/api/routes/` |
| Pipeline | `src/pipeline/` |
| RAG | `src/rag/` |
| Governance | `src/governance/` |
| Dashboard | `src/dashboard/` |
| v1 reference | `src/legacy/forge-v1/` |
| ML training | `ml/training/` |
| Synthetic data | `ml/synthesis/` |
| Deploy | `deploy/local/`, `deploy/databricks/` |

---

# §5 End-to-end data flow

## 5.1 Medallion pipeline

| Stage | Hackathon | Production |
|---|---|---|
| Bronze | CSV / SQLite raw | Auto Loader → Delta |
| Silver | pandas + Pydantic validation | Delta Live Tables |
| Gold | Feature builder + physics features | Feature Store |

## 5.2 Data flow sequence

1. **Ingest** — sensor window per asset per cycle  
2. **Validate** — schema, units, timestamps, null audit  
3. **Feature engineer** — rolling stats + 3 physics features (degradation rate, temp stress, load stress)  
4. **Health model** — Weibull H(t) → health_index 0–100, rul_days, ci_95  
5. **Anomaly check** — DataSentinel Z-score + Mahalanobis  
6. **Trigger evaluation** — if health<40 OR rul_days<14 OR severity=critical → GötzeEngine  
7. **IIS scoring** — rank all candidate interventions  
8. **Root cause** — RAG retrieval + causal chain  
9. **Executive brief** — 3 bullets for leadership  
10. **Present** — dashboard shows ONE action + runner-up + gap  
11. **Approve** — human yes/no → audit record  
12. **Feedback** — outcome stored (production recalibration narrative)

## 5.3 Synthetic data schema (demo universe)

- **30 assets** × **20 signals** × **3 failure modes** × **500 cycles**  
- Asset types: pump, compressor, motor, bearing, valve  
- Failure modes: gradual_wear, sudden_impact, intermittent_fault  
- Kaggle seed (CMAPSS, PRONOSTIA) calibrates Weibull λ, β

## 5.4 Physics model (canonical)

```
H(t) = 100 · exp(−λ · S · t^β)
S = AF_temp · AF_load  (unity at 25°C, rated load)
RUL_days = f(H, λ, β, H_threshold=20) / CYCLES_PER_DAY
CYCLES_PER_DAY = 6.0 [ESTIMATE]
```

| Asset | λ | β | life_ref (cycles) |
|---|---|---|---|
| pump | 1.49e-6 | 2.3 | 420 |
| compressor | 1.83e-5 | 1.9 | 400 |
| motor | 5.98e-8 | 2.8 | 450 |
| bearing | 2.01e-9 | 3.5 | 350 |
| valve | 1.53e-4 | 1.5 | 480 |

---

# §6 Agentic workflows

## 6.1 The five agents (hackathon scope)

| # | Agent | Role | Autonomous? | Engine |
|---|---|---|---|---|
| 1 | DataSentinel | Inspector — flag anomalies | No | Z-score + Mahalanobis |
| 2 | AssetHealthOracle | Doctor — health + RUL | No | Weibull (+ optional PINN) |
| 3 | GötzeEngine ⭐ | Coach — ONE best action | **Requires human approval** | IIS + Groq narrative |
| 4 | RootCauseAnalyst | Detective — why, with citations | No | ChromaDB RAG |
| 5 | ExecutiveSummarizer | Chief of staff — 3 bullets | No | Aggregation + ROI |

## 6.2 Orchestration (LangGraph directed sequence)

```
Orchestrator
  → DataSentinel      → log(sentinel)
  → AssetHealthOracle → log(health)
  → GötzeEngine       → log(gotze, requires_approval=true)
  → RootCauseAnalyst  → log(rootcause)
  → ExecutiveSummarizer → log(summary)
  → Human             → APPROVE / REJECT
  → Audit             → log(approval, immutable hash chain)
```

## 6.3 Graceful degradation

| Failure | Fallback |
|---|---|
| Groq API down | Templated reason per action type |
| PINN not trained | Analytical Weibull (invisible to judges) |
| RAG empty | "Cause uncertain — manual review" |
| Any agent throws | Partial UI; demo continues |

## 6.4 v1 FORGE mapping (reference implementation)

| v1 Layer/Role | Maps to v2 |
|---|---|
| DataEngineerRole (ingest + features) | Ingestor + FeatureStore + DataSentinel inputs |
| MLEngineerRole (RandomForest RUL) | AssetHealthOracle (interim — RF replaces Weibull for C-MAPSS demo) |
| GotzeEngine (G-score) | GötzeEngine (IIS — formula migration pending) |
| ProofEngineerRole (RED→GREEN) | Proof visualization + governance partial |

---

# §7 Decision engine — IIS and G-score reconciliation

## 7.1 Canonical: Intervention Impact Score (IIS)

```
IIS(i) = 0.35·ΔP_failure + 0.25·ΔDowntimeCost + 0.20·Feasibility
       + 0.15·HistoricalSuccess − 0.05·SafetyRiskDelta
```

- All terms normalized [0,1]  
- Demo: fixed weights  
- SafetyRiskDelta above ceiling → hard veto  
- Human approval required before action logged

## 7.2 v1 implementation: G-score (forge-v1)

```
G = 0.40·ΔHealth + 0.25·(1−NormCost) + 0.20·(1−NormTime) + 0.15·Safety
```

## 7.3 Unified action catalog

| Canonical action | v1 alias | Typical IIS driver |
|---|---|---|
| reduce_load_now | reduce_load | High feasibility, moderate ΔP |
| replace_bearing | replace_bearing | High ΔP, high cost/time |
| flush_lubrication | flush_lubrication | Moderate ΔP, low cost |
| schedule_maintenance_window | monitor_only (v1) | Low disruption |
| emergency_stop | (scenario B) | Safety veto override |

## 7.4 Proof stack (combined)

1. **IIS ranking** — why this action won (term breakdown)  
2. **RED→GREEN chart** — counterfactual health trajectory (v1 built)  
3. **Audit record** — immutable hash-chain log with lineage  
4. **Human approval** — governance gate

---

# §8 Model routing techniques

## 8.1 Design rule

> **AI does uncertain work. Deterministic rules decide.**

| Task type | Model | Registry ID |
|---|---|---|
| IIS / G-score math | Deterministic Python | `scoring-deterministic` |
| Agent narrative | Groq Llama 3.3 70B | `narrative-primary` |
| Fast labels | Groq Llama 3.2 3B | `summary-fast` |
| Root cause reasoning | DeepSeek R1 or Groq 70B | `reasoning-heavy` |
| Embeddings | all-MiniLM-L6-v2 (local) | `embeddings-local` |
| Health (canonical) | scipy Weibull | `health-physics-v2` |
| RUL (v1 demo) | RandomForest C-MAPSS | `rul-ml-v1` |
| PINN stretch | PyTorch 1D-CNN+BiLSTM | `health-stretch` |
| Architecture docs | Claude (IDE only) | `architect-docs` |

## 8.2 Routing flow

```
Request → Task classifier → MODEL-REGISTRY lookup → Adapter → Fallback if fail
```

- Registry: `ops/MODEL-REGISTRY.md`  
- Adapters: `src/agents/_llm.py`, `src/rag/_embeddings.py`  
- Never call provider SDK directly from agent business logic

## 8.3 Cost control

| Tier | Use for |
|---|---|
| Free local | Embeddings, Weibull, IIS, G-score |
| Groq free tier | Narrative, summaries |
| DeepSeek cheap | Heavy RCA when needed |
| Claude | IP/docs only — not runtime demo |

---

# §9 API routing and contracts

## 9.1 FastAPI route pattern (v2 target)

```
GET  /api/v1/assets                    → list assets + health summary
GET  /api/v1/assets/{id}/health        → AssetHealthReport
POST /api/v1/assets/{id}/evaluate      → trigger agent pipeline
GET  /api/v1/assets/{id}/decision      → GötzeDecision
POST /api/v1/decisions/{id}/approve    → approval + audit write
GET  /api/v1/audit                     → paginated audit trail
POST /api/v1/scenarios/inject          → demo scenario injector
```

## 9.2 Shared contracts (LOCKED)

**PhysicsModelInterface output:**
`{health_index, rul_estimate, confidence_interval, physics_explanation}`

**GötzeDecision:**
`{top_intervention, iis_score, runner_up, iis_gap, narrative, confidence, requires_human_approval}`

**AuditRecord:**
`{record_id, timestamp, asset_id, stage, actor, model_used, input_ref, output, iis_score, requires_approval, decision, reason, lineage[]}`

## 9.3 Dashboard rule

Streamlit **consumes JSON contracts only** — never imports physics or agent internals.

---

# §10 Demo architecture and scenarios

## 10.1 Hero scenario (Scenario A)

Pump health drifts → crosses threshold → 5 agents fire → **"reduce load + schedule seal swap"** → human approves → audit updates.

## 10.2 Scenario matrix

| ID | Mode | Proves |
|---|---|---|
| A | gradual_pump_wear | One-best-action magic ⭐ |
| B | sudden_bearing_impact | Urgency + emergency stop |
| C | intermittent_valve | Mahalanobis pattern detection |
| D | sensor_dropout | Data quality vs. machine fault |

## 10.3 5-minute judge script

| Time | Beat |
|---|---|
| 0:00–0:45 | Götze 2014 hook |
| 0:45–1:30 | Healthy plant + LTTS–Databricks |
| 1:30–3:00 | Scenario A — health 38, RUL 12d, ONE action |
| 3:00–3:45 | Human approve → audit |
| 3:45–4:30 | Edge case (sensor dropout) |
| 4:30–5:00 | Physics + IIS + governance + $-impact |

## 10.4 v1 demo (available today)

```powershell
cd C:\Users\hp\Claude\Projects\PlantMind-Live\src\legacy\forge-v1
streamlit run app.py
```

Tabs: Decision · Proof Chart · Fleet View · Agent Trace

---

# §11 Technology stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| API | FastAPI + Pydantic v2 |
| Agents | CrewAI + LangGraph |
| LLM | Groq Llama 3.3 70B / 3.2 3B |
| Embeddings | sentence-transformers all-MiniLM-L6-v2 |
| Vector DB | ChromaDB |
| Physics | scipy Weibull; PyTorch PINN (stretch) |
| ML | scikit-learn (v1 RUL) |
| Dashboard | Streamlit + Plotly |
| Storage | SQLite (hackathon) → Delta Lake (production) |
| Cloud narrative | Databricks CE — DLT, Feature Store, Unity Catalog, Mosaic AI |

---

# §12 ROI and business case

```
Value = (failures_prevented) × (avg_downtime_hours) × (cost_per_hour) − intervention_cost
```

- **cost_per_hour:** [ESTIMATE $50K–$500K/hr by sector]  
- Demo: interactive calculator with conservative inputs  
- ExecutiveSummarizer rolls up downtime_saved_estimate

---

# §13 Research and competitive position

## 13.1 Research completed

| Phase | Artifact | Location |
|---|---|---|
| 1 Pain register | 35 pains, 5 themes | `docs/research/PAIN_REGISTER_*.md` |
| 2 Competitive map | 12+ competitors | `docs/research/COMPETITIVE_MAP_*.md` |
| 3–6 | Databricks, data, ROI, arch lock | Planned |

## 13.2 Competitive wedge

| Competitors | Gap |
|---|---|
| AspenTech, Emerson, ABB, C3.ai, Seeq | Predict and alert — no agentic one-action loop with proof |
| PlantMind | Open framework + physics IIS + human-governed audit + Databricks reference |

---

# §14 Governance, security, and IP

## 14.1 Non-negotiable principles

1. **Non-autonomous** — human approves all actions  
2. **Explainable** — reason + citations where possible  
3. **Logged** — immutable audit with hash-chain lineage  
4. **Conservative failure** — "manual review required" if AI unavailable

## 14.2 Patent posture

- **Strongest claims:** Counterfactual proof engine; IIS scoring method; closed decision loop  
- **Framing:** Patent-candidate, pending prior-art review — never "no one has done this"  
- **Files:** `src/legacy/forge-v1/PATENT_IDEAS.md`

---

# §15 24-hour build plan (hackathon)

| Hours | Milestone |
|---|---|
| 0–4 | Scaffold, synthetic data, agent stubs, Streamlit shell |
| 4–8 | DataSentinel + AssetHealthOracle |
| **H8** | Health visible on dashboard |
| 8–12 | GötzeEngine + IIS |
| 12–16 | RootCause + ExecutiveSummarizer |
| **H16** | **Full 5-agent flow — DEMO SAFE** |
| 16–20 | PINN stretch OR harden fallbacks |
| **H20** | Feature freeze |
| 20–23 | Rehearse 5+ times, backup video |
| **H23** | Tag `v1.0-hackathon-submission` |

**Golden rule:** Not integrated by Hour 16 → not in demo.

---

# §16 Implementation status and roadmap

| Component | v1 forge-v1 | v2 target | Status |
|---|---|---|---|
| Data ingest C-MAPSS | ✅ | ✅ | Built |
| Weibull multi-asset | ❌ | ✅ | Specified |
| RandomForest RUL | ✅ | Fallback | Built |
| IIS scorer | ❌ | ✅ | Locked |
| G-score | ✅ | v1 alias | Built |
| 5 agents LangGraph | ❌ | ✅ | Specified |
| FastAPI | ❌ | ✅ | Scaffolded |
| RAG RootCause | ❌ | ✅ | Specified |
| Human approve UI | ❌ | ✅ | Specified |
| RED→GREEN proof | ✅ | ✅ | Built |
| Audit hash-chain | Partial | ✅ | Specified |
| Streamlit dashboard | ✅ | Migrate | Built |
| Databricks port | Narrative | ✅ | Documented |

**ROADMAP:** See `ROADMAP.md` at project root.

---

# §17 Team structure and lanes

| Lane | Owner | Deliverable |
|---|---|---|
| 1 Backend & Agents | Sourav | agents, API, orchestrator, audit |
| 2 Physics & ML | Sourav | Weibull, synthetic data, training |
| 3 Dashboard & UI | Member 2/3 | Streamlit, IIS panel, audit views |
| 4 Databricks Port | Sourav/team | DLT, Feature Store, Unity Catalog |
| 5 Demo & Pitch | Member 4/Sourav | script, ROI, Q&A, governance story |

---

# Appendix A — Operating the single folder

| Question | Answer |
|---|---|
| Where to work? | `PlantMind-Live` only |
| What to read first? | `00-START-HERE.md` |
| What's locked? | `LOCKED_STATE.md` |
| What's next? | `ROADMAP.md` NOW |
| Where did old stuff go? | `MIGRATION-MAP.md`, `docs/CONFLICT-RESOLUTION.md` |

---

# Appendix B — Source lineage

| Version | Folder | Role |
|---|---|---|
| v1 | PlantMind/FORGE → `src/legacy/forge-v1/` | Runnable reference |
| v2 vault | PlantMind_hckthn → `docs/architecture/` | Locked specification |
| Live | PlantMind-Live | **Canonical workspace** |

---

*End of Consolidated Project Blueprint v1.0*