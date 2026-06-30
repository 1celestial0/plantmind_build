---
title: PlantMind Code-Lineage Vault
updated: 2026-07-01
mirrors: src/ and ml/ (live code tree)
---

# 🧩 PlantMind Code-Lineage Vault

> **A living map of the actual codebase, kept current with the code.** Every module links to the DNA feature (F-XX) it implements and the contract it depends on.
> Canonical truth for *behaviour* is [[../obsidian-vault/PROJECT-DNA|PROJECT-DNA]] §6 (features) + `LOCKED_STATE.md` §4 (contracts). This vault maps **where each feature LIVES in code**.
> **Maintenance rule:** update on every merge that adds/moves a module, and at each session close. Re-scan with `Glob src/**/*.py` + `ml/**/*.py`.

## Module → Feature → Contract map (live as of 2026-07-01)

### `src/contracts/` — Layer-0 IP (F-10)
| File | Holds | Status |
|---|---|---|
| `physics.py` | PhysicsModelInterface, AssetHealthReport | ✅ |
| `ui.py` | GötzeDecision, AssetHealthReport, ExecutiveBrief shapes | ✅ |
| `audit.py` | AuditRecord | ✅ |
| **`manifest.py`** | **Plant Config Manifest schema** | 🔴 **MISSING — build (F-02/F-10, top-20 #2)** |
| **`workorder.py`** | **WorkOrder (MaintenanceScheduler output)** | 🔴 **MISSING — build (F-03, top-20 #2)** |

### `src/agents/` — the agent loop (F-01,04,05,06,07 + F-15)
| File | Feature |
|---|---|
| `data_sentinel.py` | F-04 DataSentinel |
| `asset_health_oracle.py` | F-05 AssetHealthOracle |
| `gotze_engine.py` | F-01 GötzeEngine + F-08 IIS |
| `root_cause_analyst.py` | F-06 RootCauseAnalyst |
| `executive_summarizer.py` | F-07 ExecutiveSummarizer |
| **`maintenance_scheduler.py`** | 🔴 **MISSING — build (F-03)** |
| `base.py` | agent base class |

### `src/physics/` — F-05 (must use LOCKED_STATE §6a λ/β)
`weibull.py` · `stress.py` · `constants.py` · `model.py` — ⚠️ verify §6a λ/β wired; RUL=days (top-20 #7)

### `src/pipeline/` — F-15 orchestrator
`orchestrator.py` (state machine) · `schemas.py` (PlantMindState)

### `src/governance/` — F-09
`audit.py` (append-only + hash chain) — verify integrity check runs (may raise rubric #6)

### `src/rag/` — F-06
`store.py` (ChromaDB → Vector Search in L1)

### `src/dashboard/` — F-13,14 + Config Viewer (F-02) ⚠️ needs dark→light reskin (C3)
`app.py` · `styles.py` · `pages/{plant_overview,fleet_overview,gotze_decision,audit_log}.py` · `demo_scenarios.py` · `fleet_data.py` · `failure_patterns.py`
🔴 **MISSING pages: Config Viewer (F-02), Decisions/Audit-Lineage explorer (F-09)**

### `src/api/` — FastAPI serving
`main.py` · `routes/{analyze,decisions,audit_log,health_check}.py`

### `ml/` — training/calibration (F-05 stretch PINN)
*(scan `ml/**` to populate — calibrate_weibull, optional PINN)*

## Open code gaps (→ top-20 build items)
1. 🔴 `contracts/manifest.py` + `contracts/workorder.py` (#2)
2. 🔴 `agents/maintenance_scheduler.py` (#13)
3. ⚠️ config loader/composer for the manifest (#9 — highest risk)
4. ⚠️ verify §6a λ/β + RUL units in `physics/` (#7)
5. dashboard light reskin + Config Viewer + Audit explorer (#16,17)

---
*Seeded 2026-07-01 from live `Glob src/**/*.py`. Keep current with code.*
