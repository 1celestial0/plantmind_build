# Parallel documentation — one doc per lane, updated while you build

These files **mirror the five build lanes**. Update your lane doc when you ship something — do not wait for session close.

| File | Lane | Owner updates when… |
|------|------|---------------------|
| `lane-01-backend.md` | 1 | agents, API, audit change |
| `lane-02-physics.md` | 2 | Weibull, synthesis, data change |
| `lane-03-dashboard.md` | 3 | UI mockups, Streamlit change |
| `lane-04-databricks.md` | 4 | notebooks, deploy change |
| `lane-05-demo-pitch.md` | 5 | script, ROI, Q&A change |
| `testing.md` | all | scenarios, pytest, test-log change |
| **`STATUS.md`** | rollup | **any lane moves — 1-line per lane** |

**Truth order:** `LOCKED_STATE` > `ARCHITECTURE_LOCK` > these living docs > chat.

**CLI rule:** Any AI updating code in a lane should offer to update the matching `lane-0N-*.md` in the same goal batch.