# CLI Registry — all AI tools, one folder

> **Extensible pattern:** Add a row + entry file when you adopt a new CLI. Never create a second project folder for a new tool.

---

## Active CLIs

| CLI | Entry file | Session start command | Best for |
|---|---|---|---|
| **Claude Code** | `CLAUDE.md` | Read `AI-OPERATING-SYSTEM.md` → `00-START-HERE.md` | Architecture, vault updates, close ritual |
| **Grok CLI** | `AGENTS.md` | Same | Research, web, parallel prompts |
| **Gemini CLI** | `GEMINI.md` | Same | Physics/math, long context |
| **Codex CLI** | `CODEX.md` | Same | Code generation, refactors |
| **Human** | `00-START-HERE.md` | `.\scripts\start-session.ps1` | — |

---

## Universal session protocol (every CLI)

```
1. cd C:\Users\hp\Claude\Projects\{ProjectName}
2. .\scripts\start-session.ps1
3. AI reads: AI-OPERATING-SYSTEM.md → LOCKED_STATE.md → ROADMAP NOW
4. AI declares lane (if building)
5. Work in routed folder (ops/ROUTING.md)
6. git commit per phase gate
7. "close session" → ROADMAP + Chat Context + git
```

---

## Adding a new CLI (e.g. Cursor, Windsurf, Aider)

| Step | Action |
|---|---|
| 1 | Add row to table above |
| 2 | Create `{TOOL}.md` at project root (copy from `CODEX.md` template) |
| 3 | Point it to `AI-OPERATING-SYSTEM.md` — do not duplicate rules |
| 4 | If tool has global config elsewhere, note path in `{TOOL}.md` only |

**Never:** duplicate LOCKED_STATE, ROADMAP, or build specs in tool-specific files.

---

## Write-lock (prevent multi-CLI conflicts)

| Rule | Why |
|---|---|
| One lane per active chat | Prevents two CLIs editing same module |
| git commit before switching CLI | Diff shows who changed what |
| Contracts change = LOCKED_STATE vault update | Single source of truth |
| Next steps only in ROADMAP.md | Not in Chat Context or tool memory |

---

## Tool → folder routing

See `ops/ROUTING.md`. Same for all CLIs.