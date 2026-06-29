"""PhysicsModelInterface output — Lane 2 owns; Lane 1 consumes."""

from pydantic import BaseModel, Field


class PhysicsModelOutput(BaseModel):
    """LOCKED_STATE §4 — PhysicsModelInterface output shape."""

    health_index: float = Field(..., ge=0.0, le=100.0, description="Asset health 0–100")
    rul_estimate: float = Field(..., ge=0.0, description="RUL in days")
    confidence_interval: tuple[float, float] = Field(
        ...,
        description="95% CI for RUL in days (low, high)",
    )
    physics_explanation: str = Field(..., min_length=1)

    model_config = {"frozen": True}