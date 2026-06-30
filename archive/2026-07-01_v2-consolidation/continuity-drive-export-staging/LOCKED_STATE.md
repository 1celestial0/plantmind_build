# LOCKED_STATE.md — PlantMind × Götze Engine
> The canonical heartbeat of the vault. Every chat reads this first and treats it as truth. Update it only via 🔒 VAULT UPDATE blocks. Last synced: 2026-06-29 (PlantMind).

---

## 0. Project identity (LOCKED)
- **Project:** PlantMind × Götze Engine — Physics-Informed Engineering Intelligence for industrial assets.
- **Canonical workspace:** `C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live`
- **Owner:** Sourav Dutta, Senior Data Engineer, LTTS.
- **Event:** LTTS Global Engineering Intelligence Hackathon — 2026-07-09 (24h, OpenHack, 4 members).
- **Strategic anchor (verified):** LTTS × Databricks Industrial AI / Engineering Intelligence partnership, announced 2026-06-11. Five joint areas: Predictive Asset Reliability, Energy & Emissions Optimization, OEE & Production Intelligence, Quality Intelligence, Sustainability Analytics.

## 1. The 5 agents (LOCKED — hackathon scope)
1. **DataSentinel** — flags sensor anomalies (Z-score + Mahalanobis). Flags only.
2. **AssetHealthOracle** — health 0–100 + RUL + CI (Weibull). Reports only.
3. **GötzeEngine** ⭐ — scores candidate interventions via IIS → one best action. **Requires human approval.**
4. **RootCauseAnalyst** — RAG over manuals/logs → cited causal chain.
5. **ExecutiveSummarizer** — 3-bullet leadership brief.
- **6th agent:** UNDECIDED. Candidates: MaintenanceScheduler (approved action → work order) or SafetyGuardian (hard veto on unsafe actions). [OPEN]

## 2. The IIS formula (LOCKED)
```
IIS(i) = 0.35·ΔP_failure + 0.25·ΔDowntimeCost + 0.20·Feasibility
       + 0.15·HistoricalSuccess − 0.05·SafetyRiskDelta
```
- All terms normalized to [0,1] before weighting.
- **Demo:** fixed weights. **Production:** self-calibrating (narrative only — no outcome data in 24h).
- Hard rule: SafetyRiskDelta above ceiling → action vetoed regardless of score.

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

## 8. Lane ownership
| Lane | Owner | Builds | Folder |
|---|---|---|---|
| 1 Backend & Agents | Sourav | agents, orchestrator, IIS, API, audit | `src/agents/`, `src/api/`, `src/pipeline/` |
| 2 Physics & ML | Sourav | Weibull, synthetic data, PhysicsModelInterface, PINN(stretch) | `src/physics/`, `ml/` |
| 3 UI & Mockups | Member 2 / 3 | Streamlit, charts, best-action panel, audit views | `src/dashboard/` |
| 4 Databricks Port | Sourav / team | DLT, Feature Store, Unity Catalog, Mosaic AI | `deploy/databricks/` |
| 5 Demo & Pitch | Member 4 / Sourav | injector, script, Q&A, ROI, governance story | `ops/runbooks/` |

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
> Append one line per change. Format: YYYY-MM-DD | lane | what changed | why.