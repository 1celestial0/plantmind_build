# MetaGPT Adoption Guide for PlantMind
## Mental Model: How MetaGPT Fits, What to Take, What to Ignore

---

## WHAT IS METAGPT (the 60-second version)

MetaGPT is an open-source multi-agent framework that assigns **software engineering roles** to LLM agents:
- **ProductManager** → writes PRDs from a one-sentence idea
- **Architect** → converts PRD into system design + API signatures
- **ProjectManager** → breaks design into task tickets
- **Engineer** → writes the actual code per ticket
- **QAEngineer** → writes test plans and runs tests

The key insight MetaGPT demonstrates:
> "When you give an LLM a *role* instead of a *task*, the output quality jumps dramatically."

MIT License → you can use, modify, build on, commercialise it freely.

---

## WHY MetaGPT MATTERS FOR PLANTMIND

| PlantMind need | MetaGPT provides |
|---|---|
| Structured multi-layer system | Role-based architecture that naturally maps to layers |
| Patent-worthy IP | FORGE concept: structured, timestamped, role-attributed code = strong invention disclosure |
| Scalable agent design | MetaGPT's `Role`, `Action`, `Message` architecture → use for your LLM diagnosis agent |
| Code quality | MetaGPT enforces structured output (JSON, typed responses) — same discipline you need |
| Multi-agent coordination | Your 5-layer pipeline IS a multi-agent pipeline in disguise |

---

## THE ADOPTION MENTAL MODEL: 3 LEVELS

```
LEVEL 1: CONCEPTUAL (adopt today — no code changes)
  Use MetaGPT's THINKING PATTERNS in how you design PlantMind
  Role → Action → Output → next Role's Input

LEVEL 2: STRUCTURAL (adopt this week — restructure your src/)
  Use MetaGPT's MESSAGE PASSING architecture for layer communication
  Each layer becomes a Role. Layers talk via typed Messages.

LEVEL 3: RUNTIME (adopt post-hackathon — full MetaGPT integration)
  Actually install MetaGPT. Replace manual orchestration with MetaGPT's Environment.
  Scale to multiple asset types, multiple plants, multiple LLM backends.
```

---

## LEVEL 1: ADOPT THE THINKING PATTERN (TODAY)

### MetaGPT Role → PlantMind Layer mapping

| MetaGPT Role | PlantMind equivalent | Current file |
|---|---|---|
| ProductManager | Blueprint + Rubric strategy | `01-PlantMind-Blueprint.md` |
| Architect | 5-layer system design | Section in Blueprint |
| ProjectManager | 7-day sprint plan | `02-PlantMind-7Day-Plan.md` |
| Engineer (Data) | Ingestion + Features | `src/ingestion.py`, `src/features.py` |
| Engineer (ML) | RUL model | `src/model.py` |
| Engineer (Decision) | Götze Engine | `src/gotze_engine.py` |
| QAEngineer | REVERSE_ENGINEER.md | `FORGE/REVERSE_ENGINEER.md` |

**Action:** Every time you write a new module, ask: "Which role owns this? What is its typed input/output contract?"

### MetaGPT Action → PlantMind step mapping

MetaGPT's `Action` class has one rule: **one input type → one output type**. Apply this to PlantMind:

```python
# MetaGPT pattern (conceptual — you don't need to import MetaGPT yet)
# 
# WHAT  : Every Action has exactly ONE job and ONE typed output
# WHY   : Makes the system debuggable — if output is wrong, exactly ONE action is the cause
# HOW   : Input type → Action logic → Output type → next Action's input
# WHEN  : Always — never let an action produce ambiguous or untyped output
# WHY NOT: Functions that return "anything" are impossible to test or swap

class IngestAction:
    input:  str            # file path to C-MAPSS txt file
    output: pd.DataFrame   # cleaned dataframe with RUL column

class FeatureAction:
    input:  pd.DataFrame   # output of IngestAction
    output: pd.DataFrame   # dataframe with rolling features added

class PredictAction:
    input:  pd.DataFrame   # output of FeatureAction
    output: list[EngineHealth]  # typed dataclass per engine

class GotzeAction:
    input:  EngineHealth   # one RED engine
    output: EngineDecision # typed decision with winner + proof
```

---

## LEVEL 2: STRUCTURAL REFACTOR (THIS WEEK)

### The Message Bus pattern

MetaGPT agents communicate via a shared **Environment** (message bus). For PlantMind:

```python
# ═══════════════════════════════════════════════════════════════
# WHAT  : Typed message dataclasses for inter-layer communication
# WHY   : Makes PlantMind's layers swappable — change Layer 2 without
#         touching Layer 3 as long as you keep the output type identical
# HOW   : Python dataclass + type hints + validation = contract enforcement
# WHEN  : Import these in every layer module
# WHY NOT: Dicts (untyped) → impossible to catch schema drift;
#           plain tuples → no field names → unreadable
# ═══════════════════════════════════════════════════════════════

from dataclasses import dataclass
import pandas as pd
from typing import List

@dataclass
class SensorReading:
    """Output of Layer 1 (Ingestion). Input to Layer 2 (Features)."""
    engine_id: int
    cycle: int
    sensors: dict[str, float]   # s1..s21
    rul_label: float             # clipped to 130

@dataclass
class EngineHealth:
    """Output of Layer 2+3 (Features + Prediction). Input to Layer 4."""
    engine_id: int
    current_rul: float
    feature_vector: list[float]
    health_status: str           # "RED" | "YELLOW" | "GREEN"

@dataclass
class EngineDecision:
    """Output of Layer 4 (Götze). Input to Layer 5 (Dashboard)."""
    engine_id: int
    current_rul: float
    root_cause: str
    winner_action: str
    winner_score: float
    rul_gain: float
    is_rescued: bool
    all_scores: list[dict]       # for chart rendering
```

### Directory refactor for MetaGPT alignment

```
FORGE/
├── src/
│   ├── messages.py      ← NEW: all typed message dataclasses
│   ├── roles/           ← NEW: each "role" owns one layer
│   │   ├── data_engineer.py    (wraps ingestion.py + features.py)
│   │   ├── ml_engineer.py      (wraps model.py)
│   │   ├── decision_engine.py  (wraps gotze_engine.py)
│   │   └── proof_renderer.py   (RED→GREEN chart generation)
│   ├── ingestion.py     ← keep (pure functions, no change)
│   ├── features.py      ← keep
│   ├── model.py         ← keep
│   └── gotze_engine.py  ← keep
└── run_demo.py          ← orchestrates roles, not raw functions
```

---

## LEVEL 3: FULL METAGPT RUNTIME (POST-HACKATHON)

### Install MetaGPT
```bash
# WHAT  : Install MetaGPT and its dependencies
# WHY   : Gives us the Environment, Role, Action, Message infrastructure
# HOW   : pip install from PyPI; config via config2.yaml
# WHEN  : Post-hackathon, when scaling beyond single-machine prototype
# WHY NOT: Don't install before hackathon — adds dependency risk to demo

pip install metagpt
metagpt --init-config   # creates ~/.metagpt/config2.yaml
```

### Configure for PlantMind
```yaml
# ~/.metagpt/config2.yaml
llm:
  api_type: "anthropic"
  model: "claude-sonnet-4-6"
  api_key: "YOUR_KEY"
```

### PlantMind as a MetaGPT Team
```python
# ═══════════════════════════════════════════════════════════════
# WHAT  : Wire PlantMind's 5 layers as a MetaGPT Team
# WHY   : Gets you automatic message routing, parallel execution,
#         LLM-powered diagnosis (replace hardcoded root cause)
# HOW   : Each Role subscribes to an input message type and publishes
#         its output to the Environment for the next Role to consume
# WHEN  : Post-hackathon v2 of PlantMind
# WHY NOT: Overkill for hackathon; adds 3h of setup risk
# ═══════════════════════════════════════════════════════════════

import asyncio
from metagpt.team import Team
from metagpt.roles import Role

# Each PlantMind layer becomes a Role
# (full implementation in FORGE/metagpt_integration/ post-hackathon)
team = Team()
team.hire([
    DataEngineerRole(),      # Layer 1+2
    MLEngineerRole(),        # Layer 3
    GotzeDecisionRole(),     # Layer 4
    ProofRendererRole(),     # Layer 5
])
asyncio.run(team.run(idea="Diagnose all RED engines in C-MAPSS FD001"))
```

---

## WHY MetaGPT FORGE = PATENT-READY REPO

MetaGPT's FORGE repository structure creates three things that matter for IP:

1. **Timestamped commits** = proof of invention date (GitHub commit timestamp = prior art date)
2. **Role-attributed code** = "Götze Decision Engine role invented by [authors]" is traceable
3. **Structured documentation** = Architecture docs + API specs are 80% of a provisional patent application

The separate FORGE GitHub repo (see `GITHUB-FORGE-REPO-GUIDE.md`) exploits this directly.

---

## WHAT TO IGNORE IN MetaGPT (for now)

| MetaGPT feature | Skip it because |
|---|---|
| `Software Company` example | Generates code from scratch — you already have the code |
| `Researcher` role | Generates research papers — not your use case |
| `DataInterpreter` | Good for data science notebooks, but adds overhead |
| Full `Environment` class | Overkill until you're running 5+ concurrent agents |
| `Memory` class | Use your own `feedback_loop.py` instead |

---

*METAGPT-ADOPTION-GUIDE.md · PlantMind · v1.0 · 2026-06-20*
