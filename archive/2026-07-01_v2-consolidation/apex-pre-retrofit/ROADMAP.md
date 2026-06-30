# ROADMAP - PlantMind
_Last updated: 2026-06-30 · paired with context v1.8_

## Growth ledger
| Date | Context version | Items added | Items completed | Net delta | Open items total |
|------|------------------|-------------|------------------|-----------|-------------------|
| 2026-06-29 | v1.0 | 12 | 0 | +12 | 12 |
| 2026-06-29 | v1.0 | 2 | 6 | -4 | 10 |
| 2026-06-30 | v1.2 | 1 | 0 | +1 | 11 |
| 2026-06-30 | v1.3 | 1 | 10 | -9 | 2 |
| 2026-06-30 | v1.4 | 2 | 1 | +1 | 3 |
| 2026-06-30 | v1.5 | 0 | 2 | -2 | 1 |
| 2026-06-30 | v1.6 | 0 | 1 | -1 | 0 |
| 2026-06-30 | v1.7 | 5 | 8 | -3 | 5 |
| 2026-06-30 | v1.8 | 0 | 2 | -2 | 3 |

## NOW
- [ ] Lane 5: Judge Q&A bank + ROI calculator (`ops/runbooks/`) — HIGH priority, 9 days to hackathon
- [ ] Wire GROQ_API_KEY env var for real LLM-backed RCA + executive brief

## NEXT
- [ ] Lane 4: `deploy/databricks/` runbook + notebook skeleton
- [ ] 2-tier testing framework: add `smoke` + `heavy` pytest markers to `tests/conftest.py`

## DEFERRED (demo polish — revisit before hackathon freeze)
- [ ] Confirm v1 demo smoke + fix FORGE imports / RUL snapshot / `run_demo.py` (user skip 2026-06-30)
- [ ] Port v1 Streamlit → `src/dashboard/` from legacy (superseded by Lane 3 contract-first build)
- [ ] `scripts/run-demo.ps1` unified runner

## HORIZON
- [ ] Wire scenario injectors A–E to `ml/synthesis/` + integration pytest (catalog exists)
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
- [x] TEAM-OPERATIONS-PLAYBOOK + CLI-PARITY + testing framework (14 pytest) — 2026-06-30
- [x] `docs/parallel/` lane living docs + `scripts/check-status.ps1` — 2026-06-30
- [x] Lane 2: `src/physics/` Weibull engine + `ml/synthesis/` generator (15k rows, 32 tests) — 2026-06-30
- [x] Lane 1: 5 agents + orchestrator + FastAPI + governance + RAG stub (78 tests, 6.5ms/call) — 2026-06-30
- [x] Lane 3: Streamlit dashboard — Plant Overview (gauge + RUL bar + anomaly badges), GötzeDecision (IIS chart + approval gate), Audit Log (lineage table) — 2026-06-30
- [x] Fleet Operations Center: 5-plant fleet view, sector-tagged cards, $3.17M savings KPI, nav to plant drill-down — 2026-06-30
- [x] Weibull dual-path projection: historical/do-nothing/act-now with maintenance window rect — 2026-06-30
- [x] Signal Anomaly Waterfall: 5-signal subplot, red anomaly highlights, last 45 cycles — 2026-06-30
- [x] Savings Decay Timeline + What-If ROI panel ($540k vs $70k = $470k net saving) — 2026-06-30
- [x] Failure Injector sidebar + 5 named failure patterns + cascade chain visualization — 2026-06-30
- [x] Live Feed toggle + speed selector (1x/5x/10x) with synthetic twin mode — 2026-06-30
- [x] Groq LLM integration (llama-3.3-70b) with template fallback for RCA + executive brief — 2026-06-30
- [x] RL feedback loop: `ml/feedback/outcome_logger.py` + Model Accuracy KPI in fleet overview — 2026-06-30
- [x] Full UI overhaul: dark-theme CSS (styles.py), horizontal page_link nav, per-page sidebars, internal st.tabs() on all 4 pages — 2026-06-30
- [x] RL Feedback tab: log_outcome() UI wired into Audit Log page (record selector + outcome form + Model Health tab) — 2026-06-30