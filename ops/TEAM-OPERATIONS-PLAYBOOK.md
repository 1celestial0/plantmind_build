# PlantMind — Team Operations Playbook

**The one manual for you and every teammate.**  
_Last updated: 2026-06-30 · use this every session_

| Doc | When to use |
|-----|-------------|
| **This playbook** | Start, work, test, close — full workflow |
| `ops/TEAM-CHAT-GUIDE.md` | Quick lane-chat cheat sheet |
| `ops/CLI-PARITY.md` | Same rules for Claude / Grok / Gemini / Codex |
| `docs/parallel/STATUS.md` | Live build status per lane |
| `continuity/goal-log.json` | What goals completed and why |
| `continuity/test-log.json` | Automated test run history |

---

## 1. Before you close today

Know these facts:

| Item | State (2026-06-30) |
|------|-------------------|
| **Phase** | Wave 1 spine done; **build Lane 1 + 2 next** |
| **Context** | `Chat Context/2026-06-30_v1.4_project-context.md` |
| **Open NOW** | Physics (L2) + agent stubs (L1) — see `ROADMAP.md` |
| **Demo v1** | **Deferred** — known bugs; do not rely on it for judges yet |
| **Contracts** | `src/contracts/` — lanes must use these only |
| **Git** | Committed; remote not configured |

**You do not need to remember chat history.** Everything important is in `ROADMAP`, `Chat Context`, `goal-log`, and `test-log`.

---

## 2. Tomorrow — start in 3 minutes

### Step A — Terminal (human)

```powershell
cd "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live"
powershell -ExecutionPolicy Bypass -File .\scripts\start-session.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\check-status.ps1
```

### Step B — Open AI (any CLI)

Open **one** tool (Claude, Grok, Gemini, Codex, Cursor). First message:

> Read `AI-OPERATING-SYSTEM.md` and `ops/TEAM-OPERATIONS-PLAYBOOK.md`. Summarize ROADMAP NOW and ask which lane I want.

**Every CLI must behave the same** — see `ops/CLI-PARITY.md`.

### Step C — Pick work

| If you want to… | Say to AI |
|-----------------|-----------|
| Build physics | "Lane 2 — Proceed with Goals after you propose" |
| Build agents | "Lane 1 — …" |
| Check health | "Run status check and test log summary" |
| Research only | "Read-only — explain ARCHITECTURE_LOCK" |

---

## 3. How to check status (any time)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-status.ps1
```

Shows: latest Chat Context, ROADMAP NOW, git status, last test run, goal-log tail.

Or ask any AI: **"What's project status?"** — it must read the same files (not guess).

---

## 4. How work actually flows

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐     ┌────────────┐
│ START       │ ──► │ ORIENT       │ ──► │ PROPOSE goals   │ ──► │ YOU:       │
│ start-      │     │ AI reads     │     │ (no file writes)│     │ Proceed    │
│ session.ps1 │     │ truth files  │     │ goals table     │     │ with Goals │
└─────────────┘     └──────────────┘     └─────────────────┘     └─────┬──────┘
                                                                        │
                    ┌──────────────┐     ┌─────────────────┐            ▼
                    │ CLOSE        │ ◄── │ OPERATE + LOG   │ ◄── ┌────────────┐
                    │ ROADMAP +    │     │ code/docs/tests │     │ One lane   │
                    │ Context+git  │     │ goal-log entry  │     │ per chat   │
                    └──────────────┘     └─────────────────┘     └────────────┘
```

### Modes (all CLIs)

| Mode | Trigger | AI writes files? |
|------|---------|------------------|
| ORIENT | Session start, "what's status" | No |
| PROPOSE | "Build X", "fix Y" | No — goals table only |
| OPERATE | **"Proceed with Goals"** | Yes — confirmed goals only |

### After each goal

AI appends to `continuity/goal-log.json` with: why, artifacts, impacts, recommendations.

### Parallel documentation

While building, update **your lane's** file in `docs/parallel/lane-0N-*.md` and the rollup `docs/parallel/STATUS.md`.

---

## 5. Testing workflow

### Scenario catalog (automatic)

Machine-readable: `ops/testing/scenarios.json`  
Human-readable: `ops/testing/SCENARIO-CATALOG.md`  
Generator: `ops/testing/scenario_generator.py`

Scenarios A–D map to demo + pytest cases (contracts today; full pipeline when lanes land).

### Run tests + log

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run-tests.ps1
```

Appends run to `continuity/test-log.json`. Run at:

- Session start (optional quick check)
- After **Proceed with Goals** batch
- Before **close session**

### What gets tested today

| Suite | File | Proves |
|-------|------|--------|
| Contracts | `tests/test_contracts.py` | LOCKED_STATE §4 shapes |
| Scenarios | `tests/test_scenarios.py` | Scenario catalog valid + test cases generated |

---

## 6. Close session (today / any day)

Say to AI:

> **close session**

Coach will PROPOSE close goals → you say **Proceed with Goals** → then:

1. Update `ROADMAP.md`
2. New `Chat Context/YYYY-MM-DD_vX.Y_project-context.md`
3. Append `continuity/goal-log.json`
4. Run `scripts/run-tests.ps1` (or log skip reason)
5. `git commit`

Optional manual:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\export-to-drive.ps1
```

---

## 7. Multi-teammate rules

| Rule | Why |
|------|-----|
| One lane per person per chat | No merge conflicts on `src/agents/` vs `src/physics/` |
| `git pull` / check status before start | See others' commits |
| Contract change = vault update | `LOCKED_STATE.md` + `src/contracts/` together |
| Same playbook for all CLIs | No "Grok does it differently" |

---

## 8. File map (memorize 5)

| File | Purpose |
|------|---------|
| `ROADMAP.md` | What to do next |
| `Chat Context/*_vX.Y_*` | Session memory |
| `LOCKED_STATE.md` | Frozen decisions |
| `ops/TEAM-OPERATIONS-PLAYBOOK.md` | This file |
| `docs/parallel/STATUS.md` | Lane build progress |

---

## 9. Tomorrow's recommended first message

Copy-paste into **any** CLI:

```
PlantMind session resume. Read AI-OPERATING-SYSTEM.md, ops/TEAM-OPERATIONS-PLAYBOOK.md,
latest Chat Context, ROADMAP NOW. Summarize status. I want Lane 2 (physics) —
propose goals for Weibull + ml/synthesis scaffold. Do not write until I say Proceed with Goals.
```