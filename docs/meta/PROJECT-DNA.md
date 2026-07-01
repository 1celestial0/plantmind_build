# PROJECT-DNA.md — PlantMind × Götze Engine
> **THE CONSTITUTION. Apex source of truth.** Every session, every AI (Claude/Grok/Gemini), every teammate reads this FIRST and treats it as final.
> **Precedence:** PROJECT-DNA (L0) ▸ LOCKED_STATE (L1) ▸ derived docs (L2) ▸ execution state (L3). If any other document disagrees with this one, **the other document is wrong** until a dated Amendment (§10) changes the DNA.
> **Change rule:** §2 Identity and §3 Scope Fence change ONLY via a numbered Amendment with date + reason. No relitigation without an Amendment.
>
> **Version:** v1.0 · **Status:** ✅ LOCKED · **Date:** 2026-07-01 · **Owner:** Sourav Dutta (LTTS)
> Ratified 2026-07-01. §2 Identity, §3 Scope Fence, §6 Feature Inventory (15), §7 Rubric are LOCKED. Change only via a numbered Amendment (§10).

---

## 1. Document Hierarchy & Precedence (the anti-loop rule)
```
L0  PROJECT-DNA.md      Constitution: identity, pillars, scope fence, taxonomy,
                        feature template, rubric.  ← YOU ARE HERE. Apex truth.
L1  LOCKED_STATE.md     Technical vault: contracts, λ/β, thresholds, lane ownership.
                        Conforms to L0. Changes via 🔒 VAULT UPDATE.
L2  Derived renderings  Project Spec · Pitch Deck · UI Spec · Databricks Guide.
                        AUDIENCE VIEWS of the DNA. NEVER a source of truth.
                        Each carries: "Derived from PROJECT-DNA v1.0 — not authoritative."
L3  Execution state     ROADMAP · Chat Context vX.Y · lane prompts. Day-to-day.
```
**Operating principle:** stop reconciling documents. Conform to the DNA, or file an Amendment. That is the whole cure for the revisiting loop.

---

## 2. Identity (IMMUTABLE — amend only)
- **What it is:** A config-driven, physics-informed, agentic **decision fabric** for asset-intensive industries. It turns existing plant data into trusted, ranked, human-approved, audited engineering actions.
- **What it is NOT:** Not a digital twin, not an alerting/PdM tool, not a generic agent builder — it is the *governed decision-and-action layer* that sits on top of them and closes the loop.
- **Who it's for:** **Users** — Plant Reliability Engineers / Ops Leads (primary), Maintenance Planners, Plant Leadership. **Economic buyer** — plant owner via LTTS's "Intelligent Operations" upsell; **LTTS owns the Layer-0 framework as licensable CoE IP** (the real business).
- **Why it exists:** Regulated, high-stakes plants drown in alerts and tribal knowledge but lack a *governed, auditable* way to turn data into ranked, feasible actions — and every new plant today needs custom integration. PlantMind closes that gap.
- **Positioning (locked sentence):** *"PlantMind is the config-driven decision fabric that turns existing plant data and digital twins into trusted, physics-grounded, auditable engineering actions — at scale, across any asset class, without rip-and-replace."*
- **TWO CO-EQUAL PILLARS (locked 2026-07-01, C1):**
  - **P1 — Closed decision loop:** physics health → IIS → one approved, audited action. *(Trust/governance wedge.)*
  - **P2 — Config-driven modularity:** a declarative Plant Config Manifest composes the whole stack; new plant/asset/use-case = config, not code. *(Scale/CoE/productization wedge.)*
  - **Demo attention-order (co-equal in weight, sequenced in the telling):** SHOW P1 as the hero (the Götze "one best action" moment) → REVEAL P2 right after ("…and onboarding the next plant is just config").
- **The one thing a judge must remember:** the **Götze one-best-action moment** — data becomes a single, defensible, approved action.
- **Win condition:** a rehearsed demo of the one-best-action moment + honest $-impact + Databricks tie-in. Not unbuilt physics.

---

## 3. Scope Fence (the un-reopenable list)
**IN (must exist for the demo):** 5+1 agents · analytical Weibull health+RUL · IIS scoring (fixed weights) + Groq narrative · config-driven pipeline for ≥1 asset class · Config Viewer + live IIS-profile swap · human approval gate · append-only audit + hash chain + lineage · synthetic data + degradation injector · Databricks medallion (as narrative/credibility layer).

**Demo shape (PINNED):** **3 assets** on stage; **hero = PUMP-001** (centrifugal pump, `gradual_wear`); 30-asset fleet visible behind it. **Headline $-impact = ~$180k downtime saved per prevented pump failure** (1 incident, from the locked ROI table — confirm exact figure with Lane 5). One profile swap shown: reliability_first → energy_optimization.

**OUT (do not build; narrate as production if asked):** autonomous execution (always human-approved) · real live OT connectors to PI/OPC/MQTT (adapters narrated) · multi-tenant low-code manifest UI · self-calibrating IIS weights · rip-and-replace of any historian/EAM.

**CLOSED DECISIONS (settled 2026-07-01 — reopening requires an Amendment):**
| # | Question | Locked answer |
|---|---|---|
| C1 | Headline innovation | Two co-equal pillars (P1 + P2) |
| C2 | 6th agent | **MaintenanceScheduler** (approved → work order). SafetyGuardian rejected — veto lives in IIS. |
| C3 | UI theme | **Light** high-trust palette (#FAFAFA/#003366/#FF6B00). Supersedes the dark dashboard. |
| C4 | Manifest build scope | **Full** config-driven pipeline, with **Hour-16 freeze → static-path fallback**. |
| C5 | Physics model | Weibull analytical baseline ships always; **PINN is STRETCH only**, frozen Hour 14. |
| C6 | IIS weights in demo | Fixed; self-calibration is production narrative only. |
| C7 | Data | **Synthetic, physics-seeded from CMAPSS/PRONOSTIA — by design, not a limitation.** Rehearsed answer, not an apology. |
| C8 | Demo shape | 3 assets · hero PUMP-001 gradual_wear · headline ~$180k/incident · one profile swap. (See Demo shape above.) |
| C9 | Live-demo platform | **Local (Streamlit+SQLite) is the guaranteed spine.** Databricks live path built in parallel; **promote to stage ONLY if stable by Hour 20**, else Databricks stays the narrative/lineage/screenshot layer. Cloud/trial is never a hard demo dependency. |
| C10 | LLM live-failure | **Pre-cached Götze narrative** if Groq is unavailable live. IIS score is deterministic; only the prose needs the LLM. |

**STRETCH (only if core is green):** PINN · editable manifest · Impact/ROI analytics screen · Request-Second-Opinion · Databricks Model Serving endpoint · live-on-Databricks stage demo (C9 upside).

**FALLBACK (must always run):** local static/hardcoded path for the 3 demo assets · pre-cached Götze narrative (C10) · v1 FORGE demo until `src/dashboard/` is wired.

**Freeze Schedule (stop gambling on time):**
| Hour | Freeze |
|---|---|
| H-14 | PINN — drop if not validating (C5) |
| H-16 | Config pipeline — fall back to static path if unstable (C4) |
| H-20 | Feature freeze + decide C9 (local vs Databricks live) |
| post-H20 | Rehearsal only — no new features |

---

## 4. Categorization / Taxonomy (how every piece is filed)
- **Pillars:** P1 closed-loop · P2 config-driven.
- **Architecture layers:** L0 Framework (portable contracts) · L1 Databricks reference impl. *(See LOCKED_STATE §9.)*
- **Agents (6):** DataSentinel · AssetHealthOracle · GötzeEngine⭐ · RootCauseAnalyst · ExecutiveSummarizer · MaintenanceScheduler⭐.
- **Use-case profiles (IIS):** reliability_first(default) · energy_optimization · quality_driven · sustainability_max → map 1:1 to the 5 Databricks joint areas. *(LOCKED_STATE §2a.)*
- **Personas:** Reliability Engineer · Maintenance Planner · Plant Leadership · LTTS CoE.
- **Lanes:** L1 Backend/Agents · L2 Physics/ML · L3 UI · L4 Databricks · L5 Demo/Pitch. *(LOCKED_STATE §8.)*
- **Rubric dimensions:** 8 (see §7).

---

## 5. Feature Definition Template (use for EVERY feature, always)
```
### F-XX  <Feature name>
- Category:  <pillar / layer / agent / profile — from §4>
- WHAT:      one-line definition  +  Scope: [IN] … [OUT] …
- WHO:       persona served  |  Lane owner
- HOW:       mechanism / contract ref / dependencies
- WHY:       problem solved  →  scores on Rubric dim #<n>
- STATUS:    LOCKED | BUILDING | STRETCH | FALLBACK
- PROOF:     the demo-able artifact that shows it works
```

---

## 6. Feature Inventory (15 features — the source for Spec, Scorecard & PPT)
> Every downstream doc renders FROM this section. Status enum: LOCKED | BUILDING | STRETCH | FALLBACK.

### F-01  Götze Decision Panel
- Category: P1 closed-loop · agent: GötzeEngine
- WHAT: surfaces the single best intervention with IIS score, plain-English reason, runner-up + score gap, citations. Scope: [IN] one-best-action panel; [OUT] auto-execute.
- WHO: Reliability Engineer | Lane L1 (logic) + L3 (panel)
- HOW: IIS multi-criteria scorer + Groq Llama 3.3 70B narrative; consumes AssetHealthReport + CausalChain; emits `GötzeDecision` (LOCKED_STATE §4).
- WHY: turns alerts into one defensible action → Rubric #1, #6.
- STATUS: BUILDING
- PROOF: select degraded asset → panel renders top action + gap + Approve/Reject.

### F-02  Plant Config Manifest + Config Viewer
- Category: P2 config-driven · layer L0
- WHAT: declarative YAML that composes the stack; UI viewer with live IIS-profile swap. Scope: [IN] ≥1 asset class real + 1 profile swap; [OUT] low-code editor, multi-tenant.
- WHO: LTTS CoE / Reliability Engineer | Lane L1 + L3
- HOW: manifest schema in `src/contracts/`; loader composes ingest→features→health→IIS; **must carry LOCKED_STATE §6a λ/β** (not Grok example values).
- WHY: "new plant = config" → Rubric #1, #5; the scale story.
- STATUS: BUILDING (⚠️ highest-risk; Hour-16 fallback per C4)
- PROOF: Config Viewer shows manifest driving the pipeline; swap reliability→energy reorders the recommendation.

### F-03  MaintenanceScheduler
- Category: P1 closed-loop · agent (6th)
- WHAT: on approval, turns the Götze action into a work order. Scope: [IN] work-order record + audit entry; [OUT] live SAP/Maximo write (narrated).
- WHO: Maintenance Planner | Lane L1
- HOW: fires post-approval only; emits WorkOrder model (add to `src/contracts/`); appends to audit.
- WHY: closes loop into business systems → Rubric #3, #6.
- STATUS: BUILDING
- PROOF: Approve → work order appears in queue + audit log.

### F-04  DataSentinel
- Category: P1 closed-loop · agent
- WHAT: flags abnormal sensor behavior as typed anomaly + severity. Scope: [IN] Z-score + Mahalanobis flags; [OUT] root-cause (F-06), auto-action.
- WHO: Reliability Engineer | Lane L1
- HOW: Z-score + Mahalanobis over `sensor_window`; emits `DataQualityReport`; first node in orchestrator (F-15).
- WHY: turns raw telemetry into a typed signal → Rubric #2, #6.
- STATUS: BUILDING
- PROOF: inject anomaly → DataQualityReport shows typed flag + severity.

### F-05  AssetHealthOracle
- Category: P1 · agent · physics (L2)
- WHAT: health 0–100 + RUL (days) + 95% CI + physics explanation. Scope: [IN] analytical Weibull baseline; [OUT] PINN (STRETCH, C5).
- WHO: Reliability Engineer | Lane L2
- HOW: H(t)=100·exp(−λ·S·t^β) with Arrhenius/load stress (LOCKED_STATE §6a); emits `AssetHealthReport`. **Must use §6a λ/β; RUL = DAYS.**
- WHY: physics-grounded health, not a black box → Rubric #1, #2, #6.
- STATUS: BUILDING
- PROOF: health curve degrades realistically (no cycle-30 collapse); RUL + CI render.

### F-06  RootCauseAnalyst
- Category: P1 · agent
- WHAT: cited causal chain from manuals/SOPs/fault logs. Scope: [IN] RAG over 10–20 docs + similar past faults; [OUT] doc authoring.
- WHO: Reliability Engineer | Lane L1
- HOW: ChromaDB + sentence-transformers (local) → Databricks Vector Search (L1); emits `CausalChain` (steps + citations).
- WHY: explainability — every recommendation has a sourced "why" → Rubric #1, #6.
- STATUS: BUILDING
- PROOF: Decision panel "Why?" expands to manual-page + fault-log citations.

### F-07  ExecutiveSummarizer
- Category: P1 · agent
- WHAT: 3-bullet leadership brief + rough $-impact. Scope: [IN] aggregation + small LLM; [OUT] full BI dashboards.
- WHO: Plant Leadership | Lane L1
- HOW: Llama 3.2 3B (Groq) over state; emits `ExecutiveBrief` (critical_alerts, gotze_pending, downtime_saved_estimate).
- WHY: leadership-readable ROI → Rubric #3.
- STATUS: BUILDING
- PROOF: brief renders 3 bullets + the pinned $180k figure (C8).

### F-08  IIS Scoring Engine & Weight Profiles
- Category: P1+P2 · core logic
- WHAT: multi-criteria scorer ranking every intervention; swappable profiles. Scope: [IN] 5-term formula, fixed weights, 4 profiles; [OUT] self-calibration (C6).
- WHO: Reliability Engineer / LTTS CoE | Lane L1
- HOW: IIS formula (LOCKED_STATE §2) with profile weights (§2a); SafetyRiskDelta ceiling = hard veto; powers F-01 + the F-02 swap.
- WHY: explicit trade-offs + per-business modularity → Rubric #1, #5.
- STATUS: BUILDING
- PROOF: same asset, swap profile → recommendation reorders, weights visible.

### F-09  Governance: Audit, Hash-Chain & Lineage
- Category: P1 · governance · layer
- WHAT: immutable append-only audit, tamper-evident hash chain, full lineage + Audit Explorer screen. Scope: [IN] SQLite append-only + hash chain + lineage view; [OUT] external SIEM.
- WHO: Reliability Engineer / Auditor | Lane L1 + L3
- HOW: `AuditRecord` per stage (LOCKED_STATE §4); integrity check; lineage Sensor→Health→IIS→Cause→Approval; Unity Catalog + Delta time-travel in L1.
- WHY: regulated-industry defensibility → Rubric #6 (your strength).
- STATUS: BUILDING — *verify it runs; if so bump §7 #6 to 4.5.*
- PROOF: Audit Explorer shows chain "valid"; click row → full decision state.

### F-10  Two-Layer Interface Contracts (Layer 0 IP)
- Category: P2 · layer · the licensable asset
- WHAT: vendor-agnostic Pydantic interface contracts the manifest composes against. Scope: [IN] 7 interfaces + shared models in `src/contracts/`; [OUT] every vendor adapter impl.
- WHO: LTTS CoE / all lanes | Lane L1
- HOW: Ingestor/FeatureStore/PhysicsModel/InterventionScorer/KnowledgeRetriever/Governance/Orchestrator interfaces (LOCKED_STATE §9) + `PlantMindState, GötzeDecision, AssetHealthReport, ExecutiveBrief, AuditRecord, WorkOrder, Manifest`.
- WHY: the portable licensable IP; the API between all 5 lanes → Rubric #1, #5.
- STATUS: BUILDING — **HIGHEST-PRIORITY LOCK (blocks all code + all docs).**
- PROOF: Manifest + WorkOrder models validate; every lane imports from `src/contracts/`.

### F-11  Synthetic Data + Degradation Injector
- Category: P1/P2 · data
- WHAT: physics-seeded synthetic fleet + live degradation injection for the demo. Scope: [IN] 30 assets, 3 failure modes, controllable injection; [OUT] real customer data (C7).
- WHO: Demo driver | Lane L2 / L5
- HOW: generator seeded from CMAPSS/PRONOSTIA λ/β (§6a); injector drives hero-asset health drop live.
- WHY: deterministic, repeatable demo + honest data story → Rubric #3, #7.
- STATUS: BUILDING
- PROOF: trigger injection → PUMP-001 health drops → Götze fires.

### F-12  Databricks Medallion Reference Impl (Layer 1)
- Category: P2 · layer L1 · credibility
- WHAT: Bronze/Silver/Gold on Databricks as the production/scale narrative. Scope: [IN] medallion + Unity Catalog lineage + Vector Search; [OUT] hard live-demo dependency (C9 — local is the spine).
- WHO: Judges (credibility) / LTTS | Lane L4
- HOW: Auto Loader→DLT→Gold; Feature Store; MLflow; Mosaic AI; SAME Layer-0 contracts (F-10).
- WHY: partnership alignment + scale proof → Rubric #5, #8.
- STATUS: BUILDING (parallel; promote to stage only if stable H-20, C9).
- PROOF: Unity Catalog lineage Bronze→Gold decision shown (live or screenshots).

### F-13  Plant Overview Dashboard
- Category: P1 · UI screen
- WHAT: at-a-glance fleet health + Götze queue. Scope: [IN] KPI cards, health grid, Götze queue, filters; [OUT] custom report builder.
- WHO: Reliability Engineer | Lane L3
- HOW: Streamlit + Plotly, **light palette (C3)**; cards red/amber/green; health<40 / RUL<14 triggers; click → F-14.
- WHY: progressive-disclosure entry point → Rubric #7.
- STATUS: BUILDING — **needs dark→light reskin (C3).**
- PROOF: grid loads, hero asset shows red trigger, click opens detail.

### F-14  Asset Detail Hero Screen
- Category: P1 · UI screen
- WHAT: split view — left asset intelligence, right Götze panel (F-01). Scope: [IN] health gauge, RUL+CI, physics text, sensor trends, stress factors; [OUT] raw-tag config (that's F-02).
- WHO: Reliability Engineer | Lane L3
- HOW: Streamlit + Plotly gauge + multi-line trends; light palette; right 45% = F-01 panel.
- WHY: the stage for the hero moment → Rubric #7.
- STATUS: BUILDING (reskin).
- PROOF: select PUMP-001 → gauge + trends + Götze panel all render.

### F-15  Orchestrator State Machine
- Category: P1+P2 · backbone
- WHAT: directed state machine routing the 6 agents + attaching audit, with graceful degradation. Scope: [IN] LangGraph/CrewAI sequence + per-agent error handling; [OUT] dynamic agent discovery.
- WHO: all | Lane L1
- HOW: enriches `PlantMindState` through DataSentinel→Oracle→Götze→RootCause→ExecSummarizer→(approval)→MaintenanceScheduler; logs each stage (F-09); manifest selects behaviors (F-02).
- WHY: "demo never dies" — one agent fails, panel still renders → Rubric #2, #7.
- STATUS: BUILDING
- PROOF: kill one agent mid-run → orchestrator logs + continues; panel still renders.

---

## 7. Hard Rubric & Current Score (the improvement scoreboard)
Re-score at every session close. Maturity 1–5; readiness = Σ(weight × maturity/5).
**Weights tuned for LTTS/Databricks-partnership judges** (business + scale + partnership-fit outweigh raw novelty).
**Target ≥90% by Jul 8. RED-LINE: cut scope on any dimension still <3.0 by Jul 7.**

| # | Dimension | Weight | Maturity | Weighted | Judge's killer question | Gap → action |
|---|---|---|---|---|---|---|
| 1 | Innovation / novelty | 15 | 4.0 | 12.0 | "How is this not just a digital twin / agent wrapper?" | Nail "what it is NOT" + two-pillar line |
| 2 | Technical depth & feasibility | 12 | 3.0 | 7.2 | "Show the config actually composing the pipeline, live." | ⚠️ Config pipeline unproven (F-02) |
| 3 | Business impact / ROI | 18 | 4.0 | 14.4 | "Defend the $180k — line by line." | Keep $-impact honest + sourced |
| 4 | Fit to existing data / zero rip-replace | 10 | 3.0 | 6.0 | "Show it working with MY historian's tag names." | Demo 1 adapter + semantic map |
| 5 | Scalability / modularity | 13 | 3.5 | 9.1 | "Onboard a new asset class right now, no code." | Prove via live profile swap |
| 6 | Governance / trust / explainability | 10 | 3.5 | 7.0 | "Prove this decision wasn't tampered with." | Verify hash-chain + lineage actually run |
| 7 | Demo quality / storytelling | 10 | 2.5 | 5.0 | "Run the whole thing end-to-end, no cuts." | ⚠️ Rehearse; finish light reskin |
| 8 | Databricks / partnership alignment | 12 | 4.0 | 9.6 | "Why does this need Databricks specifically?" | Strong — 5 areas → IIS profiles |
| | **TOTAL READINESS** | **100** | | **70.3%** | | Gaps cluster in **#7 demo, #2 feasibility, #4 data-fit** |

---

## 8. Change-Control Ritual (so the loop never returns)
1. **DNA-first:** no feature is built without a §5 entry + STATUS.
2. **Conform-or-amend:** a derived doc/PDF that conflicts with the DNA is wrong until an Amendment (§10) updates the DNA.
3. **Immutables are gated:** changing §2 Identity or §3 Scope Fence requires a numbered Amendment (date + reason).
4. **Re-score at session close:** update §7; that single number tells you where you stand.
5. **Technical detail goes to L1:** λ/β, contracts, thresholds live in LOCKED_STATE, not here.
6. **Keep both Obsidian vaults current (derived, never authoritative):** on every Amendment / VAULT UPDATE / session close, refresh `knowledge/obsidian-vault/` (source-of-truth mirror) and `knowledge/code-lineage-vault/` (code map, re-scan `src/**`). If a vault disagrees with DNA/LOCKED_STATE, the canonical file wins.

---

## 9. Pointers
- **Technical vault (L1):** `LOCKED_STATE.md` (§2a IIS profiles, §6a physics λ/β, §9 config architecture, §10 UI).
- **Living vaults (L2, derived — keep current per §8.6):** `knowledge/obsidian-vault/_Index.md` (source-of-truth mirror) · `knowledge/code-lineage-vault/_Index.md` (code map).
- **Derived renderings (banner-tag each):** `PlantMind_Project_Specification_*.pdf` · `PlantMind_UI_UX_Design_Specification_*.pdf` · `PlantMind_Databricks_Implementation_Guide_*.pdf` · Pitch Deck (tbd) · the to-be-generated Industry Spec / Scorecard / PPT.
- **Archived (historical, NOT truth):** `/archive/2026-07-01_v2-consolidation/` — v1 vault, legacy, staging dups, competing DNA/Master-Spec/architecture. See its `ARCHIVE-README.md`.
- **Retire/merge:** "Project Understanding" → folded into §2.

---

## 10. Amendment Log
```
2026-07-01 | v1.0-DRAFT created. Identity + two pillars + scope fence + taxonomy + rubric baseline + 3 exemplar features. | break the revisiting loop; establish apex precedence
2026-07-01 | v1.0 LOCKED (ratified). §2 sharpened (what-it-is-NOT, buyer, demo-order); §3 hardened (demo shape pinned, C7–C10, freeze schedule); §6 completed (15 features); §7 reweighted to business/scale + harsher honest scores (70.3%) + killer-question column. | final ratification; downstream docs may now be generated
```
> Append one line per amendment. Format: YYYY-MM-DD | vX.Y | what changed | why.
