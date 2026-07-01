# PlantMind — Grok / Agent Instructions

**Canonical workspace:** `C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live`  
**Read first:** `docs/meta/AI-OPERATING-SYSTEM.md` → `docs/meta/00-START-HERE.md` → `docs/meta/LOCKED_STATE.md` → `docs/meta/ROADMAP.md`

## Coach + confirmation gate
- **Before any file change:** PROPOSE sequential goals table — wait for **"Proceed with Goals"**
- **After each goal:** goal completion log (why, artifacts, impacts, recommendations)
- See `ops/workflows/confirmation-gate.md` and `ops/workflows/agentic-loop.md`

## Session start
1. Read files above in order
2. Summarize: project phase, top 3 ROADMAP NOW items, your assigned lane (ask if unclear)
3. Never write to `../PlantMind_Archive/`, `../PlantMind_OS/`, or `../PlantMind_GitHub/` (except publish script)

## Build rules
- Code: `src/` and `ml/` only
- Contracts: `src/contracts/` — changes need LOCKED_STATE vault update
- Research output: `docs/research/`
- Prompts: `ops/prompts/`
- Implementation detail: `docs/IMPLEMENTATION-GUIDE-ULTRA.md`

## Lane discipline
One task = one lane. See `ops/ROUTING.md`.

## Locked facts (do not re-derive)
- 5 agents: DataSentinel, AssetHealthOracle, GötzeEngine, RootCauseAnalyst, ExecutiveSummarizer
- IIS formula and weights in `docs/meta/LOCKED_STATE.md` §2
- Human approval required before action logged
- Weibull ships first; PINN is stretch only

## Demo path
- **Runnable today:** `streamlit run src/legacy/demo-v1-metagpt/app.py`
- **Building toward:** `src/` per IMPLEMENTATION-GUIDE-ULTRA.md phases P0–P6

## Session close
When user says "close session": update ROADMAP, new Chat Context version, git commit.