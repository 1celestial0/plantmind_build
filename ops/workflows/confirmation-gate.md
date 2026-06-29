# Confirmation Gate — goals before actions

> Every AI CLI in `PlantMind_live` follows this. Humans chat in natural language; AI proposes, user confirms.

---

## Modes

| Mode | Trigger | AI may write files? |
|---|---|---|
| **ORIENT** | Session start, "discuss", "plan only" | No |
| **PROPOSE** | Any build/change/move/commit request | No — goals table only |
| **OPERATE** | User says **"Proceed with Goals"** | Yes — confirmed goals only |

---

## PROPOSE output shape (required)

```markdown
## Proposed goals — [task name]
_Mode: plan · No changes until you confirm_

| # | Goal | Outcome | AI does | You do (manual) |
|---|---|---|---|---|
| G1 | ... | ... | ... | — or M1 |

**Dependencies:** G2 after G1
**Touches:** paths listed
**Reply:** "Proceed with Goals" or "Proceed with Goals G1 only"
```

Max **3–5 goals** per round.

---

## Goal completion log (required after each goal)

```markdown
## Goal log — G{N}: {title}

### Why this goal existed
### Artifacts touched (path | action)
### What changed
### Impacts on other areas
### Recommendations (manual steps + next goal)
### ROADMAP delta
```

Append summary to `continuity/goal-log.json` when that file exists (Phase 1).

---

## After task batch — completion block

```markdown
## Done — [summary]

### Your manual steps
| # | Action | Why |

### Suggested next goals (not started)
| # | Goal | Why now |

Pick one · "Proceed with Goals N1" · or "close session"
```

---

## What counts as an action

Writes, moves, deletes, `git commit/push`, Drive export, publish to GitHub, VAULT UPDATE, dependency install, deploy.

**Read-only** (no gate): explain, summarize, read files, discuss research.

---

## Trigger phrases

| User | AI |
|---|---|
| Task implying change | PROPOSE goals |
| **Proceed with Goals** | OPERATE all proposed |
| **Proceed with Goals G2 only** | OPERATE subset |
| **close session** | PROPOSE close goals → confirm → run |
| **what's next** | Completion block, no execution |