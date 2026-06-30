"""Generate PlantMind Project Specification PDF (20-30 pages) for team-share."""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "team-share"
MOCKUP_DIR = OUT_DIR / "mockups"
SESSION_IMAGES = Path(
    r"C:\Users\hp\.grok\sessions"
    r"\C%3A%5CUsers%5Chp%5CClaude%5CProjects%5CPlantMind%5CPlantMind_live"
    r"\019f1ae3-9d75-7972-bf82-134eca042caf\images"
)
OUT_PDF = OUT_DIR / "PlantMind_Project_Specification_v3.0_2026-07-01.pdf"

NAVY = (0, 51, 102)
ORANGE = (255, 107, 0)
GRAY = (80, 80, 80)
LIGHT = (245, 247, 250)

REPLACEMENTS = {
    "\u2014": "-",
    "\u2013": "-",
    "\u2192": "->",
    "\u00b7": "-",
    "\u0394": "d",
    "\u00f6": "o",
    "\u00d6": "O",
    "\u2265": ">=",
    "\u26a0": "[!]",
    "\u2b50": "*",
}


def ascii_safe(text: str) -> str:
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    return text.encode("ascii", "replace").decode("ascii")


def copy_mockups() -> dict[str, Path]:
    mapping = {
        "plant-overview.jpg": "1.jpg",
        "config-viewer.jpg": "2.jpg",
        "asset-detail-gotze.jpg": "3.jpg",
        "audit-lineage.jpg": "4.jpg",
        "architecture.jpg": "5.jpg",
    }
    MOCKUP_DIR.mkdir(parents=True, exist_ok=True)
    copied: dict[str, Path] = {}
    for dest_name, src_name in mapping.items():
        dest = MOCKUP_DIR / dest_name
        src = SESSION_IMAGES / src_name
        if src.exists():
            shutil.copy2(src, dest)
            copied[dest_name] = dest
    return copied


class SpecPDF(FPDF):
    CONTENT_W = 190
    LEFT_M = 10

    def _reset_x(self) -> None:
        self.set_x(self.LEFT_M)

    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 8, "PlantMind Project Specification v3.0 | DERIVED from PROJECT-DNA v1.0", align="C")
        self.ln(10)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def cover(self) -> None:
        self.add_page()
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 297, style="F")
        self.set_y(70)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(255, 255, 255)
        self.multi_cell(0, 14, "PlantMind x Gotze Engine", align="C")
        self.ln(6)
        self.set_font("Helvetica", "", 16)
        self.multi_cell(
            0,
            10,
            "Detailed Project Specification\nwith Implementation Scenarios & UI Mockups",
            align="C",
        )
        self.ln(12)
        self.set_font("Helvetica", "I", 11)
        self.multi_cell(
            0,
            8,
            "DERIVED from PROJECT-DNA.md v1.0 (LOCKED) + LOCKED_STATE.md\n"
            "LTTS Global Engineering Intelligence Hackathon | 2026-07-09",
            align="C",
        )
        self.ln(20)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 8, f"Version 3.0 | Generated {date.today().isoformat()}", align="C")

    def section_title(self, num: str, title: str) -> None:
        self.add_page()
        self.set_fill_color(*LIGHT)
        self.rect(10, self.get_y(), 190, 14, style="F")
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*NAVY)
        self.cell(0, 14, ascii_safe(f"{num}. {title}"), ln=True)
        self.ln(4)

    def h2(self, text: str) -> None:
        self._reset_x()
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*NAVY)
        self.multi_cell(self.CONTENT_W, 7, ascii_safe(text))
        self.ln(2)

    def body(self, text: str) -> None:
        self._reset_x()
        self.set_font("Helvetica", "", 10)
        self.set_text_color(33, 33, 33)
        self.multi_cell(self.CONTENT_W, 5.5, ascii_safe(text))
        self.ln(2)

    def bullet_list(self, items: list[str]) -> None:
        self.set_font("Helvetica", "", 10)
        self.set_text_color(33, 33, 33)
        for item in items:
            self._reset_x()
            self.multi_cell(self.CONTENT_W, 5.5, ascii_safe(f"  - {item}"))
        self.ln(2)

    def table(self, headers: list[str], rows: list[list[str]], col_widths: list[int]) -> None:
        self._reset_x()
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(*NAVY)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 8, h, border=1, align="C", fill=True)
        self.ln()
        self.set_font("Helvetica", "", 8)
        self.set_text_color(33, 33, 33)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(*LIGHT)
            else:
                self.set_fill_color(255, 255, 255)
            max_h = 8
            for i, cell in enumerate(row):
                self.cell(col_widths[i], max_h, ascii_safe(cell), border=1, fill=True)
            self.ln()
            fill = not fill
        self.ln(3)

    def mockup(self, path: Path, caption: str) -> None:
        if not path.exists():
            self.body(f"[Mockup unavailable: {path.name}]")
            return
        usable_w = 180
        self.image(str(path), x=15, w=usable_w)
        self._reset_x()
        self.ln(2)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*GRAY)
        self.multi_cell(self.CONTENT_W, 5, ascii_safe(caption))
        self.ln(4)

    def scenario_box(self, title: str, context: str, flow: list[str], outcome: str) -> None:
        if self.get_y() > 250:
            self.add_page()
        y = self.get_y()
        self.set_fill_color(*ORANGE)
        self.rect(12, y, 186, 4, style="F")
        self.ln(6)
        self._reset_x()
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*NAVY)
        self.multi_cell(self.CONTENT_W, 6, ascii_safe(title))
        self.body(context)
        self.h2("Flow")
        self.bullet_list(flow)
        self.h2("Outcome")
        self.body(outcome)
        self.ln(2)


def build_pdf(mockups: dict[str, Path]) -> Path:
    pdf = SpecPDF()
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.cover()

    # TOC
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(*NAVY)
    pdf.cell(0, 12, "Table of Contents", ln=True)
    pdf.ln(4)
    toc = [
        "1. Executive Summary & Innovation Thesis",
        "2. Problem Statement & Market Context",
        "3. Two-Pillar Architecture (Layer 0 + Layer 1)",
        "4. Plant Config Manifest & Config-Driven Modularity",
        "5. Six-Agent Decision Pipeline",
        "6. GötzeEngine & IIS Scoring",
        "7. Physics, Health & RUL Model",
        "8. Governance, Audit & Human Approval",
        "9. UI/UX Specification & Visual Mockups",
        "10. Feature Inventory (F-01 to F-15)",
        "11. Real-Life Implementation Scenarios",
        "12. Databricks Production Path",
        "13. Hackathon Demo Plan & ROI",
        "14. Differentiation & Competitive Position",
        "15. Technical Stack & Contracts Appendix",
    ]
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(33, 33, 33)
    for line in toc:
        pdf.cell(0, 8, line, ln=True)

    # 1 Executive Summary
    pdf.section_title("1", "Executive Summary & Innovation Thesis")
    pdf.body(
        "PlantMind is a config-driven, physics-informed, agentic decision fabric for asset-intensive "
        "industries. It turns existing plant historian data, CMMS records, and digital-twin outputs into "
        "trusted, ranked, human-approved, audited engineering actions — without rip-and-replace of OT or IT systems."
    )
    pdf.h2("Two Co-Equal Innovation Pillars")
    pdf.bullet_list([
        "P1 — Closed decision loop: physics health -> IIS scoring -> one approved, audited action.",
        "P2 — Config-driven modularity: Plant Config Manifest composes the stack; new plant = config change.",
    ])
    pdf.body(
        "Positioning (LOCKED): PlantMind is the config-driven decision fabric that turns existing plant data "
        "and digital twins into trusted, physics-grounded, auditable engineering actions — at scale, across "
        "any asset class, without rip-and-replace."
    )
    pdf.h2("What PlantMind Is NOT")
    pdf.bullet_list([
        "Not a digital twin (it consumes twin outputs; it does not replace simulation).",
        "Not an alerting or PdM tool (it ranks interventions and closes the loop).",
        "Not a generic agent builder (physics + governance are first-class).",
    ])

    # 2 Problem
    pdf.section_title("2", "Problem Statement & Market Context")
    pdf.body(
        "Regulated, high-stakes plants drown in alerts and tribal knowledge. Historians, EAM/CMMS, and "
        "dashboards exist — but there is no governed way to turn heterogeneous signals into one defensible "
        "action with full lineage. Every new site still requires custom integration code."
    )
    pdf.table(
        ["Pain", "Current State", "PlantMind Response"],
        [
            ["Alert fatigue", "100+ daily alarms", "One IIS-ranked best action"],
            ["Tribal knowledge", "SOPs in binders", "RAG-cited causal chains"],
            ["Audit risk", "Spreadsheet decisions", "Hash-chained immutable log"],
            ["Scale", "Per-site custom code", "Manifest-driven onboarding"],
        ],
        [45, 55, 90],
    )

    # 3 Architecture
    pdf.section_title("3", "Two-Pillar Architecture (Layer 0 + Layer 1)")
    if "architecture.jpg" in mockups:
        pdf.mockup(mockups["architecture.jpg"], "Figure 3.1 — Two-Layer architecture and agent pipeline")
    pdf.h2("Layer 0 — Framework (Portable LTTS IP)")
    pdf.body(
        "Vendor-agnostic Pydantic contracts in src/contracts/. Interfaces: Ingestor, FeatureStore, "
        "PhysicsModel, InterventionScorer (GötzeEngine), KnowledgeRetriever, Governance, Orchestrator."
    )
    pdf.h2("Layer 1 — Databricks Reference Implementation")
    pdf.bullet_list([
        "Auto Loader + DLT: Bronze / Silver / Gold medallion",
        "Feature Store for engineered degradation signals",
        "MLflow + Mosaic AI for Götze IIS serving",
        "Unity Catalog + Vector Search for governance and RAG",
        "Workflows for scheduled health and decision refresh",
    ])
    pdf.body(
        "Hackathon realizes Layer 0 locally (Python, SQLite, ChromaDB, Streamlit) with identical contracts "
        "so judges see production parity without live OT connectors (C9)."
    )

    # 4 Manifest
    pdf.section_title("4", "Plant Config Manifest & Config-Driven Modularity")
    pdf.body(
        "A declarative YAML manifest (config/plants/*.yaml) is the single source of truth composing "
        "ingestion, features, health, IIS, governance, and dashboard behavior at runtime."
    )
    pdf.table(
        ["Section", "Purpose", "Example"],
        [
            ["plant_id", "Site identity", "hero_refinery_unit_3"],
            ["asset_hierarchy", "Assets & classes", "PUMP-001 centrifugal"],
            ["tag_mapping", "Semantic layer", "PI.VIB_01A -> vibration_rms"],
            ["physics_model", "Weibull params", "lambda=1.49e-6 beta=2.3"],
            ["intervention_library", "Candidate actions", "Replace seal, rebalance"],
            ["iis_profile", "Business weights", "reliability_first"],
            ["governance", "Approval rules", "human_required=true"],
        ],
        [42, 58, 90],
    )
    pdf.body(
        "CRITICAL: Manifest physics MUST use LOCKED_STATE section 6a lambda/beta — NOT the superseded "
        "Grok example (0.0023, 2.1) which collapses health by cycle 30."
    )

    # 5 Agents
    pdf.section_title("5", "Six-Agent Decision Pipeline")
    pdf.table(
        ["Agent", "Role", "Output"],
        [
            ["DataSentinel", "Sensor anomaly detection", "DataQualityReport"],
            ["AssetHealthOracle", "Weibull health + RUL", "AssetHealthReport"],
            ["GötzeEngine", "IIS rank interventions", "GötzeDecision"],
            ["RootCauseAnalyst", "RAG causal chain", "CausalChain"],
            ["ExecutiveSummarizer", "Leadership brief", "ExecutiveBrief"],
            ["MaintenanceScheduler", "Post-approval WO", "WorkOrder"],
        ],
        [48, 62, 80],
    )
    pdf.body(
        "Directed state machine with graceful degradation: if one agent fails, orchestrator logs and "
        "continues — the Götze panel still renders (demo never dies)."
    )

    # 6 IIS
    pdf.section_title("6", "GötzeEngine & IIS Scoring")
    pdf.body("IIS(i) = w1*dP_failure + w2*dDowntimeCost + w3*Feasibility + w4*HistoricalSuccess - w5*SafetyRiskDelta")
    pdf.body("All terms normalized [0,1]. SafetyRiskDelta above ceiling = hard veto. requires_human_approval always True.")
    pdf.table(
        ["Profile", "dP_fail", "dDt$", "Feas", "Hist", "-Safety", "Databricks Area"],
        [
            ["reliability_first", "0.35", "0.25", "0.20", "0.15", "0.05", "Predictive Reliability"],
            ["energy_optimization", "0.20", "0.35", "0.20", "0.15", "0.10", "Energy & Emissions"],
            ["quality_driven", "0.30", "0.20", "0.25", "0.20", "0.05", "Quality Intelligence"],
            ["sustainability_max", "0.20", "0.20", "0.20", "0.10", "0.30", "Sustainability"],
        ],
        [34, 20, 20, 20, 20, 20, 56],
    )

    # 7 Physics
    pdf.section_title("7", "Physics, Health & RUL Model")
    pdf.body("H(t) = 100 * exp(-lambda * S * t^beta), S = AF_temp * AF_load. RUL always in DAYS.")
    pdf.table(
        ["Asset Class", "lambda", "beta", "life_ref cycles"],
        [
            ["pump", "1.49e-6", "2.3", "420"],
            ["compressor", "1.83e-5", "1.9", "400"],
            ["motor", "5.98e-8", "2.8", "450"],
            ["bearing", "2.01e-9", "3.5", "350"],
            ["valve", "1.53e-4", "1.5", "480"],
        ],
        [45, 45, 35, 65],
    )
    pdf.body("Triggers: health < 40 OR rul_days < 14 OR DataSentinel critical. Weibull ships first; PINN is stretch only (freeze H-14).")

    # 8 Governance
    pdf.section_title("8", "Governance, Audit & Human Approval")
    pdf.bullet_list([
        "Append-only AuditRecord per pipeline stage with lineage chain.",
        "Hash chain integrity check (hackathon) / Unity Catalog time-travel (production).",
        "Human approval gate: Approve, Approve with comment, Reject with reason.",
        "MaintenanceScheduler fires ONLY after approval — never autonomous.",
        "Groq LLM narrative with pre-cached fallback (C10); IIS score is deterministic.",
    ])

    # 9 UI Mockups
    pdf.section_title("9", "UI/UX Specification & Visual Mockups")
    pdf.body(
        "Light high-trust palette: bg #FAFAFA, navy #003366, accent #FF6B00. "
        "Typography: Inter / tabular figures. Feel: SCADA meets Notion. WCAG 2.1 AA."
    )
    pdf.h2("9.1 Plant Overview")
    if "plant-overview.jpg" in mockups:
        pdf.mockup(mockups["plant-overview.jpg"], "Figure 9.1 — Plant Overview: KPI cards, health grid, Götze queue")
    pdf.h2("9.2 Asset Detail & Götze Decision Panel (Hero Screen)")
    if "asset-detail-gotze.jpg" in mockups:
        pdf.mockup(mockups["asset-detail-gotze.jpg"], "Figure 9.2 — Split view: asset intelligence + one-best-action panel")
    pdf.h2("9.3 Config Viewer & IIS Profile Swap")
    if "config-viewer.jpg" in mockups:
        pdf.mockup(mockups["config-viewer.jpg"], "Figure 9.3 — Manifest viewer with live profile swap (modularity demo)")
    pdf.h2("9.4 Audit & Lineage Explorer")
    if "audit-lineage.jpg" in mockups:
        pdf.mockup(mockups["audit-lineage.jpg"], "Figure 9.4 — Decision audit table with lineage graph and hash-chain valid")

    # 10 Features
    pdf.section_title("10", "Feature Inventory (F-01 to F-15)")
    features = [
        ("F-01", "Götze Decision Panel", "One-best-action UI with IIS bar and citations"),
        ("F-02", "Config Manifest + Viewer", "YAML composes pipeline; live profile swap"),
        ("F-03", "MaintenanceScheduler", "Approved action -> work order + audit"),
        ("F-04", "DataSentinel", "Z-score + Mahalanobis anomaly flags"),
        ("F-05", "AssetHealthOracle", "Weibull health, RUL days, CI, physics text"),
        ("F-06", "RootCauseAnalyst", "RAG over manuals/SOPs/fault logs"),
        ("F-07", "ExecutiveSummarizer", "3-bullet brief + downtime $ estimate"),
        ("F-08", "IIS Engine & Profiles", "Multi-criteria scorer + 4 profiles"),
        ("F-09", "Audit/Hash-Chain/Lineage", "Immutable governance record"),
        ("F-10", "Layer-0 Contracts", "Portable licensable IP — blocks all lanes"),
        ("F-11", "Synthetic Data + Injector", "Physics-seeded 30-asset fleet"),
        ("F-12", "Databricks Medallion", "Bronze/Silver/Gold reference path"),
        ("F-13", "Plant Overview", "Fleet health dashboard"),
        ("F-14", "Asset Detail Hero", "Split intelligence + Götze panel"),
        ("F-15", "Orchestrator", "6-agent state machine + graceful degradation"),
    ]
    pdf.table(["ID", "Feature", "Demo Proof"], [[a, b, c] for a, b, c in features], [18, 62, 110])

    # 11 Scenarios
    pdf.section_title("11", "Real-Life Implementation Scenarios")
    pdf.scenario_box(
        "Scenario 11.1 — Preventing PUMP-001 Failure ($180k ROI)",
        "Context: Gulf Coast refinery unit. PUMP-001 (centrifugal, gradual_wear) shows health 38%, "
        "RUL 11 days. Vibration trending up 18% over 72h. Maintenance window in 5 days.",
        [
            "DataSentinel flags vibration anomaly (severity: warning).",
            "AssetHealthOracle: health=38, rul_days=11, physics cites seal wear + load factor 1.12.",
            "GötzeEngine ranks: (1) Replace mechanical seal IIS=0.87, (2) Rebalance rotor IIS=0.71.",
            "RootCauseAnalyst cites OEM manual p.42 + 3 similar past faults.",
            "Reliability engineer reviews panel, approves seal replacement.",
            "MaintenanceScheduler creates WO-2026-0847, audit hash chain appended.",
        ],
        "Prevented unplanned shutdown (~$180k downtime). Full lineage exportable for audit.",
    )
    pdf.scenario_box(
        "Scenario 11.2 — IIS Profile Swap (Reliability -> Energy)",
        "Context: Same PUMP-001 data. Plant leadership asks: can we optimize for energy this quarter?",
        [
            "Engineer opens Config Viewer, toggles iis_profile: reliability_first -> energy_optimization.",
            "IIS weights shift: downtime cost weight 0.25 -> 0.35, failure prob 0.35 -> 0.20.",
            "GötzeEngine re-ranks: top action becomes 'Reduce operating speed 8%' (IIS=0.82).",
            "Runner-up remains seal replacement (IIS=0.79) — gap narrows, trade-off visible.",
            "Engineer narrates: same data, different business objective, no code deploy.",
        ],
        "Proves config-driven modularity (P2) live on stage — the scale/CoE story.",
    )
    pdf.scenario_box(
        "Scenario 11.3 — Onboarding a New Compressor Class (Zero Code)",
        "Context: LTTS deploys PlantMind at a second site with reciprocating compressors.",
        [
            "CoE copies hero.yaml manifest template for new plant_id.",
            "Adds asset_hierarchy entry COMP-012, maps PI tags via tag_mapping.",
            "Sets physics_model lambda/beta from section 6a compressor row.",
            "Loads intervention_library from OEM maintenance guide.",
            "Selects quality_driven IIS profile for pharmaceutical site.",
            "Config loader composes pipeline; dashboard renders within hours.",
        ],
        "New asset class onboarded via config only — no src/ code changes (production narrative).",
    )
    pdf.scenario_box(
        "Scenario 11.4 — Groq Outage During Demo (C10 Fallback)",
        "Context: Live hackathon demo; Groq API unavailable mid-presentation.",
        [
            "GötzeEngine IIS computation continues (deterministic, no LLM).",
            "Orchestrator swaps to pre-cached narrative for top intervention.",
            "Panel renders IIS bar, runner-up, gap, and cached plain-English reason.",
            "Judge asks about narrative — presenter shows MODEL-REGISTRY fallback note.",
        ],
        "Demo never dies. IIS score and approval flow unaffected.",
    )
    pdf.scenario_box(
        "Scenario 11.5 — Databricks Production Cutover",
        "Context: Post-hackathon, customer wants Unity Catalog lineage visible to auditors.",
        [
            "Bronze: Auto Loader ingests historian CSV landing zone.",
            "Silver DLT: physics features with section 6a UDF (RUL in DAYS).",
            "Gold: asset_health_status, gotze_decisions, audit_records tables.",
            "Götze wrapped as MLflow PyFunc; Vector Search indexes maintenance KB.",
            "Streamlit dashboard swaps SQLite for Databricks SQL connector (C9 gate).",
        ],
        "Same Layer-0 contracts; Layer-1 swap demonstrates Databricks partnership fit.",
    )

    # 12 Databricks
    pdf.section_title("12", "Databricks Production Path")
    pdf.bullet_list([
        "Medallion: Bronze raw tags -> Silver physics features -> Gold decisions",
        "Feature Store registers degradation signals for fleet models",
        "MLflow tracks Weibull calibration and Götze IIS versions",
        "Unity Catalog enforces lineage Sensor -> Health -> IIS -> Approval",
        "Vector Search replaces ChromaDB for RootCauseAnalyst at scale",
    ])

    # 13 Demo
    pdf.section_title("13", "Hackathon Demo Plan & ROI")
    pdf.body("Demo shape (PINNED): 3 assets on stage; hero PUMP-001; 30-asset fleet behind; ~$180k per prevented failure; one profile swap.")
    pdf.table(
        ["Hour", "Freeze", "Action"],
        [
            ["H-14", "PINN", "Drop if not validating"],
            ["H-16", "Config pipeline", "Fall back to static path if unstable"],
            ["H-20", "Features", "Decide C9 local vs Databricks live"],
            ["Post-H20", "Rehearsal", "No new features"],
        ],
        [30, 55, 105],
    )

    # 14 Differentiation
    pdf.section_title("14", "Differentiation & Competitive Position")
    pdf.table(
        ["Alternative", "Stops At", "PlantMind Advantage"],
        [
            ["PdM / anomaly tools", "Alerts", "Ranked action + approval + WO"],
            ["Digital twins", "Simulation", "Governed decision layer on top"],
            ["Generic agents", "Chat", "Physics + IIS + audit baked in"],
            ["Custom integrators", "Per-site code", "Manifest-driven scale"],
        ],
        [50, 50, 90],
    )

    # 15 Appendix
    pdf.section_title("15", "Technical Stack & Contracts Appendix")
    pdf.body(
        "Python 3.11 | FastAPI | Pydantic v2 | CrewAI + LangGraph | Groq Llama 3.3 70B / 3.2 3B | "
        "sentence-transformers | ChromaDB | scikit-learn + scipy | Streamlit + Plotly | SQLite."
    )
    pdf.h2("Shared Contracts (src/contracts/)")
    pdf.bullet_list([
        "PhysicsModelOutput, GotzeDecision, AssetHealthReport, ExecutiveBrief",
        "AuditRecord, LineageEntry",
        "Plant Config Manifest (manifest.py) — BUILDING",
        "WorkOrder (workorder.py) — BUILDING",
    ])
    pdf.h2("Readiness Rubric (DNA section 7)")
    pdf.body("Current readiness: 70.3%. Target >= 90% by Jul 8. Gaps cluster in demo quality (#7), technical feasibility (#2), data-fit (#4).")
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*GRAY)
    pdf._reset_x()
    pdf.multi_cell(
        pdf.CONTENT_W,
        5,
        ascii_safe(
            "END OF DOCUMENT - Derived from PROJECT-DNA v1.0 (LOCKED) and LOCKED_STATE.md. "
            "Not authoritative; conform to DNA or file Amendment. "
            "Visual mockups are illustrative wireframes for hackathon UI direction."
        ),
    )

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT_PDF))
    return OUT_PDF


def main() -> None:
    mockups = copy_mockups()
    out = build_pdf(mockups)
    page_count = len(FPDF().pages)  # not accurate; re-open not needed
    print(f"Generated: {out}")
    print(f"Mockups copied: {len(mockups)}")
    # Count pages by reading file size heuristic - use fpdf page count from build
    from fpdf import FPDF as _F

    class _C(_F):
        pass

    # Re-read via pypdf if available, else estimate
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(out))
        print(f"Pages: {len(reader.pages)}")
    except Exception:
        print("Pages: (install pypdf to count)")


if __name__ == "__main__":
    main()