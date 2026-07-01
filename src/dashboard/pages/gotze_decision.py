"""Page 2 — GotzeEngine Decision: IIS ranking, what-if paths, cascade chain, approval gate."""
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
from src.shared.audit import update_decision
from src.pipeline.schemas import PipelineResult


# ── helpers ───────────────────────────────────────────────────────────────────

def _iis_chart(top_intervention: str) -> go.Figure:
    eligible = sorted([c for c in CANDIDATES if not c.vetoed], key=lambda c: c.iis, reverse=True)
    colors   = ["#4C78A8" if c.name == top_intervention else "#222244" for c in eligible]
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
        height=360, margin=dict(t=20, b=20, l=160, r=80),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
        xaxis={"title": "IIS Score", "range": [0, 1.05], "gridcolor": "#1a1a30"},
        yaxis={"autorange": "reversed"}, showlegend=False,
    )
    return fig


def _formula_breakdown(top_name: str) -> None:
    cand = next((c for c in CANDIDATES if c.name == top_name), None)
    if not cand:
        return
    st.markdown(f"""
**IIS formula breakdown for `{top_name}`** (LOCKED_STATE section 2):

| Term | Weight | Value | Contribution |
|------|--------|-------|-------------|
| delta-P failure | 0.35 | {cand.delta_p_failure:.2f} | **{0.35*cand.delta_p_failure:.4f}** |
| delta-Downtime Cost | 0.25 | {cand.delta_downtime_cost:.2f} | **{0.25*cand.delta_downtime_cost:.4f}** |
| Feasibility | 0.20 | {cand.feasibility:.2f} | **{0.20*cand.feasibility:.4f}** |
| Historical Success | 0.15 | {cand.historical_success:.2f} | **{0.15*cand.historical_success:.4f}** |
| Safety Risk Delta | -0.05 | {cand.safety_risk_delta:.2f} | **{-0.05*cand.safety_risk_delta:.4f}** |
| | | **IIS =** | **{cand.iis:.4f}** |
""")


def _what_if_panel(rul_days: float) -> None:
    planned_days   = 3
    unplanned_days = 15
    daily_cost     = 15_000
    emergency_cost = 75_000
    parts_cost     = 25_000
    cascade_mult   = 1.8

    do_nothing = (unplanned_days * daily_cost + emergency_cost) * cascade_mult
    act_now    = planned_days * daily_cost + parts_cost
    saving     = do_nothing - act_now

    cl, cr = st.columns(2)
    with cl:
        st.markdown(
            f'<div class="wif-bad">'
            f'<div class="wif-title" style="color:#FF4B4B">DO NOTHING - Failure Path</div>'
            f'<div class="wif-row">Failure in<b>{rul_days:.1f} d (catastrophic)</b></div>'
            f'<div class="wif-row">Unplanned downtime<b>{unplanned_days} days</b></div>'
            f'<div class="wif-row">Emergency repair + parts rush<b>${emergency_cost:,.0f}</b></div>'
            f'<div class="wif-row">Cascade multiplier<b>{cascade_mult}x (motor + compressor)</b></div>'
            f'<div class="wif-total" style="color:#FF4B4B">${do_nothing:,.0f}</div>'
            f'<div style="font-size:0.7rem;color:#662222">Total exposure</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with cr:
        st.markdown(
            f'<div class="wif-good">'
            f'<div class="wif-title" style="color:#00CC88">ACT NOW - GotzeEngine Path</div>'
            f'<div class="wif-row">Planned shutdown in<b>7 days from now</b></div>'
            f'<div class="wif-row">Planned downtime<b>{planned_days} days</b></div>'
            f'<div class="wif-row">Pre-staged parts + labour<b>${parts_cost:,.0f}</b></div>'
            f'<div class="wif-row">Cascade risk<b>Isolated shutdown - contained</b></div>'
            f'<div class="wif-total" style="color:#00CC88">${act_now:,.0f}</div>'
            f'<div style="font-size:0.7rem;color:#226644">Total cost</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.metric("Net Saving by Acting Now", f"${saving:,.0f}",
              delta="vs. letting it fail", delta_color="normal")


def _cascade_panel(asset_type: str, asset_id: str) -> None:
    chain = ASSET_CASCADE.get(asset_type, [])
    if not chain:
        st.info("No downstream cascade risk identified for this asset type.")
        return

    st.markdown(
        f'<div class="cas-primary">'
        f'<div class="cas-asset" style="color:#FF4B4B">{asset_id}</div>'
        f'<div class="cas-reason">PRIMARY FAILURE POINT</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    for i, (downstream_type, reason) in enumerate(chain, start=1):
        cls = "cas-node-1" if i == 1 else "cas-node-2"
        col = "#FFA500" if i == 1 else "#cc3333"
        arrow = "->" * i
        st.markdown(
            f'<div class="{cls}">'
            f'<div class="cas-asset" style="color:{col}">{arrow} {downstream_type} assets</div>'
            f'<div class="cas-reason">{reason}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.markdown('<div class="sb-section">Navigation</div>', unsafe_allow_html=True)
if st.sidebar.button("<- Back to Fleet", use_container_width=True):
    st.switch_page("pages/fleet_overview.py")
if st.sidebar.button("<- Plant Overview", use_container_width=True, key="back_plant"):
    st.switch_page("pages/plant_overview.py")

st.sidebar.divider()
st.sidebar.markdown('<div class="sb-section">Decision Context</div>', unsafe_allow_html=True)
st.sidebar.caption("Review the GotzeEngine recommendation, examine evidence, then approve or reject.")

# ── page ──────────────────────────────────────────────────────────────────────

st.markdown(
    '<div class="pm-page-hdr">'
    '<div>'
    '<div class="pm-page-title">GotzeEngine Decision</div>'
    '<div class="pm-page-sub">IIS-ranked intervention recommendation &nbsp;|&nbsp; Human-in-the-loop approval gate</div>'
    '</div>'
    '<span class="pm-badge pm-badge-blue">LOCKED_STATE v2</span>'
    '</div>',
    unsafe_allow_html=True,
)

result: PipelineResult | None = st.session_state.get("pipeline_result")

if result is None:
    st.info("No result yet. Run a scenario on the **Plant Detail** tab first.")
    st.stop()

if not result.gotze_triggered:
    st.success(
        f"GotzeEngine was NOT triggered for **{result.asset_id}** — asset is within safe thresholds. "
        f"Health {result.health_report.health_score:.1f}/100, RUL {result.health_report.rul_days:.1f} d."
    )
    st.stop()

dec          = result.gotze_decision
already_done = st.session_state.get("approval_submitted", False)

_raw        = result.asset_id.split("_")[0] if "_" in result.asset_id else "bearing"
_asset_type = "compressor" if _raw == "comp" else _raw

# ── tabs ──────────────────────────────────────────────────────────────────────

tab_rec, tab_ev, tab_appr = st.tabs([
    "Recommendation", "Evidence", "Approval Gate"
])

# ────────────────────── TAB 1: Recommendation ─────────────────────────────────
with tab_rec:
    st.markdown(f"##### Asset: {result.asset_id} &nbsp;|&nbsp; Health {result.health_report.health_score:.1f}/100",
                unsafe_allow_html=True)

    rc_left, rc_right = st.columns([3, 2])

    with rc_left:
        st.markdown(
            f'<div class="rec-card">'
            f'<div class="rec-label">Top Recommendation</div>'
            f'<div class="rec-action">{dec.top_intervention.replace("_", " ").upper()}</div>'
            f'<div style="display:flex;align-items:baseline;gap:16px;margin:10px 0">'
            f'<div>'
            f'<div style="font-size:0.65rem;color:#33335a;text-transform:uppercase;letter-spacing:0.12em">IIS Score</div>'
            f'<div class="rec-iis">{dec.iis_score:.3f}</div>'
            f'</div>'
            f'<div style="font-size:3rem;font-weight:900;color:#22224a">|</div>'
            f'<div>'
            f'<div style="font-size:0.65rem;color:#33335a;text-transform:uppercase;letter-spacing:0.12em">Confidence</div>'
            f'<div style="font-size:2rem;font-weight:900;color:#4C78A8">{dec.confidence:.0%}</div>'
            f'</div>'
            f'</div>'
            f'<div class="rec-narrative">{dec.narrative}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with rc_right:
        st.markdown("<br>", unsafe_allow_html=True)
        st.metric("Runner-up",  dec.runner_up.replace("_", " "))
        st.metric("IIS Gap",    f"{dec.iis_gap:.3f}", delta="vs runner-up")
        st.metric("RUL",        f"{result.health_report.rul_days:.1f} d")
        st.metric("Health",     f"{result.health_report.health_score:.1f}/100")

    if already_done:
        st.success(f"Decision already submitted for audit record `{result.audit_record_id}`.")
    else:
        st.warning("Awaiting operator approval — use the **Approval Gate** tab.")

    st.divider()
    st.markdown("##### What Happens If We Don't Act?")
    _what_if_panel(result.health_report.rul_days)

# ────────────────────── TAB 2: Evidence ──────────────────────────────────────
with tab_ev:
    st.markdown("##### All Candidates — IIS Ranking")
    st.caption("IIS = 0.35*dP_failure + 0.25*dDowntimeCost + 0.20*Feasibility + 0.15*HistoricalSuccess - 0.05*SafetyRiskDelta")
    st.plotly_chart(_iis_chart(dec.top_intervention), use_container_width=True)

    with st.expander("IIS formula breakdown for top candidate"):
        _formula_breakdown(dec.top_intervention)

    st.divider()
    st.markdown("##### Cascade Failure Chain")
    st.caption("Assets that will fail next if primary asset is not maintained.")
    _cascade_panel(_asset_type, result.asset_id)

    if result.rca_narrative:
        st.divider()
        st.markdown("##### RootCauseAnalyst — Causal Chain")
        st.markdown(f"> {result.rca_narrative}")
        if result.rca_citations:
            st.caption("Sources: " + " | ".join(result.rca_citations))

# ────────────────────── TAB 3: Approval Gate ──────────────────────────────────
with tab_appr:
    st.markdown("##### Human Approval Gate")
    st.warning("This action requires operator approval before execution. (LOCKED_STATE sections 1, 7)")

    if already_done:
        st.success(f"Decision already submitted for audit record `{result.audit_record_id}`.")
        st.stop()

    st.markdown(
        f'<div style="background:#0d0d1e;border:1px solid #14142a;border-radius:10px;padding:16px;margin-bottom:16px">'
        f'<div style="font-size:0.72rem;color:#33335a;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px">Decision Summary</div>'
        f'<div style="color:#fff;font-weight:700">{dec.top_intervention.replace("_"," ").upper()}</div>'
        f'<div style="color:#4C78A8;font-size:0.85rem;margin-top:4px">IIS {dec.iis_score:.3f} &nbsp;&bull;&nbsp; '
        f'Confidence {dec.confidence:.0%} &nbsp;&bull;&nbsp; RUL {result.health_report.rul_days:.1f} d</div>'
        f'<div style="color:#44446a;font-size:0.78rem;margin-top:6px">{dec.narrative}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    reason_input = st.text_area(
        "Approval note (optional):",
        placeholder="e.g. 'Confirmed with shift supervisor. Parts available.'",
        height=80,
        key="approval_note",
    )

    app_col, rej_col, _ = st.columns([1, 1, 3])
    with app_col:
        if st.button("Approve", type="primary", use_container_width=True):
            update_decision(result.audit_record_id, "approved",
                            reason_input or "Approved by operator")
            st.session_state.approval_submitted = True
            st.success(f"APPROVED - audit record `{result.audit_record_id}` updated.")
            st.balloons()
            st.rerun()

    with rej_col:
        if st.button("Reject", type="secondary", use_container_width=True):
            update_decision(result.audit_record_id, "rejected",
                            reason_input or "Rejected by operator")
            st.session_state.approval_submitted = True
            st.info(f"REJECTED - audit record `{result.audit_record_id}` updated.")
            st.rerun()
