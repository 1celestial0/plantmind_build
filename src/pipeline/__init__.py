"""Lane 1 pipeline exports."""

__all__ = [
    "run",
    "SensorReading",
    "PipelineResult",
    "load_manifest",
    "compose_runtime_plan",
    "RuntimePlan",
]


def __getattr__(name: str):
    if name == "run":
        from .orchestrator import run

        return run

    if name in {"SensorReading", "PipelineResult"}:
        from .schemas import PipelineResult, SensorReading

        return {"SensorReading": SensorReading, "PipelineResult": PipelineResult}[name]

    if name in {"load_manifest", "compose_runtime_plan", "RuntimePlan"}:
        from .composer import RuntimePlan, compose_runtime_plan
        from .manifest_loader import load_manifest

        return {
            "load_manifest": load_manifest,
            "compose_runtime_plan": compose_runtime_plan,
            "RuntimePlan": RuntimePlan,
        }[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
