"""Validate src/contracts match LOCKED_STATE §4."""

from datetime import datetime, timezone

import pytest

from src.contracts import (
    AssetHealthReport,
    AuditRecord,
    ExecutiveBrief,
    GotzeDecision,
    LineageEntry,
    PhysicsModelOutput,
)


def test_physics_model_output_roundtrip():
    m = PhysicsModelOutput(
        health_index=38.2,
        rul_estimate=12.4,
        confidence_interval=(9.1, 16.2),
        physics_explanation="Weibull H(t) crossed threshold",
    )
    assert m.rul_estimate == 12.4
    assert m.confidence_interval == (9.1, 16.2)


def test_gotze_decision_requires_approval():
    d = GotzeDecision(
        top_intervention="reduce_load",
        iis_score=0.74,
        runner_up="flush_lubrication",
        iis_gap=0.18,
        narrative="Reduce load now; schedule seal swap.",
        confidence=0.85,
    )
    assert d.requires_human_approval is True


def test_asset_health_report():
    r = AssetHealthReport(
        asset_id="pump_07",
        health_score=38.0,
        rul_days=12.0,
        ci_95=(9.0, 15.0),
        physics_text="Seal contamination trend",
    )
    assert r.asset_id == "pump_07"


def test_executive_brief():
    b = ExecutiveBrief(
        critical_alerts=["pump_07 RED"],
        gotze_pending=1,
        downtime_saved_estimate=125000.0,
    )
    assert b.gotze_pending == 1


def test_audit_record_with_lineage():
    ts = datetime.now(timezone.utc)
    rec = AuditRecord(
        record_id="AUD-001",
        timestamp=ts,
        asset_id="pump_07",
        stage="gotze_decision",
        actor="GotzeEngine",
        input_ref="health:pump_07",
        output={"top_intervention": "reduce_load"},
        iis_score=0.74,
        lineage=[LineageEntry(stage="health", actor="AssetHealthOracle", timestamp=ts)],
    )
    assert rec.decision == "pending"
    assert len(rec.lineage) == 1