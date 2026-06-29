---
name: plantmind-session
description: Start and close PlantMind_live work sessions with correct read order, confirmation gate, ROADMAP update, Chat Context versioning, and goal-log append. Use at session start, session end, or when user says "close session".
---

# PlantMind session skill

## Session start

1. `cd C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live`
2. Optional: `.\scripts\start-session.ps1`
3. Read in order:
   - `00-START-HERE.md`
   - `LOCKED_STATE.md`
   - Highest `Chat Context/*_project-context.md` (parse vX.Y as integers)
   - `ROADMAP.md` NOW section
4. Summarize: phase, top 3 NOW items, ask which lane if unclear
5. **Do not write files** until user says **Proceed with Goals**

## During work

- One lane per chat (`ops/prompts/lanes/`)
- Propose goals table before changes (`ops/workflows/confirmation-gate.md`)
- Append completion to `continuity/goal-log.json`

## Session close

When user says **close session**:

1. PROPOSE close goals → wait for Proceed
2. Move completed ROADMAP items → DONE
3. Add ≥1 HORIZON item if needed
4. Create `Chat Context/YYYY-MM-DD_vX.Y_project-context.md` (increment version)
5. Update `continuity/STATE.json` pointers
6. `git add` + `git commit`
7. Offer `.\scripts\export-to-drive.ps1` for NotebookLM sync

## Demo command (deferred polish)

v1 reference only — known bugs. Target: `src/dashboard/app.py` when Lane 3 wires v2.