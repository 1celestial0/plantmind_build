# PlantMind-Live — Grok / Agent Instructions

**Canonical workspace:** `C:\Users\hp\Claude\Projects\PlantMind-Live`  
**Read first:** `AI-OPERATING-SYSTEM.md` → `00-START-HERE.md` → `LOCKED_STATE.md` → `ROADMAP.md`

## Session start
1. Read files above in order
2. Summarize: project phase, top 3 ROADMAP NOW items, your assigned lane (ask if unclear)
3. Never write to `../PlantMind/` or `../PlantMind_hckthn/` — archives only

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
- IIS formula and weights in `LOCKED_STATE.md` §2
- Human approval required before action logged
- Weibull ships first; PINN is stretch only

## Demo path
- **Runnable today:** `streamlit run src/legacy/forge-v1/app.py`
- **Building toward:** `src/` per IMPLEMENTATION-GUIDE-ULTRA.md phases P0–P6

## Session close
When user says "close session": update ROADMAP, new Chat Context version, git commit.