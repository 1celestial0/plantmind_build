---
tags: [technology, framework, metagpt]
created: 2026-06-20
---

# MetaGPT

## What It Is

MetaGPT is an open-source multi-agent framework (MIT license) where LLM agents are assigned **software engineering roles** and collaborate to complete development tasks.

Published: Hong et al., arXiv:2308.00352 (2023)
GitHub: https://github.com/geekan/MetaGPT

## Core Architecture

```
One natural-language idea
    ↓
ProductManager → writes PRD (Product Requirements Document)
    ↓
Architect → produces system design + API signatures
    ↓
ProjectManager → breaks design into task tickets
    ↓
Engineer → writes code per ticket
    ↓
QAEngineer → writes tests
```

The key insight: giving an LLM a *role* instead of a *task* dramatically improves output quality.

## How PlantMind Adopts MetaGPT

Three adoption levels (see `LEARNING/METAGPT-ADOPTION-GUIDE.md`):

**Level 1 (now):** Use MetaGPT's *thinking patterns* — typed inputs/outputs, role boundaries, message contracts — without installing MetaGPT.

**Level 2 (this week):** Restructure `FORGE/src/` with MetaGPT-aligned message passing. Each PlantMind layer becomes a Role with typed I/O.

**Level 3 (post-hackathon):** Install MetaGPT, replace manual orchestration with MetaGPT's Environment. Scale to multi-plant, multi-agent deployments.

## PlantMind → MetaGPT Role Mapping

| MetaGPT Role | PlantMind equivalent |
|---|---|
| ProductManager | Blueprint + Rubric strategy |
| Architect | 5-layer system design |
| ProjectManager | 7-day sprint plan |
| Engineer (ML) | `src/model.py` + `src/features.py` |
| Engineer (Decision) | `src/gotze_engine.py` |
| QAEngineer | `FORGE/REVERSE_ENGINEER.md` |

## What Makes PlantMind's MetaGPT Use Novel

Standard MetaGPT: builds software from requirements.
PlantMind's MetaGPT: builds **industrial AI decisions** — each "product" is a maintenance recommendation, not code.

This extension to industrial decision-making is what's covered by [[Patent 3 - Domain Adaptive KB]] and [[Patent 4 - Research Augmented MetaGPT]].

## Connected Nodes

- PlantMind builds on → MetaGPT conceptually
- Extended by → [[Patent 4 - Research Augmented MetaGPT]]
- Extended by → [[Patent 3 - Domain Adaptive KB]]
- Deep guide → `LEARNING/METAGPT-ADOPTION-GUIDE.md`
- FORGE repo → `FORGE/GITHUB-FORGE-REPO-GUIDE.md`
