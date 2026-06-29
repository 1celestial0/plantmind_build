"""Quick end-to-end smoke test — run from project root."""
from src.pipeline import run, SensorReading

r = run(SensorReading(
    asset_id="pump_07",
    asset_type="pump",
    cycle=340.0,
    signals={"vibration_rms": 2.8, "kurtosis": 8.5, "temperature_bearing": 78.0},
    temp_celsius=38.0,
    load_ratio=1.15,
))

print("=== Hero scenario: pump_07 cycle 340 ===")
print(f"Health:         {r.health_report.health_score}/100")
print(f"RUL:            {r.health_report.rul_days} days  CI {r.health_report.ci_95}")
print(f"Severity:       {r.anomaly_severity}")
print(f"Flagged:        {r.flagged_signals}")
print(f"GotzeTriggered: {r.gotze_triggered}")
if r.gotze_decision:
    print(f"Top action:     {r.gotze_decision.top_intervention} (IIS {r.gotze_decision.iis_score})")
    print(f"Runner-up:      {r.gotze_decision.runner_up} (gap {r.gotze_decision.iis_gap})")
    print(f"Needs approval: {r.gotze_decision.requires_human_approval}")
rca = r.rca_narrative or ""
print(f"RCA:            {rca[:90]}...")
print(f"Critical alerts:{r.executive_brief.critical_alerts}")
saved = r.executive_brief.downtime_saved_estimate
print(f"Downtime saved: USD {saved:,.0f}")
print(f"Audit ID:       {r.audit_record_id}")
print(f"Duration:       {r.pipeline_duration_ms} ms")
