# ROADMAP - PlantMind
_Last updated: 2026-06-30 · paired with context v1.2_

## Growth ledger
| Date | Context version | Items added | Items completed | Net delta | Open items total |
|------|------------------|-------------|------------------|-----------|-------------------|
| 2026-06-29 | v1.0 | 12 | 0 | +12 | 12 |
| 2026-06-29 | v1.0 | 2 | 6 | -4 | 10 |
| 2026-06-30 | v1.2 | 1 | 0 | +1 | 11 |

## NOW
- [ ] Confirm v1 demo still runs: `streamlit run src/legacy/demo-v1-metagpt/app.py` (origin: v1.0 — path updated Phase 0)
- [ ] Wave 1 Phase 1: goal-log + OPERATIONS-MANUAL + TEAM-CHAT-GUIDE (origin: v1.2)

## NEXT
- [ ] Split `PLANTMIND_5_CHAT_PROMPTS.md` into `ops/prompts/lanes/lane-01..05.md` (origin: v1.0)
- [ ] Create `src/contracts/` Pydantic models from LOCKED_STATE §4 JSON shapes (origin: v1.0)
- [ ] Port v1 Streamlit shell → `src/dashboard/` (read-only JSON contract first) (origin: v1.0)
- [ ] Complete research Phases 3–6 (DATABRICKS_MAP, DATA_REALITY, ROI, ARCH_LOCK) → `docs/research/` (origin: v1.0)

## HORIZON
- [ ] `scripts/export-to-drive.ps1` for NotebookLM-Sources whitelist (new — v1.2)
- [ ] Single `scripts/run-demo.ps1` from `PlantMind_live` regardless of v1/v2 path (new — v1.0)
- [ ] MLflow experiment tracking under `ml/models/` with run IDs linked in audit log (new — v1.0)
- [ ] Project-local Grok/Cursor skill at `ops/skills/plantmind-session/` wrapping start/close ritual (new — v1.0)
- [ ] Notion + Drive sync for PlantMind (migrate IDs from old PlantMind STATE.json) (new — v1.0)

## DONE
- [x] Intelligent merge of PlantMind + PlantMind_hckthn into Live (246+ files) — 2026-06-29
- [x] CONFLICT-RESOLUTION.md + CONSOLIDATED-PROJECT-BLUEPRINT.md — 2026-06-29
- [x] Word handover doc + PPT deck generated — 2026-06-29
- [x] Copy vault KB → docs/architecture + docs/dna — 2026-06-29
- [x] Copy research → docs/research — 2026-06-29
- [x] Copy FORGE → src/legacy/demo-v1-metagpt — 2026-06-29
- [x] git init + first commit — 2026-06-29
- [x] Bookmark `PlantMind_live` as only workspace (00-START-HERE) — 2026-06-30
- [x] Phase 0: 4-folder portfolio + continuity + coach SOPs (G0–G6) — 2026-06-30