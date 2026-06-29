"""Scenario catalog integrity + auto-generated test case registry."""

import json
from pathlib import Path

import pytest

from ops.testing.scenario_generator import generate_test_cases, load_scenarios

_SCENARIOS = Path(__file__).resolve().parents[1] / "ops" / "testing" / "scenarios.json"


def test_scenarios_json_valid():
    data = load_scenarios()
    assert data["schema_version"] == "1.0"
    assert len(data["scenarios"]) >= 5


@pytest.mark.parametrize("scenario", load_scenarios()["scenarios"], ids=lambda s: s["id"])
def test_each_scenario_has_required_fields(scenario):
    assert scenario["id"]
    assert scenario["slug"]
    assert scenario["asset_id"]
    assert scenario["mode"]
    assert scenario["priority"] in ("hero", "core", "edge")


def test_generate_test_cases_count():
    cases = generate_test_cases()
    assert len(cases) == len(load_scenarios()["scenarios"])
    assert all(c["test_id"].startswith("SCENARIO-") for c in cases)


def test_hero_scenario_pump_07():
    data = load_scenarios()
    hero = next(s for s in data["scenarios"] if s["id"] == "A")
    assert hero["asset_id"] == "pump_07"
    assert hero["human_approval_required"] is True


def test_scenarios_file_matches_generator():
    """Persist generated cases snapshot for test-log traceability."""
    cases = generate_test_cases()
    out = Path(__file__).resolve().parents[1] / "continuity" / "generated-test-cases.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(cases, f, indent=2)
        f.write("\n")
    assert out.exists()