# PlantMind × Götze Engine — Project Specification v2.0
_Generated 2026-07-01 · **DERIVED from `PROJECT-DNA.md` v1.0 (LOCKED) + `LOCKED_STATE.md`.** Where any doc differs, those win. Supersedes the June Grok spec (which was pre-lock)._
**LTTS Global Engineering Intelligence Hackathon · 2026-07-09**

---

## 1. Executive summary & innovation thesis
PlantMind is a **config-driven, physics-informed, agentic decision fabric** for asset-intensive industries. It turns existing plant data into **trusted, ranked, human-approved, audited engineering actions** — without rip-and-replace.

**Two co-equal innovation pillars:**
- **P1 — Closed decision loop:** physics health → IIS scoring → one approved, audited action. (Trust/governance wedge.)
- **P2 — Config-driven modularity:** a declarative Plant Config Manifest composes the whole stack; onboarding a new plant/asset/use-case is a *config change, not a code deploy*. (Scale / CoE / productization wedge.)

**Positioning:** *"PlantMind is the config-driven decision fabric that turns existing plant data and digital twins into trusted, physics-grounded, auditable engineering actions — at scale, across any asset class, without rip-and-replace."*

**What it is NOT:** not a digital twin, not an alerting/PdM tool, not a generic agent builder — it is the governed decision-and-action layer on top of them.

## 2. The problem
Asset-intensive plants have historians, EAM/CMMS, and dashboards — but lack a *governed* way to turn data into ranked, feasible, auditable actions, and every new site needs custom integration. Result: alert fatigue, tribal knowledge, slow response, pilots that don't scale. PlantMind closes that gap.

## 3. Architecture — two layers
- **Layer 0 — Framework (portable LTTS IP):** vendor-agnostic Pydantic interface contracts. The licensable / reusable asset. Lives in `src/contracts/`.
  Interfaces: `IngestorInterface · FeatureStoreInterface · PhysicsModelInterface · InterventionScorerInterface (GötzeEngine) · KnowledgeRetrieverInterface · GovernanceInterface · OrchestratorInterface`.
- **Layer 1 — Reference implementation (Databricks-native):** Auto Loader + DLT (Bronze/Silver/Gold) · Feature Store · MLflow + Mosaic AI (Götze serving) · Unity Catalog + Vector Search (governance + RAG) · Workflows. The hackathon realizes the same Layer-0 contracts locally (Python/Pydantic/SQLite/ChromaDB/Streamlit).

## 4. Config-driven modularity — the Plant Config Manifest
A declarative manifest (`config/plants/*.yaml`) is the single source of truth that composes the stack. Sections:
`plant_id · asset_hierarchy (asset_id, asset_class) · data_sources + tag_mapping (semantic layer: raw tag → signal_type/unit/failure_mode) · physics_model (per asset_class — uses LOCKED_STATE §6a λ/β) · intervention_library · iis_profile (→ §6 weights) · governance (approval_workflow, audit_retention) · use_cases`.
Onboarding a new plant/asset/use-case = editing the manifest. **Hackathon build = full config-driven pipeline for ≥1 asset class, with a static fallback path (frozen by Hour 16 if unstable).**

## 5. The 6 specialist agents (directed state machine)
| Agent | Role | Engine | Output |
|---|---|---|---|
| DataSentinel | flag abnormal sensors | Z-score + Mahalanobis | DataQualityReport |
| AssetHealthOracle | health + RUL with physics | Weibull (analytical) | AssetHealthReport (health 0–100, **RUL in days**, CI, physics text) |
| **GötzeEngine ⭐** | score every intervention → one best action | IIS scorer + Groq narrative | GötzeDecision (top action, IIS, runner-up, gap, requires_approval=True) |
| RootCauseAnalyst | cited causal chain | RAG (ChromaDB → Vector Search) | CausalChain (steps + citations) |
| ExecutiveSummarizer | 3-bullet leadership brief | small LLM (Llama 3.2 3B) | ExecutiveBrief (alerts, pending, downtime_saved) |
| **MaintenanceScheduler ⭐** | approved action → work order | post-approval handler | WorkOrder (+ audit entry) |
**Graceful degradation:** if one agent fails, the orchestrator logs and continues — the "one best action" panel still renders. *(SafetyGuardian is NOT a separate agent — its veto lives in IIS.)*

## 6. GötzeEngine & the Intervention Impact Score (IIS)
```
IIS(i) = w1·ΔP_failure + w2·ΔDowntimeCost + w3·Feasibility + w4·HistoricalSuccess − w5·SafetyRiskDelta
```
All terms normalized to [0,1]. Hard rule: SafetyRiskDelta above ceiling → action vetoed regardless of score. **Demo uses fixed weights; self-calibration is production narrative only.** Every recommendation carries `requires_human_approval = True` — never autonomous.

**Swappable weight profiles (declared in the manifest) — each maps to a Databricks joint area:**
| Profile | ΔP_fail | ΔDt$ | Feas | Hist | −Safety | Maps to |
|---|---|---|---|---|---|---|
| reliability_first (demo default) | 0.35 | 0.25 | 0.20 | 0.15 | 0.05 | Predictive Asset Reliability |
| energy_optimization | 0.20 | 0.35 | 0.20 | 0.15 | 0.10 | Energy & Emissions |
| quality_driven | 0.30 | 0.20 | 0.25 | 0.20 | 0.05 | Quality Intelligence |
| sustainability_max | 0.20 | 0.20 | 0.20 | 0.10 | 0.30 | Sustainability Analytics |
Demo *shows* modularity by live-swapping reliability_first → energy_optimization and watching the top recommendation reorder.

## 7. Physics & ML (guaranteed path)
Analytical Weibull degradation: `H(t) = 100 · exp(−λ · S · t^β)`, stress `S = AF_temp · AF_load` (=1 at reference). **λ/β per asset class are LOCKED in LOCKED_STATE §6a** (calibration targets — *not* the old 0.0023 example, which collapses health by ~cycle 30). `CYCLES_PER_DAY = 6.0`, `H_FAILURE_THRESHOLD = 20`. Triggers: health < 40 OR rul_days < 14 OR DataSentinel critical. **RUL is always in DAYS.** PINN is a stretch only (freeze Hour 14). Medallion: Bronze → Silver (physics features) → Gold (status, triggers, decision history, RAG KB).

## 8. Governance & trust
Immutable append-only audit with **hash chain** (hackathon) / Unity Catalog + Delta time-travel (production); full lineage Sensor → Health → IIS → Cause → Approval; human approval gate; every output carries citations or physics narrative; governance rules declared in the manifest.

## 9. Feature inventory (15 — full detail in PROJECT-DNA §6)
F-01 Götze Decision Panel · F-02 Config Manifest + Viewer · F-03 MaintenanceScheduler · F-04 DataSentinel · F-05 AssetHealthOracle · F-06 RootCauseAnalyst · F-07 ExecutiveSummarizer · F-08 IIS Engine & Profiles · F-09 Audit/Hash-Chain/Lineage · F-10 Layer-0 Contracts · F-11 Synthetic Data + Injector · F-12 Databricks Medallion · F-13 Plant Overview · F-14 Asset Detail Hero · F-15 Orchestrator. Each defined what/who/how/why with demo-proof in the DNA.

## 10. UI/UX (light, high-trust)
Palette: off-white `#FAFAFA`, deep navy `#003366`, accent/critical orange `#FF6B00`, health green/amber/red; Inter + tabular figures; "SCADA meets Notion." 6-section nav: Plant Overview · Assets · Decisions · **Config** (manifest + IIS-profile swap) · Audit & Lineage · Impact. Hero = Asset Detail split view (left intelligence, right Götze panel; "Human Approval Required" always visible). Stack: Streamlit + Plotly (hackathon) → React/TS/Tailwind (production).

## 11. Hackathon scope & demo
**Demo shape (pinned):** 3 assets on stage; **hero = PUMP-001** (centrifugal, gradual_wear); 30-asset fleet behind it; headline **~$180k downtime saved per prevented pump failure**; one IIS-profile swap. **Demo runs locally** (Streamlit + SQLite); Databricks shown as scale/credibility via Unity Catalog lineage (promoted to stage only if stable by Hour 20). **Groq live-fail fallback:** pre-cached Götze narrative (IIS score is deterministic). Freeze schedule: H-14 PINN · H-16 config pipeline · H-20 feature freeze · then rehearsal only.

## 12. Differentiation
vs PdM/anomaly (stops at alerts) · vs digital twins (visualize/simulate) · vs generic agent platforms (not physics/governance-grounded) · vs custom services (per-site code). PlantMind = the config-driven, governed decision fabric that closes the loop and scales by config.

## Appendix — stack & contracts
Python 3.11 · FastAPI · Pydantic v2 · CrewAI + LangGraph · Groq Llama 3.3 70B (narrative) / 3.2 3B (summary) · sentence-transformers all-MiniLM-L6-v2 · ChromaDB · scikit-learn + scipy (+ PyTorch optional PINN) · Streamlit + Plotly · SQLite. Shared contracts (`src/contracts/`): PhysicsModelInterface, GötzeDecision, AssetHealthReport, ExecutiveBrief, AuditRecord, WorkOrder, Plant Config Manifest — see LOCKED_STATE §4/§9.

— End of Project Specification v2.0 · derived from PROJECT-DNA v1.0 · 2026-07-01 —
