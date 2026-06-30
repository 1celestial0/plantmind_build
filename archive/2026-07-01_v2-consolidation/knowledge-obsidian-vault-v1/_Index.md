# PlantMind Knowledge Graph
## Map of Content (MOC) — Start Here

> **How to use this vault in Obsidian:**
> Open Obsidian → "Open folder as vault" → select `PlantMind/Knowledge Graph/`
> Click the graph icon (top right) to see all nodes and connections.
> Click any `[[linked concept]]` to navigate the graph.

---

## 🧠 Core Concepts

- [[Götze Score]] — The core IP. How PlantMind makes decisions.
- [[Counterfactual Proof]] — How PlantMind PROVES the fix works.
- [[Remaining Useful Life]] — What the ML model predicts.
- [[Surrogate Twin]] — The simulated engine used in counterfactuals.
- [[RED-GREEN Transition]] — The "money shot" of the demo.
- [[Asset Health]] — How we classify engine state.

---

## 🏗️ Architecture Layers

- [[Layer 1 - Data]] — C-MAPSS ingestion + RUL labeling
- [[Layer 2 - Features]] — Rolling window feature engineering
- [[Layer 3 - Prediction]] — RandomForest RUL model
- [[Layer 4 - Götze Engine]] — Decision engine (CORE IP)
- [[Layer 5 - Proof and Learn]] — Dashboard + recalibration

---

## ⚖️ Key Engineering Decisions

- [[Decision - RandomForest over LSTM]] — Why not deep learning?
- [[Decision - Deterministic over LLM Scoring]] — Why math, not AI, decides
- [[Decision - Clip RUL at 130]] — Why cap the label?
- [[Decision - Window Size 30]] — Why 30 cycles, not 10 or 50?
- [[Decision - RED Threshold 30]] — Why 30 cycles = critical?

---

## 🔬 Patent Portfolio

- [[Patent 1 - Counterfactual Proof Engine]] — Strongest claim
- [[Patent 2 - Götze Scoring Method]] — Deterministic wrapper over AI
- [[Patent 3 - Domain Adaptive KB]] — Self-bootstrapping knowledge
- [[Patent 4 - Research Augmented MetaGPT]] — Live standards validation layer

---

## ⚙️ Technology Stack

- [[NASA C-MAPSS]] — The dataset
- [[MetaGPT]] — The multi-agent framework we build on
- [[MLflow]] — Model tracking + registry
- [[Delta Lake]] — Versioned feature storage
- [[Databricks]] — Cloud deployment platform
- [[Streamlit]] — Demo UI framework

---

## 🔗 Key Relationships (read this first)

```
[[NASA C-MAPSS]]
    → feeds → [[Layer 1 - Data]]
    → produces → [[Remaining Useful Life]]

[[Remaining Useful Life]]
    → predicted by → [[Layer 3 - Prediction]]
    → flags → [[Asset Health]] (RED if RUL < 30)

[[Asset Health]] RED
    → triggers → [[Layer 4 - Götze Engine]]
    → scores via → [[Götze Score]]
    → produces → [[Counterfactual Proof]]
    → visualized as → [[RED-GREEN Transition]]

[[Götze Score]]
    → depends on → [[Surrogate Twin]] (for ΔHealth term)
    → is protected by → [[Patent 1 - Counterfactual Proof Engine]]
    → is protected by → [[Patent 2 - Götze Scoring Method]]

[[MetaGPT]]
    → extended by → [[Patent 3 - Domain Adaptive KB]]
    → extended by → [[Patent 4 - Research Augmented MetaGPT]]
```

---

*Last updated: 2026-06-20 · Add new nodes freely — Obsidian will auto-link them*
