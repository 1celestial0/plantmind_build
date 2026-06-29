# Codebase Inventory & Lineage
**Project:** PlantMind | **Updated:** 2026-06-29 | **Workspace:** `C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live`

---

## 1. Inventory summary

| Zone | Path | Files | Status | Role |
|---|---|---|---|---|
| v2 target | `src/` (excl. legacy) | scaffold | BUILD | Production codebase |
| v1 reference | `src/legacy/demo-v1-metagpt/` | 19 py/md | **RUNNABLE** | Hackathon demo |
| ML | `ml/` | scaffold | BUILD | Data, training, synthesis |
| Ops | `ops/` | 10+ | ACTIVE | Prompts, routing, registry |
| Docs | `docs/` | 42+ | CANONICAL | Spec, research, legacy |
| Deploy | `deploy/` | scaffold | PLAN | Local + Databricks |
| Knowledge | `knowledge/obsidian-vault/` | many | REF | Obsidian graph |
| Archive source | `PlantMind_Archive/*` | 235+ | **READ-ONLY** | Pre-merge snapshots |

---

## 2. v1 runnable inventory (`src/legacy/demo-v1-metagpt/`)

| File | Layer | Input → Output | Lineage parent |
|---|---|---|---|
| `src/ingestion.py` | L1 Data | CSV → DataFrame+RUL | NASA C-MAPSS loader |
| `src/features.py` | L2 Features | DataFrame → feature matrix | 30-cycle window |
| `src/model.py` | L3 Prediction | features → RUL float | RandomForest |
| `src/messages.py` | Contracts | — | 5 frozen dataclasses |
| `src/gotze_engine.py` | L4 Decision | EngineHealth → EngineDecision | G-score IP |
| `src/pipeline.py` | Orchestrator | engine_id → full result | MetaGPT pattern |
| `src/roles/data_engineer.py` | Role | raw → prepared data | MetaGPT L2 |
| `src/roles/ml_engineer.py` | Role | data → EngineHealth | MetaGPT L2 |
| `src/roles/proof_engineer.py` | Role | decision → chart JSON | MetaGPT L2 |
| `app.py` | Dashboard | pipeline → Streamlit UI | 4 tabs |
| `run_demo.py` | CLI | synthetic demo | No install path |

**Run:** `streamlit run src/legacy/demo-v1-metagpt/app.py`

---

## 3. v2 target inventory (`src/` — to build)

| Path | Phase | Replaces / extends |
|---|---|---|
| `src/contracts/` | P0 | `messages.py` + LOCKED_STATE §4 |
| `src/physics/weibull.py` | P1 | `model.py` (canonical health) |
| `src/agents/data_sentinel.py` | P2 | new |
| `src/agents/asset_health_oracle.py` | P2 | `ml_engineer` role |
| `src/agents/gotze_engine.py` | P3 | `gotze_engine.py` (IIS rewrite) |
| `src/agents/root_cause_analyst.py` | P4 | new (RAG) |
| `src/agents/executive_summarizer.py` | P4 | new |
| `src/pipeline/orchestrator.py` | P4 | `pipeline.py` (LangGraph) |
| `src/api/routes/*.py` | P4 | new |
| `src/governance/audit.py` | P4 | JSONL partial |
| `src/dashboard/app.py` | P5 | `app.py` + approve UI |
| `ml/synthesis/generate_data.py` | P1 | new |

---

## 4. Data lineage diagram

```
[Kaggle CMAPSS] ──calibrate──► plant_config.yaml (λ, β)
                                    │
[Synthetic 30 assets] ──► ml/data/processed/ ──► features
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
            v1: RandomForest                  v2: Weibull H(t)
            (demo-v1-metagpt/model.py)               (src/physics/)
                    │                               │
                    └───────────┬───────────────────┘
                                ▼
                    EngineHealth / AssetHealthReport
                                ▼
              v1: G-score (demo-v1-metagpt)  │  v2: IIS (src/agents/)
                                ▼
                    GötzeDecision + proof + audit
                                ▼
                    dashboard (Streamlit)
```

---

## 5. Document lineage

| Document | Status | Superseded by |
|---|---|---|
| `docs/00-MASTER-SPEC.md` | **CANONICAL** | — (merges all below) |
| `LOCKED_STATE.md` | **LOCKED** | — (decisions only) |
| `docs/CONSOLIDATED-PROJECT-BLUEPRINT.md` | merged into MASTER-SPEC §1-9 | 00-MASTER-SPEC |
| `docs/IMPLEMENTATION-GUIDE-ULTRA.md` | merged into MASTER-SPEC §10-12 | 00-MASTER-SPEC |
| `docs/CONFLICT-RESOLUTION.md` | audit trail — keep | — |
| `docs/WIN-STRATEGY-ASSESSMENT.md` | merged into MASTER-SPEC §13 | 00-MASTER-SPEC |
| `docs/architecture/01-10` | source KB — keep | MASTER-SPEC references |
| `docs/legacy/v1-blueprint/` | frozen reference | MASTER-SPEC §legacy |
| `_archive/.../snapshot-*` | frozen | MIGRATION-MAP |

---

## 6. Archive lineage

| Snapshot | Original path | Date | Contents |
|---|---|---|---|
| `20260629_snapshot-v1-forge` | `Projects/PlantMind/` | 2026-06-29 | FORGE, research, v1 blueprints |
| `20260629_snapshot-hackathon-vault` | `Projects/PlantMind_hckthn/` | 2026-06-29 | 10-doc KB, LOCKED_STATE source |

Active workspace absorbed both → `Projects/PlantMind/`