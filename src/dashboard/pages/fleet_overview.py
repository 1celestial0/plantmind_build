"""Page 0 — Fleet Operations Center: all LTTS-managed plants at a glance."""
from __future__ import annotations
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import plotly.graph_objects as go
import streamlit as st

from src.dashboard.fleet_data import FLEET, SECTOR_COLORS
from ml.feedback.outcome_logger import get_feedback_summary


# ── helpers ──────────────────────────────────────────────────────────────────

def _health_color(score: int) -> str:
    if score < 50: return "#FF4B4B"
    if score < 75: return "#FFA500"
    return "#00CC88"


def _plant_card_html(plant) -> str:
    hc  = _health_color(plant.fleet_health)
    sc  = SECTOR_COLORS.get(plant.sector, "#888888")
    bc  = "#FF4B4B" if plant.critical > 3 else ("#FFA500" if plant.critical > 0 else "#00CC88")
    sav = f"${plant.projected_savings:,.0f}"
    w   = plant.fleet_health

    return f"""
<div style="
    background:#1a1a2e;
    border:2px solid {bc};
    border-radius:12px;
    padding:20px;
    margin-bottom:4px;
    font-family:sans-serif;
">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">
    <div>
      <div style="font-size:17px;font-weight:bold;color:white;margin-bottom:3px">{plant.name}</div>
      <div style="font-size:12px;color:#888">{plant.location}</div>
    </div>
    <div style="
      background:{sc}22;border:1px solid {sc};color:{sc};
      padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;white-space:nowrap
    ">{plant.sector}</div>
  </div>

  <div style="margin-bottom:14px">
    <div style="display:flex;justify-content:space-between;margin-bottom:4px">
      <span style="font-size:12px;color:#aaa">Fleet Health</span>
      <span style="font-size:14px;font-weight:bold;color:{hc}">{plant.fleet_health}/100</span>
    </div>
    <div style="background:#333;border-radius:4px;height:8px;overflow:hidden">
      <div style="background:{hc};width:{w}%;height:100%;border-radius:4px"></div>
    </div>
  </div>

  <div style="display:flex;gap:10px;margin-bottom:14px">
    <div style="flex:1;text-align:center;background:#FF4B4B22;border-radius:8px;padding:8px">
      <div style="font-size:22px;font-weight:bold;color:#FF4B4B">{plant.critical}</div>
      <div style="font-size:10px;color:#FF4B4B;font-weight:600">CRITICAL</div>
    </div>
    <div style="flex:1;text-align:center;background:#FFA50022;border-radius:8px;padding:8px">
      <div style="font-size:22px;font-weight:bold;color:#FFA500">{plant.warning}</div>
      <div style="font-size:10px;color:#FFA500;font-weight:600">WARNING</div>
    </div>
    <div style="flex:1;text-align:center;background:#00CC8822;border-radius:8px;padding:8px">
      <div style="font-size:22px;font-weight:bold;color:#00CC88">{plant.ok}</div>
      <div style="font-size:10px;color:#00CC88;font-weight:600">OK</div>
    </div>
  </div>

  <div style="display:flex;justify-content:space-between;padding-top:10px;border-top:1px solid #333">
    <div>
      <div style="font-size:11px;color:#888">Pending Decisions</div>
      <div style="font-size:16px;font-weight:bold;color:{'#FFA500' if plant.pending_decisions > 0 else '#00CC88'}">{plant.pending_decisions}</div>
    </div>
    <div style="text-align:right">
      <div style="font-size:11px;color:#888">Projected Savings</div>
      <div style="font-size:16px;font-weight:bold;color:#00CC88">{sav}</div>
    </div>
  </div>
</div>
"""


# ── page ─────────────────────────────────────────────────────────────────────

st.title("PlantMind — Fleet Operations Center")
st.caption("LTTS Intelligent Asset Intelligence | GötzeEngine Physics-Informed Decision Loop")

# ── top KPIs ──────────────────────────────────────────────────────────────────
total_critical = sum(p.critical for p in FLEET)
total_pending  = sum(p.pending_decisions for p in FLEET)
total_savings  = sum(p.projected_savings for p in FLEET)
fleet_avg      = sum(p.fleet_health for p in FLEET) // len(FLEET)
fb             = get_feedback_summary()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Plants Monitored",   len(FLEET), delta="5 active")
k2.metric("Assets Critical",    total_critical,
          delta="Requires action", delta_color="inverse")
k3.metric("Pending Decisions",  total_pending, delta_color="off")
k4.metric("Projected Savings",  f"${total_savings:,.0f}", delta="if all actioned")
k5.metric("Model Accuracy",
          f"{fb['accuracy_pct']:.0f}%" if fb["total"] else "Calibrating",
          delta=f"{fb['total']} outcomes logged" if fb["total"] else "Collecting data",
          delta_color="off")

st.divider()

# ── fleet health bar chart ─────────────────────────────────────────────────
fig = go.Figure()
names  = [p.name for p in FLEET]
scores = [p.fleet_health for p in FLEET]
colors = [_health_color(h) for h in scores]

fig.add_trace(go.Bar(
    x=names, y=scores,
    marker_color=colors,
    text=[f"{h}/100" for h in scores],
    textposition="outside",
    width=0.5,
))
fig.add_hline(y=75, line_dash="dash", line_color="rgba(255,165,0,0.5)",
              annotation_text="Warning threshold (75)")
fig.add_hline(y=50, line_dash="dash", line_color="rgba(255,75,75,0.5)",
              annotation_text="Critical threshold (50)")
fig.update_layout(
    height=270,
    margin=dict(t=20, b=10, l=20, r=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    yaxis=dict(range=[0, 115], gridcolor="#222", title="Fleet Health Score"),
    xaxis=dict(gridcolor="#222"),
    showlegend=False,
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Plant Status — Click to inspect")

# ── plant cards 2-column ─────────────────────────────────────────────────────
cols = st.columns(2)
for i, plant in enumerate(FLEET):
    with cols[i % 2]:
        st.markdown(_plant_card_html(plant), unsafe_allow_html=True)
        if st.button(
            f"Inspect {plant.name} →",
            key=f"nav_{plant.plant_id}",
            use_container_width=True,
            type="primary" if plant.critical > 0 else "secondary",
        ):
            st.session_state.selected_plant    = plant.plant_id
            st.session_state.selected_scenario = plant.scenario_key
            st.session_state.pipeline_result   = None
            st.session_state.approval_submitted = False
            st.switch_page("pages/plant_overview.py")
