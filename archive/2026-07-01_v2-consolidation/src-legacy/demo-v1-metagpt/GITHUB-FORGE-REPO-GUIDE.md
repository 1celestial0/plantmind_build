# GitHub FORGE Repo Guide
## Separate Repo for Patent Filing: PlantMind-FORGE

---

## WHY A SEPARATE GITHUB REPO FOR PATENT FILING?

A GitHub repository creates **legally defensible prior art** because:
1. Every commit has a **cryptographic timestamp** — proves invention date
2. The repo is **public and immutable** — judges (and patent examiners) can verify
3. The `README.md` + code structure IS essentially an **invention disclosure**
4. Forking activity + stars = independent third-party witnesses to the invention date

**The FORGE concept:** A "forge" in software is where raw ideas are hammered into working systems. PlantMind-FORGE is where you forge the *IP* — not just the product.

---

## REPO STRUCTURE: `PlantMind-FORGE`

```
PlantMind-FORGE/
│
├── README.md                    ← Patent-oriented description of the invention
├── LICENSE                      ← MIT (protects your open-source claim)
├── INVENTION_DISCLOSURE.md      ← The actual IP document (this IS your provisional)
│
├── claims/                      ← One file per patent claim
│   ├── CLAIM_01_counterfactual_proof_engine.md
│   ├── CLAIM_02_gotze_scoring_method.md
│   └── CLAIM_03_domain_adaptive_kb.md
│
├── prior_art/                   ← Documented prior art + why you're different
│   ├── PRIOR_ART_ANALYSIS.md
│   ├── lime_shap_gap.md
│   ├── prescriptive_maintenance_gap.md
│   └── digital_twin_gap.md
│
├── evidence/                    ← Working code = reduction to practice
│   ├── gotze_engine.py          ← Your core IP code (copy from FORGE/src/)
│   ├── counterfactual_demo.py   ← RED→GREEN proof generation
│   └── experiments/
│       ├── baseline_comparison.ipynb   ← You vs LIME/SHAP
│       └── rul_validation.ipynb        ← NASA C-MAPSS results
│
├── metagpt_integration/         ← MetaGPT-powered version (Level 3 adoption)
│   ├── roles/
│   └── team.py
│
└── docs/
    ├── architecture.md          ← System architecture (mirrors Blueprint)
    ├── gotze_formula.md         ← Math specification (term-by-term)
    └── filing_notes.md          ← Notes for your patent attorney
```

---

## STEP-BY-STEP: INITIALIZE THE REPO

### Step 1: Create the repo on GitHub (5 min)
```bash
# On GitHub web UI:
# 1. New repository → Name: "PlantMind-FORGE"
# 2. Description: "Götze Decision Engine — Counterfactual Proof System for Industrial AI"
# 3. Visibility: PUBLIC (public = prior art date is credible)
# 4. Add README: YES
# 5. License: MIT

# Clone locally
git clone https://github.com/YOUR_USERNAME/PlantMind-FORGE.git
cd PlantMind-FORGE
```

### Step 2: Write the invention disclosure README (30 min)
This is the most important file. It must answer:
- What is the invention?
- Who invented it and when?
- What problem does it solve?
- How does it work (enough detail to reproduce)?
- What makes it novel over prior art?

See the template below.

### Step 3: Commit in order (CRITICAL for patent dating)
```bash
# ════════════════════════════════════════════════════════════
# WHAT  : Commit order matters for IP — earliest commit = earliest claim date
# WHY   : Patent law: "first to file" (US) or "first to invent" (some countries)
#         GitHub timestamps are UTC and admissible as evidence
# HOW   : Commit the CONCEPT first, then the code
# WHEN  : Do this TODAY, before the hackathon, before anyone else
# WHY NOT: Waiting until code is "clean" loses you the invention date
# ════════════════════════════════════════════════════════════

# Commit 1: The concept (timestamp this today)
git add README.md INVENTION_DISCLOSURE.md
git commit -m "feat: initial invention disclosure — Counterfactual Proof Engine + Götze Method"
git push

# Commit 2: The claims
git add claims/
git commit -m "feat: patent claims — counterfactual proof engine and deterministic scoring method"
git push

# Commit 3: The evidence (working code)
git add evidence/
git commit -m "feat: working implementation — gotze_engine.py with counterfactual proof generation"
git push
```

---

## README.md TEMPLATE FOR PlantMind-FORGE

```markdown
# PlantMind-FORGE
## Counterfactual Proof Engine for Industrial Maintenance AI Decisions

**Inventors:** [Your Name], [Team Member Names]
**Date of first disclosure:** 2026-06-20
**License:** MIT

---

## The Invention (Plain English)

PlantMind-FORGE implements a novel method for selecting and *proving* 
the efficacy of industrial maintenance decisions:

1. Predict remaining useful life (RUL) from multivariate sensor data
2. Trace root cause via a causal asset-dependency graph
3. Generate candidate corrective actions
4. **Score each via counterfactual marginal-impact computation** through 
   a surrogate twin model (the Götze Score)
5. Select via deterministic argmax of that score
6. **Generate a visual proof** that the winning action rescues the asset 
   (RED → GREEN trajectory flip)
7. **Self-recalibrate** scoring weights from realized post-action outcomes

---

## What is Novel (Prior Art Gap)

| Prior Art | What it does | What it misses |
|---|---|---|
| LIME/SHAP | Explains model predictions | Does not explain action outcomes |
| Prescriptive maintenance | Proposes actions | Does not prove they work |
| Digital twins | Simulates asset | Does not rank/prove maintenance actions |
| MetaGPT | Multi-agent software dev | Industrial domain, decision scoring |

**Our gap:** The counterfactual-twin-scored, energy-aware, self-recalibrating 
decision selector as a **unified, auditable method** does not appear in prior art.

---

## Götze Score Formula

G = w₁·ΔHealth + w₂·(1−NormCost) + w₃·(1−NormTime) + w₄·Safety

Where:
- ΔHealth  = predicted RUL gain if action applied (surrogate twin output)
- NormCost = action cost normalised across candidate set (lower = better)
- NormTime = downtime hours normalised (faster = better)
- Safety   = action safety risk score [0, 1]
- w₁+w₂+w₃+w₄ = 1.0 (deterministic, auditable, reproducible)

Default weights: health=0.40, cost=0.25, time=0.20, safety=0.15

---

## Evidence of Reduction to Practice

Working implementation: `evidence/gotze_engine.py`
Counterfactual demo: `evidence/counterfactual_demo.py`
Results on NASA C-MAPSS FD001: `evidence/experiments/`
```

---

## CLAIM FILES: TEMPLATES

### `claims/CLAIM_01_counterfactual_proof_engine.md`

```markdown
# CLAIM 1: Counterfactual Proof Engine for Industrial Maintenance Decisions

## Independent Claim (broadest)
A computer-implemented method for generating proof-of-efficacy for industrial 
maintenance decisions, comprising:
  (a) receiving sensor data indicating a predicted remaining useful life 
      below a critical threshold;
  (b) simulating a counterfactual asset health trajectory for each candidate 
      maintenance action using a surrogate model trained on historical asset data;
  (c) computing a multi-objective deterministic score for each candidate action, 
      said score comprising weighted terms for health gain, cost, downtime, and safety;
  (d) selecting the candidate action with the highest deterministic score;
  (e) generating a visualization comparing the actual degradation trajectory 
      with the counterfactual rescued trajectory as auditable proof of decision efficacy.

## Dependent Claims (narrower — harder to design around)
  1a. The method of claim 1, wherein the surrogate model is retrained from 
      realized post-action outcomes in a closed feedback loop.
  1b. The method of claim 1, wherein the visualization includes an energy 
      efficiency term in the multi-objective score.
  1c. The method of claim 1, wherein the deterministic scoring layer is 
      architecturally isolated from any probabilistic AI layer.

## Novelty Argument
See `prior_art/PRIOR_ART_ANALYSIS.md` for documented gaps in prior art.
LIME/SHAP (US10657461B2) explain model predictions, not action outcomes.
Prescriptive maintenance (US20190213506A1) proposes actions without proof.
Digital twin literature simulates assets without ranking maintenance decisions.
```

---

## PRIOR ART ANALYSIS TEMPLATE

### `prior_art/PRIOR_ART_ANALYSIS.md`
```markdown
# Prior Art Analysis

## Search date: 2026-06-20
## Claim scope: Counterfactual proof of maintenance action efficacy

| Patent / Paper | Authors | Year | What it covers | Gap vs our claim |
|---|---|---|---|---|
| US10657461B2 (LIME) | Ribeiro et al. | 2016 | Model prediction explanation | Explains predictions, not action outcomes |
| US20190213506A1 | GE Digital | 2019 | Prescriptive maintenance | Proposes actions, no counterfactual proof |
| US10846625B2 | Siemens | 2020 | Digital twin simulation | Simulates asset, doesn't rank/prove actions |
| MetaGPT (arXiv 2308.00352) | Hong et al. | 2023 | Multi-agent software SDLC | Software domain only; no industrial maintenance |

### Conclusion
No prior art combines: counterfactual simulation + deterministic scoring + 
proof visualization + self-recalibrating weights in a single unified method 
for industrial maintenance decisions. Our gap is clear.
```

---

## FILING TIMELINE

| Date | Action | Cost |
|---|---|---|
| **2026-06-20** | Initialize FORGE repo, commit invention disclosure | $0 |
| **2026-07-09** | Hackathon presentation = public disclosure event | $0 |
| **2026-07-10** | File provisional patent application (USPTO) | ~$320 USD |
| **2027-07-09** | Deadline to convert provisional to full patent | ~$10K USD |
| **2026-06-30** | Submit LTTS invention disclosure (internal IP committee) | $0 |

**Critical:** US patent law gives you **12 months from first public disclosure** to file a provisional. The hackathon presentation on July 9 starts that 12-month clock.

---

## HOW METAGPT MAKES THIS STRONGER

When you later integrate MetaGPT (Level 3 adoption), the FORGE repo gains:

1. **Role-attributed commits:** "DiagnosisRole outputs root cause" is a more specific claim than "LLM outputs text"
2. **Action-level granularity:** Each MetaGPT Action is a claimable sub-method
3. **Agent coordination proof:** The multi-agent orchestration itself is a novel implementation method

---

*GITHUB-FORGE-REPO-GUIDE.md · PlantMind · v1.0 · 2026-06-20*
