"""Page 2 — GötzeEngine Decision: IIS ranking + human approval gate."""
from __future__ import annotations
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import plotly.graph_objects as go
import streamlit as st

from src.agents.gotze_engine import CANDIDATES
from src.governance.audit import update_decision
from src.pipeline.schemas import PipelineResult


def _iis_chart(top_intervention: str) -> go.Figure:
    """Horizontal bar chart of all non-vetoed candidates ranked by IIS."""
    eligible = [c for c in CANDIDATES if not c.vetoed]
    eligible_sorted = sorted(eligible, key=lambda c: c.iis, reverse=True)

    names = [c.name.replace("_", " ") for c in eligible_sorted]
    scores = [c.iis for c in eligible_sorted]
    colors = ["#4C78A8" if c.name == top_intervention else "#555577" for c in eligible_sorted]
    descriptions = [c.description for c in eligible_sorted]

    fig = go.Figure(go.Bar(
        x=scores,
        y=names,
        orientation="h",
        marker_color=colors,
        text=[f"{s:.3f}" for s in scores],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>IIS: %{x:.4f}<br>%{customdata}<extra></extra>",
        customdata=descriptions,
    ))
    fig.update_layout(
        height=380,
        margin=dict(t=20, b=20, l=160, r=80),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        xaxis={"title": "IIS Score", "range": [0, 1.05], "gridcolor": "#333"},
        yaxis={"autorange": "reversed"},
        showlegend=False,
    )
    fig.add_vline(x=0.0, line_color="white", line_width=0.5)
    return fig


def _formula_breakdown(top_name: str) -> None:
    cand = next((c for c in CANDIDATES if c.name == top_name), None)
    if not cand:
        return
    st.markdown(f"""
    **IIS formula breakdown for `{top_name}`** (LOCKED_STATE §2):

    | Term | Weight | Value | Contribution |
    |------|--------|-------|-------------|
    | ΔP_failure | 0.35 | {cand.delta_p_failure:.2f} | **{0.35 * cand.delta_p_failure:.4f}** |
    | ΔDowntimeCost | 0.25 | {cand.delta_downtime_cost:.2f} | **{0.25 * cand.delta_downtime_cost:.4f}** |
    | Feasibility | 0.20 | {cand.feasibility:.2f} | **{0.20 * cand.feasibility:.4f}** |
    | HistoricalSuccess | 0.15 | {cand.historical_success:.2f} | **{0.15 * cand.historical_success:.4f}** |
    | SafetyRiskDelta | −0.05 | {cand.safety_risk_delta:.2f} | **{-0.05 * cand.safety_risk_delta:.4f}** |
    | | | **IIS =** | **{cand.iis:.4f}** |
    """)


# ── page ─────────────────────────────────────────────────────────────────────

st.title("GötzeEngine — Decision & Approval")

result: PipelineResult | None = st.session_state.get("pipeline_result")

if result is None:
    st.info("No pipeline result yet. Run a scenario on the **Plant Overview** page first.")
    st.stop()

if not result.gotze_triggered:
    st.success(
        f"GötzeEngine was NOT triggered for **{result.asset_id}** — asset is within safe thresholds. "
        f"Health {result.health_report.health_score:.1f}/100, RUL {result.health_report.rul_days:.1f} d."
    )
    st.stop()

dec = result.gotze_decision
already_approved = st.session_state.get("approval_submitted", False)

# ── Top recommendation ────────────────────────────────────────────────────────
st.subheader(f"Asset: {result.asset_id}  |  Health {result.health_report.health_score:.1f}/100")

top_col, meta_col = st.columns([2, 1])
with top_col:
    st.markdown(
        f"""
        <div style="background:#1a1a2e;padding:20px;border-radius:10px;border:2px solid #4C78A8">
        <div style="font-size:13px;color:#888;margin-bottom:4px">TOP RECOMMENDATION</div>
        <div style="font-size:28px;font-weight:bold;color:#4C78A8">{dec.top_intervention.replace('_',' ').upper()}</div>
        <div style="font-size:36px;font-weight:bold;color:white;margin:8px 0">IIS {dec.iis_score:.3f}</div>
        <div style="color:#aaa;font-size:14px">{dec.narrative}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with meta_col:
    st.metric("Runner-up", dec.runner_up.replace("_", " "))
    st.metric("IIS Gap", f"{dec.iis_gap:.3f}")
    st.metric("Confidence", f"{dec.confidence:.1%}")
    st.metric("RUL", f"{result.health_report.rul_days:.1f} d")

st.divider()

# ── IIS candidate chart ────────────────────────────────────────────────────────
st.subheader("All Candidates — IIS Ranking")
st.plotly_chart(_iis_chart(dec.top_intervention), use_container_width=True)

with st.expander("IIS formula breakdown"):
    _formula_breakdown(dec.top_intervention)

st.divider()

# ── RCA ────────────────────────────────────────────────────────────────────────
if result.rca_narrative:
    st.subheader("RootCauseAnalyst — Causal Chain")
    st.markdown(f"> {result.rca_narrative}")
    if result.rca_citations:
        st.caption("Sources: " + " | ".join(result.rca_citations))

st.divider()

# ── Approval gate ──────────────────────────────────────────────────────────────
st.subheader("Human Approval Gate")
st.warning("This action requires operator approval before execution. (LOCKED_STATE §1, §7)")

if already_approved:
    st.success(f"Decision already submitted for audit record `{result.audit_record_id}`.")
    st.stop()

reason_input = st.text_area(
    "Approval note (optional):",
    placeholder="e.g. 'Confirmed with shift supervisor. Parts available.'",
    height=80,
)

app_col, rej_col, _ = st.columns([1, 1, 3])
with app_col:
    if st.button("Approve", type="primary", use_container_width=True):
        update_decision(result.audit_record_id, "approved", reason_input or "Approved by operator")
        st.session_state.approval_submitted = True
        st.success(f"APPROVED — audit record `{result.audit_record_id}` updated.")
        st.balloons()
        st.rerun()

with rej_col:
    if st.button("Reject", type="secondary", use_container_width=True):
        update_decision(result.audit_record_id, "rejected", reason_input or "Rejected by operator")
        st.session_state.approval_submitted = True
        st.info(f"REJECTED — audit record `{result.audit_record_id}` updated.")
        st.rerun()
