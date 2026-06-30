# BUILD PLAN — PlantMind × Götze Engine
> The realistic 24-hour plan for 4 people, the team split, the repo strategy, and the research phases. Designed so the demo is safe by Hour 16 and polished by Hour 23.

---

## 1. The prime directive

**A working, rehearsed demo of the one-best-action moment beats an ambitious half-built system every time.** Lock the guaranteed path early; treat the PINN and fancy extras as upside only.

---

## 2. Pre-hackathon (do this BEFORE the clock starts — allowed as justified boilerplate)

- [ ] Download CMAPSS, PRONOSTIA, Azure PdM datasets locally.
- [ ] Run `calibrate_weibull.py` → save λ, β per asset class to a config.
- [ ] Scaffold the repo (folders from `03_ARCHITECTURE.md`) + `requirements.txt`.
- [ ] Get Groq API key + test one call. Confirm free-tier limits.
- [ ] Seed ChromaDB with 10–20 manual/SOP docs.
- [ ] Rehearse the pitch story once (even before code exists).

> This front-loading is the single biggest risk-reducer. None of it is "the build" — it's setup.

---

## 3. Team split (parallel tracks)

| Member | Track | Owns |
|---|---|---|
| **Sourav** | Brain | 5 agents, IIS, orchestrator, FastAPI, synthetic data, Weibull (+PINN stretch) |
| **Member 2** | Viz-Plant | Streamlit shell, live sensor charts, plant overview |
| **Member 3** | Viz-Decision | The "one best action" panel, IIS visualization, audit/lineage views |
| **Member 4** | Glue + QA + Demo | Integration, scenario injector, test the edge cases, **own the demo script** |

---

## 4. Hour-by-hour (24h)

| Hours | Sourav (Brain) | M2 (Plant UI) | M3 (Decision UI) | M4 (Glue/QA) |
|---|---|---|---|---|
| **0–4** | Synthetic generator + state model + agent stubs | Streamlit shell + layout | Mock "best action" panel from fake JSON | Repo wiring, CI, scenario injector skeleton |
| **4–8** | DataSentinel + AssetHealthOracle (Weibull) working | Live sensor charts wired to data | IIS panel + runner-up display | Integrate agents 1–2 end-to-end |
| **CHECKPOINT H8** | health + anomaly visible on dashboard for one asset | | | |
| **8–12** | GötzeEngine + IIS + Groq narrative | Plant overview (5 assets) | Audit timeline + lineage view | Integrate Götze; test Scenario A |
| **12–16** | RootCause (RAG) + ExecutiveSummarizer | polish charts, thresholds config | Integrity-check button | Scenarios B, C working |
| **CHECKPOINT H16** | **full 5-agent flow runs for Scenario A. DEMO IS NOW SAFE.** | | | |
| **16–20** | (stretch) PINN OR harden agents + fallbacks | visual polish | visual polish | Edge cases (sensor dropout, no-parts), backup video |
| **CHECKPOINT H20** | freeze features. No new scope. | | | |
| **20–23** | bug-fix only | bug-fix only | bug-fix only | **rehearse demo 5+ times**, record backup |
| **CHECKPOINT H23** | **tag `v1.0-hackathon-submission`. Demo from frozen build.** | | | |
| **23–24** | submission + final rehearsal | | | |

> **Golden rule: if it's not integrated by Hour 16, it does not go in the demo.**

---

## 5. Repo strategy

```
plantmind-production/   ← protected. Sourav merges only. Final demo.
   main → tag v1.0-hackathon-submission at Hour 23

plantmind-sandbox/      ← integration. everyone PRs here first.
   dev → integration branch

4 forks (each member):
   feature/sourav-{agents,physics,api}
   feature/viz1-{plant-dashboard,sensor-charts}
   feature/viz2-{iis-ui,audit-trail}
   feature/tester-{integration,qa,demo-script}
```

- **Commit format:** `type(scope): description` → `feat(agents): GötzeEngine IIS v1`
- **Backups:** at each checkpoint, `zip -r backup_hourXX.zip .` → Google Drive.

---

## 6. Definition of Done (what "demo-ready" means)

- [ ] Scenario A runs start-to-finish with all 5 agents.
- [ ] The "one best action" panel renders even if 2 agents fail.
- [ ] Human approve/reject works and writes to the audit log.
- [ ] Integrity-check button works on stage.
- [ ] At least one edge case (sensor dropout) demonstrable.
- [ ] 5-minute script rehearsed ≥5 times.
- [ ] Backup video recorded.
- [ ] Repo tagged and frozen.

---

## 7. Research phases (optional prep, before/around the build)

Run these in the dedicated chat to generate supporting artifacts:
- **PHASE 1 — Pain register:** 30+ industrial pain points → agent mapping → IIS potential.
- **PHASE 2 — Databricks map:** each contract → exact Databricks service + GA status.
- **PHASE 3 — Physics validation:** derive IIS, validate Weibull against CMAPSS literature, prior-art note.
- **PHASE 4 — Architecture lock:** finalize all diagrams.
- **PHASE 5 — Build plan:** this document, refined per team.

> These are *supporting research*, not the build. The build follows the hour-by-hour table above.

---

## 8. Top 5 risks & mitigations

| Risk | Mitigation |
|---|---|
| PINN eats all your time | It's optional; Weibull baseline ships regardless |
| Integration hell at the end | Hard checkpoints at H8/H16; integrate continuously |
| LLM API limits/outage | Templated fallback strings; pre-warm; cache responses |
| Over-claiming novelty to judges | Use the honest "patent-candidate pending prior-art" framing |
| Laptop/demo failure on stage | Recorded backup video + frozen tagged build |
