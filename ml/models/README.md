# ml/models — trained artifact home

Store serialized models here. Link MLflow run IDs in audit records (`model_used` field).

## Layout

```
ml/models/
├── weibull/          # per-asset-class λ/β calibrations
├── anomaly/          # DataSentinel sklearn models
└── rul/              # optional RF bridge from v1
```

## MLflow

Config: `ml/tracking/mlflow_config.py`

```powershell
cd PlantMind_live
py -3 -c "from ml.tracking.mlflow_config import get_tracking_uri; print(get_tracking_uri())"
```

Hackathon: local `./mlruns` URI. Production: Databricks MLflow registry.

## Audit linkage

When logging a decision, set `AuditRecord.model_used` to `mlflow:<run_id>` or file path under this folder.