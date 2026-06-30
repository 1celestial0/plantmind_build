# ROADMAP - PlantMind
_Last updated: 2026-06-30 · paired with context v1.3_

## Growth ledger
| Date | Context version | Items added | Items completed | Net delta | Open items total |
|------|------------------|-------------|------------------|-----------|-------------------|
| 2026-06-29 | v1.0 | 12 | 0 | +12 | 12 |
| 2026-06-29 | v1.0 | 2 | 6 | -4 | 10 |
| 2026-06-30 | v1.2 | 1 | 0 | +1 | 11 |
| 2026-06-30 | v1.3 | 1 | 10 | -9 | 2 |

## NOW
- [ ] Lane 2 build: `src/physics/` Weibull + `ml/synthesis/` data generator (origin: ARCHITECTURE_LOCK P1)
- [ ] Lane 1 build: agent stubs + orchestrator + FastAPI skeleton (origin: ARCHITECTURE_LOCK P2)

## NEXT
- [ ] Lane 3: `src/dashboard/` mockups → Streamlit shell (read-only contracts)
- [ ] Lane 5: judge Q&A bank + ROI calculator spec (`ops/runbooks/`)
- [ ] Lane 4: `deploy/databricks/` runbook + notebook skeleton

## DEFERRED (demo polish — revisit before hackathon freeze)
- [ ] Confirm v1 demo smoke + fix FORGE imports / RUL snapshot / `run_demo.py` (user skip 2026-06-30)
- [ ] Port v1 Streamlit → `src/dashboard/` from legacy (superseded by Lane 3 contract-first build)
- [ ] `scripts/run-demo.ps1` unified runner

## HORIZON
- [ ] GitHub remote + publish script (`PlantMind_GitHub/`)
- [ ] Full 20-row × 10 dataset samples in `ml/synthesis/` (DATA_REALITY completion)
- [ ] PINN stretch (freeze by Hour 14 if not validating)
- [ ] 6th agent decision: MaintenanceScheduler vs SafetyGuardian

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
- [x] Wave 1 Phase 1: goal-log + OPERATIONS-MANUAL + TEAM-CHAT-GUIDE — 2026-06-30
- [x] Split `PLANTMIND_5_CHAT_PROMPTS.md` → `ops/prompts/lanes/lane-01..05.md` — 2026-06-30
- [x] Create `src/contracts/` Pydantic models from LOCKED_STATE §4 — 2026-06-30
- [x] Research Phases 3–6 (DATABRICKS_MAP, DATA_REALITY, ROI, ARCH_LOCK) — 2026-06-30
- [x] `scripts/export-to-drive.ps1` NotebookLM whitelist — 2026-06-30
- [x] MLflow scaffold `ml/tracking/` + `ml/models/` — 2026-06-30
- [x] `ops/skills/plantmind-session/` session skill — 2026-06-30
- [x] `scripts/sync-notion-drive.ps1` stub + STATE.json IDs — 2026-06-30