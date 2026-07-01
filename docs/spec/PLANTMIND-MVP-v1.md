# PLANTMIND-MVP-v1

> **Derived from `PROJECT-DNA.md` and `LOCKED_STATE.md`; not authoritative over them.**

## MVP objective
Deliver a runnable, defensible v1 closed-loop hero flow that proves both pillars (decision closure + config modularity) without broad refactors.

## In-scope MVP capabilities (must-have)
1. **Manifest validation:** Loader validates `config/plants/hero.yaml` against `PlantManifest`.
2. **Runtime composition:** Runtime composer creates a `PUMP-001` RuntimePlan from manifest.
3. **Physics health/RUL:** Deterministic Weibull path uses locked λ/β and outputs RUL in days.
4. **IIS decisioning:** IIS scoring supports profiles and profile swap changes score/ranking.
5. **Approval gate:** Human approval creates `WorkOrder`.
6. **Audit lineage:** Decision path and approval/work order are recorded in chain/lineage.
7. **Demo:** Streamlit hero flow clearly shows trigger → decision → approval → work order → audit.
8. **Build hygiene:** CI/package/smoke validation exists.

## Scope freeze boundary
### Explicitly in for rebuild-v1 foundation
- Documentation lock for spec, MVP, and epics/stories/acceptance criteria
- GitHub contribution scaffolding (PR + issue templates)
- Basic Python CI workflow
- Minimal package metadata for editable install + pytest

### Explicitly out for this PR
- Large folder moves/refactors
- Runtime feature implementation across orchestrator/agents/physics/dashboard
- Archive cleanup or deletion of current artifacts

## Stretch (non-blocking)
- Automated plant intake assistant for manifest drafting
- PINN/advanced model path beyond Weibull baseline
- Databricks live-path hard dependency for demo
- Autonomous execution beyond mandatory human approval

## Non-goals (explicit)
- Repositioning PlantMind as generic agent framework
- Replacing deterministic math path with LLM decisions
- Building full low-code manifest editor
- Claiming alternative source-of-truth outside DNA/vault
