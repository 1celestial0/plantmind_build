# PlantMind-Live — Multi-AI Operating System
**One folder. Any AI tool. Same rules.**

Use this with **Claude Code**, **Grok CLI**, **Gemini CLI**, or any other assistant. All tools read the same files and write to the same places.

---

## Canonical workspace (non-negotiable)

```
C:\Users\hp\Claude\Projects\PlantMind-Live
```

**Never write new code or docs to:**
- `C:\Users\hp\Claude\Projects\PlantMind\` (archive)
- `C:\Users\hp\Claude\Projects\PlantMind_hckthn\` (archive)
- `C:\Users\hp\Sourav AI OS\Grok Project\` (unless Grok KB experiments — not PlantMind code)

---

## Tool-specific entry files

| AI Tool | Reads first | Config file |
|---|---|---|
| **Claude Code** | `CLAUDE.md` | `CLAUDE.md` + `CLAUDE_RULES.md` |
| **Grok CLI** | `AGENTS.md` | `AGENTS.md` (this repo root) |
| **Gemini CLI** | `GEMINI.md` | `GEMINI.md` |
| **Any human** | `00-START-HERE.md` | — |
| **All tools** | `LOCKED_STATE.md` → `ROADMAP.md` NOW | — |

---

## Session start ritual (every tool, every session)

```powershell
cd "C:\Users\hp\Claude\Projects\PlantMind-Live"
.\scripts\start-session.ps1
```

Then tell the AI:

```
PlantMind session start.
Read: 00-START-HERE.md → LOCKED_STATE.md → latest Chat Context → ROADMAP NOW.
Declare your lane. Do not write outside your lane folders.
```

---

## Session close ritual (every tool, every session)

Tell the AI:

```
close session
```

AI must:
1. Update `ROADMAP.md` (move done items, add ≥1 HORIZON item)
2. Write new `Chat Context/YYYY-MM-DD_vX.Y_project-context.md`
3. `git add` + `git commit` with message `context: vX.Y - summary`

---

## Lane discipline (parallel chats)

| Lane | Write folders | Prompt file |
|---|---|---|
| 1 Backend | `src/agents/`, `src/api/`, `src/pipeline/`, `src/governance/` | `ops/prompts/PLANTMIND_5_CHAT_PROMPTS.md` Chat 1 |
| 2 Physics | `src/physics/`, `ml/` | Chat 2 |
| 3 Dashboard | `src/dashboard/` | Chat 3 |
| 4 Databricks | `deploy/databricks/` | Chat 4 |
| 5 Demo | `ops/runbooks/`, `docs/dna/` | Chat 5 |

**One chat = one lane.** Contracts in `src/contracts/` are the only API between lanes.

---

## What each tool is best for

| Task | Best tool | Why |
|---|---|---|
| Architecture + vault updates | Claude | Long context, project-continuity skill |
| Research phases 1–5 | Grok | Web research, parallel prompts |
| Code generation (agents, API) | Claude or Gemini | Pick one per lane; don't duplicate |
| Physics / math validation | Gemini or Claude | Deep reasoning |
| Quick file edits | Any | Same rules apply |
| Demo script / pitch | Claude or Grok | Narrative quality |

**Rule:** If two tools edit the same file in one day, **git commit between handoffs**.

---

## Conflict prevention between AIs

1. **LOCKED_STATE is law** — no AI changes IIS weights, agent names, or contracts without 🔒 VAULT UPDATE block
2. **ROADMAP is the backlog** — only place for "next steps"
3. **Chat Context is history** — append-only version files
4. **Code goes in `src/` or `ml/`** — never in `docs/` except specs
5. **Model APIs** — register in `ops/MODEL-REGISTRY.md` before coding

---

## Autonomous daily loop

```
Morning:
  start-session.ps1 → AI reads state → pick 1 ROADMAP NOW item

Work block (2-4h):
  One lane → one phase gate → pytest or manual test → git commit

Afternoon:
  Integration check → update ROADMAP

Evening:
  "close session" → new context version
```

---

## File priority when confused

```
1. 00-START-HERE.md        — where am I?
2. LOCKED_STATE.md         — what's frozen?
3. ROADMAP.md NOW          — what do I do next?
4. ops/ROUTING.md          — which folder?
5. docs/IMPLEMENTATION-GUIDE-ULTRA.md — how to build?
6. docs/WIN-STRATEGY-ASSESSMENT.md — are we on track?
```

---

## Three-folder confusion — resolved

| Folder | Status | Action |
|---|---|---|
| `PlantMind-Live` | **ACTIVE** | Work here |
| `PlantMind` | ARCHIVE | Read-only reference; contents copied to Live |
| `PlantMind_hckthn` | ARCHIVE | Read-only reference; contents copied to Live |

If an AI suggests editing old folders, **reject and redirect to PlantMind-Live**.