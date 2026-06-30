# PlantMind

**Single canonical project folder.** All work happens here.  
**Multi-AI rules:** See `AI-OPERATING-SYSTEM.md` (Claude + Grok + Gemini share this folder).

## Precedence (apex → low)
`PROJECT-DNA.md` (L0 constitution) ▸ `LOCKED_STATE.md` (L1 technical vault) ▸ derived docs / Obsidian vaults (L2) ▸ ROADMAP / Chat Context (L3). **If any doc disagrees with `PROJECT-DNA.md`, the other doc is wrong** until a numbered Amendment changes the DNA. Never create a new "master" doc — extend the DNA.

## Session start (mandatory, in order)
1. Read `PROJECT-DNA.md` — **the constitution (apex truth):** identity, two pillars, scope fence (CLOSED decisions), 15-feature inventory, rubric.
2. Read `LOCKED_STATE.md` — technical vault (contracts, λ/β §6a, thresholds, lanes).
3. Read `AI-OPERATING-SYSTEM.md` (if multi-tool session)
4. Read `00-START-HERE.md`
5. Read highest-version file in `Chat Context/` (parse `vX.Y` as integers)
6. Read `ROADMAP.md` — summarize NOW items before proceeding
7. If building: read `docs/IMPLEMENTATION-GUIDE-ULTRA.md` (conform to DNA §6 if they differ)
8. If task type is unclear, consult `ops/ROUTING.md`

## Session close (offer before ending)
Run project-continuity `close`: ROADMAP update → new context version → git commit.

## Code discipline
- Application code: `src/` and `ml/` only
- Shared schemas: `src/contracts/` — changes require LOCKED_STATE vault update
- Prompts/workflows: `ops/` only
- Research artifacts: `docs/research/` only
- Never treat `../PlantMind/` or `../PlantMind_hckthn/` as write targets unless explicitly migrating

## Lane discipline
One chat = one lane. See `ops/prompts/lanes/README.md`.