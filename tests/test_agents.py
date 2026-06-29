"""Lane 1 agent unit tests.

DataSentinel · AssetHealthOracle · GötzeEngine · RCA stub · ExecSummarizer.
"""
from __future__ import annotations

import pytest

from src.agents import data_sentinel, asset_health_oracle, gotze_engine, executive_summarizer
from src.agents.asset_health_oracle import should_trigger_gotze
from src.agents.gotze_engine import CANDIDATES, SAFETY_VETO_CEILING
from src.contracts.ui import AssetHealthReport, GotzeDecision


# ─── DataSentinel ─────────────────────────────────────────────────────────────

def test_sentinel_normal_signals():
    result = data_sentinel.run("pump_00", {"vibration_rms": 0.5, "temperature_bearing": 55.0})
    assert result.severity == "normal"
    assert result.flagged_signals == []


def test_sentinel_flags_high_vibration():
    result = data_sentinel.run("pump_01", {"vibration_rms": 5.0})  # way above baseline 0.5
    assert "vibration_rms" in result.flagged_signals
    assert result.severity in ("warning", "critical")


def test_sentinel_unknown_signals_ignored():
    result = data_sentinel.run("motor_00", {"nonexistent_signal": 999.0})
    assert result.severity == "normal"


def test_sentinel_mahalanobis_nonnegative():
    result = data_sentinel.run("bearing_00", {"kurtosis": 3.0, "crest_factor": 1.4})
    assert result.mahalanobis_distance >= 0.0


def test_sentinel_critical_triggers_on_extreme_z():
    # kurtosis baseline=3.0, noise=0.06*3=0.18 → z=(9-3)/0.18=33 → critical
    result = data_sentinel.run("bearing_01", {"kurtosis": 9.0})
    assert result.severity == "critical"


# ─── AssetHealthOracle ────────────────────────────────────────────────────────

def test_oracle_returns_report():
    report = asset_health_oracle.run("pump_00", "pump", cycle=100.0)
    assert isinstance(report, AssetHealthReport)


def test_oracle_health_in_range():
    report = asset_health_oracle.run("motor_00", "motor", cycle=200.0)
    assert 0.0 <= report.health_score <= 100.0


def test_oracle_rul_positive_early():
    report = asset_health_oracle.run("pump_00", "pump", cycle=0.0)
    assert report.rul_days > 0


def test_trigger_gotze_health_below_40():
    report = AssetHealthReport(
        asset_id="pump_00", health_score=35.0, rul_days=20.0,
        ci_95=(15.0, 25.0), physics_text="test"
    )
    assert should_trigger_gotze(report) is True


def test_trigger_gotze_rul_below_14():
    report = AssetHealthReport(
        asset_id="pump_00", health_score=50.0, rul_days=10.0,
        ci_95=(7.0, 14.0), physics_text="test"
    )
    assert should_trigger_gotze(report) is True


def test_trigger_gotze_no_trigger():
    report = AssetHealthReport(
        asset_id="pump_00", health_score=80.0, rul_days=30.0,
        ci_95=(20.0, 40.0), physics_text="test"
    )
    assert should_trigger_gotze(report) is False


# ─── GötzeEngine ─────────────────────────────────────────────────────────────

def test_gotze_returns_decision():
    dec = gotze_engine.run("pump_00", health_score=35.0, rul_days=10.0)
    assert isinstance(dec, GotzeDecision)


def test_gotze_always_requires_approval():
    dec = gotze_engine.run("pump_00", health_score=35.0, rul_days=10.0)
    assert dec.requires_human_approval is True


def test_gotze_iis_in_range():
    dec = gotze_engine.run("motor_00", health_score=20.0, rul_days=5.0)
    assert 0.0 <= dec.iis_score <= 1.0


def test_gotze_runner_up_different_from_top():
    dec = gotze_engine.run("bearing_00", health_score=30.0, rul_days=8.0)
    assert dec.top_intervention != dec.runner_up


def test_gotze_gap_nonnegative():
    dec = gotze_engine.run("valve_00", health_score=25.0, rul_days=12.0)
    assert dec.iis_gap >= 0.0


def test_gotze_no_vetoed_candidate_wins():
    for cand in CANDIDATES:
        if cand.vetoed:
            dec = gotze_engine.run("pump_00", health_score=10.0, rul_days=1.0)
            assert dec.top_intervention != cand.name


def test_iis_formula_correct():
    """Spot-check IIS calculation on a known candidate."""
    from src.agents.gotze_engine import Intervention, _W
    c = Intervention(
        name="test", description="t",
        delta_p_failure=0.5, delta_downtime_cost=0.5,
        feasibility=0.5, historical_success=0.5, safety_risk_delta=0.5,
    )
    expected = (
        _W["delta_p_failure"] * 0.5 + _W["delta_downtime_cost"] * 0.5
        + _W["feasibility"] * 0.5 + _W["historical_success"] * 0.5
        + _W["safety_risk_delta"] * 0.5
    )
    assert abs(c.iis - expected) < 1e-6


# ─── ExecutiveSummarizer ──────────────────────────────────────────────────────

def _make_report(health: float, rul: float) -> AssetHealthReport:
    return AssetHealthReport(
        asset_id="pump_00", health_score=health, rul_days=rul,
        ci_95=(rul * 0.8, rul * 1.2), physics_text="stub"
    )


def test_summarizer_returns_brief():
    from src.contracts.ui import ExecutiveBrief
    brief = executive_summarizer.run([_make_report(80.0, 30.0)], gotze_decision=None)
    assert isinstance(brief, ExecutiveBrief)


def test_summarizer_no_critical_when_healthy():
    brief = executive_summarizer.run([_make_report(80.0, 30.0)], gotze_decision=None)
    assert brief.critical_alerts == []
    assert brief.gotze_pending == 0


def test_summarizer_critical_when_low_health():
    brief = executive_summarizer.run([_make_report(30.0, 5.0)], gotze_decision=None)
    assert len(brief.critical_alerts) > 0


def test_summarizer_counts_pending_gotze():
    dec = gotze_engine.run("pump_00", health_score=30.0, rul_days=5.0)
    brief = executive_summarizer.run([_make_report(30.0, 5.0)], gotze_decision=dec)
    assert brief.gotze_pending == 1
