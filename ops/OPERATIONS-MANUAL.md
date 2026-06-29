# PlantMind — Operations Manual

_Last updated: 2026-06-30 · Wave 1 Phase 1_

> **Canonical team reference:** `ops/TEAM-OPERATIONS-PLAYBOOK.md` (start/close/status/testing/CLI parity).  
> This file is the structural supplement; share the **Playbook** with teammates first.

---

## 1. Canonical workspace

| Item | Value |
|------|-------|
| Work folder | `C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live` |
| Portfolio parent | `C:\Users\hp\Claude\Projects\PlantMind\` |
| Event | LTTS Hackathon — 2026-07-09 |
| Truth order | `LOCKED_STATE` → `docs/00-MASTER-SPEC` → `ROADMAP` → latest `Chat Context/` |

**Never write to:** `PlantMind_Archive/`, `PlantMind_OS/` (except publish), sibling repos unless migrating.

---

## 2. Session ritual

### Start (2 min)

```powershell
cd "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live"
.\scripts\start-session.ps1
```

AI reads: `00-START-HERE.md` → `LOCKED_STATE.md` → latest `Chat Context/` → `ROADMAP.md` (NOW).

### Work

- **One chat = one lane** (`ops/prompts/lanes/`)
- Code: `src/` and `ml/` only
- Contracts: `src/contracts/` — changes need 🔒 VAULT UPDATE in `LOCKED_STATE.md`
- Research output: `docs/research/`

### Close (5 min)

Say **"close session"** to AI. Coach will:

1. Move completed items → `ROADMAP.md` DONE
2. Add ≥1 HORIZON idea if needed
3. New `Chat Context/YYYY-MM-DD_vX.Y_project-context.md`
4. Append `continuity/goal-log.json`
5. `git commit`

---

## 3. Coach + confirmation gate

Before **any** file change, AI must PROPOSE a goals table. You reply:

- **"Proceed with Goals"** — execute all proposed goals
- **"Proceed with Goals G2 only"** — subset
- **"close session"** — continuity close batch

See `ops/workflows/confirmation-gate.md` and `ops/workflows/agentic-loop.md`.

Goal completion logs append to `continuity/goal-log.json`.

---

## 4. Five lanes (parallel build)

| Lane | Prompt file | Owns |
|------|-------------|------|
| 1 Backend | `ops/prompts/lanes/lane-01-backend.md` | agents, API, orchestrator, audit |
| 2 Physics | `ops/prompts/lanes/lane-02-physics.md` | Weibull, synthetic data, PhysicsModelInterface |
| 3 Dashboard | `ops/prompts/lanes/lane-03-dashboard.md` | Streamlit, IIS panel (consumes JSON only) |
| 4 Databricks | `ops/prompts/lanes/lane-04-databricks.md` | DLT, Feature Store, Unity Catalog port |
| 5 Demo/Pitch | `ops/prompts/lanes/lane-05-demo.md` | script, ROI, Q&A — no core code |

Lanes talk through `src/contracts/` only.

---

## 5. Folder map

```
PlantMind_live/
├── LOCKED_STATE.md      # locked decisions
├── ROADMAP.md           # NOW / NEXT / HORIZON
├── Chat Context/        # versioned session memory
├── continuity/          # STATE.json + goal-log.json
├── docs/                # architecture, research, deliverables
├── ops/                 # prompts, workflows, skills, runbooks
├── src/                 # v2 application (contracts, agents, api, dashboard)
├── ml/                  # training, synthesis, models
├── deploy/              # Databricks port
└── scripts/             # session, export, sync
```

v1 reference demo (deferred polish): `src/legacy/demo-v1-metagpt/`

---

## 6. Multi-AI tools

| Tool | Entry rule file |
|------|-----------------|
| Claude | `CLAUDE.md` |
| Grok | `AGENTS.md` |
| Gemini | `GEMINI.md` |
| All | `AI-OPERATING-SYSTEM.md` |

Same folder. Same confirmation gate. Same goal log.

---

## 7. Research workflow

Phases 1–2 complete (`PAIN_REGISTER`, `COMPETITIVE_MAP`). Phases 3–6 in `docs/research/`:

- `DATABRICKS_MAP_*`
- `DATA_REALITY_*`
- `ROI_BENCHMARKS_*`
- `ARCHITECTURE_LOCK_*`

Human validates conclusions → coach encodes in repo. NotebookLM sync via `scripts/export-to-drive.ps1` (manual upload step).

---

## 8. External sync (when ready)

IDs in `continuity/STATE.json`:

- Notion database: configured
- Drive folder: configured
- Git remote: **not configured yet**

Run `scripts/sync-notion-drive.ps1` after reviewing credentials (stub — see script header).

---

## 9. Hackathon freeze (T-6h)

- Lock dependency versions
- Screenshot charts + backup video
- Tag: `v1.0-hackathon-submission`
- Demo from frozen build only

---

## 10. Escalation

| Situation | Action |
|-----------|--------|
| Locked fact wrong | 🔒 VAULT UPDATE block → human approves → update `LOCKED_STATE.md` |
| Lane needs new contract field | Lane owner specifies field → VAULT UPDATE → all lanes re-read |
| Demo broken on stage | Backup video + v1 narrative from `docs/architecture/08_DEMO_SCENARIOS.md` |
| Two AIs edited same file | Git diff; one lane per file going forward |