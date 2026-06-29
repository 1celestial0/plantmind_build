"""GET/PATCH /api/v1/decisions — human approval gate for GötzeDecisions."""
from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.governance.audit import get_record, list_records, update_decision

router = APIRouter()


class ApprovalRequest(BaseModel):
    decision: Literal["approved", "rejected"]
    reason: str | None = None


@router.get("/decisions")
def list_decisions(asset_id: str | None = None, limit: int = 20):
    """List pending GötzeDecisions awaiting approval."""
    records = list_records(asset_id=asset_id, stage="pipeline_complete", limit=limit)
    pending = [r for r in records if r.decision == "pending"]
    return [_record_summary(r) for r in pending]


@router.get("/decisions/{record_id}")
def get_decision(record_id: str):
    record = get_record(record_id)
    if not record:
        raise HTTPException(404, f"Audit record '{record_id}' not found")
    return _record_summary(record)


@router.patch("/decisions/{record_id}")
def approve_decision(record_id: str, body: ApprovalRequest):
    """Human operator approves or rejects a GötzeDecision."""
    record = get_record(record_id)
    if not record:
        raise HTTPException(404, f"Audit record '{record_id}' not found")
    if record.decision != "pending":
        raise HTTPException(409, f"Decision already '{record.decision}' — cannot change")
    updated = update_decision(record_id, body.decision, body.reason)
    return _record_summary(updated)


def _record_summary(record) -> dict:
    return {
        "record_id": record.record_id,
        "asset_id": record.asset_id,
        "timestamp": record.timestamp.isoformat(),
        "iis_score": record.iis_score,
        "decision": record.decision,
        "reason": record.reason,
        "output": record.output,
    }
