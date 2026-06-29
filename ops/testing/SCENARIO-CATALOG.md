# Scenario Catalog — automated test + demo alignment

**Machine source:** `ops/testing/scenarios.json`  
**Generator:** `ops/testing/scenario_generator.py`  
**Pytest:** `tests/test_scenarios.py`  
**Log:** `continuity/test-log.json`

| ID | Slug | Asset | Demo role |
|----|------|-------|-------------|
| A ⭐ | gradual_pump_wear | pump_07 | Hero — one best action |
| B | sudden_bearing_impact | bearing_3 | Urgency / emergency stop |
| C | intermittent_valve | valve_11 | Mahalanobis pattern |
| D | edge | motor_2 | Bad data, not bad machine |
| E | edge | comp_4 | Conflicting signals |

When Lane 2/3 land, each scenario gets an injector hook in `ml/synthesis/` or dashboard dropdown.

**Run:** `powershell -ExecutionPolicy Bypass -File scripts/run-tests.ps1`