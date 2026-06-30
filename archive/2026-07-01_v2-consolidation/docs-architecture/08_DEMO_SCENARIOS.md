# DEMO SCENARIOS — PlantMind × Götze Engine
> How to show real failures and edge cases live, and the exact 5-minute story for judges. This is what you rehearse 20 times.

---

## 1. The core idea: you control the failures

Because the data is **synthetic and physics-seeded**, you decide exactly when and how a machine fails on stage. Build a small **"scenario injector"** — a dropdown in the dashboard (or a config flag) that triggers a chosen failure on a chosen asset, live.

```python
# scenario injector (concept)
SCENARIOS = {
  "gradual_pump_wear":      inject(asset="pump_07",  mode="gradual_wear",   onset_cycle=now+5),
  "sudden_bearing_impact":  inject(asset="bearing_3", mode="sudden_impact",  onset_cycle=now+2),
  "intermittent_valve":     inject(asset="valve_11",  mode="intermittent_fault"),
  "sensor_dropout":         inject(asset="motor_2",   mode="data_quality"),   # edge case
  "conflicting_signals":    inject(asset="comp_4",    mode="multivariate"),   # edge case
}
```

---

## 2. The four demo scenarios (3 core + ramp to edge cases)

### Scenario A — Gradual wear (the hero demo) ⭐
- Pump health drifts down over a few cycles → crosses threshold.
- All 5 agents fire → Götze surfaces **"reduce load now + schedule seal swap in next window."**
- Shows the smooth, explainable, "one best action" magic. **This is your money shot.**

### Scenario B — Sudden impact (urgency)
- Bearing takes a step-change failure → DataSentinel critical → Götze surfaces **"emergency stop"** with a high IIS gap (clearly the right call).
- Shows the system handles *fast* failures, not just slow drift.

### Scenario C — Intermittent fault (subtlety)
- Valve spikes periodically — easy to miss. DataSentinel's Mahalanobis catches the *pattern*.
- Shows depth: you catch what a simple threshold alarm would miss.

### Edge case D — Sensor dropout / conflicting signals (robustness)
- A sensor goes silent, or two signals contradict.
- DataSentinel flags **bad data, not bad machine** → system doesn't false-alarm.
- Shows maturity: it knows the difference between a broken sensor and a broken pump.

---

## 3. Edge cases to have ready (judges love poking these)

| Edge case | What you show |
|---|---|
| Two assets fail at once | ExecutiveSummarizer ranks them; Götze handles the higher-IIS one first |
| No crew / no parts available | Feasibility term drops → Götze picks a *different* best action (e.g. "reduce load + monitor") |
| Unsafe top action | SafetyRiskDelta veto kicks in → next-best action surfaces |
| LLM/API down | Templated reason still renders — demo never freezes |
| Human rejects the recommendation | Logged as rejected with reason → feedback loop story |

---

## 4. THE 5-MINUTE SCRIPT (rehearse this exactly)

**[0:00–0:45] The hook.**
> "In the 2014 World Cup final, SAP analytics told Germany's coach the single best substitution was Mario Götze. He came on and scored the winner. Today, plants don't have that coach — they have a wall of alarms. PlantMind is the coach."

**[0:45–1:30] The setup.**
> Show the live dashboard: 5 healthy assets, sensors streaming. "28 days ago, LTTS and Databricks announced an Industrial AI partnership across exactly these five areas. We built the reference implementation."

**[1:30–3:00] The magic moment (Scenario A).**
> Trigger gradual pump wear. Narrate as agents fire: "DataSentinel flags it… the Oracle says health 38, 12 days left… and here's the difference — the Götze Engine doesn't just alarm. It scored every action and surfaces ONE: reduce load now, seal swap Thursday. Here's why it beats the runner-up. Root cause: seal contamination, manual page 34."

**[3:00–3:45] The human + the audit.**
> "Nothing is autonomous. The operator approves —" *(tap Approve)* "— and it's logged immutably. Full lineage, full explainability. Exactly what a regulated plant needs."

**[3:45–4:30] The robustness flex.**
> Trigger the sensor-dropout edge case. "Watch — it flags bad *data*, not a bad *machine*. It doesn't cry wolf."

**[4:30–5:00] The close.**
> "Physics-grounded health, a patent-candidate intervention scorer, immutable governance — mapped 1:1 to the LTTS-Databricks vision. At $[X]/hour of downtime prevented, this pays for itself in one avoided failure. PlantMind: the one best action, every time."

---

## 5. Demo hygiene (so nothing goes wrong)

- **Pre-load all data.** No live downloads on stage.
- **Pre-warm the LLM** (one dummy call before you start).
- **Have a recorded backup video** of the full run — if the laptop dies, you still present.
- **Freeze the repo at Hour 23** (`v1.0-hackathon-submission` tag). Demo from the frozen build, not `dev`.
- **One person drives, one narrates.** Don't fight over the keyboard.
