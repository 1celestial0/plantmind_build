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

st.set_page_config(
    page_title="PlantMind | GötzeEngine",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state — all keys declared here so every page sees them
_defaults = {
    "pipeline_result":    None,
    "selected_scenario":  "A",
    "approval_submitted": False,
    "selected_plant":     "jamnagar",
    "live_mode":          False,
    "live_cycle":         300,
    "live_speed":         1,
    "injected_pattern":   None,   # pattern_id string or None
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

pg = st.navigation(
    [
        st.Page("pages/fleet_overview.py",  title="Fleet Overview",       icon=":material/grid_view:"),
        st.Page("pages/plant_overview.py",  title="Plant Overview",       icon=":material/factory:"),
        st.Page("pages/gotze_decision.py",  title="GotzeEngine Decision", icon=":material/bolt:"),
        st.Page("pages/audit_log.py",       title="Audit Log",            icon=":material/list:"),
    ],
    position="sidebar",
)
pg.run()
