"""Page 3 — Audit Log: immutable record trail with lineage viewer."""
from __future__ import annotations
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import pandas as pd
import streamlit as st

from src.governance.audit import get_record, list_records


def _decision_badge(decision: str) -> str:
    color = {
        "approved": "#00CC88",
        "rejected": "#FF4B4B",
        "pending": "#FFA500",
        "auto": "#888",
    }.get(decision, "#888")
    return (
        f'<span style="background:{color};padding:2px 8px;border-radius:4px;'
        f'font-size:12px;color:white">{decision.upper()}</span>'
    )


# ── sidebar filters ─────────────────────────────────────────────────────────

st.sidebar.header("Audit Filters")
asset_filter = st.sidebar.text_input("Filter by asset_id:", placeholder="e.g. pump_07")
limit = st.sidebar.slider("Max records:", 10, 100, 30)

# ── page ────────────────────────────────────────────────────────────────────

st.title("Audit Log")
st.caption("Immutable governance trail — every pipeline run logged with full lineage.")

records = list_records(asset_id=asset_filter or None, limit=limit)

if not records:
    st.info("No audit records found. Run a scenario on the Plant Overview page.")
    st.stop()

# Summary row
total = len(records)
pending = sum(1 for r in records if r.decision == "pending")
approved = sum(1 for r in records if r.decision == "approved")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total records", total)
c2.metric("Pending", pending)
c3.metric("Approved", approved)
c4.metric("Rejected", total - pending - approved - sum(1 for r in records if r.decision == "auto"))

st.divider()

# Records table
rows = []
for r in records:
    rows.append({
        "Record ID": r.record_id,
        "Asset": r.asset_id,
        "Timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "Stage": r.stage,
        "Decision": r.decision,
        "IIS Score": f"{r.iis_score:.3f}" if r.iis_score is not None else "—",
        "Lineage Steps": len(r.lineage),
    })

df = pd.DataFrame(rows)

# Colour-code the Decision column
def _style_decision(val: str) -> str:
    colors = {"approved": "color: #00CC88", "rejected": "color: #FF4B4B",
               "pending": "color: #FFA500", "auto": "color: #888888"}
    return colors.get(val, "")

st.dataframe(
    df.style.map(_style_decision, subset=["Decision"]),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# Record detail expander
st.subheader("Record Detail")
record_ids = [r.record_id for r in records]
selected_id = st.selectbox("Select record to inspect:", record_ids, index=0)
record = get_record(selected_id)

if record:
    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"**Asset:** {record.asset_id}")
        st.markdown(f"**Actor:** {record.actor}")
        st.markdown(f"**Stage:** {record.stage}")
        st.markdown(f"**Model used:** {record.model_used or 'N/A'}")
        st.markdown(
            f"**Decision:** " + _decision_badge(record.decision),
            unsafe_allow_html=True,
        )
        if record.reason:
            st.markdown(f"**Reason:** {record.reason}")
    with d2:
        st.markdown(f"**IIS Score:** {record.iis_score:.3f}" if record.iis_score else "**IIS Score:** —")
        st.markdown(f"**Requires approval:** {record.requires_approval}")
        st.markdown(f"**Input ref:** `{record.input_ref}`")
        st.markdown(f"**Timestamp:** {record.timestamp.isoformat()}")

    st.markdown("**Output:**")
    st.json(record.output)

    if record.lineage:
        st.markdown("**Lineage chain:**")
        for i, entry in enumerate(record.lineage, 1):
            st.markdown(
                f"&nbsp;&nbsp;`{i}.` **{entry.actor}** — stage: `{entry.stage}`"
                + (f" | model: `{entry.model_used}`" if entry.model_used else ""),
                unsafe_allow_html=True,
            )
