"""Pipeline orchestrator + governance integration tests."""
from __future__ import annotations

import pytest

from src.pipeline import run as pipeline_run
from src.pipeline.schemas import PipelineResult, SensorReading


def _reading(health_cycle: float = 100.0, asset_type: str = "pump") -> SensorReading:
    return SensorReading(
        asset_id=f"{asset_type}_test",
        asset_type=asset_type,
        cycle=health_cycle,
        signals={"vibration_rms": 0.5, "temperature_bearing": 55.0},
        temp_celsius=25.0,
        load_ratio=1.0,
    )


def test_pipeline_returns_result():
    result = pipeline_run(_reading(100.0))
    assert isinstance(result, PipelineResult)


def test_pipeline_audit_id_nonempty():
    result = pipeline_run(_reading(100.0))
    assert result.audit_record_id.startswith("AUD-")


def test_pipeline_no_gotze_when_healthy():
    result = pipeline_run(_reading(50.0, "motor"))  # early cycle, healthy
    assert result.gotze_triggered is False
    assert result.gotze_decision is None


def test_pipeline_gotze_triggers_at_critical_cycle():
    # bearing life_ref=350; cycle 340 should give health << 40
    result = pipeline_run(_reading(340.0, "bearing"))
    assert result.gotze_triggered is True
    assert result.gotze_decision is not None
    assert result.gotze_decision.requires_human_approval is True


def test_pipeline_rca_only_when_gotze_fires():
    healthy = pipeline_run(_reading(50.0, "motor"))
    assert healthy.rca_narrative is None

    critical = pipeline_run(_reading(340.0, "bearing"))
    assert critical.rca_narrative is not None


def test_pipeline_executive_brief_present():
    result = pipeline_run(_reading(100.0))
    assert result.executive_brief is not None


def test_pipeline_duration_positive():
    result = pipeline_run(_reading(100.0))
    assert result.pipeline_duration_ms > 0


def test_pipeline_invalid_asset_type():
    with pytest.raises(Exception):  # ValueError from SensorReading validation
        _reading(100.0, "turbine")


def test_pipeline_audit_record_persisted():
    from src.shared.audit import get_record
    result = pipeline_run(_reading(340.0, "pump"))
    record = get_record(result.audit_record_id)
    assert record is not None
    assert record.asset_id == "pump_test"


def test_pipeline_all_asset_types():
    for atype in ["pump", "compressor", "motor", "valve"]:
        result = pipeline_run(_reading(50.0, atype))
        assert result.health_report.health_score > 0
