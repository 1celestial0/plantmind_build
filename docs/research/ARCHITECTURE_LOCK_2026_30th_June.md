# ARCHITECTURE_LOCK.md
## PlantMind — Phase 6: Architecture Lock (Synthesis)
**Lock Date:** 2026-06-30  
**Inputs:** PAIN_REGISTER, COMPETITIVE_MAP, DATABRICKS_MAP, DATA_REALITY, ROI_BENCHMARKS, LOCKED_STATE

---

## Project identity (canonical)

**PlantMind** = open Engineering Intelligence framework (Layer 0) + Databricks Tier-1 reference (Layer 1).

**Pitch:** Physics-grounded health, IIS intervention scoring, human-governed audit — mapped 1:1 to LTTS×Databricks Industrial AI partnership.

**Hackathon scope:** 5 agents, Weibull-first, SQLite local, Streamlit demo, Databricks narrative.

---

## TASK 1 — Validation Gate (8 capabilities)

| # | Capability | Pain ID | Competitive gap | Databricks | Data | ROI | Status |
|---|------------|---------|-----------------|------------|------|-----|--------|
| 1 | Real-time anomaly detection | P005, P023 | vs alarm-only vendors | MLflow + Serving | sensor_readings | Part B | ✅ PASS |
| 2 | Agentic root cause + citation | P003, P010 | vs black-box ML | Vector Search | sop_chunks | Part F | ✅ PASS |
| 3 | NL maintenance recommendation | P008 | vs CMMS sort-only | Mosaic AI | gotze_decisions | Part G | ✅ PASS |
| 4 | Engineering knowledge RAG | P004, P007 | vs siloed historians | Vector Search | document_registry | Part F | ✅ PASS |
| 5 | Energy optimization insights | P013 | vs bill-only review | Feature Store | sensor_readings | Part C | ✅ PASS (stretch) |
| 6 | OEE intelligence | P021 | vs manual OEE Excel | Databricks SQL | asset_health | Part D | ✅ PASS (stretch) |
| 7 | Human-in-loop + audit | P014 | vs autonomous AI fear | Unity Catalog | audit_records | Part H | ✅ PASS |
| 8 | Feedback loop retrain | P011 | vs symptom-only fix | Workflows | maintenance_outcomes | Part B | ✅ PASS (narrative) |

No [GATE FAIL] items — build authorized for hackathon scope.

---

## TASK 2 — Layer 0 contracts (code = `src/contracts/`)

| Contract | Owner | Consumer | Pydantic model |
|----------|-------|----------|----------------|
| PhysicsModelOutput | Lane 2 | Lane 1 | `physics.py` |
| GotzeDecision | Lane 1 | Lane 3 | `ui.py` |
| AssetHealthReport | Lane 1 | Lane 3 | `ui.py` |
| ExecutiveBrief | Lane 1 | Lane 3 | `ui.py` |
| AuditRecord | Lane 1 | All | `audit.py` |

**Quality guarantees (hackathon):**
- API response < 3s (Phase 5 gate)
- IIS deterministic — same inputs → same score
- LLM never picks winner — only narrates
- SafetyRiskDelta ceiling → veto (LOCKED §2)

---

## TASK 3 — Layer 1 Databricks binding

See `DATABRICKS_MAP_2026_30th_June.md` Part B. Local SQLite audit mirrors Gold `audit_records` for demo.

---

## TASK 4 — Build sequence (locked)

| Phase | Deliverable | Lane |
|-------|-------------|------|
| P0 | Contracts + ops (this session) | — |
| P1 | Physics + synthetic data | 2 |
| P2 | Agents + orchestrator + API | 1 |
| P3 | Dashboard + approval UX | 3 |
| P4 | Scenario injector + pitch | 5 |
| P5 | Databricks notebooks | 4 |
| P6 | Integration freeze T-6h | All |

**Golden rule:** Not integrated by Hour 16 of hackathon → not in live demo.

---

## TASK 5 — Explicit non-goals (hackathon)

- PINN production dependency
- Live OPC-UA ingest
- Autonomous work order execution without approval
- 6th agent (MaintenanceScheduler vs SafetyGuardian) — UNDECIDED

---

## TASK 6 — Demo architecture lock

**Hero scenario A:** `pump_07` gradual wear → health 38 → RUL 12d → IIS winner → human approve → audit.

**Fallback:** v1 legacy shell only if v2 integration misses freeze — narrative from `08_DEMO_SCENARIOS.md`.

---

## ARTIFACT QUALITY CHECKLIST

- [x] All 8 capabilities pass 5-gate check
- [x] Layer 0 contracts implemented in `src/contracts/`
- [x] Layer 1 mapping cited
- [x] Build sequence ordered
- [x] Non-goals explicit