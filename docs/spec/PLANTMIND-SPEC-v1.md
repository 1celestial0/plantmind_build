# PLANTMIND-SPEC-v1

> **Derived from `PROJECT-DNA.md` and `LOCKED_STATE.md`; not authoritative over them.**

## 1) Purpose
This document locks the rebuild-v1 implementation specification for the `rebuild/plantmind-v1` branch and translates the constitution and vault into build-ready boundaries.

## 2) Product identity (locked rendering)
PlantMind is a **config-driven, physics-informed industrial decision fabric** that turns existing plant data into **one trusted, ranked, human-approved, auditable engineering action**.

## 3) What PlantMind is not
- Not a generic agent builder
- Not a full MetaGPT clone
- Not autonomous maintenance execution
- Not only a predictive maintenance dashboard
- Not only a digital twin
- Not Databricks-only

## 4) Two co-equal pillars
- **P1 — Closed decision loop:** physics health → IIS → one approved, audited action.
- **P2 — Config-driven modularity:** Plant Config Manifest composes runtime; new plant/asset/use-case = config, not code.

## 5) Hackathon architecture freeze line (v1)
Plant Config Manifest + deterministic Python SOP orchestrator + 6 bounded agents + Weibull health/RUL + IIS profiles + approval gate + MaintenanceScheduler + audit/hash-chain/lineage + local Streamlit/FastAPI/SQLite spine + Databricks reference path.

## 6) Agentic principle
**Agentic outside, deterministic inside.**
LLMs are used only for narrative/explanation with fallback and never for final numeric decision.

## 7) Six bounded agents (v1)
1. DataSentinel
2. AssetHealthOracle
3. GötzeEngine
4. RootCauseAnalyst
5. ExecutiveSummarizer
6. MaintenanceScheduler

## 8) Manifest mental model
The Plant Config Manifest is the plant operating passport containing:
- `plant_id`
- `asset_hierarchy`
- `data_sources`
- `tag_mapping`
- `physics_model`
- `iis_profile`
- `triggers`

## 9) Plant intake future path
Agent-assisted intake may draft manifests, but only validated and human-approved manifests drive deterministic runtime.

## 10) Demo shape lock (hero)
Hero flow is `PUMP-001` with `gradual_wear`, showing:
1. Götze one-best-action moment
2. IIS profile swap impact on ranking
3. Human approval → work order creation
4. Audit lineage evidence

## 11) Governance and truth hierarchy
`PROJECT-DNA.md` remains apex truth and `LOCKED_STATE.md` remains technical truth. This document is a derived implementation artifact and introduces no competing source-of-truth.
