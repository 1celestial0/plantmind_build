# ROADMAP - PlantMind
_Last updated: 2026-07-01 · paired with context v2.0 · backlog conforms to `PROJECT-DNA.md` v1.0 Top-20_

> Backlog only (NOW / NEXT / HORIZON). Truth lives in `PROJECT-DNA.md` (apex) + `LOCKED_STATE.md`. Items reference DNA Top-20 #n and feature F-XX.

## Growth ledger
| Date | Context version | Items added | Items completed | Net delta | Open items total |
|------|------------------|-------------|------------------|-----------|-------------------|
| 2026-06-30 | v1.7 | 5 | 8 | -3 | 5 |
| 2026-06-30 | v1.8 | 0 | 2 | -2 | 3 |
| 2026-07-01 | v2.0 | 12 | 3 | +9 | 12 |

## NOW (Phase 0–1 · today–Jul 2)
- [x] **DNA ratified → v1.0 LOCKED** (#1) — 2026-07-01
- [x] **Doc consolidation + 2 Obsidian vaults + archive** (#3) — 2026-07-01
- [ ] **Governance retrofit + git commit** (#4/#5) — *in progress*
- [ ] 🔴 **Lock `src/contracts/`: `manifest.py` (Plant Config Manifest) + `workorder.py`** (#2, F-10) — blocks all lanes
- [ ] `config/plants/hero.yaml` with §6a λ/β (#6, F-02 seed)
- [ ] ⚠️ Fix λ/β + RUL-unit traps in `src/physics/` (#7, F-05) — no cycle-30 collapse
- [ ] 🔴 Start Databricks trial: workspace/cluster/Unity Catalog + Bronze (#8, F-12) — 14-day clock

## NEXT (Phase 2–3 · Jul 2–5)
- [ ] ⚠️ Config loader/composer — manifest composes ingest→features→health→IIS (#9, F-02) — highest risk
- [ ] Hero pump end-to-end through manifest, reliability_first (#10)
- [ ] IIS profile swap reliability→energy (#11, F-08) — the modularity demo
- [ ] Keep static fallback path runnable (#12, C4/C9 guardrail)
- [ ] Build `agents/maintenance_scheduler.py` → work order + audit (#13, F-03)
- [ ] Full 6-agent orchestrator end-to-end + graceful degradation (#14, F-15)
- [ ] RAG corpus: 10–20 manuals in ChromaDB→Vector Search (#15, F-06)

## HORIZON (Phase 4–6 · Jul 4–9)
- [ ] UI dark→light reskin (#16, C3, F-13)
- [ ] Config Viewer + swap toggle, Asset Detail hero, Audit/Lineage view (#17, F-02/F-14/F-09)
- [ ] Generate derived docs from DNA: Industry Spec · Scorecard · UI/UX PPT (#18) — AFTER §6 + contracts stable
- [ ] Full demo flow + pin $180k + Lane 5 script/Q&A (#19, F-07/F-11)
- [ ] Rehearsal + cost check + H-14/16/20 freeze calls + final lock (#20)
- [ ] PINN stretch (freeze by Hour 14 if not validating — C5)
- [ ] Verify governance hash-chain + lineage actually run (may raise rubric #6)

## DONE (recent — full history in archive)
- [x] **2026-07-01 · DNA v1.0 LOCKED** — 2 pillars, scope fence C1–C10, 15 features, rubric (70.3%)
- [x] **2026-07-01 · Consolidation** — archived v1 vault/legacy/dups/competing DNA+spec+architecture; built v2 source-of-truth + code-lineage Obsidian vaults
- [x] **2026-07-01 · Apex retrofit** — CLAUDE.md + AI-OS + 00-START-HERE + ROADMAP + IMPLEMENTATION-GUIDE conform to DNA
- [x] 2026-06-30 · Wave 2: fleet view, Weibull projection, signal waterfall, Groq LLM, RL loop, dark dashboard (now superseded by light reskin)
- [x] 2026-06-30 · Lane 1: 5 agents + orchestrator + FastAPI + governance + RAG stub (78 tests)
- [x] 2026-06-30 · Lane 2: `src/physics/` Weibull + `ml/synthesis/` generator (15k rows, 32 tests)
- [x] 2026-06-30 · Lane 3: Streamlit dashboard (Plant Overview, GötzeDecision, Audit Log)
- [x] 2026-06-30 · `src/contracts/` Pydantic models from LOCKED_STATE §4
- [x] 2026-06-29 · Merge into Live (246+ files) · git init

> Older DONE items: see `archive/2026-07-01_v2-consolidation/apex-pre-retrofit/ROADMAP.md`.
