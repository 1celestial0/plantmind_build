# PROJECT DNA — PlantMind × Götze Engine
> The single 10-minute read that brings any teammate, judge, or stakeholder fully up to speed.

---

## 1. WHAT

PlantMind is a **Physics-Informed Engineering Intelligence framework** for industrial assets. It turns raw sensor + maintenance data into **explainable, actionable engineering decisions**.

Its heart is the **Götze Engine**: at the moment of maximum asset stress, instead of just raising an alarm, it scores *every* possible human intervention and surfaces the **ONE optimal action** — with a plain-English reason. A human approves. The decision is logged forever.

**Two layers:**
- **Layer 0 — Framework (LTTS IP):** tool-agnostic interface contracts. Portable to any runtime.
- **Layer 1 — Reference implementation:** Databricks-native (production narrative) + a local open-source build (the actual hackathon demo).

---

## 2. WHY IT WINS

**a) The story is unbeatable and *true*.** The Götze analogy is memorable; the LTTS × Databricks partnership (announced June 11, 2026) is real and maps 1:1 to PlantMind's scope. We built the reference implementation 28 days later. Judges remember stories, not architecture diagrams.

**b) It maps 1:1 to the five joint LTTS-Databricks solution areas:**
| Joint solution area | PlantMind piece |
|---|---|
| Predictive Asset Reliability | AssetHealthOracle (health + RUL) |
| Energy & Emissions Optimization | IIS feasibility/cost terms |
| OEE & Production Intelligence | Downtime-cost scoring |
| Quality Intelligence | DataSentinel anomaly flags |
| Sustainability Analytics | ExecutiveSummarizer ROI roll-up |

**c) The differentiator is the *decision*, not the alarm.** Everyone builds anomaly detection. Almost no one closes the loop to "here is the single best action, ranked, with reasoning." That's the IIS.

**d) Governance is built in.** Non-autonomous + explainable + immutable audit = exactly what regulated, asset-intensive enterprises require. This is a maturity signal judges reward.

---

## 3. HOW IT WORKS (the runtime story)

Five specialist agents fire in sequence on a stressed machine:

1. **DataSentinel** (inspector) — flags abnormal sensor readings.
2. **AssetHealthOracle** (doctor) — health score 0–100 + RUL in days. *Weibull lives here.*
3. **GötzeEngine** (coach) ⭐ — scores every candidate action via **IIS**, surfaces the top one + reason.
4. **RootCauseAnalyst** (detective) — searches manuals/logs (RAG) to explain *why*, with citations.
5. **ExecutiveSummarizer** (chief of staff) — 3-bullet leadership brief.

→ Operator taps **Approve** → action logged immutably.

**The IIS formula (cite this everywhere intervention scoring appears):**
```
IIS(i) = w1·ΔP_failure(i) + w2·ΔDowntimeCost(i) + w3·Feasibility(i)
         + w4·HistoricalSuccess(i) − w5·SafetyRiskDelta(i)

Default weights: [0.35, 0.25, 0.20, 0.15, 0.05]
```
- In the **demo**: weights are **fixed**. Clean and reproducible.
- In **production**: weights self-calibrate from outcome feedback. *(Narrative only — no outcome data exists in 24h.)*

---

## 4. THE TECHNICAL CORE (honest version)

**Health & RUL** come from the **Weibull degradation model** — analytical, fast, always works:
```
H(t) = 100 · exp(−λ · t^β)   (× temperature & load corrections)
```
λ and β are calibrated **before** the hackathon from free Kaggle data (CMAPSS, PRONOSTIA). This baseline is your guaranteed demo.

**The PINN (Physics-Informed Neural Network) is an OPTIONAL stretch**, not the spine. It embeds the Weibull rule as a neural training constraint for sharper RUL. **If it doesn't train in time, the analytical Weibull baseline carries the demo with zero visible difference to judges.** Build the fallback first; reach for the PINN only if ahead of schedule.

---

## 5. PATENT / NOVELTY — HANDLE WITH CARE

The honest position (say this, not more):
- Physics-informed RUL prediction is an **active research area** — PINNs for degradation exist in the literature.
- ❗ Do **not** claim "no one has done this" without a real prior-art search. That's a credibility landmine in front of judges.
- **Your defensible wedge:** *coupling* a physics-grounded health model to a **multi-criteria intervention scorer (IIS) that surfaces one approved action with audit** — the closed decision loop, not the PINN alone.
- Frame as **"novel integration, patent-candidate pending prior-art review"** — confident but honest.

---

## 6. ROI CASE (parameters, not invented certainty)

Downtime-cost prevented is the headline metric:
```
Value = (failures_prevented) × (avg_downtime_hours) × (cost_per_hour) − intervention_cost
```
- `cost_per_hour` varies hugely by industry — **[ESTIMATE: $50K–$500K/hr depending on sector; verify with a benchmark before pitching]**.
- For the demo, show the math live with conservative inputs and let judges plug their own numbers. (Interactive ROI calculator staged for the build chat.)

---

## 7. BUILD MAP (who owns what)

| Track | Owner | Deliverable |
|---|---|---|
| Brain: agents + IIS + data | **Sourav** | 5 agents, scoring logic, synthetic data, FastAPI |
| Health/ML | **Sourav** (+ help) | Weibull baseline (must-have), PINN (stretch) |
| Dashboard + charts | **Member 2** | Streamlit screens, sensor/health charts |
| IIS scoring UI + audit trail | **Member 3** | The "one best action" panel, log viewer |
| Integration + QA + demo script | **Member 4** | Wiring, test scenarios, 5-min rehearsed story |

Full hour-by-hour plan: `10_BUILD_PLAN.md`.

---

## 8. WHAT TO REHEARSE

The 5-minute demo (full script in `08_DEMO_SCENARIOS.md`):
1. Show a healthy plant dashboard.
2. Inject a failure live — a pump starts degrading.
3. Watch the 5 agents fire → the **one best action** appears with its reason.
4. Operator approves → audit log updates.
5. Close on the Götze line + the Databricks partnership.

> **The win condition is not "we trained a novel neural net." It's "we showed the one-best-action moment, it was explainable, and it ties to a real $-impact and a real partnership."**
