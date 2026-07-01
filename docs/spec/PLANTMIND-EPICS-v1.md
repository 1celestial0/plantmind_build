# PLANTMIND-EPICS-v1

> **Derived from `PROJECT-DNA.md` and `LOCKED_STATE.md`; not authoritative over them.**

## Epic 1 — Spec lock and governance
### Story 1.1: Publish derived v1 specification set
**Acceptance criteria**
- `docs/spec/PLANTMIND-SPEC-v1.md`, `PLANTMIND-MVP-v1.md`, and `PLANTMIND-EPICS-v1.md` exist.
- Each document explicitly states derived/non-authoritative status.
- Pillars, freeze line, six-agent scope, and truth hierarchy are consistent.

### Story 1.2: Preserve truth hierarchy
**Acceptance criteria**
- Docs explicitly defer to `PROJECT-DNA.md` and `LOCKED_STATE.md`.
- No wording claims new canonical source-of-truth.

## Epic 2 — GitHub build system
### Story 2.1: Add contribution templates
**Acceptance criteria**
- PR template exists at `.github/pull_request_template.md`.
- Issue templates exist at `.github/ISSUE_TEMPLATE/epic.md`, `story.md`, and `bug.md`.

### Story 2.2: Add basic CI workflow
**Acceptance criteria**
- Workflow exists at `.github/workflows/ci.yml`.
- Python 3.11 is used.
- Workflow runs pytest and supports editable install path.

## Epic 3 — Manifest runtime
### Story 3.1: Validate hero manifest contract
**Acceptance criteria**
- `config/plants/hero.yaml` validates against `PlantManifest`.
- Validation executes in tests/CI without custom ad-hoc command dependencies.

### Story 3.2: Compose runtime plan from manifest
**Acceptance criteria**
- Runtime planner maps hero manifest into deterministic execution plan for `PUMP-001`.
- Plan carries iis profile and physics model references.

## Epic 4 — Physics health engine
### Story 4.1: Enforce locked Weibull parameters
**Acceptance criteria**
- Locked λ/β are used for v1 assets.
- Health behavior avoids collapse trap and aligns with lock constraints.

### Story 4.2: Standardize RUL unit
**Acceptance criteria**
- RUL is represented and tested in days.
- Conversion assumptions are explicit and consistent.

## Epic 5 — Götze IIS decision engine
### Story 5.1: Deterministic IIS scoring
**Acceptance criteria**
- IIS computation is deterministic and testable.
- Safety veto remains enforced independently of ranking.

### Story 5.2: Profile-driven ranking shift
**Acceptance criteria**
- Switching profile changes scores and can reorder recommendations.
- Profile identity is visible in decision artifacts.

## Epic 6 — Six-agent SOP orchestrator
### Story 6.1: Bounded six-agent chain
**Acceptance criteria**
- Orchestrator path includes all six bounded agents.
- Stage outputs follow contracts and are logged.

### Story 6.2: Deterministic core with narrative fallback
**Acceptance criteria**
- Numeric decisions do not depend on LLM calls.
- Narrative/explanations have fallback path.

## Epic 7 — Governance, audit, lineage
### Story 7.1: Approval gate + work order linkage
**Acceptance criteria**
- No maintenance action is recorded without human approval.
- Approved decision maps to a `WorkOrder` artifact.

### Story 7.2: Hash-chain and lineage visibility
**Acceptance criteria**
- Audit entries are append-only and chain-linked.
- Lineage from signal to action is queryable.

## Epic 8 — Dashboard demo
### Story 8.1: Hero closed-loop visualization
**Acceptance criteria**
- Dashboard shows hero `PUMP-001` path from health to one-best-action.
- Approval action and work-order outcome are visible.

### Story 8.2: Profile swap demonstration
**Acceptance criteria**
- UI exposes profile swap and resulting ranking change.
- Swap can be shown live in rehearsal.

## Epic 9 — Plant intake accelerator
### Story 9.1: Assisted manifest drafting
**Acceptance criteria**
- Intake assistant can draft manifest candidate with required sections.
- Draft is explicitly marked non-runtime until approval.

### Story 9.2: Manifest approval workflow
**Acceptance criteria**
- Validation and human approval step are mandatory before runtime use.
- Approved manifest is versioned for traceability.

## Epic 10 — Demo/package/deployment validation
### Story 10.1: Packaging baseline
**Acceptance criteria**
- `pyproject.toml` exists with minimal setuptools configuration.
- Repository supports editable install for CI.

### Story 10.2: Validation pipeline readiness
**Acceptance criteria**
- CI executes `python -m pytest` successfully in standard path.
- Any known dependency blockers are documented rather than hidden.
