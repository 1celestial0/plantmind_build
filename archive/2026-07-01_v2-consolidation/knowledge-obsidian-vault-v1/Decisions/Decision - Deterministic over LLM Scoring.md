---
tags: [decision, core-ip, why-not]
created: 2026-06-20
---

# Decision: Deterministic over LLM Scoring

## The Decision

The [[Götze Score]] is computed by a **deterministic weighted formula**, not by an LLM.

The LLM is only used for the *diagnosis* step (root cause identification and generating the action menu). The final decision — which action to implement — is always made by the deterministic Götze formula.

## Why This Matters (it's the architecture's beating heart)

```
WRONG architecture (pure LLM):
  LLM: "Based on sensor readings, I recommend replacing the bearing."
  Engineer: "Why?"
  LLM: "Based on my analysis of the pattern..."
  → Not auditable. Not reproducible. Can't be patented. 
     Different temperature setting = different answer.

CORRECT architecture (PlantMind):
  LLM: identifies root cause, proposes 4 candidate actions
  Götze formula: G = 0.40·ΔHealth + 0.25·(1-NormCost) + ...
  Score: replace_bearing=0.54, reduce_load=0.89 ← argmax wins
  Engineer: "Why reduce_load?"
  Answer: "Score = 0.89 because ΔHealth=0.31, cost is low (0.86), 
           downtime is near-zero (0.96), safety is perfect (1.00)"
  → Fully auditable. Reproducible. Patentable. Defensible in court.
```

## The Core Insight

> AI does uncertain work. Deterministic rules make every actual decision.

The LLM's uncertainty is appropriate for open-ended reasoning (what could cause this failure?). The formula's certainty is required for consequential decisions (which action should we take?). Mixing these two — letting the LLM also decide — collapses both benefits.

## Why This is a Patent Advantage

[[Patent 2 - Götze Scoring Method]] claims the **architectural isolation** of the deterministic layer from the probabilistic AI layer. This is specifically what LIME/SHAP, prescriptive maintenance systems, and LLM chatbots for maintenance DON'T do. They let the AI decide. We don't.

## WHAT / WHY / HOW / WHEN / WHY NOT

**WHAT:** The final recommendation always comes from a deterministic formula, never from an LLM output.

**WHY:** Industrial safety decisions need to be reproducible and auditable. An LLM can change its answer based on phrasing, temperature, and version updates. A formula cannot.

**HOW:** LLM generates the action *candidates*; Götze formula scores and ranks them; argmax picks the winner. Two separate architectural layers with a typed interface between them.

**WHEN:** This rule applies to every decision in [[Layer 4 - Götze Engine]].

**WHY NOT:**
- Full LLM: outputs vary by temperature, prompt wording, model version → unacceptable for safety-critical systems
- Full rule-based: can't generate nuanced root cause analysis; too brittle for novel failure modes
- Hybrid (LLM scores + formula validates): adds complexity without clear benefit; the formula IS the validation

## Connected Nodes

- Implemented in → [[Layer 4 - Götze Engine]]
- The formula itself → [[Götze Score]]
- Protected by → [[Patent 2 - Götze Scoring Method]]
- Contrast with → pure LLM approaches (not patentable, not auditable)
