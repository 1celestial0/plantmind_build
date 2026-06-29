# Parallel doc — testing & scenarios

**Catalog:** `ops/testing/scenarios.json`  
**Log:** `continuity/test-log.json`  
**Generated cases:** `continuity/generated-test-cases.json` (refreshed on pytest)

## Commands

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-tests.ps1
powershell -ExecutionPolicy Bypass -File scripts/check-status.ps1
```

## Current suites

| Suite | Tests | Status |
|-------|-------|--------|
| `tests/test_contracts.py` | 5 | Active |
| `tests/test_scenarios.py` | 6+ | Active |

## Scenario → implementation map

| ID | Implemented in code | pytest |
|----|---------------------|--------|
| A–E | Catalog only | metadata + field checks |
| A–E injector | Pending Lane 2/3 | future integration tests |

Update this file when injectors land.