# ROADMAP - PlantMind-Live
_Last updated: 2026-06-29 · paired with context v1.0_

## Growth ledger
| Date | Context version | Items added | Items completed | Net delta | Open items total |
|------|------------------|-------------|------------------|-----------|-------------------|
| 2026-06-29 | v1.0 | 12 | 0 | +12 | 12 |

## NOW
- [ ] Read `00-START-HERE.md` once end-to-end and bookmark this folder as the only workspace (origin: v1.0)
- [ ] Copy vault KB from `PlantMind_hckthn/` → `docs/architecture/` + `docs/dna/` per `MIGRATION-MAP.md` (origin: v1.0)
- [ ] Copy `PlantMind/PlantMind_Research/*.md` → `docs/research/` (origin: v1.0)
- [ ] `git init` PlantMind-Live + first commit of scaffold (origin: v1.0)
- [ ] Confirm v1 demo still runs: `streamlit run ../PlantMind/FORGE/app.py` (origin: v1.0 — hackathon fallback)

## NEXT
- [ ] Split `PLANTMIND_5_CHAT_PROMPTS.md` into `ops/prompts/lanes/lane-01..05.md` (origin: v1.0)
- [ ] Create `src/contracts/` Pydantic models from LOCKED_STATE §4 JSON shapes (origin: v1.0)
- [ ] Port FORGE Streamlit shell → `src/dashboard/` (read-only JSON contract first) (origin: v1.0)
- [ ] Complete research Phases 3–6 (DATABRICKS_MAP, DATA_REALITY, ROI, ARCH_LOCK) → `docs/research/` (origin: v1.0)

## HORIZON
- [ ] Single `make demo` or `scripts/run-demo.ps1` that launches from PlantMind-Live root regardless of v1/v2 code path (new — v1.0)
- [ ] MLflow experiment tracking under `ml/models/` with run IDs linked in audit log (new — v1.0)
- [ ] Project-local Grok/Cursor skill at `ops/skills/plantmind-session/` wrapping start/close ritual (new — v1.0)
- [ ] Notion + Drive sync for PlantMind-Live (migrate IDs from old PlantMind STATE.json) (new — v1.0)

## DONE
_(empty — scaffold session)_