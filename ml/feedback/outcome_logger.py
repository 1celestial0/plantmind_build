"""Outcome logger — the RL feedback loop. Every approved decision + actual result = training data."""
from __future__ import annotations
import sqlite3
from datetime import datetime
from pathlib import Path

from src.governance.audit import DB_PATH


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_table() -> None:
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS outcomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                audit_record_id TEXT NOT NULL,
                actual_outcome TEXT NOT NULL,
                days_to_event REAL,
                iis_was_correct INTEGER,
                notes TEXT,
                logged_at TEXT
            )
        """)
        c.commit()


def log_outcome(
    audit_record_id: str,
    actual_outcome: str,
    days_to_event: float | None = None,
    notes: str = "",
) -> None:
    """Record what actually happened after a GötzeEngine decision.

    actual_outcome: "failure_prevented" | "failure_occurred" | "false_alarm" | "no_event"
    """
    _ensure_table()
    valid = {"failure_prevented", "failure_occurred", "false_alarm", "no_event"}
    if actual_outcome not in valid:
        raise ValueError(f"actual_outcome must be one of {valid}")
    iis_correct = 1 if actual_outcome == "failure_prevented" else (0 if actual_outcome == "failure_occurred" else None)
    with _conn() as c:
        c.execute(
            "INSERT INTO outcomes (audit_record_id, actual_outcome, days_to_event, iis_was_correct, notes, logged_at) "
            "VALUES (?,?,?,?,?,?)",
            (audit_record_id, actual_outcome, days_to_event, iis_correct, notes, datetime.utcnow().isoformat()),
        )
        c.commit()


def get_feedback_summary() -> dict:
    """Summary stats for the learning panel in the dashboard."""
    _ensure_table()
    try:
        with _conn() as c:
            rows = c.execute(
                "SELECT actual_outcome, iis_was_correct FROM outcomes"
            ).fetchall()
    except Exception:
        rows = []

    if not rows:
        return {"total": 0, "prevented": 0, "false_alarms": 0, "accuracy_pct": 0.0}

    total     = len(rows)
    prevented = sum(1 for r in rows if r["actual_outcome"] == "failure_prevented")
    false_a   = sum(1 for r in rows if r["actual_outcome"] == "false_alarm")
    correct   = [r["iis_was_correct"] for r in rows if r["iis_was_correct"] is not None]
    accuracy  = round(sum(correct) / len(correct) * 100, 1) if correct else 0.0

    return {
        "total":         total,
        "prevented":     prevented,
        "false_alarms":  false_a,
        "accuracy_pct":  accuracy,
    }
