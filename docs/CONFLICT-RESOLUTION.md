# PlantMind — Intelligent Merge Conflict Resolution
**Date:** 2026-06-29 | **Canonical workspace:** PlantMind

This document records how conflicts between `PlantMind/` (v1 FORGE) and `PlantMind_hckthn/` (v2 vault) were resolved. **Nothing was deleted** from source folders; all assets were copied into PlantMind.

---

## Resolution principles

1. **v2 vault (LOCKED_STATE) wins** for product architecture, agents, IIS, contracts, and governance.
2. **v1 FORGE wins** for what is already built and runnable (preserved at `src/legacy/demo-v1-metagpt/`).
3. **Research artifacts** from both streams are kept; pain register uses Layer 0 interface names (aligned with v2).
4. **Dual-path hackathon strategy** is explicit: demo can ship from v1 while v2 migrates into `src/`.

---

## Conflict matrix (resolved)

| # | Topic | v1 (PlantMind/FORGE) | v2 (PlantMind_hckthn) | **Canonical decision** |
|---|---|---|---|---|
| C1 | Organizing model | 5 Layers (Data→Features→RUL→Decision→Proof) | 5 Agents (Sentinel→Oracle→Götze→RCA→Summarizer) | **Both valid views.** Layers = data pipeline. Agents = runtime orchestration. Map Layer 1-3 → Agents 1-2; Layer 4 → Agent 3; Layer 5 → Agents 4-5 + governance. |
| C2 | Scoring formula | G-score: 0.40·ΔHealth + 0.25·cost + 0.20·time + 0.15·Safety | IIS: 0.35·ΔP + 0.25·ΔCost + 0.20·Feasibility + 0.15·History − 0.05·Safety | **IIS is canonical** for product/IP. G-score retained as v1 implementation alias. Migration maps ΔHealth→ΔP_failure, NormCost→ΔDowntimeCost, NormTime→Feasibility proxy. |
| C3 | Health / RUL model | RandomForest on C-MAPSS cycles; RED if RUL<30 cycles | Weibull H(t); RUL in days; trigger health<40 or rul_days<14 | **Weibull analytical is canonical** for multi-asset plant. RF-CMAPSS is **v1 demo path** for turbofan proof. PINN = optional stretch only. |
| C4 | Orchestration | MetaGPT PipelineOrchestrator + 3 roles | CrewAI + LangGraph 5-agent sequence | **LangGraph 5-agent sequence is canonical.** MetaGPT = v1 structural POC preserved in demo-v1-metagpt. |
| C5 | LLM in decision | Blueprint: LLM root cause; FORGE: zero LLM | Groq narrative only; IIS math deterministic | **Deterministic scoring + LLM narrative only** (v2 rule). v1's no-LLM path acceptable for demo fallback. |
| C6 | Human approval | Not implemented | Required before action logged | **Required** — v2 governance; gap in v1 noted as P0 for v2 dashboard. |
| C7 | Proof mechanism | RED→GREEN counterfactual chart (built) | IIS ranking + audit + approve | **Combined proof story:** counterfactual chart (visual) + immutable audit + human approve (governance). Both ship in full vision. |
| C8 | Root cause | Rule-based sensor attribution in gotze_engine | RootCauseAnalyst RAG + citations | **RAG with citations is canonical.** v1 rule-based = stub until RAG wired. |
| C9 | Data scope | NASA C-MAPSS 100 turbofans | 30 synthetic assets × 5 types | **Both:** C-MAPSS calibrates Weibull λ,β; synthetic plant is demo universe. |
| C10 | API / backend | Streamlit direct to pipeline | FastAPI + Pydantic + SQLite audit | **FastAPI + contracts is canonical.** v1 Streamlit-direct = interim. |
| C11 | Tagline | "Predict the failure. Decide the fix. Prove it." | Götze one-best-action + partnership | **Same story** — unified tagline kept. |
| C12 | Team lanes | Sourav brain + 3 viz | 5 lanes (backend, physics, UI, Databricks, demo) | **5 lanes canonical** for hackathon execution. |
| C13 | "IIS" meaning | Industrial Intelligence System (7 interfaces) in research | Intervention Impact Score in LOCKED_STATE | **Disambiguated:** IIS-score = Intervention Impact Score (formula). IIS-framework = 7 Layer-0 interfaces in research docs. |
| C14 | Action catalog | replace_bearing, reduce_load, flush_lubrication, monitor_only | reduce_load_now, swap_seal, schedule_window, emergency_stop | **Unified catalog** in blueprint §7 with v1/v2 aliases. |
| C15 | Chat Context | v1.0–v1.2 in PlantMind | None | **Preserved** in `Chat Context/archive-from-plantmind/`; new versions only in Live root. |

---

## Asset preservation map

| Source | Live destination | Status |
|---|---|---|
| PlantMind_hckthn (14 files) | docs/architecture, docs/dna, ops/prompts | ✅ Copied |
| PlantMind/FORGE | src/legacy/demo-v1-metagpt | ✅ Copied |
| PlantMind/PlantMind_Research | docs/research | ✅ Copied |
| PlantMind v1 blueprints | docs/legacy/v1-blueprint | ✅ Copied |
| PlantMind/LEARNING, RESEARCH | docs/learning, docs/research-sources | ✅ Copied |
| PlantMind/Chat Context | Chat Context/archive-from-plantmind | ✅ Copied |
| PlantMind/Knowledge Graph | knowledge/obsidian-vault | ✅ Copied |
| PlantMind deliverables (pptx, pdf, svg) | docs/deliverables | ✅ Copied |

**Total files in PlantMind after merge:** 246+

---

## What was NOT lost

- All FORGE Python source, tests, patents docs
- All 10-doc vault KB
- Pain register (35 pains) + competitive map (12+ competitors)
- MetaGPT build history (Chat Context v1.0–v1.2)
- Obsidian knowledge graph
- Original pitch deck and blueprint PDF