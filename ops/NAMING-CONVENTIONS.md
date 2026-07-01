# Naming Conventions — all artifacts

> Every new file, folder, branch, and doc must follow these rules. Conflicts: **canonical spec wins** (see `docs/00-MASTER-SPEC.md`).

---

## 1. Project folder layout (portfolio)

```
C:\Users\hp\Claude\Projects\{PortfolioName}\
├── {Name}_live\               # ONE active workspace (git repo)
├── {Name}_OS\                 # Template — copy to start new project
├── {Name}_Archive\            # YYYYMMDD_snapshot-{label}\ — frozen, read-only
└── {Name}_GitHub\             # Public publish target (script-fed)

PlantMind example:
C:\Users\hp\Claude\Projects\PlantMind\
├── PlantMind_live\
├── PlantMind_OS\
├── PlantMind_Archive\
└── PlantMind_GitHub\
```

---

## 2. Root files (every active project)

| File | Purpose |
|---|---|
| `00-START-HERE.md` | Human entry (number prefix = read first) |
| `AI-OPERATING-SYSTEM.md` | Multi-CLI rules |
| `LOCKED_STATE.md` | Frozen decisions |
| `ROADMAP.md` | Backlog only |
| `CLAUDE.md` / `AGENTS.md` / `GEMINI.md` / `CODEX.md` | Per-CLI pointers |
| `MIGRATION-MAP.md` | Archive lineage |

---

## 3. Documentation naming

| Pattern | Example | Use |
|---|---|---|
| `docs/00-MASTER-SPEC.md` | — | Single merged canonical spec |
| `docs/INDEX.md` | — | Doc registry + supersession map |
| `docs/dna/{TOPIC}.md` | `PROJECT_DNA.md` | Story, pitch, identity |
| `docs/architecture/{NN}_{TOPIC}.md` | `03_ARCHITECTURE.md` | Numbered KB chain |
| `docs/research/{ARTIFACT}_{YYYY}_{DDth}_{Month}.md` | `PAIN_REGISTER_2026_25th_June.md` | Research outputs |
| `docs/legacy/` | v1 blueprints | Superseded — never edit |
| `docs/deliverables/` | `.docx`, `.pptx`, `.pdf` | Handover exports |
| `docs/CODEBASE-INVENTORY.md` | — | File lineage registry |

**Rule:** New research artifacts use `SCREAMING_SNAKE` + date suffix.

---

## 4. Code naming

### 4a. Symbol conventions

| Symbol type | Convention | Example |
|---|---|---|
| Classes, types/interfaces | `PascalCase` | `AssetHealthReport`, `GotzeDecision` |
| Functions and variables | `snake_case` (Python/PEP 8) | `compute_health`, `asset_id` |
| Module-level constants and env vars | `UPPER_SNAKE_CASE` | `CYCLES_PER_DAY`, `SAFETY_VETO_CEILING`, `_WEIGHTS` |

> **Note:** Python requires `snake_case` for functions and variables per PEP 8. The generic camelCase convention applies to non-Python code (JS/TS) if added in future.

### 4b. File and folder conventions

| Item | Convention | Example | Exception |
|---|---|---|---|
| Files and folders | `kebab-case` | `plant-config.yaml`, `gen-team-docs.py` | Python modules (see below) |
| Python modules (importable) | `snake_case.py` | `gotze_engine.py`, `data_sentinel.py` | Python cannot import modules with hyphens |
| Agents | `{role}.py` in `src/agents/` | `data_sentinel.py` | — |
| Contracts | `src/contracts/{domain}.py` | `physics.py` | — |
| API routes | `src/api/routes/{resource}.py` | `assets.py` | — |
| Tests | `tests/test_{module}.py` | `test_gotze_iis.py` | — |
| Standalone scripts (not imported) | `kebab-case.py` | `smoke-test.py`, `gen-team-docs.py` | — |
| Config files | `kebab-case.yaml` | `plant-config.yaml` | — |
| Legacy code | `src/legacy/{label}/` | `demo-v1-metagpt/` | — |

---

## 5. Git conventions

| Item | Pattern |
|---|---|
| Branch | `feature/lane{N}-{short-desc}` |
| Commit | `type(scope): message` — e.g. `feat(agents): IIS scorer v1` |
| Tag | `v{major}.{minor}-{label}` — e.g. `v1.0-hackathon-submission` |
| Context file | `Chat Context/YYYY-MM-DD_vX.Y_project-context.md` |

---

## 6. Conflict resolution (naming)

| Conflict | Canonical name |
|---|---|
| G-score vs IIS | **IIS** in new code; `g_score` alias in legacy only |
| 5 layers vs 5 agents | **agents** in runtime; **layers** in data pipeline docs |
| FORGE vs src | **src/** for new; **src/legacy/demo-v1-metagpt/** frozen |
| PlantMind | **PlantMind** (retired name) |
| IIS (formula) vs IIS (framework) | **IIS-score** vs **IIS-framework** in prose |

---

## 7. Archive snapshots

```
_archive/{ProjectName}/YYYYMMDD_snapshot-{label}/
```

Labels: `v1-forge`, `hackathon-vault`, `pre-merge`, etc. Never rename after freeze.