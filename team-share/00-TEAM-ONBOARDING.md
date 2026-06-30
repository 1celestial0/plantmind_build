# PlantMind — Team Onboarding Pack
_Shared 2026-07-01 · for team members + senior engineers · verify, then build in parallel_

## The documents (all verified-correct, conform to the lock)
| # | Document | Role | Authority |
|---|---|---|---|
| 1 | **PROJECT-DNA.md** | The constitution — identity, 2 pillars, scope fence, 15 features, rubric | 🟢 **TRUTH (apex)** |
| 2 | **LOCKED_STATE.md** | Technical vault — contracts, physics λ/β (§6a), thresholds, lanes | 🟢 **TRUTH (technical)** |
| 3 | **PlantMind_Project_Specification_v2.0_2026-07-01.md** | Industry spec, every feature — regenerated from the lock | 🟢 **correct (derived)** |

> **Every doc in this pack is current and conforms to the locked DNA.** The earlier June Grok PDFs (5-agent, dark-UI, `lambda:0.0023` examples) were **pre-lock and partially incorrect — they are deliberately excluded.** Do not use them.
> **Coming next (regenerating now from the lock):** corrected **UI/UX Spec** and **Databricks Implementation Guide**. Until they land, L3 uses `PROJECT-DNA §10` (light palette + screens) and L4 uses `LOCKED_STATE §9` + Project Spec §3/§7.

## What's already locked & correct (so you can trust it)
- **6 agents** incl. MaintenanceScheduler · **light UI** · **physics λ/β per LOCKED_STATE §6a** · **RUL in days** · **config-driven pillar** · **local demo spine**. All baked into the docs above — no stale deltas to reconcile.

## Your parallel lanes (pick yours, start now)
| Lane | Owner | Builds | Folder |
|---|---|---|---|
| L1 Backend & Agents | Sourav | agents, orchestrator, IIS, API, audit | `src/agents/`, `src/api/`, `src/pipeline/` |
| L2 Physics & ML | Sourav | Weibull, synthetic data, PINN (stretch) | `src/physics/`, `ml/` |
| L3 UI & Mockups | Member 2 / 3 | Streamlit (light reskin), charts, Götze panel, Config Viewer, audit views | `src/dashboard/` |
| L4 Databricks Port | Sourav / team | DLT, Feature Store, Unity Catalog, Mosaic AI | `deploy/databricks/` |
| L5 Demo & Pitch | Member 4 / Sourav | injector, script, Q&A, ROI, governance story | `ops/runbooks/` |

**One lane per person per work-session.** Lanes talk only through `src/contracts/` — never reach into another lane's internals.

## What's blocking everyone (do these first)
1. 🔴 **`src/contracts/` lock** — `manifest.py` (Plant Config Manifest) + `workorder.py`. *Every lane depends on these shapes. L1 owns; others wait for it before wiring.*
2. `config/plants/hero.yaml` (the demo manifest, §6a λ/β).
3. Fix λ/β + RUL traps in `src/physics/`.

Full sequence: `ROADMAP.md` (Top-20).

## How we work (rules of engagement)
- **DNA-first:** no feature is built without a what/who/how/why entry in PROJECT-DNA §6.
- **Conform-or-amend:** disagree with a locked decision? Don't relitigate in chat — propose a numbered Amendment to PROJECT-DNA §10.
- **Contracts = vault update:** any change to `src/contracts/` requires a LOCKED_STATE §4 vault update, reviewed.
- **Code only in `src/` and `ml/`.** Commit before switching tools.
- Operating manual: `00-START-HERE.md`. Routing: `ops/ROUTING.md`.

## Verify-and-confirm (what we need back from you)
Reply with: (a) your lane, (b) anything in PROJECT-DNA §3 scope fence you think is wrong (with reasoning → becomes an Amendment), (c) your read of the rubric §7 weak spots.
