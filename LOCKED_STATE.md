# LOCKED_STATE.md — PlantMind × Götze Engine
> The canonical heartbeat of the vault. Every chat reads this first and treats it as truth. Update it only via 🔒 VAULT UPDATE blocks. Last synced: 2026-07-01 (PlantMind) — **PRODUCT IDEA LOCKED** after final deep-research pass (3 Grok specs absorbed).

---

## 0. Project identity (LOCKED)
- **Project:** PlantMind × Götze Engine — Config-Driven, Physics-Informed Engineering Intelligence for industrial assets.
- **Canonical workspace:** `C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live`
- **Owner:** Sourav Dutta, Senior Data Engineer, LTTS.
- **Event:** LTTS Global Engineering Intelligence Hackathon — 2026-07-09 (24h, OpenHack, 4 members).
- **Strategic anchor (verified):** LTTS × Databricks Industrial AI / Engineering Intelligence partnership, announced 2026-06-11. Five joint areas: Predictive Asset Reliability, Energy & Emissions Optimization, OEE & Production Intelligence, Quality Intelligence, Sustainability Analytics → each maps 1:1 to a swappable IIS profile (see §2a).
- **TWO CO-EQUAL INNOVATION PILLARS (LOCKED 2026-07-01):**
  1. **Closed decision loop** — physics health → IIS → one approved, audited action. (The trust/governance wedge.)
  2. **Config-driven modularity** — a declarative Plant Config Manifest composes the whole stack; onboarding a new plant/asset/use-case is a *config change, not a code deploy*. (The scale/CoE/productization wedge.) See §9.
- **One-sentence positioning (LOCKED):** "PlantMind is the config-driven decision fabric that turns existing plant data and digital twins into trusted, physics-grounded, auditable engineering actions — at scale, across any asset class, without rip-and-replace."

## 1. The 5 agents (LOCKED — hackathon scope)
1. **DataSentinel** — flags sensor anomalies (Z-score + Mahalanobis). Flags only.
2. **AssetHealthOracle** — health 0–100 + RUL + CI (Weibull). Reports only.
3. **GötzeEngine** ⭐ — scores candidate interventions via IIS → one best action. **Requires human approval.**
4. **RootCauseAnalyst** — RAG over manuals/logs → cited causal chain.
5. **ExecutiveSummarizer** — 3-bullet leadership brief.
6. **MaintenanceScheduler** ⭐ (RESOLVED 2026-07-01) — on human approval, turns the Götze action into a work order (SAP PM / Maximo REST in production; queued work-order record + audit entry in hackathon). Closes the loop back into existing business systems. **Fires only after approval; never autonomous.** SafetyGuardian was rejected as a separate agent — its veto already lives in IIS (SafetyRiskDelta + hard ceiling, §2).

## 2. The IIS formula (LOCKED)
```
IIS(i) = 0.35·ΔP_failure + 0.25·ΔDowntimeCost + 0.20·Feasibility
       + 0.15·HistoricalSuccess − 0.05·SafetyRiskDelta
```
- All terms normalized to [0,1] before weighting.
- **Demo:** fixed weights. **Production:** self-calibrating (narrative only — no outcome data in 24h).
- Hard rule: SafetyRiskDelta above ceiling → action vetoed regardless of score.

## 2a. IIS weight profiles (LOCKED 2026-07-01 — declared in the manifest, swappable per site/asset)
Same formula, different weights = different business outcome. Each profile maps to a Databricks joint area (§0).
| Profile | ΔP_fail | ΔDowntime$ | Feasibility | HistSuccess | −SafetyRiskΔ | Maps to |
|---|---|---|---|---|---|---|
| **reliability_first** (demo default) | 0.35 | 0.25 | 0.20 | 0.15 | 0.05 | Predictive Asset Reliability |
| energy_optimization | 0.20 | 0.35 | 0.20 | 0.15 | 0.10 | Energy & Emissions Optimization |
| quality_driven | 0.30 | 0.20 | 0.25 | 0.20 | 0.05 | Quality Intelligence |
| sustainability_max | 0.20 | 0.20 | 0.20 | 0.10 | 0.30 | Sustainability Analytics |
> Weights for non-reliability profiles are [ESTIMATE] — tune at build. Demo SHOWS modularity by live-swapping reliability_first → energy_optimization and watching the top recommendation reorder (UI Config Viewer toggle, §10).

## 3. Trigger thresholds (LOCKED, tunable in plant_config.yaml)
- Invoke GötzeEngine if `health < 40` OR `rul_days < 14` OR DataSentinel severity == critical.

## 4. Shared contracts (LOCKED — the API between lanes)
**Code home:** `src/contracts/` (Pydantic models must match these shapes)

**PhysicsModelInterface** (Lane 2 owns; Lane 1 consumes):
```
output = {health_index: float, rul_estimate: float,
          confidence_interval: [low, high], physics_explanation: str}
```
**UI JSON** (Lane 1 owns; Lane 3 consumes): GötzeDecision + AssetHealthReport + ExecutiveBrief
```
GötzeDecision = {top_intervention, iis_score, runner_up, iis_gap,
                 narrative, confidence, requires_human_approval}
AssetHealthReport = {asset_id, health_score, rul_days, ci_95, physics_text}
ExecutiveBrief = {critical_alerts, gotze_pending, downtime_saved_estimate}
```
**AuditRecord** (Lane 1 owns; all consume):
```
{record_id, timestamp, asset_id, stage, actor, model_used, input_ref,
 output, iis_score, requires_approval, decision, reason, lineage[]}
```

## 5. Stack (LOCKED — local/hackathon)
Python 3.11 · FastAPI · Pydantic v2 · CrewAI + LangGraph · Groq Llama 3.3 70B (narrative) / 3.2 3B (summary) · sentence-transformers all-MiniLM-L6-v2 · ChromaDB · scikit-learn + scipy (+ PyTorch for optional PINN) · Streamlit + Plotly · SQLite.
> Verify model availability / free-tier limits / library versions at build time.
> Model routing registry: `ops/MODEL-REGISTRY.md`

## 6. Data (LOCKED)
- Kaggle seed: CMAPSS, PRONOSTIA, Azure PdM → calibrate λ, β.
- Synthetic: 30 assets × 20 signals × 3 failure modes × 500 cycles, physics-seeded.
- RAG corpus: 10–20 manuals/SOPs/fault logs in ChromaDB.

## 6a. Physics constants (LOCKED — Lane 2 owns; Lane 4 must mirror)
- **PhysicsModelInterface.rul_estimate unit = DAYS.** confidence_interval also in days. (cycles ÷ CYCLES_PER_DAY)
- **CYCLES_PER_DAY = 6.0** [ESTIMATE]. **H_FAILURE_THRESHOLD = 20.0** (RUL→0). Intervention trigger stays health<40 / rul_days<14 (§3).
- **Stress folded into effective rate:** H(t)=100·exp(−λ·S·t^β), S=AF_temp·AF_load, ==1 at reference (25°C, rated load). Arrhenius EA=0.15 eV [ESTIMATE]; load exponent m=2.0 [ESTIMATE].
- **Corrected Weibull params** (β from KB; λ recalibrated to life_ref so H hits 20 within 350–480 cycles). These SUPERSEDE the Databricks KB λ values (0.0021 etc., which collapse health by ~cycle 30). Lane 4 UDF must adopt these:
  | asset | λ | β | life_ref |
  |---|---|---|---|
  | pump | 1.49e-6 | 2.3 | 420 |
  | compressor | 1.83e-5 | 1.9 | 400 |
  | motor | 5.98e-8 | 2.8 | 450 |
  | bearing | 2.01e-9 | 3.5 | 350 |
  | valve | 1.53e-4 | 1.5 | 480 |
  λ are [ESTIMATE] calibration targets — replace with calibrate_weibull.py MLE output when ready.

## 7. Locked decisions (do not relitigate without a VAULT UPDATE)
- **Weibull analytical baseline ships first and always.** PINN is optional stretch; freeze it by Hour 14 if not validating; fallback is invisible to judges.
- **Demo uses fixed IIS weights.** Self-calibration is production narrative only.
- **Novelty framing:** "patent-candidate, pending prior-art review." Defensible wedge = the closed decision loop (physics health → IIS → one approved, audited action), NOT the PINN alone. Never claim "no one has done this."
- **All agents non-autonomous, explainable, logged.**
- **Win condition:** rehearsed demo of the one-best-action moment + honest $-impact + Databricks tie-in. Not unbuilt physics.
- **v1 FORGE fallback:** `../PlantMind/FORGE/` remains runnable demo until `src/dashboard/` is wired. Not canonical for contracts.
- **Config-driven is now a co-equal headline pillar (LOCKED 2026-07-01), not just production narrative.** See §9.
- **Build scope = FULL config-driven pipeline (LOCKED 2026-07-01)** — the manifest genuinely composes ingestion/features/health/IIS/dashboard at runtime. **GUARDRAIL (non-negotiable, per win condition):** a static/hardcoded path for the 3 demo assets must stay runnable at all times; if manifest wiring isn't stable by **Hour 16**, freeze it and demo the static path — the "read any plant as config" claim is then shown via the Config Viewer + one live profile swap, narrated as the generalization. Demo never dies.
- **⚠️ λ/β TRAP:** the Grok Project-Spec manifest example (`lambda: 0.0023, beta: 2.1`) reintroduces SUPERSEDED naive values that collapse health by ~cycle 30. Manifest examples are illustrative ONLY; **§6a values are canonical.** Any manifest used for the demo MUST carry §6a λ/β.
- **⚠️ RUL-unit TRAP:** Grok Databricks-guide PyFunc passes `rul_cycles=float(row["rul_days"])` — feeds days into a cycles param (6× error). RUL = DAYS everywhere (§6a). Fix on copy.

## 8. Lane ownership
| Lane | Owner | Builds | Folder |
|---|---|---|---|
| 1 Backend & Agents | Sourav | agents, orchestrator, IIS, API, audit | `src/agents/`, `src/api/`, `src/pipeline/` |
| 2 Physics & ML | Sourav | Weibull, synthetic data, PhysicsModelInterface, PINN(stretch) | `src/physics/`, `ml/` |
| 3 UI & Mockups | Member 2 / 3 | Streamlit, charts, best-action panel, audit views | `src/dashboard/` |
| 4 Databricks Port | Sourav / team | DLT, Feature Store, Unity Catalog, Mosaic AI | `deploy/databricks/` |
| 5 Demo & Pitch | Member 4 / Sourav | injector, script, Q&A, ROI, governance story | `ops/runbooks/` |

## 9. Config-Driven Architecture & Two-Layer IP (LOCKED 2026-07-01)
**Plant Config Manifest** (`src/contracts/` schema + `config/plants/*.yaml`) is the single source of truth. Sections (LOCKED):
`plant_id` · `asset_hierarchy` (asset_id, asset_class) · `data_sources` + `tag_mapping` (semantic layer: raw tag → signal_type/unit/failure_mode) · `physics_model` (per asset_class — **must use §6a λ/β**) · `intervention_library` · `iis_profile` (→ §2a weights) · `governance` (approval_workflow, audit_retention) · `use_cases`.
- **Demo manifest:** ≥1 asset class real end-to-end + reliability_first profile; Config Viewer shows it driving the running pipeline + one live profile swap.
- **Two-Layer architecture (LOCKED):**
  - **Layer 0 — Framework (portable LTTS IP):** vendor-agnostic interface contracts. The licensable/reusable asset. Lives in `src/contracts/`.
    Interfaces: `IngestorInterface · FeatureStoreInterface · PhysicsModelInterface · InterventionScorerInterface (GötzeEngine) · KnowledgeRetrieverInterface · GovernanceInterface · OrchestratorInterface`.
  - **Layer 1 — Reference impl (Databricks-native):** Auto Loader+DLT (Bronze/Silver/Gold) · Feature Store · MLflow+Mosaic AI (Götze serving) · Unity Catalog+Vector Search (governance+RAG) · Workflows. This is the "production path" judges see; hackathon realizes it locally (Python/Pydantic/SQLite/ChromaDB/Streamlit) with the SAME Layer-0 contracts.
- **Business model framing (LOCKED):** Layer 0 = LTTS CoE / licensable framework; "PlantMind Implementation & Config-Driven EI Transformation" service offering; accelerates Databricks GTM as the decision-fabric layer.

## 10. UI/UX (LOCKED 2026-07-01 — realign from current dark theme)
- **Palette (LIGHT, high-trust):** bg off-white `#FAFAFA`; primary deep navy `#003366`; accent/CTA + critical orange `#FF6B00`; health green `#2E7D32` / amber `#F9A825` / red `#C62828`; text `#212121`. Feel: "SCADA meets Notion" — calm, not flashy. **Supersedes the dark-theme dashboard from commit d40a00a — Lane 3 reskins to light.**
- **Typography:** Inter / system sans; tabular figures / mono for precision numbers.
- **Nav (6, persistent sidebar):** Plant Overview · Assets · Decisions · **Config** (manifest viewer + IIS-profile swap = innovation showcase) · Audit & Lineage · Impact (stretch).
- **Hero screen:** Asset Detail split view — left 55% asset intelligence (health gauge, RUL+CI, physics text, sensor trends); right 45% **Götze Decision Panel** (top rec + IIS bar + plain-English reason + key drivers; runner-up + score gap; expandable citations; Approve/Approve-w-comment/Reject-w-reason/[Request 2nd opinion stretch]). "Human Approval Required" always visible, non-dismissible.
- **Trust signals everywhere:** every number has context; physics confidence %; "based on N similar assets"; calm/informative loading & error states. WCAG 2.1 AA; color never sole signal (icon+text).
- **Stack:** Streamlit + Plotly (hackathon) → React/TS/Tailwind+shadcn (production narrative).

---

## EVOLUTION_LOG
```
2026-06-28 | vault | Initial LOCKED_STATE created from 10-doc KB + Databricks KB. | baseline
```
```
2026-06-28 | lane2 | Added §6a physics constants; corrected λ. | unblock Lane1 consume + Lane4 parity
```
```
2026-06-29 | ops | PlantMind canonical workspace; contracts → src/contracts/; MODEL-REGISTRY; v1 FORGE fallback note. | single living folder
```
```
2026-07-01 | vault | PRODUCT LOCKED. Absorbed 3 Grok specs (Project/Databricks/UI). Added 2nd pillar (config-driven, §0/§9); IIS profiles §2a; 6th agent=MaintenanceScheduler §1; Two-Layer IP §9; UI light-palette realign §10; full-config-pipeline build scope + Hour-16 fallback, λ/β + RUL traps §7. | final deep-research pass; idea frozen
```
> Append one line per change. Format: YYYY-MM-DD | lane | what changed | why.