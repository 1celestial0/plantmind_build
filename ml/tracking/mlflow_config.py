"""MLflow tracking configuration for PlantMind hackathon builds."""

from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_LOCAL_MLRUNS = _PROJECT_ROOT / "mlruns"
_EXPERIMENT_NAME = "plantmind-hackathon"


def get_tracking_uri() -> str:
    """Local file store for hackathon; swap for databricks URI in deploy."""
    _LOCAL_MLRUNS.mkdir(parents=True, exist_ok=True)
    return _LOCAL_MLRUNS.as_uri()


def get_experiment_name() -> str:
    return _EXPERIMENT_NAME


def configure_mlflow() -> None:
    """Call once at training job start."""
    import mlflow

    mlflow.set_tracking_uri(get_tracking_uri())
    mlflow.set_experiment(get_experiment_name())