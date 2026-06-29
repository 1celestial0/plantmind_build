# PlantMind — 7-Day Execution Plan
### Strategy · Execution · Deployment · Tooling
**Goal:** Complete, demo-ready, patent-ready PlantMind by EOD Day 6. Day 7 = rehearsal only.

---

## GOVERNING RULES

1. **One working demo beats ten perfect modules.** Cut scope ruthlessly; never cut the RED→GREEN chart.
2. **Freeze the build at Hour 18 of Hackathon Day.** No new features after that — only bug fixes.
3. **Data first, AI second.** If the data pipeline isn't working, nothing else works.
4. **Mock what doesn't affect the core claim.** The LLM agent's reasoning can be pre-computed. The Götze score must be live.
5. **One integration test per day** — end-to-end from raw CSV to Streamlit output.

---

## TEAM TAGS

- **[S]** = Sourav (data eng, ML, engine)
- **[A]** = Streamlit dev (app, wiring)
- **[V1]** = Viz person 1 (charts)
- **[V2]** = Viz person 2 (dashboard)
- **[ALL]** = sync required

---

## DAY 0 — TONIGHT (Pre-kickoff, ~2 hours)

### Strategy
Lock the product. No more scope changes after tonight.

### Actions
- **[ALL]** Read the Blueprint doc fully — confirm understanding of 5 layers and 11 steps
- **[S]** Clone NASA C-MAPSS from Kaggle/GitHub — confirm FD001 loads in pandas without error
- **[S]** Set up GitHub repo: `plantmind-ei-2026` — add all 4 as collaborators
- **[A]** Install: `pip install streamlit plotly scikit-learn anthropic`
- **[V1] [V2]** Confirm Plotly works: run `import plotly.express as px; px.line([1,2,3]).show()`
- **[ALL]** Create shared folder (Google Drive or GitHub `/docs`) for interim outputs

### Learn (20 min)
Read these two pages only:
- NASA C-MAPSS readme: [https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/](https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository/)
- Streamlit quickstart: [https://docs.streamlit.io/get-started/tutorials/create-an-app](https://docs.streamlit.io/get-started/tutorials/create-an-app)

### Success checkpoint
- Repo exists, everyone has access
- `df = pd.read_csv('train_FD001.txt', sep=' ', header=None)` → prints a dataframe ✓

---

## DAY 1 — DATA PIPELINE + RUL MODEL [S leads]

### Strategy
Get a working RUL number out of real data. Everything downstream depends on this.

### Learn (30 min) — before building
- Read: [https://github.com/Azure/PredictiveMaintenance](https://github.com/Azure/PredictiveMaintenance) — the Microsoft reference implementation of C-MAPSS preprocessing. Borrow the feature-engineering pattern, not the code.
- Understand: C-MAPSS has 26 columns: engine_id, cycle, 3 op_settings, 21 sensors. RUL = max_cycle − current_cycle.

### Implement

```python
# Step 1: Load and label
import pandas as pd
cols = ['engine_id','cycle','setting_1','setting_2','setting_3'] + [f's{i}' for i in range(1,22)]
train = pd.read_csv('train_FD001.txt', sep=r'\s+', header=None, names=cols)
train['RUL'] = train.groupby('engine_id')['cycle'].transform(max) - train['cycle']

# Step 2: Feature engineering — rolling stats over last 30 cycles
feat_cols = [f's{i}' for i in [2,3,4,7,8,9,11,12,13,14,15,17,20,21]]  # high-variance sensors only
window = 30
for col in feat_cols:
    train[f'{col}_mean'] = train.groupby('engine_id')[col].transform(lambda x: x.rolling(window, min_periods=1).mean())
    train[f'{col}_std']  = train.groupby('engine_id')[col].transform(lambda x: x.rolling(window, min_periods=1).std().fillna(0))

# Step 3: Train RUL model
from sklearn.ensemble import RandomForestRegressor
feature_cols = [c for c in train.columns if '_mean' in c or '_std' in c]
X = train[feature_cols]; y = train['RUL'].clip(upper=130)
from sklearn.model_selection import train_test_split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, n_jobs=-1, random_state=42)
model.fit(X_tr, y_tr)

# Step 4: Save model
import joblib; joblib.dump(model, 'rul_model.pkl')
print("RMSE:", ((model.predict(X_te) - y_te)**2).mean()**0.5)
```

### Tooling
- scikit-learn, pandas, joblib
- Target RMSE < 25 cycles on FD001 (achievable with RF, no tuning)

### [V1] parallel task
- Build the RUL timeline chart template (just with dummy data today):
  - X: cycles, Y: health score (100 − RUL/max_RUL × 100)
  - Two lines: red (do-nothing) and green (will get real data Day 3)
  - Amber horizontal line at threshold (health = 30)

### [V2] parallel task
- Build the asset-health dashboard tile grid: 6 engine tiles, each showing engine_id + health status badge (RED/AMBER/GREEN) + RUL number
- Use dummy data today; wire real model output Day 2

### Success checkpoint EOD Day 1
- `model.predict(X_te)` → RMSE < 30 ✓
- RUL timeline chart renders with dummy data ✓
- Asset tile grid renders with 6 dummy tiles ✓

---

## DAY 2 — SURROGATE TWIN + HEALTH FLAG [S + A]

### Strategy
Build the counterfactual engine's backbone — the surrogate twin. This is the highest technical risk in the project. Keep it simple.

### Learn (20 min)
The Twin does NOT need to be a physics model. It only needs to answer: "If I take action X, how does the degradation rate change?"

A degradation model is: `health(t) = 100 × exp(−λ × t)` where λ is the degradation rate.

Each action modifies λ: `λ_action = λ_base × action_modifier`

- Replace failing part → λ resets to near-zero
- Reduce load 15% → λ × 0.60 (40% slower degradation)
- Reroute workload → λ × 0.75
- Do nothing → λ × 1.0

### Implement

```python
import numpy as np

# Fit baseline degradation rate from real RUL data
def fit_lambda(engine_df):
    """Fit exponential degradation rate for one engine."""
    cycles = engine_df['cycle'].values
    health = (1 - engine_df['cycle'] / engine_df['cycle'].max()).values * 100
    from scipy.optimize import curve_fit
    try:
        popt, _ = curve_fit(lambda t, lam: 100 * np.exp(-lam * t), cycles, health, p0=[0.01], maxfev=1000)
        return max(popt[0], 1e-5)
    except:
        return 0.015  # fallback

# Action modifier table (deterministic rules)
ACTION_MODIFIERS = {
    'replace_part':     {'lambda_mult': 0.05, 'cost': 8.0,  'label': 'Replace failing component'},
    'reduce_load_15':   {'lambda_mult': 0.60, 'cost': 2.0,  'label': 'Reduce operating load 15%'},
    'reroute_workload': {'lambda_mult': 0.75, 'cost': 1.5,  'label': 'Reroute to parallel unit'},
    'monitor_only':     {'lambda_mult': 1.00, 'cost': 0.1,  'label': 'Monitor only (do nothing)'},
}

def simulate_action(current_cycle, max_cycle, lam_base, action_key, future_cycles=60):
    """Return simulated health trajectory under given action."""
    mod = ACTION_MODIFIERS[action_key]
    lam_new = lam_base * mod['lambda_mult']
    future = np.arange(current_cycle, current_cycle + future_cycles)
    health = 100 * np.exp(-lam_new * (future - current_cycle))
    failure_cycle = next((f for f, h in zip(future, health) if h < 30), current_cycle + future_cycles)
    return {'cycles': future.tolist(), 'health': health.tolist(), 'failure_cycle': int(failure_cycle), 'action': action_key}
```

### [A] parallel task
- Wire `rul_model.pkl` into Streamlit: load model on app startup, run prediction on FD001 test data
- Show live RUL numbers in the dashboard tiles
- Add a RED/AMBER/GREEN badge: RUL < 30 = RED, 30–60 = AMBER, > 60 = GREEN

### Success checkpoint EOD Day 2
- `simulate_action(35, 80, 0.015, 'reduce_load_15')` → returns a trajectory that fails later than `monitor_only` ✓
- Streamlit dashboard shows real RED/GREEN/AMBER status on real model output ✓

---

## DAY 3 — GÖTZE DECISION ENGINE [S leads]

### Strategy
This is the patent core. Build it precisely. The formula must be deterministic, auditable, and produce a number you can explain term by term.

### Learn (15 min)
Multi-objective decision scoring is well-established in operations research. Our novelty is:
1. The objectives are computed from a counterfactual twin (not from historical data)
2. Energy is one of the four objectives (ties to Sustainability)
3. The weights recalibrate from realized outcomes (closed loop)

### Implement

```python
import numpy as np

def gotze_score(sim_result, action_key, confidence, current_rul, base_rul=30):
    """
    Compute GötzeScore for a candidate action.
    
    Parameters
    ----------
    sim_result   : dict from simulate_action() — contains failure_cycle
    action_key   : str — key in ACTION_MODIFIERS
    confidence   : float [0,1] — diagnosis agent's confidence
    current_rul  : float — current RUL from ML model
    base_rul     : float — RUL of do-nothing baseline
    
    Returns
    -------
    dict with score, breakdown, and explanation
    """
    mod = ACTION_MODIFIERS[action_key]
    
    # Objective 1: Life gained (normalized to 0-1)
    delta_life = (sim_result['failure_cycle'] - base_rul) / 100.0
    delta_life = max(delta_life, 0.0)
    
    # Objective 2: Throughput preserved (proxy: inverse of degradation disruption)
    # Rerouting and monitoring preserve throughput; replacement briefly disrupts
    throughput_map = {'replace_part': 0.60, 'reduce_load_15': 0.85, 'reroute_workload': 0.80, 'monitor_only': 1.00}
    delta_throughput = throughput_map.get(action_key, 0.70)
    
    # Objective 3: Energy saved (lambda reduction = proxy for energy efficiency gain)
    # Lower lambda_mult = more load reduction = more energy saved
    delta_energy = 1.0 - mod['lambda_mult']  # 0 = no saving, 0.95 = near-full saving
    
    # Objective 4: Risk reduced (how far failure_cycle moves past threshold)
    risk_headroom = (sim_result['failure_cycle'] - 30) / 100.0
    delta_risk = max(min(risk_headroom, 1.0), 0.0)
    
    # Weights (recalibrated by feedback loop; start at these priors)
    W = {'life': 0.40, 'throughput': 0.25, 'energy': 0.20, 'risk': 0.15}
    
    # Raw score
    raw = (W['life'] * delta_life
         + W['throughput'] * delta_throughput
         + W['energy'] * delta_energy
         + W['risk'] * delta_risk)
    
    # Confidence adjustment and cost normalization
    cost = mod['cost']
    score = (raw * confidence) / cost
    
    return {
        'action': mod['label'],
        'score': round(score, 4),
        'breakdown': {
            'delta_life':       round(delta_life, 3),
            'delta_throughput': round(delta_throughput, 3),
            'delta_energy':     round(delta_energy, 3),
            'delta_risk':       round(delta_risk, 3),
            'confidence':       confidence,
            'cost':             cost,
            'raw_weighted':     round(raw, 4),
        },
        'explain': (f"Score {score:.4f} = "
                    f"({W['life']}×{delta_life:.2f} life "
                    f"+ {W['throughput']}×{delta_throughput:.2f} throughput "
                    f"+ {W['energy']}×{delta_energy:.2f} energy "
                    f"+ {W['risk']}×{delta_risk:.2f} risk) "
                    f"× {confidence:.2f} conf ÷ {cost:.1f} cost")
    }

def rank_actions(current_cycle, lam_base, confidence, current_rul):
    """Score all candidate actions and return ranked list."""
    results = []
    base = simulate_action(current_cycle, 80, lam_base, 'monitor_only')
    base_rul = base['failure_cycle']
    for action_key in ACTION_MODIFIERS:
        sim = simulate_action(current_cycle, 80, lam_base, action_key)
        score_dict = gotze_score(sim, action_key, confidence, current_rul, base_rul)
        score_dict['trajectory'] = sim
        results.append(score_dict)
    return sorted(results, key=lambda x: x['score'], reverse=True)
```

### [V1] parallel task — wire the money-shot chart
```python
import plotly.graph_objects as go

def make_counterfactual_chart(base_traj, winner_traj):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=base_traj['cycles'],   y=base_traj['health'],   name='Do nothing', line=dict(color='#F0544A', width=3)))
    fig.add_trace(go.Scatter(x=winner_traj['cycles'], y=winner_traj['health'], name='Götze action', line=dict(color='#35C97D', width=3)))
    fig.add_hline(y=30, line_dash='dash', line_color='#EFA63C', annotation_text='failure threshold')
    fig.update_layout(template='plotly_dark', xaxis_title='Cycles', yaxis_title='Asset Health', height=380)
    return fig
```

### [V2] parallel task
- Add score-comparison bar chart: horizontal bars per action, colored by rank (gold/silver/bronze/grey)
- Add "Götze breakdown" panel: small table showing each term's contribution for the winner

### Success checkpoint EOD Day 3
- `rank_actions(35, 0.015, 0.85, 25)` → returns ranked list, monitor_only last ✓
- Winner's score > monitor_only score ✓
- Counterfactual chart renders in Streamlit with real trajectories ✓

---

## DAY 4 — LLM AGENT + INTEGRATION [S + A]

### Strategy
Wire the LLM agent for diagnosis and action proposal. Keep prompts tight — output must be parseable JSON. Pre-compute for the demo engine.

### Learn (20 min)
Read: [https://docs.anthropic.com/en/docs/build-with-claude/tool-use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
The agent needs only two capabilities: (1) reason about sensor deviations and (2) propose actions as structured JSON.

### Implement

```python
import anthropic, json

client = anthropic.Anthropic()

ASSET_GRAPH = {
    's9':  {'label': 'HPC outlet pressure',     'downstream': ['compressor_efficiency']},
    's11': {'label': 'HPC outlet temperature',  'downstream': ['compressor_efficiency', 'combustor_temp']},
    's15': {'label': 'Bypass duct pressure',    'downstream': ['fan_load']},
    's20': {'label': 'LPT outlet temperature',  'downstream': ['turbine_efficiency']},
}

def diagnose(sensor_deviations: dict, engine_id: int) -> dict:
    """
    Ask LLM agent to trace root cause from sensor anomalies.
    sensor_deviations: {sensor_name: deviation_score}
    Returns: {root_cause, confidence, actions}
    """
    prompt = f"""You are an industrial asset diagnostics agent for a turbofan engine.

Engine {engine_id} has the following sensor deviations from normal (higher = worse):
{json.dumps(sensor_deviations, indent=2)}

Asset graph (sensor → what it affects):
{json.dumps(ASSET_GRAPH, indent=2)}

Task:
1. Identify the most likely root-cause component (one of: fan, compressor, combustor, turbine, bypass_duct)
2. Assign a confidence score 0-1
3. Propose exactly 3 corrective actions from: replace_part, reduce_load_15, reroute_workload, monitor_only

Respond ONLY as JSON:
{{"root_cause": "...", "mechanism": "...", "confidence": 0.0, "actions": ["...", "...", "..."]}}"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    try:
        return json.loads(response.content[0].text)
    except json.JSONDecodeError:
        return {"root_cause": "compressor", "mechanism": "thermal stress", "confidence": 0.80, "actions": ["reduce_load_15", "replace_part", "reroute_workload"]}

def get_sensor_deviations(engine_df, current_cycle):
    """Compute deviation of key sensors from their baseline mean."""
    sensors = ['s9', 's11', 's15', 's20']
    baseline = engine_df[engine_df['cycle'] < 20][sensors].mean()
    current  = engine_df[engine_df['cycle'] == current_cycle][sensors].mean()
    deviations = ((current - baseline) / (baseline.abs() + 1e-6)).to_dict()
    return {k: round(float(v), 3) for k, v in deviations.items()}
```

### [A] integration task — full pipeline in Streamlit
```python
# app.py skeleton
import streamlit as st
import joblib, pandas as pd

@st.cache_resource
def load_model(): return joblib.load('rul_model.pkl')

def main():
    st.set_page_config(page_title='PlantMind', layout='wide', page_icon='🏭')
    st.title('🏭 PlantMind — Agentic Asset Intelligence')
    
    model = load_model()
    # [wire data, predictions, diagnosis, Götze engine, charts here]
    # Keep each section as a clearly named function

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader('Asset Health')
        # tile grid
    with col2:
        st.subheader('Decision Engine')
        # chart + score bars

if __name__ == '__main__': main()
```

### Success checkpoint EOD Day 4
- `diagnose(deviations, engine_id=1)` → returns valid JSON ✓
- Full pipeline: CSV → prediction → diagnosis → rank_actions → chart → renders in Streamlit ✓
- End-to-end integration test passes without exceptions ✓

---

## DAY 5 — FEEDBACK LOOP + DATABRICKS SHOWCASE [S]

### Strategy
Build the weight recalibration loop. Set up Databricks CE for the "production pathway" story.

### Learn (20 min)
Read Databricks Community Edition quickstart: [https://docs.databricks.com/en/getting-started/community-edition.html](https://docs.databricks.com/en/getting-started/community-edition.html)

You only need:
1. Create a free account
2. Create a cluster (DBR 14.x, single node)
3. Upload the C-MAPSS CSV files
4. Run the preprocessing notebook

### Implement — feedback loop

```python
import json, os

WEIGHTS_FILE = 'gotze_weights.json'
DEFAULT_WEIGHTS = {'life': 0.40, 'throughput': 0.25, 'energy': 0.20, 'risk': 0.15}

def load_weights():
    if os.path.exists(WEIGHTS_FILE):
        return json.load(open(WEIGHTS_FILE))
    return DEFAULT_WEIGHTS.copy()

def recalibrate_weights(weights, predicted_rul, actual_rul, action_taken):
    """
    Nudge weights based on outcome error.
    If action saved more life than predicted → increase life weight.
    If action saved less life than predicted → decrease life weight.
    """
    error = (actual_rul - predicted_rul) / 100.0  # normalize
    lr = 0.05  # learning rate — small enough that one bad outcome doesn't break it
    
    if action_taken in ('replace_part', 'reduce_load_15'):
        weights['life'] = min(0.60, max(0.20, weights['life'] + lr * error))
    
    # Re-normalize weights to sum to 1
    total = sum(weights.values())
    weights = {k: round(v / total, 4) for k, v in weights.items()}
    
    json.dump(weights, open(WEIGHTS_FILE, 'w'), indent=2)
    return weights
```

### Databricks notebook (paste into CE cell)
```python
# Databricks Cell 1: Setup
%pip install scikit-learn
import pandas as pd, numpy as np

# Databricks Cell 2: Load data from DBFS
cols = ['engine_id','cycle','s1','s2','s3'] + [f's{i}' for i in range(1,22)]
df = spark.read.csv('/FileStore/tables/train_FD001.txt', sep=' ').toPandas()

# Databricks Cell 3: Feature engineering (same as local)
df['RUL'] = df.groupby('engine_id')['cycle'].transform(max) - df['cycle']

# Databricks Cell 4: Log to MLflow
import mlflow
mlflow.sklearn.autolog()
with mlflow.start_run(run_name='plantmind-rul-v1'):
    from sklearn.ensemble import RandomForestRegressor
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(X_tr, y_tr)
    # mlflow auto-logs metrics, params, and model artifact
```

### [V1] [V2] polish pass
- Final chart styling: consistent dark theme, LTTS-appropriate colors
- Add loading spinners and status messages
- Mobile-friendly layout check

### Success checkpoint EOD Day 5
- Databricks CE account created, C-MAPSS loaded, preprocessing notebook runs ✓
- `recalibrate_weights(...)` → weights shift correctly, sum to 1 ✓
- Full demo runs start-to-finish without errors ✓

---

## DAY 6 — POLISH · FREEZE · PATENT BRIEF [ALL]

### Strategy
No new features. Harden everything. Prepare the patent brief.

### Actions
- **[S]** Freeze model artifacts: `rul_model.pkl`, `gotze_weights.json`, pre-computed diagnosis for demo engine
- **[A]** Add "pre-computed" label in UI for demo engine diagnosis — be honest, build trust
- **[V1]** Final RED→GREEN chart — ensure it's the most beautiful thing on screen
- **[V2]** Add "agent reasoning trace" panel — scrollable log of the 5 diagnosis steps
- **[ALL]** Run 3 full end-to-end demos. Find and fix any crash.
- **[S]** Write the 1-page patent brief (see template below)

### Patent brief template (1 page, hand to judges)
```
PLANTMIND — PROVISIONAL PATENT BRIEF

Title: Method for Energy-Aware, Counterfactual-Scored Industrial Asset
       Remediation Using Self-Recalibrating Multi-Objective Decision Scoring

Field: Industrial predictive/prescriptive maintenance; AI-driven ER&D

Problem addressed: Existing PdM tools predict failure but do not select
optimal corrective actions. Human decision-making is inconsistent and 
does not account for energy, cost, and confidence simultaneously.

Novel method:
  (a) Predict RUL from multivariate sensor telemetry
  (b) Trace root cause via causal asset-dependency graph traversal
  (c) Generate candidate corrective actions
  (d) Score each via: Σ(wₖ·Δkₖ(a))·conf ÷ cost, where Δkₖ is computed
      counterfactually through a surrogate degradation twin
  (e) Select via deterministic argmax
  (f) Recalibrate weights wₖ from realized post-action outcomes

Prior art gap: Prior art covers (a) alone or (a)+(b). No prior art covers
the counterfactual surrogate-scored energy-aware closed-loop decision method
as a unified system.

Inventors: [Team names]
Filing intent: Provisional application within 90 days
```

### Success checkpoint EOD Day 6
- 3 clean demo runs ✓
- Patent brief printed (1 page) ✓
- GitHub README complete ✓
- All team members can independently explain the RED→GREEN story ✓

---

## DAY 7 — REHEARSAL ONLY

### Schedule
- 09:00 — Full demo rehearsal, all 4 members present
- 09:30 — Solo rehearsal: each person explains their section out loud
- 10:00 — Trap-question drill: one person asks "the data is run-to-failure, how do you know the action works?" — answer it cold, every time
- 10:30 — Final freeze: no changes to code or deck
- Afternoon — Rest, travel, mental prep

### The 5 things every team member must be able to say without notes
1. "Prediction is commodity. The prize is the decision."
2. "The Twin imagines the timeline the data never recorded."
3. "The score is a formula: life × throughput × energy ÷ cost. Action 1 won with 0.82."
4. "This maps to LTTS's Lakshya-31: Plant Modernization, Industrial Automation, and Software Platforms in EI."
5. "We can file a provisional patent for this method within 90 days."

---

*7-Day Plan v1.0 · PlantMind · LTTS EI Hackathon 2026*
