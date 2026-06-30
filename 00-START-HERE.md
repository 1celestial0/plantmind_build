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

## Session lifecycle (the CLI SOP)

| Phase | Say / do | What happens |
|---|---|---|
| **START** | open terminal in `PlantMind_live`, launch CLI | AI reads `PROJECT-DNA` → `LOCKED_STATE` → latest `Chat Context/` → `ROADMAP` NOW, then proposes ≤3–5 sequential goals |
| **CONFIRM** | **"Proceed with Goals"** (or `G1 only`) | AI starts work — never writes before this |
| **WORK** | stay in **one lane** | code only in `src/`/`ml/` · contract change → LOCKED_STATE vault update · feature needs a DNA §6 entry first · AI logs each goal (why/artifacts/impact) |
| **PAUSE** (short break, same task) | **"pause"** | AI commits WIP (`git commit -m "wip: …"`) + writes a one-line state to `ROADMAP` NOW. No full close. Resume is clean. |
| **RESUME** | **"resume"** | AI re-runs START reads + `git log -1` / `git status`, picks up the in-progress NOW item |
| **CLOSE** (end of work) | **"close session"** | re-score DNA §7 rubric · update both Obsidian vaults (§8.6) · ROADMAP update · new `Chat Context/YYYY-MM-DD_vX.Y` · `git commit` |
| **RESTART** (clean slate / went sideways) | **"restart"** | close properly first; OR if corrupted, `git reset --hard <last-good>` then re-orient from `PROJECT-DNA` |

**Switching CLI (Claude ↔ Grok ↔ Gemini):** always **CLOSE or PAUSE (commit) first** — the next tool reads the same committed truth.

## Artifact create/update SOP (where things go)
| Artifact | Home | Rule |
|---|---|---|
| Product idea / scope / feature | `PROJECT-DNA.md` | change via numbered Amendment (§10) |
| Contracts / λ-β / thresholds | `LOCKED_STATE.md` + `src/contracts/` | change via 🔒 VAULT UPDATE (paired) |
| Research findings | `docs/research/` | new file; cite source; link from DNA if it changes a decision |
| Application code | `src/`, `ml/` | one lane; talk via contracts |
| Prompts / workflows / runbooks | `ops/` | — |
| Derived spec / deck / scorecard | generate FROM the DNA; banner-tag "derived" | never authoritative |
| Knowledge | `knowledge/obsidian-vault/` (truth) + `knowledge/code-lineage-vault/` (code) | refresh at every close (§8.6) |

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
