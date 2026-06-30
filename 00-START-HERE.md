# PlantMind — START HERE (operating manual)

> **One folder. One truth. One next step.**
> Path: `C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live`
> Last updated: 2026-07-01 (v2 consolidation — product idea LOCKED)

---

## Precedence (read this first, always)

```
L0  PROJECT-DNA.md      ← THE CONSTITUTION (apex truth). Identity, 2 pillars, scope fence, 15 features, rubric.
L1  LOCKED_STATE.md     ← Technical vault (contracts, λ/β §6a, thresholds, lanes).
L2  Derived: 3 Grok PDFs · Obsidian vaults · generated Spec/Scorecard/PPT.   (never authoritative)
L3  ROADMAP.md · Chat Context/ · lane prompts.                              (execution state)
```
**If any doc disagrees with `PROJECT-DNA.md`, the other doc is wrong** until a numbered Amendment changes the DNA. Never create a new "master" doc — extend the DNA.

## If you only remember one thing

| Question | Answer |
|---|---|
| **What do I read first?** | `PROJECT-DNA.md` → `LOCKED_STATE.md` → `ROADMAP.md` (NOW) |
| **Where do I work?** | Always `PlantMind_live` |
| **Where is the code?** | `src/` (v2). v1 demo is **archived** at `/archive/2026-07-01_v2-consolidation/` |
| **What's the product?** | Config-driven, physics-informed decision fabric → one approved, audited action. 2 pillars: closed-loop + config-driven. |
| **What's locked?** | DNA §3 CLOSED decisions C1–C10 (don't relitigate) |
| **How do I end a session?** | Say **"close session"** → ROADMAP + new Chat Context + git commit |

## The 6 agents (DNA §4 / LOCKED_STATE §1)
DataSentinel → AssetHealthOracle → **GötzeEngine ⭐** → RootCauseAnalyst → ExecutiveSummarizer → **MaintenanceScheduler ⭐**

---

## Zones (mental model)

```
PlantMind_live/
├── 🧭 ROOT            PROJECT-DNA · LOCKED_STATE · ROADMAP · Chat Context
├── 📚 docs/           research/ · IMPLEMENTATION-GUIDE-ULTRA · INDEX   (architecture/ + master-spec archived)
├── 🧠 knowledge/      obsidian-vault/ (truth mirror) · code-lineage-vault/ (code map)  — both DERIVED, kept current
├── ⚙️  ops/            prompts · workflows · runbooks · MODEL-REGISTRY · ROUTING
├── 💻 src/            contracts · physics · agents · pipeline · api · governance · rag · dashboard
├── 🧪 ml/             synthesis · training · feedback
├── 🚀 deploy/         databricks (Layer-1 reference impl)
└── 🗄️  archive/        quarantined v1/legacy/duplicates — historical only, NOT truth
```

## Task router — "I want to…"

| I want to… | Open | Lane |
|---|---|---|
| Know what the product IS | `PROJECT-DNA.md` | — |
| Know what's technically locked | `LOCKED_STATE.md` | — |
| See next steps | `ROADMAP.md` → NOW | — |
| Add Manifest/WorkOrder schema | `src/contracts/` (= LOCKED_STATE vault update) | L1 |
| Write agent logic | `src/agents/` | L1 |
| Physics / Weibull / synthetic | `src/physics/` + `ml/synthesis/` | L2 |
| Streamlit / dashboard (light reskin) | `src/dashboard/` | L3 |
| Databricks port | `deploy/databricks/` | L4 |
| Demo script / pitch | `ops/runbooks/demo.md` | L5 |

Full routing: `ops/ROUTING.md`

---

## Session ritual

**START:** read `PROJECT-DNA` → `LOCKED_STATE` → latest `Chat Context/` → `ROADMAP` NOW → AI gives top-3 NOW items.
**WORK:** one lane per chat · code only in `src/` or `ml/` · contract changes → LOCKED_STATE vault update · features must have a DNA §6 entry first.
**CLOSE:** re-score DNA §7 rubric · update both Obsidian vaults (DNA §8.6) · ROADMAP update · new `Chat Context/YYYY-MM-DD_vX.Y` · `git commit`.

## Run (PowerShell)

```powershell
cd "C:\Users\hp\Claude\Projects\PlantMind\PlantMind_live"
streamlit run src\dashboard\app.py        # v2 dashboard
uvicorn src.api.main:app --reload         # v2 API
```

## Files at root

| File | Purpose |
|---|---|
| `PROJECT-DNA.md` | **The constitution — apex truth (read first)** |
| `LOCKED_STATE.md` | Technical vault (contracts, λ/β, decisions) |
| `00-START-HERE.md` | This operating manual |
| `ROADMAP.md` | Living backlog (NOW / NEXT / HORIZON) |
| `CLAUDE.md` · `AI-OPERATING-SYSTEM.md` | AI entry + multi-CLI rules |
| `Chat Context/` | Versioned session memory |

---
*You forget less when every question routes to one constitution and one table.*
