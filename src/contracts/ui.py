"""UI-consumed JSON — Lane 1 owns; Lane 3 consumes."""

from pydantic import BaseModel, Field


class GotzeDecision(BaseModel):
    """LOCKED_STATE §4 — GötzeEngine decision for dashboard."""

    top_intervention: str
    iis_score: float = Field(..., ge=0.0, le=1.0)
    runner_up: str
    iis_gap: float = Field(..., ge=0.0)
    narrative: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    requires_human_approval: bool = True

    model_config = {"frozen": True}


class AssetHealthReport(BaseModel):
    """LOCKED_STATE §4 — health summary per asset."""

    asset_id: str
    health_score: float = Field(..., ge=0.0, le=100.0)
    rul_days: float = Field(..., ge=0.0)
    ci_95: tuple[float, float] = Field(..., description="RUL 95% CI in days")
    physics_text: str

    model_config = {"frozen": True}


class ExecutiveBrief(BaseModel):
    """LOCKED_STATE §4 — leadership rollup."""

    critical_alerts: list[str]
    gotze_pending: int = Field(..., ge=0)
    downtime_saved_estimate: float = Field(..., ge=0.0)

    model_config = {"frozen": True}