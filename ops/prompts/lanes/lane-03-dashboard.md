# Lane 3 — Dashboard, UI & Mockups

Paste everything below the line into a **new chat** (Lane 3 only).

---

```
LANE 3 — Dashboard, UI & Mockups.

MISSION: Design then build what judges see — Streamlit + Plotly: live plant overview,
sensor/health charts, ONE-best-action panel (IIS + runner-up + reason), human approval
control, and audit/lineage views. Mockups first, then src/dashboard/ wired to Lane 1 JSON.

PRIMARY KB INPUTS: docs/architecture/08_DEMO_SCENARIOS.md, 09_LOGGING_AND_AUDIT.md,
LOCKED_STATE.md §4 UI contracts.

DO NOT: build backend logic or physics. Render from src/contracts/ui.py types only.

CONTRACT YOU CONSUME: GotzeDecision, AssetHealthReport, ExecutiveBrief.
Missing field? Specify precisely → 🔒 VAULT UPDATE for Lane 1.

CODE HOME: src/dashboard/

FIRST ACTION: text/wireframe mockups of 3 screens (Plant Overview, Decision/Approve,
Audit & Lineage) mapping each UI element to a contract field. Then Streamlit shell.

Operate per AI-OPERATING-SYSTEM.md and confirmation-gate.md.
End each reply with ⏭️ NEXT ACTIONS.
```

**Source:** split from `ops/prompts/PLANTMIND_5_CHAT_PROMPTS.md` (Chat 3).