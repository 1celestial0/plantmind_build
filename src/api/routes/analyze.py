"""POST /api/v1/analyze — full 5-agent pipeline trigger."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from src.pipeline import run as pipeline_run
from src.pipeline.schemas import SensorReading

router = APIRouter()


@router.post("/analyze")
def analyze(reading: SensorReading):
    """
    Run the full PlantMind pipeline on one sensor snapshot.

    Returns PipelineResult including health, anomaly flags, GötzeDecision
    (if triggered), RCA narrative, executive brief, and audit record ID.
    GötzeDecision always requires_human_approval = True.
    """
    try:
        result = pipeline_run(reading)
    except KeyError as exc:
        raise HTTPException(422, str(exc)) from exc
    return result.model_dump()
