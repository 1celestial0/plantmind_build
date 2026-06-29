"""SQLite-backed audit store — LOCKED_STATE §4 AuditRecord persistence.

DB path: ml/data/audit.db (created on first write).
Records are immutable once written; decisions updated via separate column.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from src.contracts.audit import AuditRecord, LineageEntry

DB_PATH = Path("ml/data/audit.db")

DecisionType = Literal["approved", "rejected", "pending", "auto"]

_CREATE_SQL = """
CREATE TABLE IF NOT EXISTS audit_records (
    record_id   TEXT PRIMARY KEY,
    timestamp   TEXT NOT NULL,
    asset_id    TEXT NOT NULL,
    stage       TEXT NOT NULL,
    actor       TEXT NOT NULL,
    model_used  TEXT,
    input_ref   TEXT NOT NULL,
    output_json TEXT NOT NULL,
    iis_score   REAL,
    requires_approval INTEGER NOT NULL DEFAULT 1,
    decision    TEXT NOT NULL DEFAULT 'pending',
    reason      TEXT,
    lineage_json TEXT NOT NULL DEFAULT '[]'
);
"""


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute(_CREATE_SQL)
    conn.commit()
    return conn


def write_record(record: AuditRecord) -> str:
    """Persist a new AuditRecord. Returns record_id."""
    conn = _connect()
    conn.execute(
        """
        INSERT OR REPLACE INTO audit_records
          (record_id, timestamp, asset_id, stage, actor, model_used,
           input_ref, output_json, iis_score, requires_approval,
           decision, reason, lineage_json)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            record.record_id,
            record.timestamp.isoformat(),
            record.asset_id,
            record.stage,
            record.actor,
            record.model_used,
            record.input_ref,
            json.dumps(record.output),
            record.iis_score,
            int(record.requires_approval),
            record.decision,
            record.reason,
            json.dumps([e.model_dump(mode="json") for e in record.lineage]),
        ),
    )
    conn.commit()
    conn.close()
    return record.record_id


def get_record(record_id: str) -> AuditRecord | None:
    conn = _connect()
    row = conn.execute(
        "SELECT * FROM audit_records WHERE record_id = ?", (record_id,)
    ).fetchone()
    conn.close()
    return _row_to_record(row) if row else None


def list_records(
    asset_id: str | None = None,
    stage: str | None = None,
    limit: int = 50,
) -> list[AuditRecord]:
    conn = _connect()
    where = []
    params: list = []
    if asset_id:
        where.append("asset_id = ?")
        params.append(asset_id)
    if stage:
        where.append("stage = ?")
        params.append(stage)
    sql = "SELECT * FROM audit_records"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return [_row_to_record(r) for r in rows]


def update_decision(
    record_id: str,
    decision: DecisionType,
    reason: str | None = None,
) -> AuditRecord | None:
    """Update decision on a pending record. Returns updated record or None if not found."""
    conn = _connect()
    conn.execute(
        "UPDATE audit_records SET decision = ?, reason = ? WHERE record_id = ?",
        (decision, reason, record_id),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM audit_records WHERE record_id = ?", (record_id,)
    ).fetchone()
    conn.close()
    return _row_to_record(row) if row else None


def _row_to_record(row: sqlite3.Row) -> AuditRecord:
    lineage_raw = json.loads(row["lineage_json"])
    lineage = [LineageEntry(**e) for e in lineage_raw]
    return AuditRecord(
        record_id=row["record_id"],
        timestamp=datetime.fromisoformat(row["timestamp"]),
        asset_id=row["asset_id"],
        stage=row["stage"],
        actor=row["actor"],
        model_used=row["model_used"],
        input_ref=row["input_ref"],
        output=json.loads(row["output_json"]),
        iis_score=row["iis_score"],
        requires_approval=bool(row["requires_approval"]),
        decision=row["decision"],
        reason=row["reason"],
        lineage=lineage,
    )
