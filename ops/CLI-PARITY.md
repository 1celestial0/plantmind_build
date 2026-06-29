# CLI Parity — identical behavior across all AI tools

Every CLI working in `PlantMind_live` **must** follow this. No tool gets special rules.

---

## Registered tools

See `ops/CLI-REGISTRY.md`. Entry files: `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `CODEX.md` — all point to `AI-OPERATING-SYSTEM.md`.

---

## Mandatory behaviors (non-negotiable)

| # | Behavior | Wrong behavior |
|---|----------|----------------|
| 1 | Read truth files before advising | Answer from chat memory only |
| 2 | PROPOSE goals table before any write | Silently edit files |
| 3 | Wait for **"Proceed with Goals"** | Auto-implement on "please fix" |
| 4 | Log each goal to `continuity/goal-log.json` | Skip completion log |
| 5 | One lane per chat | Mix backend + UI in one thread |
| 6 | Code only in `src/` and `ml/` | Edit Archive or OS template in place |
| 7 | Contract change → VAULT UPDATE | Change `src/contracts/` without LOCKED_STATE |
| 8 | Next steps only in `ROADMAP.md` | Hide backlog in Chat Context |
| 9 | Session close ritual on "close session" | End without ROADMAP/Context/git |
| 10 | Run or offer `scripts/run-tests.ps1` after code goals | Ship without test log |

---

## Session start (identical)

```
1. cd PlantMind_live
2. scripts/start-session.ps1 (human)
3. AI reads: 00-START-HERE → LOCKED_STATE → latest Chat Context → ROADMAP NOW
4. AI summarizes ≤5 sentences + asks lane
5. ORIENT mode — no writes
```

---

## Session close (identical)

```
User: "close session"
AI: PROPOSE close goals (ROADMAP, Context, tests, git)
User: "Proceed with Goals"
AI: EXECUTE + append goal-log + commit
```

---

## Status check (identical)

Human runs `scripts/check-status.ps1` **or** asks "project status".

AI must read: `continuity/STATE.json`, latest Chat Context, `ROADMAP.md` NOW, tail of `goal-log.json` and `test-log.json`.

---

## Routing (identical)

`ops/ROUTING.md` + `ops/prompts/lanes/` — same for every CLI.

---

## Adding a new CLI

1. Add row to `ops/CLI-REGISTRY.md`
2. Create `{TOOL}.md` at repo root → link `AI-OPERATING-SYSTEM.md` + this file
3. Do **not** duplicate LOCKED_STATE or ROADMAP in tool config

---

## Verification

If a CLI behaves differently, paste into that chat:

> Follow ops/CLI-PARITY.md and ops/TEAM-OPERATIONS-PLAYBOOK.md exactly. Confirm ORIENT mode and propose goals before writes.