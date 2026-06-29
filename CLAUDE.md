# PlantMind-Live

**Single canonical project folder.** All work happens here.

## Session start (mandatory, in order)
1. Read `00-START-HERE.md`
2. Read `LOCKED_STATE.md`
3. Read highest-version file in `Chat Context/` (parse `vX.Y` as integers)
4. Read `ROADMAP.md` — summarize NOW items before proceeding
5. If task type is unclear, consult `ops/ROUTING.md`

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