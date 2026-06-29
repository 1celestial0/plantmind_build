"""Append pytest JUnit XML results to continuity/test-log.json."""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

_ROOT = Path(__file__).resolve().parents[2]
_LOG_PATH = _ROOT / "continuity" / "test-log.json"
_JUNIT_DEFAULT = _ROOT / "continuity" / "last-test-results.xml"


def _load_log() -> dict:
    if _LOG_PATH.exists():
        with _LOG_PATH.open(encoding="utf-8") as f:
            return json.load(f)
    return {"schema_version": "1.0", "project": "PlantMind", "runs": []}


def _save_log(data: dict) -> None:
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LOG_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def append_from_junit(junit_path: Path, trigger: str = "manual") -> int:
    if not junit_path.exists():
        print(f"No JUnit file at {junit_path}", file=sys.stderr)
        return 1

    root = ET.parse(junit_path).getroot()
    cases = []
    passed = failed = 0

    for suite in root.findall("testsuite"):
        for case in suite.findall("testcase"):
            name = case.get("name", "unknown")
            classname = case.get("classname", "")
            time_s = float(case.get("time", "0") or 0)
            failure = case.find("failure")
            error = case.find("error")
            status = "pass"
            message = None
            if failure is not None:
                status = "fail"
                message = (failure.get("message") or failure.text or "")[:500]
            elif error is not None:
                status = "error"
                message = (error.get("message") or error.text or "")[:500]

            if status == "pass":
                passed += 1
            else:
                failed += 1

            cases.append(
                {
                    "test_id": name,
                    "class": classname,
                    "status": status,
                    "duration_ms": int(time_s * 1000),
                    "message": message,
                }
            )

    log = _load_log()
    log["runs"].append(
        {
            "run_id": str(uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "trigger": trigger,
            "passed": passed,
            "failed": failed,
            "total": passed + failed,
            "cases": cases,
        }
    )
    _save_log(log)
    print(f"Logged test run: {passed} passed, {failed} failed → {_LOG_PATH}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else _JUNIT_DEFAULT
    trigger = sys.argv[2] if len(sys.argv) > 2 else "manual"
    raise SystemExit(append_from_junit(path, trigger))