# PlantMind — Standard Deliverable Set (always-live)

> One source of truth, many renderings. **`PROJECT-DNA.md` is the only truth.** Everything below is *generated from it* and re-generated whenever the DNA changes — so all artifacts stay consistent. Never edit a rendering as if it were truth; change the DNA, then regenerate.

## The set
| # | Artifact | Format | Made by | Regenerate with |
|---|---|---|---|---|
| — | PROJECT-DNA | md | — (apex truth) | hand-edited via Amendment (§10) |
| — | LOCKED_STATE | md | — (technical truth) | VAULT UPDATE |
| 1 | Team Intro deck | PPTX + PDF | Gamma | ask AI: "regenerate the deck" |
| 2 | Executive Brief | DOCX | `scripts/gen_team_docs.py` | `python scripts/gen_team_docs.py` |
| 3 | Feature/Rubric/Top-20 Tracker | XLSX | `scripts/gen_team_docs.py` | `python scripts/gen_team_docs.py` |
| 4 | Project / UI-UX / Databricks Spec v2.0 | md | AI from DNA | ask AI: "regenerate the specs" |
| 5 | Onboarding cover | md | AI from DNA | ask AI: "regenerate onboarding" |

## Keep it live (the rule)
After any **DNA Amendment** or **LOCKED_STATE VAULT UPDATE**:
1. `python scripts/gen_team_docs.py` → refreshes Brief + Tracker.
2. Ask AI to regenerate the deck + specs from the DNA.
3. **"sync to drive"** → AI re-uploads the set to the project Drive folder.
4. **"push to github"** → `scripts/git-sync.ps1` commits + pushes.

This way every interconnected artifact always reflects the current locked truth.

## Distribution
- **Drive (team-facing):** `PlantMind / PlantMind_SourceOfTruth_v2_2026-07-01/` — Google Docs.
- **GitHub (code + truth):** https://github.com/1celestial0/plantmind_build (private, branch `main`).
