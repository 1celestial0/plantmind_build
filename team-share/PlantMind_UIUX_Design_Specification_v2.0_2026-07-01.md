# PlantMind — UI/UX Design Specification v2.0
_Generated 2026-07-01 · **DERIVED from `PROJECT-DNA.md` §10 (LOCKED).** Supersedes the June Grok UI PDF (which showed a dark theme / 5 agents)._

## Design philosophy
High-trust, calm, professional industrial interface — **"SCADA meets Notion."** Light, not flashy. Every screen communicates clarity, physics grounding, and human control. The interface exists to make the GötzeEngine's "one best action" moment feel inevitable and trustworthy. No black boxes.

## Personas & primary journey
- **Reliability Engineer / Ops Lead** (primary) · **Maintenance Planner** · **Plant Leadership** (occasional).
- **Journey:** Plant Overview (health cards) → spot critical asset (health<40 / RUL<14) → Asset Detail → Götze Decision Panel appears → review ranked interventions + reason + citations → **Approve & Create Work Order** (→ MaintenanceScheduler) or Reject → decision logged with lineage.

## Information architecture — 6-section nav (persistent sidebar)
Plant Overview · Assets · Decisions · **Config** (manifest viewer + IIS-profile swap = innovation showcase) · Audit & Lineage · Impact (stretch).

## Key screens
1. **Plant Overview** — 4 KPI cards (total / critical / warning / pending Götze), asset health grid (color-coded cards: health %, RUL days, Götze trigger badge), Götze queue sidebar. Click card → Asset Detail.
2. **Asset Detail (hero)** — split view. *Left 55%:* health gauge (0–100) + trend arrow, RUL days + 95% CI, physics explanation, sensor trends, stress factors. *Right 45%:* **Götze Decision Panel** — top recommendation (IIS bar + plain-English reason + key drivers), runner-up + score gap, expandable citations, **[Approve & Create Work Order] / [Approve w/ comment] / [Reject + reason]**. "Human Approval Required" always visible.
3. **Decisions & Audit Explorer** — filterable table (Approved/Rejected/Pending), row → full audit record + lineage graph (Sensor→Health→IIS→Cause→Approval) + hash-chain "valid" indicator + export.
4. **Config Viewer** — read-only manifest (asset hierarchy, tag mapping, physics params, intervention library, IIS profile, governance) + **live "switch IIS profile" toggle** (reliability_first → energy_optimization reorders the recommendation). This is the modularity showcase.

## Visual system (LIGHT — locked DNA §10)
- **Palette:** background off-white `#FAFAFA`; primary deep navy `#003366`; accent/CTA + critical `#FF6B00`; health green `#2E7D32` / amber `#F9A825` / red `#C62828`; text `#212121`.
- **Type:** Inter / system sans; tabular figures / mono for precision numbers.
- **Patterns:** every number has context; visible reasoning path (physics→history→citations); calm loading/error states; color never the only signal (icon + text).

## Interaction & accessibility
Progressive disclosure (overview → depth); immediate feedback on approve (audit entry appears live); full keyboard nav; desktop-first (control room), tablet for supervisors, mobile view-only. WCAG 2.1 AA (contrast, focus states, ARIA).

## Tech stack
Hackathon: **Streamlit + Plotly** (light theme via `styles.py` — reskin from the current dark build). Production: React + TS + Tailwind + shadcn/ui.

## Build deltas from current code (L3 lane)
- Reskin `src/dashboard/styles.py` dark → light.
- Add **Config Viewer** page + IIS-profile toggle (new).
- Add **Audit & Lineage** explorer (hash-chain indicator).
- Wire **Approve & Create Work Order** → MaintenanceScheduler (F-03).

— Derived from PROJECT-DNA v1.0 · 2026-07-01 —
