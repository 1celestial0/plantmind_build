# Claude Rules — PlantMind-Live

## UNIVERSAL (project-continuity)

### U1 — Read order at session start
1. `00-START-HERE.md`
2. `LOCKED_STATE.md`
3. Highest `Chat Context/YYYY-MM-DD_vX.Y_project-context.md`
4. `ROADMAP.md` NOW section

### U2 — Checkpoint every ~15 messages
> "Context check — worth a new context version now or at close?"

### U3 — ROADMAP must not shrink at close
Add ≥1 HORIZON item every close unless hp approves decrease.

### U4 — Never delete Chat Context history
Append-only version files.

### U5 — Offer close before session ends

---

## PROJECT-SPECIFIC

### R1 — Single workspace
All new writes go to `PlantMind-Live/`. Old folders are read-only archives unless migrating per `MIGRATION-MAP.md`.

### R2 — Lane discipline
One chat = one lane (`ops/prompts/lanes/`). Do not cross lane internals.

### R3 — Contracts are the API
Modules communicate via `src/contracts/` only. Schema change = `LOCKED_STATE` vault update.

### R4 — Model registry
No new LLM/embedding provider without a row in `ops/MODEL-REGISTRY.md`.

### R5 — Routing
Unclear task type → consult `ops/ROUTING.md` before acting.

### R6 — 5W comments on all functions
WHAT / WHY / HOW / WHEN / WHY NOT

### R7 — Deterministic decisions
IIS/Götze scoring math is deterministic. LLMs are narrative-only.

### R8 — Patent-aware
Flag novel combinations before implementing. Frame as patent-candidate pending prior-art.

### R9 — Demo-first
Guaranteed path (Weibull baseline, v1 FORGE fallback) before stretch goals (PINN, async).

### R10 — Vault updates
Locked fact changes end with 🔒 VAULT UPDATE block for `LOCKED_STATE.md`.