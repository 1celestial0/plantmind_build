"""PlantMind Dashboard — main entry point.

Run from project root:
    streamlit run src/dashboard/app.py
"""
import sys
from pathlib import Path

# Ensure project root (PlantMind_live/) is on sys.path so `src.*` imports resolve.
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

# Initialise session state keys so all pages see them from the start
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "selected_scenario" not in st.session_state:
    st.session_state.selected_scenario = "A"
if "approval_submitted" not in st.session_state:
    st.session_state.approval_submitted = False

pg = st.navigation(
    [
        st.Page("pages/plant_overview.py",   title="Plant Overview",      icon=":material/factory:"),
        st.Page("pages/gotze_decision.py",   title="GotzeEngine Decision", icon=":material/bolt:"),
        st.Page("pages/audit_log.py",        title="Audit Log",            icon=":material/list:"),
    ],
    position="sidebar",
)
pg.run()
