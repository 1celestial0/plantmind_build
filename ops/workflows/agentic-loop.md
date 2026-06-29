# Agentic Loop — research-centric workflow

> **You:** research + validation + decisions. **AI coach:** everything else after **Proceed with Goals**.

---

## Roles

| Human | AI coach |
|---|---|
| Research questions | Read LOCKED_STATE → Chat Context → ROADMAP every chat |
| Validate findings ("approved" / "change X") | Draft docs/code from validation |
| Approve VAULT UPDATE | Propose goals before any write |
| NotebookLM sync click | Export whitelist to Drive (when script exists) |
| Demo-day presence | Scripts, smoke tests, decks |
| **Proceed with Goals** | Execute + goal completion logs |

---

## Loop (every session)

```
START   → start-session.ps1 · coach summarizes · top 3 NOW
PICK    → you choose ONE thing (natural language)
PROPOSE → goals table (confirmation-gate.md)
CONFIRM → "Proceed with Goals"
OPERATE → goals in order + logs
MANUAL  → you do M1, M2 rows only
NEXT    → coach suggests goals; you pick or close
CLOSE   → "close session" → ROADMAP + Chat Context + git
```

---

## Research loop

```
1. You research (chat / NotebookLM / web)
2. You validate conclusions in chat
3. Coach PROPOSES goals to encode in repo + Drive
4. You: Proceed with Goals
5. Coach writes docs · exports · commits · logs
6. Coach prompts manual NotebookLM sync if needed
```

---

## Truth hierarchy

```
LOCKED_STATE  >  docs/00-MASTER-SPEC  >  ROADMAP  >  Chat Context  >  Obsidian  >  chat memory
```

---

## Automation phases (later waves)

| Wave | Automates |
|---|---|
| Phase 0 | Structure, SOPs, coach rules (this doc) |
| Phase 1 | goal-log.json, skills |
| Phase 2 | Drive export on close |
| Phase 3 | GitHub publish + team branches |
| Phase 4 | P0 contracts + lanes |