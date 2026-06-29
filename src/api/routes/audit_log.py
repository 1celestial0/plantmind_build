"""GET /api/v1/audit — audit log read endpoints."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.governance.audit import get_record, list_records

router = APIRouter()


@router.get("/audit")
def list_audit(asset_id: str | None = None, limit: int = 50):
    records = list_records(asset_id=asset_id, limit=limit)
    return [
        {
            "record_id": r.record_id,
            "asset_id": r.asset_id,
            "timestamp": r.timestamp.isoformat(),
            "stage": r.stage,
            "actor": r.actor,
            "decision": r.decision,
            "iis_score": r.iis_score,
            "lineage_steps": len(r.lineage),
        }
        for r in records
    ]


@router.get("/audit/{record_id}")
def get_audit_record(record_id: str):
    record = get_record(record_id)
    if not record:
        raise HTTPException(404, f"Audit record '{record_id}' not found")
    return record.model_dump(mode="json")
