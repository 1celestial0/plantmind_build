# PlantMind — Gemini CLI Instructions

**Workspace:** `C:\Users\hp\Claude\Projects\PlantMind`

## Before any task
Read in order:
1. `AI-OPERATING-SYSTEM.md`
2. `LOCKED_STATE.md`
3. Latest file in `Chat Context/` (highest vX.Y)
4. `ROADMAP.md` — NOW section

## Write permissions
| Allowed | Forbidden |
|---|---|
| `src/`, `ml/`, `tests/`, `deploy/` | `../PlantMind/`, `../PlantMind_hckthn/` |
| `docs/` (specs only) | Changing LOCKED_STATE without vault update |
| `ops/` | Duplicating backlog outside ROADMAP |

## Primary references
- **How to build:** `docs/IMPLEMENTATION-GUIDE-ULTRA.md`
- **Win strategy:** `docs/WIN-STRATEGY-ASSESSMENT.md`
- **Model APIs:** `ops/MODEL-REGISTRY.md`
- **Task routing:** `ops/ROUTING.md`

## Code standards
- Python 3.11, type hints, 5W comments on functions
- IIS/Götze scoring: deterministic Python only — no LLM in math path
- Dashboard reads API JSON only — no direct physics imports

## Close session
Update ROADMAP + new Chat Context + git commit when user requests close.