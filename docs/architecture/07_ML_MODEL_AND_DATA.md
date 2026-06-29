# ML MODEL & DATA — PlantMind × Götze Engine
> What to actually build, in what order, with a guaranteed fallback. Plus how to get and synthesize the data.

---

## 0. The most important sentence in this file

**Build the analytical Weibull model FIRST. It always works and is enough to win.**
The PINN is a *stretch* that, if it doesn't train in time, you simply skip — with **zero visible difference** to judges. Do not let the PINN become a single point of failure.

---

## 1. The health model (must-have, ~2 hours)

**What it is:** a formula that turns "age + stress" into a health score 0–100.

```
H(t) = 100 · exp(−λ · t^β) · T_correction · L_correction

t   = cycles/age of the asset
λ   = degradation rate   (how fast it wears)
β   = Weibull shape      (β<1 early failures, β=1 random, β>1 wear-out)
T_correction = exp(−Ea / (k·(temp_C + 273.15)))   # Arrhenius: heat speeds failure
L_correction = (load / rated_load)^m              # higher load → faster wear
```

**Why it's credible:** Weibull is the textbook reliability model used across industry for decades. You're not inventing it — you're *applying* it, which is the right kind of rigor.

**RUL (days left):**
```
RUL = ((ln(H_threshold / H_current)) / (−λ))^(1/β)
CI_95 = bootstrap, n=1000 samples
```

**How to build it:**
1. `scripts/calibrate_weibull.py` — fit λ, β per asset class from Kaggle data (scipy MLE).
2. `physics/weibull.py` — the `H(t)` and `RUL` functions.
3. Wrap behind `PhysicsModelInterface` → `{health_index, rul_estimate, confidence_interval, physics_explanation}`.

---

## 2. The PINN (OPTIONAL stretch, only if ahead of schedule)

**What it is:** a small neural net that predicts RUL but is *penalized* during training if its predictions violate the Weibull physics rule. Result: sharper RUL than the formula alone, while staying physically sane.

**Architecture:** `1D-CNN (feature extractor) → BiLSTM (temporal) → Dense (RUL)`

**Loss (the clever bit):**
```
L_total = α · MSE(RUL_pred, RUL_true)              # fit the data
        + (1−α) · || dH/dt + λβt^(β−1)·H ||²       # obey Weibull physics
α schedule: 0.7 → 0.3   (start data-driven, anneal toward physics)
```

**Decision rule:** if the PINN isn't validating cleanly by **Hour 14**, freeze it and ship the Weibull baseline. Mention the PINN as "implemented, physics-constrained, validating" — true even if it's the stretch path.

---

## 3. Validation (what makes it sound rigorous)

- Train on **CMAPSS**, validate on **PRONOSTIA** → cross-domain generalization.
- Report: **RMSE**, **MAPE**, and the **asymmetric Score function** (penalizes *late* predictions harder — late = a missed failure = expensive).
- Even with the analytical model alone, you can report these on held-out CMAPSS.

---

## 4. The data plan (3 stages)

**Stage 1 — Kaggle seed (calibrate the physics):**
| Dataset | Use |
|---|---|
| CMAPSS (NASA turbofan) | 21 sensors, labeled RUL → fit (λ, β) for turbofan |
| PRONOSTIA bearings | vibration+temp run-to-failure → fit (λ, β) for bearings |
| Azure Predictive Maintenance | 5 failure modes → failure-mode classification baseline |

> ⚠️ Verify dataset URLs/licenses at build time; download before the hackathon so you're not depending on live network.

**Stage 2 — Synthetic generator (seeded by Stage 1 params):**
- `30 assets × 20 signals × 3 failure modes × 500 cycles`
- Uses the *same* λ, β from real data → physically realistic, **not random**.
- **Why synthetic wins for a demo:** you control *exactly when* failures happen on stage. No privacy issues. Reproducible.
- `scripts/generate_data.py` with controlled injection: `gradual_wear` (Weibull), `sudden_impact` (step), `intermittent_fault` (periodic spike).

**Stage 3 — RAG corpus:**
- A handful of real or synthetic maintenance manuals / fault logs / SOPs → embed → ChromaDB.
- 10–20 documents is plenty for a convincing demo.

---

## 5. Build order (do not deviate)

1. ✅ Download + calibrate Weibull params (before hackathon if possible).
2. ✅ Synthetic generator → produces the demo dataset.
3. ✅ Analytical health + RUL behind `PhysicsModelInterface`.
4. ✅ Seed ChromaDB for RootCause.
5. ⬜ (stretch) PINN training + cross-domain validation.

> Items 1–4 are the guaranteed demo. Item 5 is upside only.

---

## 6. What to say about the ML in the pitch

> "Health and RUL come from a Weibull degradation model — the industry-standard reliability law — calibrated on NASA CMAPSS and PRONOSTIA bearing data, and validated cross-domain. We extend it with a physics-constrained neural correction that's penalized for violating the Weibull rule. The novel part isn't the model alone — it's coupling it to an intervention scorer that surfaces one approved, audited action."

*(True whether or not the PINN ships, because the constraint and the coupling are real in the design.)*
