# REVERSE ENGINEER GUIDE
## Learning PlantMind FORGE by Breaking and Rebuilding It

> **The method:** Run it first. Understand what it does.
> Then break one thing. See what fails. Fix it. Now you own that concept.
> Repeat per file. By the end of Day 1 you'll understand the full pipeline.

---

## STEP 0 — Make It Work (15 min)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full demo
python run_demo.py

# Expected: 5 layers execute, RED engines get diagnosed, GREEN proof printed
```

If it runs → move to Step 1.
If it errors → read the error, fix the import, run again. That IS learning.

---

## STEP 1 — Layer 1: Data (30 min)

**File:** `src/ingestion.py`

**Run standalone:**
```bash
python -m src.ingestion
```

**Break it → learn:**
| Experiment | What to change | What to observe |
|---|---|---|
| 1a | `clip_rul=50` instead of 130 | Does R² go up or down in Layer 3? Why? |
| 1b | `n_engines=5` | How does model quality change with less data? |
| 1c | Remove `.clip()` entirely | Print `df['RUL'].describe()` — what's the max now? |
| 1d | Add a column `df['rul_category'] = (df['RUL'] < 30).astype(int)` | Does it pass through to Layer 2? |

**Concept you now own:** RUL labeling, why clipping matters, data volume effects.

---

## STEP 2 — Layer 2: Features (30 min)

**File:** `src/features.py`

**Run standalone:**
```bash
python -m src.features
```

**Break it → learn:**
| Experiment | What to change | What to observe |
|---|---|---|
| 2a | `window=5` | Features become noisy. Why does this hurt the model? |
| 2b | `window=100` | Many NaN at engine start. How does `min_periods=1` help? |
| 2c | Remove `DEGRADING_SENSORS` filter — use all 21 sensors | Model more or less accurate? |
| 2d | Add rolling `.min()` per sensor | Does R² improve? |

**Concept you now own:** Why rolling features matter, the tradeoff of window size.

---

## STEP 3 — Layer 3: Model (45 min)

**File:** `src/model.py`

**Run standalone:**
```bash
python -m src.model
```

**Break it → learn:**
| Experiment | What to change | What to observe |
|---|---|---|
| 3a | `n_estimators=5` | Accuracy drops. What's the tradeoff with speed? |
| 3b | `RED_THRESHOLD=50` | More engines flagged RED. Is that conservative or aggressive? |
| 3c | Replace `RandomForestRegressor` with `GradientBoostingRegressor` | Better R²? |
| 3d | Remove `max_depth=15` | Does training get slower? Does accuracy improve? |
| 3e | Print `predictor.top_features(10)` | Which sensors matter most? Does it match `DEGRADING_SENSORS`? |

**Concept you now own:** RF hyperparameters, overfitting, threshold design.

---

## STEP 4 — Layer 4: Götze Engine (45 min)

**File:** `src/gotze_engine.py`

**Run standalone:**
```bash
python -m src.gotze_engine
```

**Break it → learn:**
| Experiment | What to change | What to observe |
|---|---|---|
| 4a | Set `WEIGHTS = {"health": 0.1, "cost": 0.7, "time": 0.1, "safety": 0.1}` | Does cheapest action win? |
| 4b | Add a 5th action with `cost_usd=500, rul_gain=90` | Does it dominate? Why/why not? |
| 4c | Set `monitor_only` safety_score = 0.0 | Score drops to last place. Weights working? |
| 4d | Change `SURROGATE_GAIN_MAP["replace_bearing"] = 5` | Does the winner change? |
| 4e | Make weights NOT sum to 1 | What happens? Read the assert error — why is that constraint necessary? |

**Concept you now own:** Multi-objective scoring, normalisation, deterministic decision-making over AI outputs.

---

## STEP 5 — The Full Pipeline (1 hour)

**File:** `run_demo.py`

Now modify the orchestrator:

| Experiment | What to change | What to learn |
|---|---|---|
| 5a | Run with `--engines 200` | Does model improve? How long does it take? |
| 5b | Increase RED threshold in `model.py` — make more engines RED | Does Götze Engine scale? |
| 5c | Print the full `EngineDecision` object to JSON | What does the data contract look like? |
| 5d | Add a `for decision in results["decisions"]: decision.summary()` | Build your own output format |

---

## STEP 6 — Connect to Streamlit (with your teammate)

After you understand all 5 layers, the API contract to the Streamlit dev is simple:

```python
# What YOUR code exposes (src/gotze_engine.py EngineDecision)
{
    "engine_id"   : int,
    "current_rul" : float,
    "root_cause"  : str,
    "winner": {
        "action_name"  : str,
        "gotze_score"  : float,
        "rul_gain"     : float,
        "cost_usd"     : float,
        "downtime_hr"  : float,
    },
    "is_rescued"  : bool,
    "all_actions" : [...]   # for the comparison chart
}
```

Your teammate just calls `run_demo()` and gets this dict. That's the integration.

---

## REFINE LOOP (repeat until demo-day)

```
Run → See output → Question one number → Find it in the code → Change it → Re-run
```

Every cycle = one concept understood. After 20 cycles you understand the full engine.

---

## File Reading Order (fastest path to understanding)

1. `src/ingestion.py`     — what is the data?
2. `src/features.py`      — how is the data transformed?
3. `src/model.py`         — how does the ML work?
4. `src/gotze_engine.py`  — how is the decision made?
5. `run_demo.py`           — how do the layers connect?
