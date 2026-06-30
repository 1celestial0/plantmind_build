# PlantMind — Databricks Setup, Runbook & Cheatsheet
### Community Edition · Project-Aligned · Safe-to-Demo

---

## WHY DATABRICKS IN THIS PROJECT

LTTS announced a formal partnership with Databricks in June 2026 for "industrial AI for asset-intensive Energy, Petrochemicals and Industrials clients." Showcasing PlantMind running on Databricks is not a requirement — it's a strategic signal to judges that this product belongs in the ecosystem LTTS is already selling.

**Usage strategy:**
- Build everything locally first (local = zero risk)
- Use Databricks Community Edition for steps 01–03 only (data + feature engineering + RUL model training)
- Log the model to MLflow (built into Databricks) — show this in the pitch as "production-ready model management"
- Never make the live demo depend on Databricks connectivity

---

## PART 1: ACCOUNT SETUP (30 minutes, Day 5)

### Step 1: Create Community Edition account
1. Go to [https://community.cloud.databricks.com/login.html](https://community.cloud.databricks.com/login.html)
2. Click "Sign up" → select "Community Edition" (free, no credit card)
3. Verify email → log in
4. You land on the Databricks workspace home

### Step 2: Create a cluster
1. Left sidebar → **Compute** → **Create Compute**
2. Configuration:
   - Cluster name: `plantmind-dev`
   - Cluster mode: **Single Node**
   - Databricks Runtime: **14.3 LTS (Scala 2.12, Spark 3.5.0)** — use LTS for stability
   - Node type: any (CE gives you one shared node)
3. Click **Create Compute**
4. Wait ~5 minutes for cluster to start (spinner turns green)

> **CE limitation:** Clusters auto-terminate after 120 minutes of inactivity. Always restart before your demo. Never rely on a CE cluster being live during a live demo — use local Python instead.

### Step 3: Upload C-MAPSS data to DBFS
1. Left sidebar → **Data** → **Add data** → **Upload files**
2. Upload: `train_FD001.txt`, `test_FD001.txt`, `RUL_FD001.txt`
3. Target path: `/FileStore/plantmind/cmapss/`
4. Confirm: **Data** → **DBFS** → browse to `/FileStore/plantmind/` → files should appear

### Step 4: Install libraries on cluster
1. Go to your cluster → **Libraries** tab → **Install New**
2. Source: PyPI → Package name: `scikit-learn` → Install
3. Repeat for: `scipy`, `matplotlib`, `pandas`
4. MLflow is pre-installed in all Databricks runtimes — no install needed

---

## PART 2: PROJECT NOTEBOOKS

Create these 3 notebooks in this order. Import them via **Workspace** → **Import** → paste the code.

### Notebook 1: `01_data_prep`
```python
# Cell 1: Load raw C-MAPSS data
cols = ['engine_id','cycle','op1','op2','op3'] + [f's{i}' for i in range(1,22)]
df = (spark.read
      .option("sep", " ")
      .option("inferSchema", True)
      .csv("/FileStore/plantmind/cmapss/train_FD001.txt")
      .toDF(*cols)
      .dropna(axis=1, how='all'))   # C-MAPSS has trailing empty columns

# Cell 2: Compute RUL label
from pyspark.sql import functions as F
max_cycles = df.groupby("engine_id").agg(F.max("cycle").alias("max_cycle"))
df = df.join(max_cycles, "engine_id").withColumn("RUL", F.col("max_cycle") - F.col("cycle"))

# Cell 3: Feature engineering — rolling windows
import pandas as pd
pandas_df = df.toPandas()

SENSOR_COLS = [f's{i}' for i in [2,3,4,7,8,9,11,12,13,14,15,17,20,21]]
WINDOW = 30

for col in SENSOR_COLS:
    pandas_df[f'{col}_mean'] = pandas_df.groupby('engine_id')[col].transform(
        lambda x: x.rolling(WINDOW, min_periods=1).mean())
    pandas_df[f'{col}_std'] = pandas_df.groupby('engine_id')[col].transform(
        lambda x: x.rolling(WINDOW, min_periods=1).std().fillna(0))

# Cell 4: Save as Delta table (Databricks best practice)
processed_spark = spark.createDataFrame(pandas_df)
processed_spark.write.format("delta").mode("overwrite").save("/delta/plantmind/features")
print(f"Saved {pandas_df.shape[0]} rows, {pandas_df.shape[1]} columns")
```

### Notebook 2: `02_rul_model_mlflow`
```python
# Cell 1: Load features
df = spark.read.format("delta").load("/delta/plantmind/features").toPandas()
feature_cols = [c for c in df.columns if '_mean' in c or '_std' in c]
X = df[feature_cols]
y = df['RUL'].clip(upper=130)  # cap at 130 — beyond 130 cycles the label is not informative

from sklearn.model_selection import train_test_split
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

# Cell 2: Train with MLflow auto-logging
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

mlflow.sklearn.autolog()

with mlflow.start_run(run_name="plantmind_rul_rf_v1") as run:
    rf = RandomForestRegressor(n_estimators=200, max_depth=15, n_jobs=-1, random_state=42)
    rf.fit(X_tr, y_tr)
    preds = rf.predict(X_te)
    rmse = np.sqrt(mean_squared_error(y_te, preds))
    mlflow.log_metric("rmse", rmse)
    mlflow.log_param("dataset", "C-MAPSS FD001")
    print(f"RMSE: {rmse:.2f} cycles")
    run_id = run.info.run_id

# Cell 3: Register model in MLflow Model Registry
model_uri = f"runs:/{run_id}/model"
mlflow.register_model(model_uri, "PlantMind-RUL-Model")
print(f"Model registered: {model_uri}")

# Cell 4: Download model artifact for local use
# (Run this locally, not in Databricks)
# mlflow.artifacts.download_artifacts(model_uri, dst_path="./models/")
```

### Notebook 3: `03_gotze_demo` (for demo screenshot only)
```python
# Cell 1: Show the Götze scoring in Databricks environment
import pandas as pd

scores = pd.DataFrame({
    'Action': ['Replace component', 'Reduce load 15%', 'Reroute workload', 'Monitor only'],
    'GötzeScore': [0.54, 0.89, 0.71, 0.12],
    'ΔLife': [35, 28, 18, 0],
    'ΔEnergy%': [0, 15, 8, 0],
    'Cost': [8.0, 2.0, 1.5, 0.1],
    'Winner': ['', '✓ WINNER', '', ''],
})
display(scores.sort_values('GötzeScore', ascending=False))

# Cell 2: Visualization (Databricks has built-in chart capability)
import matplotlib.pyplot as plt
import numpy as np

cycles = np.arange(35, 100)
health_base   = 100 * np.exp(-0.015 * (cycles - 35))
health_winner = 100 * np.exp(-0.015 * 0.60 * (cycles - 35))

plt.figure(figsize=(10, 5), facecolor='#1a1a2e')
ax = plt.gca(); ax.set_facecolor('#1a1a2e')
plt.plot(cycles, health_base,   color='#F0544A', linewidth=2.5, label='Do nothing')
plt.plot(cycles, health_winner, color='#35C97D', linewidth=2.5, label='Götze action')
plt.axhline(30, color='#EFA63C', linestyle='--', label='Failure threshold')
plt.xlabel('Cycles', color='white'); plt.ylabel('Asset Health', color='white')
plt.title('PlantMind: RED → GREEN', color='white', fontsize=14)
plt.legend(); plt.tight_layout()
display()  # Databricks display() shows the plot inline
```

---

## PART 3: RUNBOOK (Hackathon Day)

### Before you present (T−30 minutes)
```
□ Open community.cloud.databricks.com in browser
□ Start cluster plantmind-dev (takes 3–5 min to start)
□ Open Notebook 03_gotze_demo — run all cells — confirm no errors
□ Take a screenshot of the output (scores table + RED→GREEN chart)
□ Have screenshot ready to show if cluster dies during presentation
□ Open local Streamlit: streamlit run app.py — confirm it loads
□ Run end-to-end once locally — confirm no crashes
□ Close all unnecessary browser tabs — reduce distraction risk
```

### During demo
```
1. Start with Streamlit (local, zero risk) — show prediction + scoring
2. Switch to Databricks screenshot OR live if cluster is up
3. Point to MLflow run: "Model is tracked, versioned, ready for production deployment"
4. Never run a notebook cell during a live demo — pre-run, show outputs
```

### If Databricks fails
```
Fallback line: "Let me show you the local version — the Databricks deployment 
is the production target; this is the prototype."
→ Switch to Streamlit immediately
→ Never apologize more than once
→ The local demo is sufficient to win
```

---

## PART 4: CHEATSHEET

### Essential Databricks commands (copy-paste ready)

```python
# Read Delta table
df = spark.read.format("delta").load("/delta/plantmind/features")

# Show schema
df.printSchema()

# Count rows
print(df.count())

# Convert to pandas (safe for C-MAPSS — it's small)
pandas_df = df.toPandas()

# Write Delta table
df.write.format("delta").mode("overwrite").save("/path/to/table")

# Read CSV from DBFS
df = spark.read.csv("/FileStore/plantmind/cmapss/train_FD001.txt", sep=" ", inferSchema=True)

# MLflow: start run
import mlflow
with mlflow.start_run(run_name="my_run"):
    mlflow.log_metric("rmse", 18.4)
    mlflow.log_param("n_estimators", 200)

# MLflow: load registered model
model = mlflow.sklearn.load_model("models:/PlantMind-RUL-Model/1")

# Display a pandas dataframe nicely in notebook
display(pandas_df.head(20))

# Install a package in notebook
%pip install scikit-learn scipy

# Check Spark version
print(spark.version)

# DBFS file listing
dbutils.fs.ls("/FileStore/plantmind/")

# Download file from DBFS to driver
dbutils.fs.cp("/FileStore/plantmind/cmapss/train_FD001.txt", "file:/tmp/train_FD001.txt")
```

### Key paths
| What | DBFS path |
|---|---|
| Raw C-MAPSS files | `/FileStore/plantmind/cmapss/` |
| Delta features table | `/delta/plantmind/features` |
| MLflow model artifacts | Auto-managed by MLflow |
| Notebook workspace | `/Users/your@email.com/plantmind/` |

---

## PART 5: CURATED KNOWLEDGE BASES

These are the official Databricks docs pages you need to read — one page per topic, nothing else.

### KB-1: Community Edition limits
**URL:** [https://docs.databricks.com/en/getting-started/community-edition.html](https://docs.databricks.com/en/getting-started/community-edition.html)
**Key facts to know:**
- Single cluster per account
- Cluster auto-terminates after 2 hours idle
- No scheduled jobs in CE (use manual run)
- DBFS storage: 10GB limit
- No autoscaling
- Sufficient for C-MAPSS (small dataset) and demo

### KB-2: MLflow experiment tracking
**URL:** [https://docs.databricks.com/en/mlflow/tracking.html](https://docs.databricks.com/en/mlflow/tracking.html)
**What to learn:**
- `mlflow.start_run()` and `mlflow.log_metric()`
- `mlflow.sklearn.autolog()` — logs everything automatically
- How to view experiments: Experiments → your experiment name
- How to register a model: Experiments → run → Register Model

### KB-3: Delta Lake basics
**URL:** [https://docs.databricks.com/en/delta/index.html](https://docs.databricks.com/en/delta/index.html)
**What to learn (5-minute read):**
- `df.write.format("delta").save(path)` — write
- `spark.read.format("delta").load(path)` — read
- Delta tables are versioned (ACID) — mention this in pitch: "our features are versioned in Delta Lake"

### KB-4: Databricks File System (DBFS)
**URL:** [https://docs.databricks.com/en/dbfs/index.html](https://docs.databricks.com/en/dbfs/index.html)
**What to learn:**
- `/FileStore/` — where you upload files; accessible in notebooks as `/dbfs/FileStore/`
- `dbutils.fs.ls("/path")` — list files
- `dbutils.fs.cp(src, dst)` — copy files

### KB-5: Databricks notebooks
**URL:** [https://docs.databricks.com/en/notebooks/index.html](https://docs.databricks.com/en/notebooks/index.html)
**What to learn:**
- Cell types: `%python`, `%sql`, `%md` (markdown for documentation)
- `display(df)` — show dataframe with interactive chart builder
- Run cell: Shift+Enter
- Run all: Ctrl+Shift+Enter

### KB-6: sklearn + MLflow integration
**URL:** [https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html](https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html)
**Key patterns:**
```python
mlflow.sklearn.autolog()          # logs params, metrics, model automatically
mlflow.sklearn.log_model(model)   # manual log
mlflow.sklearn.load_model(uri)    # load from registry
```

---

## PART 6: WHAT TO SAY IN THE PITCH

> "We built PlantMind's data and model layer on Databricks — leveraging Delta Lake for versioned feature storage and MLflow for model tracking. This mirrors the production deployment pattern from the LTTS–Databricks industrial-AI partnership announced earlier this year. Our surrogate twin and Götze engine run locally with sub-second inference — exactly the edge-intelligence pattern that LTTS's EI Centers are building for."

This one paragraph uses: Databricks, Delta Lake, MLflow, the LTTS partnership, and the edge-intelligence theme from the Munich EI Center announcement — all accurate, all strategic.

---

*Databricks Guide v1.0 · PlantMind · LTTS EI Hackathon 2026*
