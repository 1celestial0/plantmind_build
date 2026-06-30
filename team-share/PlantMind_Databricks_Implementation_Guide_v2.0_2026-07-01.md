# PlantMind — Databricks Implementation Guide v2.0
_Generated 2026-07-01 · **DERIVED from `PROJECT-DNA.md` + `LOCKED_STATE.md` §9 (LOCKED).** Supersedes the July Grok guide (which had 5 agents + a RUL-unit bug + "ship v1 if time runs out")._
**For:** Sourav Dutta + L4 team · Databricks free/trial edition.

## 0. Where Databricks sits (read first)
PlantMind is **two layers** (Spec §3): **Layer 0** = portable Pydantic contracts (`src/contracts/`); **Layer 1** = Databricks-native reference impl. **The live hackathon demo runs LOCALLY** (Streamlit + SQLite); **Databricks is the scale / credibility narrative** shown via Unity Catalog lineage + screenshots, **promoted to the live stage only if stable by Hour 20** (DNA C9). Never make the demo depend on the cloud.

## 1. Mental model (senior-DE lens)
Databricks = unified Lakehouse: Spark compute · Delta Lake storage · Unity Catalog governance · MLflow · Mosaic AI. Map your world: IICS CDI → **DLT** · Redshift/Snowflake → **Delta tables** · S3+Glue ingestion → **Auto Loader** · stored procs → **notebooks + Workflows** · DQ rules → **DLT expectations**.

## 2. Cost rule (#1 job on trial)
Bills in DBUs + cloud VM/storage. All-Purpose ~$0.40–0.55/DBU-hr (dev only) · Jobs ~$0.15–0.22 (pipelines) · Serverless SQL (dashboards). **Auto-terminate ≤25 min. Never leave clusters idle. ~$400 trial credit — target <$150.**

## 3. Medallion (same Layer-0 contracts)
- **Bronze** — Auto Loader from synthetic CSV/Parquet → `bronze_sensor_readings`.
- **Silver** — DLT physics features (rolling stats, degradation rate, stress factors) using `src/physics/` (**LOCKED_STATE §6a λ/β — NOT the old 0.0023; RUL in DAYS**) + DLT expectations.
- **Gold** — `gold_asset_current_status` (latest health), `gold_gotze_triggers` (health<40 OR rul_days<14), decision history, `maintenance_kb` for RAG.

## 4. Serving & RAG
- Wrap **Weibull** model in MLflow (log λ/β, metrics) → register `PlantMind-Weibull-RUL`.
- Wrap **GötzeEngine** as MLflow PyFunc → register `PlantMind-GotzeEngine`. ⚠️ **Pass `rul_days` (days), not cycles** — the old guide's `rul_cycles=row["rul_days"]` was a 6× bug.
- **6 agents** run via the orchestrator (incl. **MaintenanceScheduler** → work order). RootCauseAnalyst uses **Databricks Vector Search** (`databricks-bge-large-en`) on `maintenance_kb`.

## 5. Governance
Unity Catalog lineage Bronze→Gold decision · Delta time-travel = immutable audit (mirrors local hash chain) · show judges the full chain. This is the partnership-credibility centerpiece.

## 6. Codebase reuse (what to lift)
`scripts/generate_data.py` → landing CSVs · `src/physics/` → Pandas/Spark UDF + MLflow · `src/agents/` (6) → import in notebooks, wrap Götze as PyFunc · `src/contracts/` (incl. new `manifest.py` + `workorder.py`) → unchanged · dashboard → swap SQLite for Databricks SQL connector (only if going live, C9) · ChromaDB → Vector Search.

## 7. Freeze schedule (shared with build)
H-14 PINN · H-16 config pipeline → static fallback · H-20 decide local-vs-Databricks live (C9) · then rehearsal only.

## 8. Readiness checklist
☐ workspace+cluster ☐ Bronze via Auto Loader ☐ DLT Silver/Gold with §6a physics ☐ Weibull in MLflow ☐ Götze PyFunc ☐ Vector Search on maintenance_kb ☐ Unity Catalog lineage visible ☐ cost check (clusters terminated) ☐ manifest example documented.

— Derived from PROJECT-DNA v1.0 + LOCKED_STATE v · 2026-07-01 —
