# PlantMind — Multi-CLI Operating System

**One active folder:** `C:\Users\hp\Claude\Projects\PlantMind`  
**Template for new projects:** `C:\Users\hp\Claude\Projects\_ProjectOS`  
**Archives:** `C:\Users\hp\Claude\Projects\_archive\PlantMind\`

---

## Registered CLIs (extensible)

| CLI | Entry file | Add new tools in `ops/CLI-REGISTRY.md` |
|---|---|---|
| Claude Code | `CLAUDE.md` | |
| Grok CLI | `AGENTS.md` | |
| Gemini CLI | `GEMINI.md` | |
| Codex CLI | `CODEX.md` | |
| *Future* | `{TOOL}.md` | Copy CODEX.md pattern |

**Rule:** New CLI = one row in registry + one pointer file. **Never** duplicate LOCKED_STATE or specs.

---

## Session protocol (every CLI, every session)

```powershell
cd "C:\Users\hp\Claude\Projects\PlantMind"
.\scripts\start-session.ps1
```

```
Read: 00-START-HERE → LOCKED_STATE → Chat Context (latest) → ROADMAP NOW
If building: docs/00-MASTER-SPEC.md + docs/IMPLEMENTATION-GUIDE-ULTRA.md (phase)
Declare lane. Write only in routed folders (ops/ROUTING.md).
```

**Close:** `close session` → ROADMAP + new Chat Context + `git commit`

---

## Conflict prevention (multi-CLI)

| Rule | Why |
|---|---|
| git commit before switching CLI | See who changed what |
| One lane per chat | No two tools editing same module |
| Contracts → vault update | LOCKED_STATE + `src/contracts/` together |
| Next steps → ROADMAP only | Not in tool-specific memory |
| Canonical spec → `docs/00-MASTER-SPEC.md` | Merged doc wins over duplicates |

---

## Portfolio layout (all projects)

```
C:\Users\hp\Claude\Projects\
├── _ProjectOS\           ← copy to start new project
├── _archive\
│   └── {Project}\
│       └── YYYYMMDD_snapshot-{label}\
└── {Project}\            ← ONE active folder (PlantMind)
```

---

## Naming & inventory

- New artifacts: `ops/NAMING-CONVENTIONS.md`
- File lineage: `docs/CODEBASE-INVENTORY.md`
- Doc registry: `docs/INDEX.md`

---

## Never write to

- `_archive/` (read-only)
- Old paths: `PlantMind`, `PlantMind_hckthn` (retired)