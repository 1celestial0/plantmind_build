"""Page 2 — GötzeEngine Decision: IIS ranking, what-if paths, cascade chain, approval gate."""
from __future__ import annotations
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import plotly.graph_objects as go
import streamlit as st

from src.agents.gotze_engine import CANDIDATES
from src.dashboard.failure_patterns import ASSET_CASCADE
from src.governance.audit import update_decision
from src.pipeline.schemas import PipelineResult


# ── helpers ───────────────────────────────────────────────────────────────────

def _iis_chart(top_intervention: str) -> go.Figure:
    eligible = sorted([c for c in CANDIDATES if not c.vetoed], key=lambda c: c.iis, reverse=True)
    colors   = ["#4C78A8" if c.name == top_intervention else "#555577" for c in eligible]
    fig = go.Figure(go.Bar(
        x=[c.iis for c in eligible],
        y=[c.name.replace("_", " ") for c in eligible],
        orientation="h",
        marker_color=colors,
        text=[f"{c.iis:.3f}" for c in eligible],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>IIS: %{x:.4f}<extra></extra>",
    ))
    fig.update_layout(
        height=380, margin=dict(t=20, b=20, l=160, r=80),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
        xaxis={"title": "IIS Score", "range": [0, 1.05], "gridcolor": "#333"},
        yaxis={"autorange": "reversed"}, showlegend=False,
    )
    return fig


def _formula_breakdown(top_name: str) -> None:
    cand = next((c for c in CANDIDATES if c.name == top_name), None)
    if not cand:
        return
    st.markdown(f"""
**IIS formula breakdown for `{top_name}`** (LOCKED_STATE §2):

| Term | Weight | Value | Contribution |
|------|--------|-------|-------------|
| delta-P failure | 0.35 | {cand.delta_p_failure:.2f} | **{0.35*cand.delta_p_failure:.4f}** |
| delta-Downtime Cost | 0.25 | {cand.delta_downtime_cost:.2f} | **{0.25*cand.delta_downtime_cost:.4f}** |
| Feasibility | 0.20 | {cand.feasibility:.2f} | **{0.20*cand.feasibility:.4f}** |
| Historical Success | 0.15 | {cand.historical_success:.2f} | **{0.15*cand.historical_success:.4f}** |
| Safety Risk Delta | -0.05 | {cand.safety_risk_delta:.2f} | **{-0.05*cand.safety_risk_delta:.4f}** |
| | | **IIS =** | **{cand.iis:.4f}** |
""")


def _what_if_panel(rul_days: float, health: float) -> None:
    """Side-by-side cost comparison — the burning building moment."""
    planned_days   = 3
    unplanned_days = 15
    daily_cost     = 15_000
    emergency_cost = 75_000
    parts_cost     = 25_000
    cascade_mult   = 1.8

    do_nothing = (unplanned_days * daily_cost + emergency_cost) * cascade_mult
    act_now    = planned_days * daily_cost + parts_cost
    saving     = do_nothing - act_now

    st.subheader("What Happens If We Don't Act?")

    cl, cr = st.columns(2)
    with cl:
        st.markdown(
            '<div style="background:#1a0808;border:2px solid #FF4B4B;border-radius:12px;padding:18px">'
            '<div style="color:#FF4B4B;font-weight:bold;font-size:15px;margin-bottom:10px">'
            '⚠ DO NOTHING — Failure Path</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**Failure in:** {rul_days:.1f} days (catastrophic)")
        st.markdown(f"**Unplanned downtime:** {unplanned_days} days")
        st.markdown(f"**Emergency repair + parts rush:** ${emergency_cost:,.0f}")
        st.markdown(f"**Cascade multiplier:** {cascade_mult}x (motor + compressor)")
        st.markdown(f"**Total exposure:** :red[**${do_nothing:,.0f}**]")
        st.markdown("</div>", unsafe_allow_html=True)

    with cr:
        st.markdown(
            '<div style="background:#081a0e;border:2px solid #00CC88;border-radius:12px;padding:18px">'
            '<div style="color:#00CC88;font-weight:bold;font-size:15px;margin-bottom:10px">'
            '✅ ACT NOW — GötzeEngine Path</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"**Planned shutdown:** 7 days from now")
        st.markdown(f"**Planned downtime:** {planned_days} days")
        st.markdown(f"**Pre-staged parts + labour:** ${parts_cost:,.0f}")
        st.markdown(f"**Cascade:** Isolated shutdown — contained")
        st.markdown(f"**Total cost:** :green[**${act_now:,.0f}**]")
        st.markdown("</div>", unsafe_allow_html=True)

    st.metric(
        "Net Saving by Acting Now",
        f"${saving:,.0f}",
        delta=f"vs. letting it fail",
        delta_color="normal",
    )


def _cascade_panel(asset_type: str, asset_id: str) -> None:
    chain = ASSET_CASCADE.get(asset_type, [])
    if not chain:
        return

    st.subheader("Cascade Failure Chain")
    st.markdown(
        f'<div style="padding:8px 12px;background:#FF4B4B22;border-left:3px solid #FF4B4B;border-radius:4px;margin:4px 0">'
        f'<span style="color:#FF4B4B;font-weight:bold">{asset_id}</span> '
        f'<span style="color:#888;font-size:12px">— PRIMARY FAILURE</span></div>',
        unsafe_allow_html=True,
    )
    for i, (downstream_type, reason) in enumerate(chain, start=1):
        indent   = "→ " * i
        col      = "#FFA500" if i == 1 else "#FF4B4B"
        st.markdown(
            f'<div style="padding:8px 12px;background:{col}11;border-left:3px solid {col};'
            f'border-radius:4px;margin:4px 0">'
            f'<span style="color:#555">{indent}</span>'
            f'<span style="color:{col};font-weight:bold">{downstream_type} assets</span>'
            f'<div style="color:#aaa;font-size:12px;margin-top:2px">{reason}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── page ──────────────────────────────────────────────────────────────────────

if st.sidebar.button("← Back to Fleet", use_container_width=True):
    st.switch_page("pages/fleet_overview.py")

st.title("GötzeEngine — Decision & Approval")

result: PipelineResult | None = st.session_state.get("pipeline_result")

if result is None:
    st.info("No result yet. Run a scenario on the **Plant Overview** page first.")
    st.stop()

if not result.gotze_triggered:
    st.success(
        f"GötzeEngine was NOT triggered for **{result.asset_id}** — asset is within safe thresholds. "
        f"Health {result.health_report.health_score:.1f}/100, RUL {result.health_report.rul_days:.1f} d."
    )
    st.stop()

dec            = result.gotze_decision
already_done   = st.session_state.get("approval_submitted", False)

# ── top recommendation card ───────────────────────────────────────────────────
st.subheader(f"Asset: {result.asset_id}  |  Health {result.health_report.health_score:.1f}/100")

top_col, meta_col = st.columns([2, 1])
with top_col:
    st.markdown(
        f"""
        <div style="background:#1a1a2e;padding:20px;border-radius:10px;border:2px solid #4C78A8">
          <div style="font-size:13px;color:#888;margin-bottom:4px">TOP RECOMMENDATION</div>
          <div style="font-size:26px;font-weight:bold;color:#4C78A8">{dec.top_intervention.replace('_',' ').upper()}</div>
          <div style="font-size:34px;font-weight:bold;color:white;margin:8px 0">IIS {dec.iis_score:.3f}</div>
          <div style="color:#aaa;font-size:13px">{dec.narrative}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with meta_col:
    st.metric("Runner-up",  dec.runner_up.replace("_", " "))
    st.metric("IIS Gap",    f"{dec.iis_gap:.3f}")
    st.metric("Confidence", f"{dec.confidence:.1%}")
    st.metric("RUL",        f"{result.health_report.rul_days:.1f} d")

st.divider()

# ── what-if panel ─────────────────────────────────────────────────────────────
_what_if_panel(result.health_report.rul_days, result.health_report.health_score)

st.divider()

# ── cascade chain ─────────────────────────────────────────────────────────────
_raw = result.asset_id.split("_")[0] if "_" in result.asset_id else "bearing"
_asset_type = "compressor" if _raw == "comp" else _raw
_cascade_panel(_asset_type, result.asset_id)

st.divider()

# ── IIS ranking chart ─────────────────────────────────────────────────────────
st.subheader("All Candidates — IIS Ranking")
st.plotly_chart(_iis_chart(dec.top_intervention), use_container_width=True)

with st.expander("IIS formula breakdown"):
    _formula_breakdown(dec.top_intervention)

st.divider()

# ── RCA ───────────────────────────────────────────────────────────────────────
if result.rca_narrative:
    st.subheader("RootCauseAnalyst — Causal Chain")
    st.markdown(f"> {result.rca_narrative}")
    if result.rca_citations:
        st.caption("Sources: " + " | ".join(result.rca_citations))

st.divider()

# ── approval gate ─────────────────────────────────────────────────────────────
st.subheader("Human Approval Gate")
st.warning("This action requires operator approval before execution. (LOCKED_STATE §1, §7)")

if already_done:
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
        update_decision(result.audit_record_id, "approved",
                        reason_input or "Approved by operator")
        st.session_state.approval_submitted = True
        st.success(f"APPROVED — audit record `{result.audit_record_id}` updated.")
        st.balloons()
        st.rerun()

with rej_col:
    if st.button("Reject", type="secondary", use_container_width=True):
        update_decision(result.audit_record_id, "rejected",
                        reason_input or "Rejected by operator")
        st.session_state.approval_submitted = True
        st.info(f"REJECTED — audit record `{result.audit_record_id}` updated.")
        st.rerun()
