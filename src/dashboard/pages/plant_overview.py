"""Page 1 — Plant Overview: live feed, health gauges, Weibull projection, signal waterfall."""
from __future__ import annotations
import sys
import time
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from src.dashboard.demo_scenarios import SCENARIOS
from src.dashboard.fleet_data import FLEET_BY_ID
from src.dashboard.failure_patterns import FAILURE_PATTERNS, PATTERNS_BY_ID
from src.physics.constants import ASSET_PARAMS, H_FAILURE_THRESHOLD, CYCLES_PER_DAY
from src.physics.stress import composite_stress
from src.physics.weibull import health_at
from src.pipeline import run as pipeline_run
from src.pipeline.schemas import PipelineResult, SensorReading
from ml.synthesis.config import SIGNAL_SPECS


# ── pure helpers ─────────────────────────────────────────────────────────────

def _hcolor(score: float, rul: float = 999) -> str:
    if score < 40 or rul < 14: return "#FF4B4B"
    if score < 70 or rul < 30: return "#FFA500"
    return "#00CC88"


def _sev_badge(sev: str) -> str:
    cls = {"critical": "pm-badge-crit", "warning": "pm-badge-warn", "normal": "pm-badge-ok"}.get(sev, "pm-badge-blue")
    return f'<span class="pm-badge {cls}">{sev.upper()}</span>'


# ── chart builders ────────────────────────────────────────────────────────────

def _gauge(asset_id: str, health: float, rul: float) -> go.Figure:
    color = _hcolor(health, rul)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health,
        number={"suffix": "/100", "font": {"size": 22}},
        title={"text": f"<b>{asset_id}</b>", "font": {"size": 14}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "#0d0d1e",
            "steps": [
                {"range": [0, 40],   "color": "rgba(255,75,75,0.10)"},
                {"range": [40, 70],  "color": "rgba(255,165,0,0.10)"},
                {"range": [70, 100], "color": "rgba(0,204,136,0.10)"},
            ],
            "threshold": {"line": {"color": "#FF4B4B", "width": 3},
                          "thickness": 0.8, "value": 40},
        },
    ))
    fig.update_layout(height=200, margin=dict(t=40, b=0, l=20, r=20),
                      paper_bgcolor="rgba(0,0,0,0)", font_color="white")
    return fig


def _rul_bar(rul: float, ci_low: float, ci_high: float) -> go.Figure:
    color = "#FF4B4B" if rul < 14 else ("#FFA500" if rul < 30 else "#00CC88")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[rul], y=["RUL"], orientation="h",
        marker_color=color, name="RUL",
        error_x={"type": "data", "array": [ci_high - rul],
                 "arrayminus": [rul - ci_low], "color": "white"},
    ))
    fig.add_vline(x=14, line_dash="dash", line_color="rgba(255,75,75,0.5)",
                  annotation_text="14 d trigger")
    fig.update_layout(height=90, margin=dict(t=5, b=5, l=5, r=80),
                      paper_bgcolor="rgba(0,0,0,0)", font_color="white",
                      showlegend=False,
                      xaxis={"title": "days", "range": [0, max(ci_high * 1.2, 20)]})
    return fig


def _weibull_projection(asset_type: str, cycle: int | float, rul_days: float,
                         temp: float, load: float) -> go.Figure:
    cycle = int(cycle)
    p   = ASSET_PARAMS[asset_type]
    s   = composite_stress(temp, load)
    lam, beta = p["lambda_"], p["beta"]

    h_start  = max(0, cycle - 80)
    h_cycles = list(range(h_start, cycle + 1))
    h_vals   = [health_at(c, lam, beta, s) for c in h_cycles]

    dn_end    = cycle + max(10, int(rul_days * CYCLES_PER_DAY) + 15)
    dn_cycles = list(range(cycle, dn_end))
    dn_vals   = [health_at(c, lam, beta, s) for c in dn_cycles]

    maint_c   = cycle + int(7 * CYCLES_PER_DAY)
    act_end   = cycle + int(60 * CYCLES_PER_DAY)
    act_cycles = list(range(cycle, act_end))
    act_vals  = []
    for c in act_cycles:
        if c < maint_c:
            act_vals.append(health_at(c, lam, beta, s))
        else:
            pc = c - maint_c
            act_vals.append(max(0.0, 82.0 * health_at(pc, lam, beta, 1.0) / 100.0))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=h_cycles, y=h_vals, name="Historical",
                              line=dict(color="#00CC88", width=2.5)))
    fig.add_trace(go.Scatter(x=dn_cycles, y=dn_vals, name="Without action (failure path)",
                              line=dict(color="#FF4B4B", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=act_cycles, y=act_vals, name="GotzeEngine - Act now",
                              line=dict(color="#4C78A8", width=2, dash="dot"),
                              fill="tozeroy", fillcolor="rgba(76,120,168,0.06)"))

    fig.add_hline(y=H_FAILURE_THRESHOLD, line_dash="dash",
                  line_color="rgba(255,75,75,0.7)",
                  annotation_text=f"Failure threshold ({H_FAILURE_THRESHOLD})",
                  annotation_position="bottom right")
    fig.add_vline(x=cycle, line_color="rgba(255,255,255,0.35)", line_dash="dot",
                  annotation_text="Now", annotation_position="top")
    fig.add_vrect(x0=maint_c - 2, x1=maint_c + 20,
                  fillcolor="rgba(76,120,168,0.08)", layer="below", line_width=0)

    fig.update_layout(
        title=dict(text="Asset Degradation Trajectory - Weibull Model", font=dict(size=13)),
        height=300, margin=dict(t=45, b=30, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
        legend=dict(orientation="h", y=1.16, x=0, font=dict(size=11)),
        yaxis=dict(range=[0, 110], gridcolor="#1a1a30", title="Health Score"),
        xaxis=dict(gridcolor="#1a1a30", title="Cycle"),
    )
    return fig


def _signal_waterfall(cycle: int | float, flagged_signals: list[str]) -> go.Figure:
    cycle = int(cycle)
    KEY = ["vibration_rms", "temperature_bearing", "pressure_inlet", "kurtosis", "motor_current"]
    specs = {s.name: s for s in SIGNAL_SPECS}
    n, hist = len(KEY), 45
    cycles  = list(range(cycle - hist, cycle + 1))

    fig = make_subplots(
        rows=n, cols=1,
        shared_xaxes=True,
        subplot_titles=[k.replace("_", " ").title() for k in KEY],
        vertical_spacing=0.04,
    )

    rng = np.random.default_rng(42)
    for i, sig in enumerate(KEY, start=1):
        sp = specs.get(sig)
        if not sp:
            continue
        flagged = sig in flagged_signals
        history = []
        for j, c in enumerate(cycles):
            drift = 1.0 + (c / 500.0) * 0.20
            noise = rng.normal(0, sp.baseline * sp.noise_frac * 0.5)
            val   = sp.baseline * drift + noise
            if flagged and j >= hist - 14:
                val *= 2.4 + rng.uniform(0, 0.8)
            history.append(max(0.0, val))

        color    = "#FF4B4B" if flagged else "#4C78A8"
        fill_col = "rgba(255,75,75,0.08)" if flagged else "rgba(76,120,168,0.08)"
        fig.add_trace(
            go.Scatter(x=cycles, y=history, name=sig, showlegend=False,
                       line=dict(color=color, width=1.5),
                       fill="tozeroy", fillcolor=fill_col),
            row=i, col=1,
        )
        if flagged:
            _xref = "x" if i == 1 else f"x{i}"
            _yref = "y domain" if i == 1 else f"y{i} domain"
            fig.add_shape(type="rect",
                          x0=cycle - 14, x1=cycle, y0=0, y1=1,
                          xref=_xref, yref=_yref,
                          fillcolor="rgba(255,75,75,0.07)", layer="below", line_width=0)

    fig.update_layout(
        height=55 * n + 60,
        margin=dict(t=40, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
    )
    fig.update_xaxes(gridcolor="#1a1a30")
    fig.update_yaxes(gridcolor="#1a1a30", showticklabels=False)
    return fig


def _savings_timeline(rul_days: float, base: float = 180_000) -> go.Figure:
    days = list(range(0, min(int(rul_days) + 3, 16)))
    vals = []
    for d in days:
        if d >= rul_days:
            vals.append(0.0)
        else:
            vals.append(base * max(0, 1 - (d / rul_days) ** 1.8))

    colors = ["#FF4B4B" if v == 0 else ("#FFA500" if v < base * 0.4 else "#00CC88") for v in vals]
    labels = [f"${v:,.0f}" if v > 0 else "CRITICAL" for v in vals]

    fig = go.Figure(go.Bar(
        x=[f"D+{d}" for d in days], y=vals,
        marker_color=colors, text=labels, textposition="outside",
    ))
    fig.update_layout(
        title=dict(text="Savings vs. Decision Delay", font=dict(size=13)),
        height=230, margin=dict(t=40, b=10, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="white",
        yaxis=dict(range=[0, base * 1.15], gridcolor="#1a1a30", tickformat="$,.0f"),
        xaxis=dict(gridcolor="#1a1a30"),
        showlegend=False,
    )
    return fig


# ── live feed helpers ─────────────────────────────────────────────────────────

def _generate_live_reading(scenario_key: str, cycle: int,
                            pattern_id: str | None) -> SensorReading:
    base = SCENARIOS[scenario_key]["reading"]
    rng  = np.random.default_rng(int(cycle) % (2**31))

    signals: dict[str, float] = {}
    for sp in SIGNAL_SPECS:
        signals[sp.name] = sp.baseline + rng.normal(0, sp.baseline * sp.noise_frac)

    if pattern_id:
        pat = PATTERNS_BY_ID.get(pattern_id)
        if pat:
            for sig, mult in pat.signals.items():
                if sig in signals:
                    signals[sig] *= mult

    return SensorReading(
        asset_id=base.asset_id,
        asset_type=base.asset_type,
        cycle=cycle,
        signals=signals,
        temp_celsius=base.temp_celsius,
        load_ratio=base.load_ratio,
    )


# ── sidebar ───────────────────────────────────────────────────────────────────

plant_info = FLEET_BY_ID.get(st.session_state.get("selected_plant", "jamnagar"))
if plant_info:
    st.sidebar.markdown(
        f'<div style="margin-bottom:8px">'
        f'<div style="font-weight:800;color:#fff;font-size:0.95rem">{plant_info.name}</div>'
        f'<div style="font-size:0.72rem;color:#33335a;margin-top:2px">{plant_info.location} &middot; {plant_info.sector}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    if st.sidebar.button("<- Back to Fleet", use_container_width=True):
        st.switch_page("pages/fleet_overview.py")
    st.sidebar.divider()

st.sidebar.markdown('<div class="sb-section">Scenario</div>', unsafe_allow_html=True)
scenario_options = {k: v["label"] for k, v in SCENARIOS.items()}
selected = st.sidebar.radio(
    "Choose scenario:",
    options=list(scenario_options.keys()),
    format_func=lambda k: scenario_options[k],
    index=list(scenario_options.keys()).index(
        st.session_state.get("selected_scenario", "A")
    ),
    key="scenario_radio",
)
st.session_state.selected_scenario = selected
st.sidebar.caption(SCENARIOS[selected]["description"])
st.sidebar.divider()

st.sidebar.markdown('<div class="sb-section">Live Feed</div>', unsafe_allow_html=True)
live_toggle = st.sidebar.toggle(
    "Enable Live Mode",
    value=st.session_state.get("live_mode", False),
    key="live_toggle",
)
if live_toggle != st.session_state.live_mode:
    st.session_state.live_mode  = live_toggle
    st.session_state.live_cycle = int(SCENARIOS[selected]["reading"].cycle)

if st.session_state.live_mode:
    st.sidebar.markdown(
        '<span class="pm-live-dot"></span><b style="color:#FF4B4B;font-size:0.8rem">LIVE</b> &mdash; streaming',
        unsafe_allow_html=True,
    )
    speed = st.sidebar.select_slider("Speed:", options=[1, 5, 10],
                                     value=st.session_state.get("live_speed", 1),
                                     key="speed_slider")
    st.session_state.live_speed = speed
    st.sidebar.caption(f"Cycle: {st.session_state.live_cycle}")

st.sidebar.divider()

st.sidebar.markdown('<div class="sb-section">Failure Injector</div>', unsafe_allow_html=True)
pattern_options = {None: "-- Normal operation --"}
for p in FAILURE_PATTERNS:
    pattern_options[p.pattern_id] = p.name

current_pat = st.session_state.get("injected_pattern")
pat_selection = st.sidebar.selectbox(
    "Inject pattern:",
    options=list(pattern_options.keys()),
    format_func=lambda k: pattern_options[k],
    index=list(pattern_options.keys()).index(current_pat) if current_pat in pattern_options else 0,
    key="pattern_select",
)
if pat_selection != current_pat:
    st.session_state.injected_pattern  = pat_selection
    st.session_state.approval_submitted = False

if pat_selection and pat_selection in PATTERNS_BY_ID:
    pat = PATTERNS_BY_ID[pat_selection]
    st.sidebar.caption(pat.description)
    st.sidebar.warning(f"Time to catastrophic: {pat.time_to_catastrophic}")

st.sidebar.divider()

if not st.session_state.live_mode:
    run_btn = st.sidebar.button("Run Analysis", type="primary", use_container_width=True)
else:
    run_btn = False

# ── pipeline execution ────────────────────────────────────────────────────────

if st.session_state.live_mode:
    cycle   = st.session_state.live_cycle
    reading = _generate_live_reading(selected, cycle, st.session_state.injected_pattern)
    with st.spinner(""):
        result = pipeline_run(reading)
    st.session_state.pipeline_result = result
    st.session_state.live_cycle      = int(cycle) + 1

elif run_btn:
    st.session_state.approval_submitted = False
    reading = SCENARIOS[selected]["reading"]
    if st.session_state.injected_pattern:
        pat = PATTERNS_BY_ID[st.session_state.injected_pattern]
        injected_signals = dict(reading.signals)
        for sig, mult in pat.signals.items():
            if sig in injected_signals:
                injected_signals[sig] *= mult
        from src.pipeline.schemas import SensorReading as SR
        reading = SR(
            asset_id=reading.asset_id, asset_type=reading.asset_type,
            cycle=reading.cycle, signals=injected_signals,
            temp_celsius=reading.temp_celsius, load_ratio=reading.load_ratio,
        )
    with st.spinner("Running 5-agent pipeline..."):
        result = pipeline_run(reading)
    st.session_state.pipeline_result = result
    st.sidebar.success(f"Done in {result.pipeline_duration_ms:.1f} ms")
    if result.gotze_triggered:
        st.sidebar.warning("GotzeEngine fired - see Decision tab")

result: PipelineResult | None = st.session_state.pipeline_result

# ── page header ───────────────────────────────────────────────────────────────

_live_badge = (
    '<span class="pm-live-dot"></span>'
    '<span style="color:#FF4B4B;font-weight:800;font-size:0.75rem;letter-spacing:0.1em">LIVE</span>'
    if st.session_state.live_mode else ""
)

st.markdown(
    f'<div class="pm-page-hdr">'
    f'<div>'
    f'<div class="pm-page-title">Plant Overview</div>'
    f'<div class="pm-page-sub">Physics-informed engineering intelligence &nbsp;|&nbsp; GotzeEngine decision loop</div>'
    f'</div>'
    f'<div style="display:flex;gap:10px;align-items:center">{_live_badge}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

if result is None:
    st.info("Select a scenario in the sidebar and click **Run Analysis**, or enable **Live Mode**.")
    st.stop()

r     = result
brief = r.executive_brief
reading_obj  = SCENARIOS[selected]["reading"]
_proj_cycle  = int((st.session_state.live_cycle - 1) if st.session_state.live_mode else reading_obj.cycle)

# ── tabs ──────────────────────────────────────────────────────────────────────

tab_monitor, tab_degrad, tab_signals, tab_savings = st.tabs([
    "Monitor", "Degradation", "Signals", "Savings & Brief"
])

# ────────────────────── TAB 1: Monitor ────────────────────────────────────────
with tab_monitor:
    col1, col2, col3, col4 = st.columns(4)
    hc_color = _hcolor(r.health_report.health_score, r.health_report.rul_days)
    col1.metric("Health Score", f"{r.health_report.health_score:.1f}/100",
                delta="CRITICAL" if r.health_report.health_score < 40 else "OK",
                delta_color="inverse" if r.health_report.health_score < 40 else "normal")
    col2.metric("RUL", f"{r.health_report.rul_days:.1f} d",
                delta=f"CI [{r.health_report.ci_95[0]:.1f}-{r.health_report.ci_95[1]:.1f}] d")
    col3.metric("Severity", r.anomaly_severity.upper())
    col4.metric("Downtime Saved", f"${brief.downtime_saved_estimate:,.0f}",
                delta="GotzeEngine pending" if brief.gotze_pending else "No action needed")

    st.markdown(f"##### Asset: {r.asset_id}")
    gcol, rcol = st.columns([1, 1])
    with gcol:
        st.plotly_chart(
            _gauge(r.asset_id, r.health_report.health_score, r.health_report.rul_days),
            use_container_width=True,
        )
    with rcol:
        st.markdown("**Remaining Useful Life**")
        st.plotly_chart(
            _rul_bar(r.health_report.rul_days, r.health_report.ci_95[0], r.health_report.ci_95[1]),
            use_container_width=True,
        )
        st.caption(r.health_report.physics_text)

    st.divider()

    st.markdown("##### DataSentinel — Anomaly Flags")
    if r.flagged_signals:
        html = " ".join(
            f'<span class="sig-pill">{s}</span>' for s in r.flagged_signals
        )
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.success("All signals nominal — no anomalies detected")

    st.markdown("<br>", unsafe_allow_html=True)

    if r.gotze_triggered:
        if st.session_state.approval_submitted:
            st.success("GotzeEngine decision approved — see Audit Log for record.")
        else:
            st.warning(
                f"GotzeEngine fired — recommended: **{r.gotze_decision.top_intervention.replace('_',' ')}** "
                f"(IIS {r.gotze_decision.iis_score:.3f}) | Awaiting operator approval"
            )
            if st.button("Go to Decision Page ->", type="primary"):
                st.switch_page("pages/gotze_decision.py")
    else:
        st.info("GotzeEngine not triggered — asset within safe thresholds.")

    if brief.critical_alerts:
        st.markdown("##### Executive Brief — Critical Alerts")
        for alert in brief.critical_alerts:
            st.error(alert)

# ────────────────────── TAB 2: Degradation ────────────────────────────────────
with tab_degrad:
    st.markdown("##### Weibull Degradation Model — Dual-Path Projection")
    st.caption(
        "Green = historical trajectory. Red dash = failure path if no action. "
        "Blue dot = GotzeEngine recommended path. Blue band = planned maintenance window."
    )
    st.plotly_chart(
        _weibull_projection(
            reading_obj.asset_type,
            _proj_cycle,
            r.health_report.rul_days,
            reading_obj.temp_celsius,
            reading_obj.load_ratio,
        ),
        use_container_width=True,
    )
    st.markdown(f"**Physics model:** {r.health_report.physics_text}")
    ci = r.health_report.ci_95
    st.markdown(f"**Confidence interval (95%):** {ci[0]:.1f} – {ci[1]:.1f} days")

# ────────────────────── TAB 3: Signals ───────────────────────────────────────
with tab_signals:
    st.markdown("##### Signal Anomaly Waterfall — last 45 cycles")
    if r.flagged_signals:
        flag_html = " ".join(f'<span class="sig-pill">{s}</span>' for s in r.flagged_signals)
        st.markdown(f"Anomalous signals: {flag_html}", unsafe_allow_html=True)
        st.plotly_chart(
            _signal_waterfall(_proj_cycle, r.flagged_signals),
            use_container_width=True,
        )
    else:
        st.success("All 5 signals nominal — no anomalies detected in the last 45 cycles")
        st.plotly_chart(
            _signal_waterfall(_proj_cycle, []),
            use_container_width=True,
        )

# ────────────────────── TAB 4: Savings & Brief ────────────────────────────────
with tab_savings:
    sc_col, bi_col = st.columns([3, 2])

    with sc_col:
        st.markdown("##### Decision Urgency — Savings Erode Daily")
        st.caption("Every day of delay reduces the recoverable saving. Act within the window.")
        st.plotly_chart(
            _savings_timeline(r.health_report.rul_days, brief.downtime_saved_estimate),
            use_container_width=True,
        )

    with bi_col:
        st.markdown("##### Executive Brief")
        st.markdown(f"**Asset:** {r.asset_id}  \n**Severity:** {r.anomaly_severity.upper()}")
        st.markdown(f"**RUL:** {r.health_report.rul_days:.1f} days")
        st.markdown(f"**Downtime saved (estimate):** ${brief.downtime_saved_estimate:,.0f}")

        if brief.gotze_pending:
            st.warning("GotzeEngine action pending approval")
        else:
            st.info("No immediate action required")

        if brief.critical_alerts:
            for alert in brief.critical_alerts:
                st.error(alert)

        if r.rca_narrative:
            st.markdown("**Root Cause (RCA):**")
            st.markdown(f"> {r.rca_narrative}")
            if r.rca_citations:
                st.caption("Sources: " + " | ".join(r.rca_citations))

# ── live mode auto-rerun (outside tabs — runs regardless of active tab) ────────
if st.session_state.live_mode:
    delay = {1: 1.0, 5: 0.25, 10: 0.10}.get(st.session_state.live_speed, 1.0)
    time.sleep(delay)
    st.rerun()
