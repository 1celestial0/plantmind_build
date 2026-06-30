# Contributing — PlantMind Git Workflow

> Repo: https://github.com/1celestial0/plantmind_build (private). Default branch **`main`** = always-trusted, always-buildable. Source of truth = `PROJECT-DNA.md`.

## Golden rules
1. **`main` is sacred** — only reviewed, working code lands there. Never commit straight to `main` for feature work.
2. **One branch per feature** — features come from `PROJECT-DNA §6` (F-01 … F-15). Branch name encodes the feature ID.
3. **DNA-first** — adding a *new* feature (beyond F-01…F-15) requires a DNA §6 entry + an Amendment *before* the branch.
4. **Contracts = vault update** — changing `src/contracts/` requires a paired `LOCKED_STATE §4` update, reviewed.

## Branch naming
| Intent | Pattern | Example |
|---|---|---|
| Build a feature | `feat/F-XX-slug` | `feat/F-10-contracts` |
| Remove/retire | `chore/remove-F-XX-slug` | `chore/remove-pinn` |
| Fix | `fix/slug` | `fix/rul-unit-days` |
| Docs/governance | `docs/slug` | `docs/regen-deliverables` |

## Add a feature (flow)
```
git checkout main && git pull --rebase
git checkout -b feat/F-03-maintenance-scheduler
# ...build, commit small...
git push -u origin feat/F-03-maintenance-scheduler
# open a Pull Request → review → squash-merge to main → delete branch
```
After merge: re-run `python scripts/gen_team_docs.py` (status updates) and "sync to drive".

## Remove a feature
Branch `chore/remove-F-XX-…`, delete the code + its DNA §6 entry (with an Amendment noting why), PR to `main`.

## Forking (external collaborators / experiments)
Team members branch directly. Outside collaborators (or risky experiments): **fork** → branch → PR back to `1celestial0/plantmind_build`. Keep the fork's `main` synced: `git remote add upstream https://github.com/1celestial0/plantmind_build.git` then `git pull upstream main`.

## Lanes ↔ branches
One lane per working session (LOCKED_STATE §8). Two people never push the same lane's files on the same branch — branch per feature keeps lanes isolated. Lanes integrate only through `src/contracts/`.

## Sync commands (user-triggered)
- **"push to github"** → `scripts/git-sync.ps1 "msg"` (commit + pull --rebase + push).
- **"sync to drive"** → AI uploads the deliverable set to the project Drive folder.

## Milestones
Tag trusted checkpoints: `git tag -a v1.0-lock -m "Product idea locked"` then `git push origin v1.0-lock`.
