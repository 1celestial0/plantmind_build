"""Page 3 — Audit Log: immutable record trail, RL feedback loop, model health."""
from __future__ import annotations
import sys
from pathlib import Path
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from src.shared.audit import get_record, list_records
from ml.feedback.outcome_logger import get_feedback_summary, log_outcome


def _decision_color(decision: str) -> str:
    return {
        "approved": "#00CC88",
        "rejected": "#FF4B4B",
        "pending":  "#FFA500",
        "auto":     "#555577",
    }.get(decision, "#555577")


def _style_decision(val: str) -> str:
    return {
        "approved": "color: #00CC88",
        "rejected": "color: #FF4B4B",
        "pending":  "color: #FFA500",
        "auto":     "color: #555577",
    }.get(val, "")


# ── sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.markdown('<div class="sb-section">Audit Filters</div>', unsafe_allow_html=True)
asset_filter = st.sidebar.text_input("Filter by asset_id:", placeholder="e.g. pump_07")
limit = st.sidebar.slider("Max records:", 10, 100, 30)
st.sidebar.divider()
st.sidebar.markdown('<div class="sb-section">About</div>', unsafe_allow_html=True)
st.sidebar.caption(
    "Every pipeline run is logged with full lineage. "
    "Approved decisions are traceable to operator and timestamp."
)

# ── page header ───────────────────────────────────────────────────────────────

st.markdown(
    '<div class="pm-page-hdr">'
    '<div>'
    '<div class="pm-page-title">Audit Log & RL Feedback</div>'
    '<div class="pm-page-sub">Immutable governance trail &nbsp;|&nbsp; Operator outcome learning loop</div>'
    '</div>'
    '<span class="pm-badge pm-badge-blue">Governance</span>'
    '</div>',
    unsafe_allow_html=True,
)

records = list_records(asset_id=asset_filter or None, limit=limit)

# ── tabs ──────────────────────────────────────────────────────────────────────

tab_log, tab_rl, tab_health = st.tabs(["Audit Log", "RL Feedback", "Model Health"])

# ────────────────────── TAB 1: Audit Log ─────────────────────────────────────
with tab_log:
    if not records:
        st.info("No audit records found. Run a scenario on the Plant Detail page.")
    else:
        total    = len(records)
        pending  = sum(1 for r in records if r.decision == "pending")
        approved = sum(1 for r in records if r.decision == "approved")
        rejected = sum(1 for r in records if r.decision == "rejected")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Records", total)
        c2.metric("Pending",  pending,  delta_color="off")
        c3.metric("Approved", approved, delta_color="off")
        c4.metric("Rejected", rejected, delta_color="off")

        st.divider()

        rows = []
        for r in records:
            rows.append({
                "Record ID":     r.record_id,
                "Asset":         r.asset_id,
                "Timestamp":     r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "Stage":         r.stage,
                "Decision":      r.decision,
                "IIS Score":     f"{r.iis_score:.3f}" if r.iis_score is not None else "-",
                "Lineage Steps": len(r.lineage),
            })

        df = pd.DataFrame(rows)
        st.dataframe(
            df.style.map(_style_decision, subset=["Decision"]),
            use_container_width=True,
            hide_index=True,
        )

        st.divider()
        st.markdown("##### Record Detail")
        record_ids  = [r.record_id for r in records]
        selected_id = st.selectbox(
            "Select record to inspect:", record_ids, index=0, key="audit_detail_sel"
        )
        record = get_record(selected_id)

        if record:
            d1, d2 = st.columns(2)
            with d1:
                st.markdown(f"**Asset:** {record.asset_id}")
                st.markdown(f"**Actor:** {record.actor}")
                st.markdown(f"**Stage:** {record.stage}")
                st.markdown(f"**Model used:** {record.model_used or 'N/A'}")
                dc = _decision_color(record.decision)
                st.markdown(
                    f'**Decision:** <span style="background:{dc};padding:2px 8px;border-radius:4px;'
                    f'font-size:12px;color:white">{record.decision.upper()}</span>',
                    unsafe_allow_html=True,
                )
                if record.reason:
                    st.markdown(f"**Reason:** {record.reason}")
            with d2:
                if record.iis_score:
                    st.markdown(f"**IIS Score:** {record.iis_score:.3f}")
                else:
                    st.markdown("**IIS Score:** -")
                st.markdown(f"**Requires approval:** {record.requires_approval}")
                st.markdown(f"**Input ref:** `{record.input_ref}`")
                st.markdown(f"**Timestamp:** {record.timestamp.isoformat()}")

            st.markdown("**Output:**")
            st.json(record.output)

            if record.lineage:
                st.markdown("**Lineage chain:**")
                for i, entry in enumerate(record.lineage, 1):
                    model_txt = f" | model: `{entry.model_used}`" if entry.model_used else ""
                    st.markdown(
                        f"&nbsp;&nbsp;`{i}.` **{entry.actor}** - stage: `{entry.stage}`{model_txt}",
                        unsafe_allow_html=True,
                    )

# ────────────────────── TAB 2: RL Feedback ───────────────────────────────────
with tab_rl:
    st.markdown("##### Log Operator Outcome")
    st.caption(
        "After a GotzeEngine recommendation plays out, log what actually happened. "
        "This feeds the RL loop to improve future IIS scoring accuracy."
    )

    records_with_gotze = [r for r in records if r.iis_score is not None]

    if not records_with_gotze:
        st.info(
            "No GotzeEngine decisions found in current records. "
            "Run a scenario that triggers GotzeEngine, then return here."
        )
    else:
        st.markdown('<div class="rl-card"><div class="rl-card-title">Record Outcome</div>',
                    unsafe_allow_html=True)

        col_a, col_b = st.columns([2, 1])
        with col_a:
            rl_record_id = st.selectbox(
                "Audit record ID:",
                [r.record_id for r in records_with_gotze],
                key="rl_record_sel",
            )
        with col_b:
            rl_outcome = st.selectbox(
                "Actual outcome:",
                ["failure_prevented", "failure_occurred", "false_alarm", "no_event"],
                format_func=lambda x: {
                    "failure_prevented": "Failure Prevented",
                    "failure_occurred":  "Failure Occurred",
                    "false_alarm":       "False Alarm",
                    "no_event":          "No Event",
                }[x],
                key="rl_outcome_sel",
            )

        col_c, col_d = st.columns(2)
        with col_c:
            rl_days = st.number_input(
                "Days to event (optional):",
                min_value=0.0, max_value=365.0, value=0.0, step=0.5,
                key="rl_days_in",
            )
        with col_d:
            rl_notes = st.text_input(
                "Notes (optional):", key="rl_notes_in",
                placeholder="e.g. 'Bearing replaced on day 5'"
            )

        st.markdown("</div>", unsafe_allow_html=True)

        _outcome_labels = {
            "failure_prevented": ("pm-badge-ok",   "GOOD - IIS correct"),
            "failure_occurred":  ("pm-badge-crit", "BAD - missed failure"),
            "false_alarm":       ("pm-badge-warn", "FALSE ALARM - over-triggered"),
            "no_event":          ("pm-badge-blue", "NO EVENT - normal operation"),
        }
        badge_cls, badge_txt = _outcome_labels[rl_outcome]
        st.markdown(
            f'Outcome impact: <span class="pm-badge {badge_cls}">{badge_txt}</span>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Submit Outcome", type="primary", key="rl_submit"):
            log_outcome(
                audit_record_id=rl_record_id,
                actual_outcome=rl_outcome,
                days_to_event=float(rl_days) if rl_days > 0 else None,
                notes=rl_notes,
            )
            st.success(
                f"Outcome '{rl_outcome}' logged for {rl_record_id}. "
                "Model accuracy will update — check the Model Health tab."
            )
            st.rerun()

# ────────────────────── TAB 3: Model Health ───────────────────────────────────
with tab_health:
    st.markdown("##### RL Model Health")
    st.caption(
        "Aggregated feedback from operator outcomes. "
        "Used to calibrate IIS scoring and trigger thresholds."
    )

    fb = get_feedback_summary()

    if fb["total"] == 0:
        st.info(
            "No outcomes logged yet. Use the **RL Feedback** tab to record what happened "
            "after GotzeEngine recommendations. Each logged outcome improves model calibration."
        )
    else:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Outcomes Logged",    fb["total"])
        m2.metric("Failures Prevented", fb["prevented"],
                  delta=f"{fb['prevented']/fb['total']*100:.0f}% of total",
                  delta_color="normal")
        m3.metric("False Alarms",       fb["false_alarms"],
                  delta=f"{fb['false_alarms']/fb['total']*100:.0f}% of total",
                  delta_color="inverse")
        m4.metric("IIS Accuracy",
                  f"{fb['accuracy_pct']:.1f}%",
                  delta="vs. baseline 75%",
                  delta_color="normal" if fb["accuracy_pct"] >= 75 else "inverse")

        st.divider()

        pie = go.Figure(go.Pie(
            labels=["Failure Prevented", "False Alarm", "Other"],
            values=[
                fb["prevented"],
                fb["false_alarms"],
                fb["total"] - fb["prevented"] - fb["false_alarms"],
            ],
            marker_colors=["#00CC88", "#FFA500", "#333355"],
            hole=0.55,
            textinfo="label+percent",
            textfont=dict(size=12),
        ))
        pie.update_layout(
            height=260, margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)", font_color="white",
            showlegend=False,
        )

        lc, rc = st.columns([1, 1])
        with lc:
            st.plotly_chart(pie, use_container_width=True)
        with rc:
            prev_pct  = fb["prevented"]    / fb["total"] * 100
            false_pct = fb["false_alarms"] / fb["total"] * 100
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f'<div style="font-size:0.88rem;line-height:2.2">'
                f'<div><span style="color:#00CC88;font-weight:800">{fb["prevented"]}</span>'
                f' failures prevented ({prev_pct:.0f}%)</div>'
                f'<div><span style="color:#FFA500;font-weight:800">{fb["false_alarms"]}</span>'
                f' false alarms ({false_pct:.0f}%)</div>'
                f'<div style="margin-top:12px;color:#33335a;font-size:0.75rem">'
                f'Target accuracy: >80% for production confidence.</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.divider()
        if fb["accuracy_pct"] >= 80:
            st.success("Model is well-calibrated. IIS scoring is reliable.")
        elif fb["total"] < 10:
            st.info("Calibrating — log more outcomes to improve model confidence.")
        else:
            st.warning("Accuracy below target. Review IIS weights with engineering team.")
