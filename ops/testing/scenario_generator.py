"""Generate pytest test-case metadata from ops/testing/scenarios.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_SCENARIOS_PATH = Path(__file__).resolve().parent / "scenarios.json"


def load_scenarios() -> dict[str, Any]:
    with _SCENARIOS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def generate_test_cases() -> list[dict[str, Any]]:
    """One automated test case definition per scenario."""
    data = load_scenarios()
    cases: list[dict[str, Any]] = []
    for s in data["scenarios"]:
        cases.append(
            {
                "test_id": f"SCENARIO-{s['id']}",
                "slug": s["slug"],
                "name": s["name"],
                "asset_id": s["asset_id"],
                "mode": s["mode"],
                "priority": s["priority"],
                "status": "pending_implementation",
                "automated": s["id"] in ("A", "B", "C", "D", "E"),
                "assertions": _default_assertions(s),
            }
        )
    return cases


def _default_assertions(scenario: dict[str, Any]) -> list[str]:
    base = [
        f"asset_id={scenario['asset_id']}",
        f"mode={scenario['mode']}",
    ]
    if scenario.get("human_approval_required"):
        base.append("requires_human_approval=true")
    if "expected_outcome" in scenario:
        base.append(f"outcome={scenario['expected_outcome']}")
    return base


if __name__ == "__main__":
    cases = generate_test_cases()
    print(json.dumps(cases, indent=2))