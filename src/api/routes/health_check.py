"""GET /api/v1/health — service liveness + GET /api/v1/asset/{asset_id}/health."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from src.agents.asset_health_oracle import run as oracle_run
from src.physics.constants import ASSET_TYPES

router = APIRouter()


@router.get("/health")
def service_health():
    return {"status": "ok", "service": "PlantMind API v1"}


@router.get("/asset/{asset_id}/health")
def asset_health(
    asset_id: str,
    asset_type: str = Query(..., description=f"One of: {ASSET_TYPES}"),
    cycle: float = Query(..., ge=0.0),
    temp_celsius: float = Query(default=25.0),
    load_ratio: float = Query(default=1.0, gt=0.0),
):
    """Return health snapshot for one asset — no side effects, no audit write."""
    if asset_type not in ASSET_TYPES:
        raise HTTPException(422, f"asset_type must be one of {ASSET_TYPES}")
    report = oracle_run(
        asset_id=asset_id,
        asset_type=asset_type,
        cycle=cycle,
        temp_celsius=temp_celsius,
        load_ratio=load_ratio,
    )
    return report.model_dump()
