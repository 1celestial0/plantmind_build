# Team Poll: AI Scoring System Design — Your Instincts

> **How to post in Teams:**
> Paste the intro message in your channel, then use the built-in **Polls** app (+ > Polls)
> to create each question separately — or share as a Microsoft Form link.
> **Do NOT share this file with the team.** Use only the content inside "─── SEND THIS ───".

---

## ─── SEND THIS ───

**[Message to post in Teams channel]**

---

Hey team 👋

Quick design-thinking calibration — no project context, no right or wrong answers.
I'm trying to map where we collectively land on a few AI system design decisions
*before* we converge on an approach. Takes ~3 minutes.

Please reply to each question directly in thread (name your answer + one sentence why).

---

### Q1 — Signal Weighting Strategy
*When combining multiple input signals into a single composite AI score,
what should primarily drive each signal's weight?*

A) Domain expertise — engineers manually tune weights based on physical intuition
B) Purely data-driven — statistical correlation to the target outcome sets the weights
C) Hybrid — start with domain priors, then fine-tune with data
D) Equal weights as the baseline, adjust only when there's clear evidence

---

### Q2 — Conflict Resolution
*Two signals disagree: one indicates high risk, the other indicates low risk.
What should the scoring system do by default?*

A) Take the worst-case signal (conservative)
B) Weighted average — let the math resolve it
C) Use a meta-model / learned arbiter to decide
D) Flag the conflict as a separate output; don't collapse it into one score

---

### Q3 — Weight Recalibration Policy
*How should the weights in a scoring model evolve after initial deployment?*

A) Fixed — calibrate once, trust it
B) Periodic retraining on a schedule (e.g., monthly / quarterly)
C) Triggered retraining — only when score drift or degraded accuracy is detected
D) Continuous online learning — weights update incrementally with new data

---

### Q4 — Top Design Priority
*If you had to rank ONE property above all others for a composite scoring system,
which would it be?*

A) Accuracy — minimise prediction error on the target metric
B) Robustness — stable, predictable output even under noisy or missing inputs
C) Interpretability — a human can explain why a score is high or low
D) Sensitivity — catch edge cases and rare events early, even at the cost of false alarms

---

Thanks — I'll share a synthesis of where the team lands once responses are in. 🙏

---

## ─── END OF SEND ───

---

## Decoding key (for your eyes only)

| Question | What it actually probes |
|---|---|
| Q1 | Should Gotze's signal weights be expert-tuned, ML-derived, or hybrid? |
| Q2 | How should the engine handle conflicting sensor signals at scoring time? |
| Q3 | Online vs. offline retraining strategy — ties directly to deployment architecture |
| Q4 | Reveals each person's implicit design philosophy — useful for alignment |

---

*Generated for internal use. Do not distribute.*
