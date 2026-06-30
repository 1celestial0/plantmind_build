# PlantMind 🏭
### *Predict the failure. Decide the fix. Prove it.*

**LTTS Global Engineering Intelligence Hackathon · 9 July 2026**
**Engine:** Götze Decision Engine (GDE) | **Dataset:** NASA C-MAPSS | **Stack:** Python · scikit-learn · Streamlit · Plotly · Databricks

---

## What is PlantMind?

PlantMind is an **agentic EI layer** that converts industrial sensor streams into ranked, explainable corrective actions. It does what no existing tool does: not only predict failure, but *decide the optimal fix and prove it works* — by running a counterfactual simulation that flips a failing asset from RED → GREEN.

**The one-sentence kill:** *Everyone predicts. We decide. And we prove it on the same data.*

---

## Folder Structure

```
PlantMind/
│
├── 📁 Chat Context/               ← ALWAYS CHECK THIS FIRST
│   └── YYYY-MM-DD_vX.Y_project-context.md
│       Claude reads the latest file here at every session start.
│       Captures project state, decisions, open items.
│
├── 📁 FORGE/                      ← Core engine code + IP documentation
│   ├── src/
│   │   ├── ingestion.py           Layer 1: C-MAPSS data + RUL labeling
│   │   ├── features.py            Layer 2: Rolling window feature engineering
│   │   ├── model.py               Layer 3: RandomForest RUL predictor
│   │   └── gotze_engine.py        Layer 4: Götze scoring + counterfactual proof ← CORE IP
│   ├── run_demo.py                Full pipeline orchestrator
│   ├── PATENT_IDEAS.md            3 patent concepts with claim language
│   ├── REVERSE_ENGINEER.md        Hands-on learning guide (break → learn)
│   └── GITHUB-FORGE-REPO-GUIDE.md How to set up the patent GitHub repo
│
├── 📁 LEARNING/                   ← Deep-dive documentation for Sourav
│   ├── 00-DEEP-LEARNING-FRAMEWORK.md   What/Why/How/When/WhyNot coding model
│   ├── 01-DATABRICKS-1HR-SPRINT.md     60-min structured Databricks sprint
│   └── METAGPT-ADOPTION-GUIDE.md       MetaGPT mental model + adoption levels
│
├── 01-PlantMind-Blueprint.md      Full product blueprint + rubric + roles
├── 02-PlantMind-7Day-Plan.md      Sprint plan for hackathon
├── 03-PlantMind-Scenarios.md      Test scenarios + demo scripts
├── 04-PlantMind-Databricks.md     Databricks setup + notebooks + runbook
├── 05-PlantMind-Engine-Math.md    Götze formula derivation + sensitivity analysis
│
└── README.md                      ← You are here
```

---

## 5-Layer Architecture

| Layer | Name | What it does | Key file |
|---|---|---|---|
| 1 | Data | Load C-MAPSS, compute RUL, clean | `FORGE/src/ingestion.py` |
| 2 | Features | 30-cycle rolling window features | `FORGE/src/features.py` |
| 3 | Prediction | RandomForest → RUL → RED flag | `FORGE/src/model.py` |
| 4 | **Decision** | **Götze Score → ranked actions → counterfactual proof** | `FORGE/src/gotze_engine.py` |
| 5 | Proof+Learn | RED→GREEN dashboard → weight recalibration | Streamlit app |

**Core design rule (never break):**
> AI does uncertain work (predict, reason, imagine).
> Deterministic rules make every actual decision (flag, score, pick).

---

## Götze Score

```
G = w₁·ΔHealth + w₂·(1−NormCost) + w₃·(1−NormTime) + w₄·Safety
Weights: health=0.40, cost=0.25, time=0.20, safety=0.15
All terms ∈ [0,1], weights sum to 1.0
```

---

## Quick Start

```bash
# Install
pip install -r FORGE/requirements.txt

# Run full pipeline
python FORGE/run_demo.py

# Test Layer 4 only (Götze engine)
python -m FORGE.src.gotze_engine

# Learn by breaking (see FORGE/REVERSE_ENGINEER.md)
```

---

## Patent Strategy

Three patent concepts documented in `FORGE/PATENT_IDEAS.md`:
1. **Counterfactual Proof Engine** — strongest, clearest prior art gap
2. **Götze Scoring Method** — deterministic wrapper over probabilistic AI
3. **Domain-Adaptive KB Bootstrapping** — MetaGPT extension for industrial AI

Provisional patent filing target: **9 July 2026** (hackathon presentation starts the 12-month clock).

---

## Team & Roles

| Role | Owner | Responsibility |
|---|---|---|
| Brain | **Sourav** | Data pipeline, RUL model, surrogate twin, Götze engine, feedback loop |
| App | Streamlit dev | Shell scaffold, agent tool-call wiring, control panel |
| Viz 1 | Team member | RED→GREEN counterfactual chart, RUL trajectory plots |
| Viz 2 | Team member | Asset-health dashboard, score-comparison bars, agent log panel |

---

## Working with Claude (AI Co-pilot Rules)

1. **Always read `Chat Context/` first** — find the file with the highest version number
2. **Every ~15 messages** — surface a context refresh reminder
3. **For all code** — use the What/Why/How/When/Why-Not comment model (`LEARNING/00-DEEP-LEARNING-FRAMEWORK.md`)
4. **Before new features** — check rubric impact in `01-PlantMind-Blueprint.md`
5. **For any novel idea** — check if it's patent-worthy before implementing

---

*PlantMind · LTTS EI Hackathon 2026 · Team Internal*
