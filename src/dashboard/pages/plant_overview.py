"""Page 1 — Plant Overview: scenario selector, health cards, executive brief."""
from __future__ import annotations
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import plotly.graph_objects as go
import streamlit as st

from src.dashboard.demo_scenarios import SCENARIOS
from src.pipeline import run as pipeline_run
from src.pipeline.schemas import PipelineResult


# ── helpers ──────────────────────────────────────────────────────────────────

def _health_color(score: float, rul: float) -> str:
    if score < 40 or rul < 14:
        return "#FF4B4B"
    if score < 70 or rul < 30:
        return "#FFA500"
    return "#00CC88"


def _severity_emoji(severity: str) -> str:
    return {"critical": "🔴", "warning": "🟡", "normal": "🟢"}.get(severity, "⚪")


def _health_gauge(asset_id: str, health: float, rul: float) -> go.Figure:
    color = _health_color(health, rul)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health,
        number={"suffix": "/100", "font": {"size": 22}},
        title={"text": f"<b>{asset_id}</b>", "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "#1a1a2e",
            "steps": [
                {"range": [0, 40],  "color": "rgba(255,75,75,0.12)"},
                {"range": [40, 70], "color": "rgba(255,165,0,0.12)"},
                {"range": [70, 100],"color": "rgba(0,204,136,0.12)"},
            ],
            "threshold": {
                "line": {"color": "#FF4B4B", "width": 3},
                "thickness": 0.8,
                "value": 40,
            },
        },
    ))
    fig.update_layout(
        height=200, margin=dict(t=40, b=0, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", font_color="white",
    )
    return fig


def _rul_bar(rul: float, ci_low: float, ci_high: float) -> go.Figure:
    color = "#FF4B4B" if rul < 14 else ("#FFA500" if rul < 30 else "#00CC88")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[rul], y=["RUL"], orientation="h",
        marker_color=color, name="RUL",
        error_x={"type": "data", "array": [ci_high - rul], "arrayminus": [rul - ci_low], "color": "white"},
    ))
    fig.add_vline(x=14, line_dash="dash", line_color="rgba(255,75,75,0.5)", annotation_text="14 d trigger")
    fig.update_layout(
        height=90, margin=dict(t=5, b=5, l=5, r=80),
        paper_bgcolor="rgba(0,0,0,0)", font_color="white",
        showlegend=False,
        xaxis={"title": "days", "range": [0, max(ci_high * 1.2, 20)]},
    )
    return fig


# ── sidebar ──────────────────────────────────────────────────────────────────

st.sidebar.header("Scenario Selector")
scenario_options = {k: v["label"] for k, v in SCENARIOS.items()}
selected = st.sidebar.radio(
    "Choose scenario:",
    options=list(scenario_options.keys()),
    format_func=lambda k: scenario_options[k],
    index=list(scenario_options.keys()).index(st.session_state.selected_scenario),
    key="scenario_radio",
)
st.session_state.selected_scenario = selected

st.sidebar.markdown("---")
st.sidebar.caption(SCENARIOS[selected]["description"])
st.sidebar.markdown("---")

run_btn = st.sidebar.button("Run Analysis", type="primary", use_container_width=True)

if run_btn:
    st.session_state.approval_submitted = False
    with st.spinner("Running 5-agent pipeline..."):
        reading = SCENARIOS[selected]["reading"]
        result = pipeline_run(reading)
        st.session_state.pipeline_result = result
    st.sidebar.success(f"Done in {result.pipeline_duration_ms:.1f} ms")
    if result.gotze_triggered:
        st.sidebar.warning("GötzeEngine fired — see Decision page")

result: PipelineResult | None = st.session_state.pipeline_result


# ── main ─────────────────────────────────────────────────────────────────────

st.title("PlantMind — Plant Overview")
st.caption("Physics-informed engineering intelligence | GötzeEngine decision loop")

if result is None:
    st.info("Select a scenario in the sidebar and click **Run Analysis** to start.")
    st.stop()

# Executive brief
r = result
brief = r.executive_brief
col1, col2, col3, col4 = st.columns(4)
col1.metric("Health Score", f"{r.health_report.health_score:.1f}/100",
            delta=f"{'CRITICAL' if r.health_report.health_score < 40 else 'OK'}",
            delta_color="inverse" if r.health_report.health_score < 40 else "normal")
col2.metric("RUL", f"{r.health_report.rul_days:.1f} d",
            delta=f"CI [{r.health_report.ci_95[0]:.1f}–{r.health_report.ci_95[1]:.1f}] d")
col3.metric("Severity", _severity_emoji(r.anomaly_severity) + " " + r.anomaly_severity.upper())
col4.metric("Downtime Saved", f"${brief.downtime_saved_estimate:,.0f}",
            delta=f"{brief.gotze_pending} decision pending" if brief.gotze_pending else "no action needed")

st.divider()

# Asset health panel
st.subheader(f"Asset: {r.asset_id}")
gcol, rcol = st.columns([1, 1])
with gcol:
    st.plotly_chart(_health_gauge(r.asset_id, r.health_report.health_score, r.health_report.rul_days),
                    use_container_width=True)
with rcol:
    st.markdown("**Remaining Useful Life**")
    st.plotly_chart(
        _rul_bar(r.health_report.rul_days, r.health_report.ci_95[0], r.health_report.ci_95[1]),
        use_container_width=True,
    )
    st.caption(r.health_report.physics_text)

st.divider()

# Anomaly flags
st.subheader("DataSentinel — Anomaly Flags")
if r.flagged_signals:
    badge_html = " ".join(
        f'<span style="background:#FF4B4B;padding:2px 8px;border-radius:4px;margin:2px;'
        f'font-size:13px">{s}</span>'
        for s in r.flagged_signals
    )
    st.markdown(badge_html, unsafe_allow_html=True)
else:
    st.success("All signals nominal")

st.markdown("---")

# GötzeEngine status
if r.gotze_triggered:
    if st.session_state.approval_submitted:
        st.success("GötzeEngine decision approved — see Audit Log for record.")
    else:
        st.warning(
            f"GötzeEngine fired — recommended action: **{r.gotze_decision.top_intervention}** "
            f"(IIS {r.gotze_decision.iis_score:.3f}) | Awaiting operator approval"
        )
        st.page_link("pages/gotze_decision.py", label="Go to Decision Page →", icon=":material/bolt:")
else:
    st.info("GötzeEngine not triggered — asset within safe thresholds.")

# Critical alerts
if brief.critical_alerts:
    st.subheader("Executive Brief — Critical Alerts")
    for alert in brief.critical_alerts:
        st.error(alert)
