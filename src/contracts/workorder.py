"""WorkOrder contract for LOCKED_STATE §1 MaintenanceScheduler / DNA F-03.

Production target is SAP PM / Maximo REST integration; the hackathon target is a
queued work-order record paired with an audit entry after human approval.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Priority = Literal["low", "medium", "high", "critical"]
WorkOrderStatus = Literal["queued", "scheduled", "in_progress", "completed", "cancelled"]


class WorkOrder(BaseModel):
    """Approved Götze action queued for maintenance execution."""

    work_order_id: str = Field(..., pattern=r"^WO-[A-Za-z0-9_-]+$")
    asset_id: str = Field(..., min_length=1)
    intervention: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    priority: Priority = "high"
    status: WorkOrderStatus = "queued"
    created_at: datetime
    scheduled_for: datetime | None = None
    iis_score: float | None = Field(default=None, ge=0.0, le=1.0)
    approved_by: str = Field(..., min_length=1)
    source_decision_ref: str = Field(..., min_length=1)
    audit_record_id: str | None = None
    notes: str | None = None

    model_config = {"frozen": True}
