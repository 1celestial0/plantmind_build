"""PlantMind Dashboard — main entry point.

Run from project root:
    streamlit run src/dashboard/app.py
"""
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st
from src.dashboard.styles import GLOBAL_CSS

st.set_page_config(
    page_title="PlantMind | GotzeEngine",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject global styles first
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Session state — all keys declared here so every page sees them
_defaults = {
    "pipeline_result":    None,
    "selected_scenario":  "A",
    "approval_submitted": False,
    "selected_plant":     "jamnagar",
    "live_mode":          False,
    "live_cycle":         300,
    "live_speed":         1,
    "injected_pattern":   None,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Navigation — hidden so our custom tab bar is the only nav
pg = st.navigation(
    [
        st.Page("pages/fleet_overview.py",  title="Fleet Overview",       icon=":material/grid_view:"),
        st.Page("pages/plant_overview.py",  title="Plant Overview",       icon=":material/factory:"),
        st.Page("pages/gotze_decision.py",  title="GotzeEngine Decision", icon=":material/bolt:"),
        st.Page("pages/audit_log.py",       title="Audit Log",            icon=":material/list:"),
    ],
    position="hidden",
)

# ── Sidebar brand (appears on every page above page-specific controls) ──────
with st.sidebar:
    st.markdown(
        '<div class="sb-brand">'
        '<div class="sb-brand-name">PlantMind x GotzeEngine</div>'
        '<div class="sb-brand-sub">LTTS Engineering Intelligence</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.divider()

# ── Animated gradient bar ────────────────────────────────────────────────────
st.markdown('<div class="pm-topbar"></div>', unsafe_allow_html=True)

# ── Horizontal tab navigation (page_link — auto-marks active page) ───────────
st.markdown('<div class="pm-nav-bar">', unsafe_allow_html=True)
_nc = st.columns([1, 1, 1, 1, 5])
with _nc[0]:
    st.page_link("pages/fleet_overview.py", label="Fleet Operations", use_container_width=True)
with _nc[1]:
    st.page_link("pages/plant_overview.py", label="Plant Detail",     use_container_width=True)
with _nc[2]:
    st.page_link("pages/gotze_decision.py", label="GotzeEngine",      use_container_width=True)
with _nc[3]:
    st.page_link("pages/audit_log.py",      label="Audit & RL",       use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Run active page ──────────────────────────────────────────────────────────
pg.run()
