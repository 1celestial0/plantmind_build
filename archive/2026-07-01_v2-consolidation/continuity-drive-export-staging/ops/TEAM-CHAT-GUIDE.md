# PlantMind — Team Chat Guide

_How to run parallel AI chats without stepping on each other · 2026-06-30_

---

## Quick start (new teammate)

1. Clone/open `PlantMind_live` only (not old `PlantMind/` or `PlantMind_hckthn/` paths).
2. Read `00-START-HERE.md` (5 min).
3. Skim `LOCKED_STATE.md` §1–§4 (agents, IIS, contracts).
4. Open `ROADMAP.md` → pick **one** NOW item or ask coach for top 3.
5. Open **one** lane chat — paste **one** file from `ops/prompts/lanes/`.

---

## The one rule

**One person · one chat · one lane · one task.**

If you need backend + UI, use **two chats** with two lane prompts — do not mix in one thread.

---

## Opening a lane chat

Copy the **entire** contents of your lane file as the first message:

| You are building… | Paste this file |
|-------------------|-----------------|
| API, agents, audit | `ops/prompts/lanes/lane-01-backend.md` |
| Weibull, data, physics | `ops/prompts/lanes/lane-02-physics.md` |
| Streamlit / judges UI | `ops/prompts/lanes/lane-03-dashboard.md` |
| Databricks notebooks | `ops/prompts/lanes/lane-04-databricks.md` |
| Pitch, ROI, demo script | `ops/prompts/lanes/lane-05-demo.md` |

Add one line at the end if helpful:

> "My task today: [e.g. scaffold src/agents/ stubs]"

---

## Talking to the coach

| You say | Coach does |
|---------|------------|
| "What's NOW on the roadmap?" | Reads ROADMAP, summarizes |
| "I want to build X" | Proposes goals table — **waits** |
| **"Proceed with Goals"** | Executes confirmed goals only |
| "Explain IIS / Weibull / lane 2" | Read-only answer |
| "close session" | ROADMAP + Chat Context + git commit |

**Do not** say "just do it" expecting silent writes — coach will still propose goals first unless you explicitly said Proceed.

---

## What you can change vs not

| OK in your lane | Do not touch (other lane) |
|-----------------|---------------------------|
| `src/agents/` (L1) | `src/physics/` internals (L2) |
| `src/physics/` (L2) | Streamlit layout (L3) |
| `src/dashboard/` (L3) | Agent logic — render JSON only |
| `deploy/databricks/` (L4) | New contract shapes without vault |
| `ops/runbooks/`, pitch docs (L5) | `src/` implementation |

**Shared:** `src/contracts/` — any change → tell team + VAULT UPDATE.

---

## Vault updates (when something locked changes)

If an agent name, IIS weight, or JSON shape changes:

1. Lane owner posts 🔒 **VAULT UPDATE** block in chat.
2. Human approves.
3. Someone updates `LOCKED_STATE.md`.
4. All lane chats re-read vault on next message.

---

## Handoffs between lanes

Use contract JSON examples, not "call my function":

```
Lane 2 delivers: PhysicsModelOutput { health_index, rul_estimate, ... }
Lane 1 wraps it → AssetHealthReport for UI
Lane 3 renders AssetHealthReport.health_score — no Weibull imports
```

See `src/contracts/` for exact Pydantic models.

---

## Demo work (deferred for now)

v1 at `src/legacy/demo-v1-metagpt/` is a **reference shell** — known bugs (imports, RUL snapshot). Team agreed to skip deep demo testing until v2 spine is ready.

Target demo story: `docs/architecture/08_DEMO_SCENARIOS.md` (5-minute judge script).

---

## Deliverables for management

| Audience | Give them |
|----------|-----------|
| Engineers + TL | `docs/deliverables/PlantMind_Ultra_Implementation_Team_Guide.docx` |
| Executives | `docs/deliverables/PlantMind_Complete_Project_Blueprint.docx` |
| Presentation | `docs/deliverables/PlantMind_Complete_Handover_Deck.pptx` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| AI edited wrong folder | Point to `PlantMind_live`; cite `00-START-HERE.md` |
| Merge conflict on contracts | Stop; one owner lane resolves + vault update |
| "I don't know my lane" | Read `ops/ROUTING.md` or ask: backend / physics / UI / Databricks / pitch? |
| Lost context between sessions | Latest file in `Chat Context/` — highest `vX.Y` |

---

## Session close checklist (human)

- [ ] Confirm coach updated `ROADMAP.md`
- [ ] New `Chat Context` version exists
- [ ] `git log -1` shows today's commit
- [ ] Optional: run `scripts/export-to-drive.ps1` for NotebookLM