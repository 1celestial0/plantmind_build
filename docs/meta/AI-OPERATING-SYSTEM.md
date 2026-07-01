# PlantMind — Multi-CLI Operating System

**Work here only:** `C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live`
**Portfolio:** `C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live\` (live · OS · Archive · GitHub)

---

## Coach behavior (all CLIs)

1. **ORIENT** — read truth files; summarize in ≤5 sentences; never write until confirmed.
2. **PROPOSE** — sequential goals table (max 3–5) before any action. See `ops/workflows/confirmation-gate.md`.
3. **OPERATE** — only after user says **"Proceed with Goals"** (optional: `G1 only`).
4. **LOG** — goal completion log after each goal (why, artifacts, impacts, recommendations).
5. **PROMPT** — after work: manual steps + suggested next goals (do not auto-run).

**Agentic loop:** `ops/workflows/agentic-loop.md`

---

## Registered CLIs

| CLI | Entry file | Registry |
|---|---|---|
| Claude Code | `CLAUDE.md` | `ops/CLI-REGISTRY.md` |
| Grok CLI | `AGENTS.md` | |
| Gemini CLI | `GEMINI.md` | |
| Codex CLI | `CODEX.md` | |
| *Future* | `{TOOL}.md` | Copy `CODEX.md` pattern |

**Rule:** Entry files point here — never duplicate LOCKED_STATE or specs.

---

## Session protocol

```powershell
cd "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live"
powershell -ExecutionPolicy Bypass -File .\scripts\start-session.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\check-status.ps1
```

**Team playbook (human + AI):** `ops/TEAM-OPERATIONS-PLAYBOOK.md`  
**CLI parity:** `ops/CLI-PARITY.md` — identical behavior in every tool

**Read order:** `PROJECT-DNA` (apex constitution) → `LOCKED_STATE` → `00-START-HERE` → Chat Context (latest `vX.Y`) → `ROADMAP` NOW  
**Building:** `PROJECT-DNA.md` §6 (feature inventory) + `docs/IMPLEMENTATION-GUIDE-ULTRA.md` · declare lane · `ops/ROUTING.md`  
**Precedence:** any doc that disagrees with `PROJECT-DNA.md` is wrong until a numbered Amendment changes the DNA. (`docs/00-MASTER-SPEC.md` was archived 2026-07-01 → superseded by the DNA.)

**Close:** say **"close session"** → propose close goals → on confirm: ROADMAP + new Chat Context + `git commit`

---

## Portfolio layout

```
PlantMind/
├── PlantMind_live/      ← daily workspace (git)
├── PlantMind_OS/        ← template + templates/
├── PlantMind_Archive/   ← read-only snapshots
└── PlantMind_GitHub/    ← public publish target
```

---

## Continuity (tool-agnostic)

| File | Role |
|---|---|
| `Chat Context/` | Append-only session history |
| `ROADMAP.md` | Backlog only (NOW / NEXT / HORIZON) |
| `LOCKED_STATE.md` | Frozen decisions (VAULT UPDATE) |
| `continuity/STATE.json` | Machine pointer + sync metadata |

Templates for new projects: `../PlantMind_OS/templates/`

---

## Conflict prevention

| Rule | Why |
|---|---|
| git commit before switching CLI | See who changed what |
| One lane per chat | `ops/ROUTING.md` |
| Contracts ↔ vault together | LOCKED_STATE + `src/contracts/` |
| Next steps → ROADMAP only | Not in Chat Context |
| Goals before writes | `confirmation-gate.md` |

---

## Naming & inventory

- `ops/NAMING-CONVENTIONS.md`
- `docs/CODEBASE-INVENTORY.md`
- `docs/INDEX.md`

---

## Never write to

- `../PlantMind_Archive/` (read-only)
- `../PlantMind_GitHub/` (publish script only)
- `../PlantMind_OS/` (template — copy out, don't edit in place for product work)