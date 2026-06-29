"""AuditRecord — Lane 1 owns; all lanes consume for lineage."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class LineageEntry(BaseModel):
    """Single step in an audit lineage chain."""

    stage: str
    actor: str
    model_used: str | None = None
    timestamp: datetime

    model_config = {"frozen": True}


DecisionType = Literal["approved", "rejected", "pending", "auto"]


class AuditRecord(BaseModel):
    """LOCKED_STATE §4 — immutable governance record."""

    record_id: str
    timestamp: datetime
    asset_id: str
    stage: str
    actor: str
    model_used: str | None = None
    input_ref: str
    output: dict[str, Any]
    iis_score: float | None = Field(default=None, ge=0.0, le=1.0)
    requires_approval: bool = True
    decision: DecisionType = "pending"
    reason: str | None = None
    lineage: list[LineageEntry] = Field(default_factory=list)

    model_config = {"frozen": True}