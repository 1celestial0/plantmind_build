# Demo runbook

## v1 (today — FORGE fallback)

```powershell
cd "C:\Users\hp\Claude\Projects\PlantMind"
pip install -r FORGE/requirements.txt
streamlit run FORGE/app.py
```

**Tabs:** Decision · Proof Chart · Fleet View · Agent Trace

## v2 (target — from PlantMind)

```powershell
cd "C:\Users\hp\Claude\Projects\PlantMind"
# streamlit run src/dashboard/app.py   # when wired
# uvicorn src.api.main:app --reload    # when API ready
```

## 5-minute script

Source: migrate from `PlantMind_hckthn/08_DEMO_SCENARIOS.md`

1. Healthy plant dashboard
2. Inject failure (pump degrading)
3. 5 agents fire → one best action + IIS
4. Human approves → audit updates
5. Close: Götze line + Databricks partnership

## Freeze protocol (6h before July 9)

- Lock `requirements.txt` versions
- Screenshot all charts
- Record backup video
- Tag git: `v1.0-hackathon-submission`