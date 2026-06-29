"""Pipeline-level request/response schemas (not in LOCKED_STATE contracts)."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from src.contracts.ui import AssetHealthReport, ExecutiveBrief, GotzeDecision
from src.physics.constants import ASSET_TYPES


class SensorReading(BaseModel):
    """Pipeline input — one snapshot of sensor readings for one asset."""

    asset_id: str
    asset_type: str = Field(..., description=f"One of: {ASSET_TYPES}")
    cycle: float = Field(..., ge=0.0)
    signals: dict[str, float] = Field(default_factory=dict)
    temp_celsius: float = Field(default=25.0)
    load_ratio: float = Field(default=1.0, gt=0.0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def model_post_init(self, __context: Any) -> None:
        if self.asset_type not in ASSET_TYPES:
            raise ValueError(f"asset_type must be one of {ASSET_TYPES}, got '{self.asset_type}'")


class PipelineResult(BaseModel):
    """Full pipeline output — one result per SensorReading."""

    asset_id: str
    health_report: AssetHealthReport
    anomaly_severity: str                    # normal | warning | critical
    flagged_signals: list[str]
    gotze_triggered: bool
    gotze_decision: GotzeDecision | None
    rca_narrative: str | None
    rca_citations: list[str]
    executive_brief: ExecutiveBrief
    audit_record_id: str
    pipeline_duration_ms: float
