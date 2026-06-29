"""Main pipeline orchestrator — chains all 5 agents with audit logging.

Flow:
  SensorReading
  → DataSentinel         (always)
  → AssetHealthOracle    (always)
  → GötzeEngine          (if trigger thresholds met)
  → RootCauseAnalyst     (if GötzeEngine fired)
  → ExecutiveSummarizer  (always)
  → AuditRecord written  (always)
  → PipelineResult

All agents are non-autonomous and explainable. Approval gate enforced by GötzeEngine.
"""
from __future__ import annotations

import time
import uuid
from datetime import datetime, timezone

from src.agents import (
    asset_health_oracle,
    data_sentinel,
    executive_summarizer,
    gotze_engine,
    root_cause_analyst,
)
from src.agents.asset_health_oracle import should_trigger_gotze
from src.contracts.audit import AuditRecord, LineageEntry
from src.governance.audit import write_record
from .schemas import PipelineResult, SensorReading


def run(reading: SensorReading) -> PipelineResult:
    """Execute full 5-agent pipeline for one sensor snapshot."""
    t0 = time.perf_counter()
    lineage: list[LineageEntry] = []
    now = datetime.now(timezone.utc)

    # ── Stage 1: DataSentinel ────────────────────────────────────────────────
    sentinel = data_sentinel.run(reading.asset_id, reading.signals)
    lineage.append(LineageEntry(stage="anomaly_detection", actor="DataSentinel", timestamp=now))

    # ── Stage 2: AssetHealthOracle ───────────────────────────────────────────
    health_report = asset_health_oracle.run(
        asset_id=reading.asset_id,
        asset_type=reading.asset_type,
        cycle=reading.cycle,
        temp_celsius=reading.temp_celsius,
        load_ratio=reading.load_ratio,
    )
    lineage.append(LineageEntry(stage="health_assessment", actor="AssetHealthOracle", timestamp=now))

    # ── Stage 3: Trigger check ───────────────────────────────────────────────
    trigger_health = should_trigger_gotze(health_report)
    trigger_sentinel = sentinel.severity == "critical"
    gotze_triggered = trigger_health or trigger_sentinel

    gotze_decision = None
    rca_result = None

    if gotze_triggered:
        # ── Stage 4: GötzeEngine ────────────────────────────────────────────
        gotze_decision = gotze_engine.run(
            asset_id=reading.asset_id,
            health_score=health_report.health_score,
            rul_days=health_report.rul_days,
            flagged_signals=sentinel.flagged_signals,
        )
        lineage.append(LineageEntry(stage="gotze_decision", actor="GotzeEngine", timestamp=now))

        # ── Stage 5: RootCauseAnalyst ────────────────────────────────────────
        rca_result = root_cause_analyst.run(
            asset_id=reading.asset_id,
            asset_type=reading.asset_type,
            flagged_signals=sentinel.flagged_signals,
            rul_days=health_report.rul_days,
            health_score=health_report.health_score,
        )
        lineage.append(LineageEntry(stage="root_cause", actor="RootCauseAnalyst", timestamp=now))

    # ── Stage 6: ExecutiveSummarizer ─────────────────────────────────────────
    brief = executive_summarizer.run(
        health_reports=[health_report],
        gotze_decision=gotze_decision,
    )
    lineage.append(LineageEntry(stage="executive_summary", actor="ExecutiveSummarizer", timestamp=now))

    # ── Audit record ─────────────────────────────────────────────────────────
    record_id = f"AUD-{uuid.uuid4().hex[:12].upper()}"
    audit = AuditRecord(
        record_id=record_id,
        timestamp=now,
        asset_id=reading.asset_id,
        stage="pipeline_complete",
        actor="Orchestrator",
        input_ref=f"cycle:{reading.cycle}|asset:{reading.asset_id}",
        output={
            "health_score": health_report.health_score,
            "rul_days": health_report.rul_days,
            "severity": sentinel.severity,
            "gotze_triggered": gotze_triggered,
            "top_intervention": gotze_decision.top_intervention if gotze_decision else None,
        },
        iis_score=gotze_decision.iis_score if gotze_decision else None,
        requires_approval=bool(gotze_decision),
        decision="pending" if gotze_decision else "auto",
        lineage=lineage,
    )
    write_record(audit)

    duration_ms = round((time.perf_counter() - t0) * 1000, 1)

    return PipelineResult(
        asset_id=reading.asset_id,
        health_report=health_report,
        anomaly_severity=sentinel.severity,
        flagged_signals=sentinel.flagged_signals,
        gotze_triggered=gotze_triggered,
        gotze_decision=gotze_decision,
        rca_narrative=rca_result.narrative if rca_result else None,
        rca_citations=rca_result.citations if rca_result else [],
        executive_brief=brief,
        audit_record_id=record_id,
        pipeline_duration_ms=duration_ms,
    )
