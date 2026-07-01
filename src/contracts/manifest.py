"""Plant Config Manifest schema for LOCKED_STATE §9 / DNA F-02 and F-10.

This Layer-0 manifest contract is portable LTTS IP. It defines the declarative
shape a future loader/composer will validate with `PlantManifest.model_validate`.
YAML parsing belongs outside this schema module.
"""

from typing import Literal

from pydantic import BaseModel, Field

AssetClass = Literal["pump", "compressor", "motor", "bearing", "valve"]
IISProfile = Literal[
    "reliability_first",
    "energy_optimization",
    "quality_driven",
    "sustainability_max",
]


class AssetSpec(BaseModel):
    """Declared asset in the plant hierarchy."""

    asset_id: str = Field(..., min_length=1)
    asset_class: AssetClass
    description: str | None = None
    failure_mode: str | None = None

    model_config = {"frozen": True}


class TagMapping(BaseModel):
    """Semantic map from raw plant tag to canonical signal meaning."""

    raw_tag: str = Field(..., min_length=1)
    signal_type: str = Field(..., min_length=1)
    unit: str = Field(..., min_length=1)
    failure_mode: str | None = None

    model_config = {"frozen": True}


class DataSource(BaseModel):
    """Declarative source descriptor for historian, file, or API inputs."""

    name: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1)
    uri: str | None = None
    path: str | None = None
    tag_mapping: list[TagMapping] = Field(default_factory=list)

    model_config = {"frozen": True}


class PhysicsModelConfig(BaseModel):
    """Per-asset-class Weibull parameters declared in the manifest."""

    asset_class: AssetClass
    lambda_: float = Field(
        ...,
        gt=0.0,
        description="LOCKED_STATE §6a λ value. Never replace with superseded naive example values.",
    )
    beta: float = Field(
        ...,
        gt=0.0,
        description="LOCKED_STATE §6a β value paired with the canonical λ calibration.",
    )
    life_ref: float = Field(..., gt=0.0, description="Reference life in cycles.")

    model_config = {"frozen": True}


class TriggerConfig(BaseModel):
    """Optional trigger overrides. RUL thresholds are always in days."""

    health_threshold: float = Field(default=40.0, ge=0.0, le=100.0)
    rul_days_threshold: float = Field(default=14.0, ge=0.0)
    critical_severity: bool = True

    model_config = {"frozen": True}


class PlantManifest(BaseModel):
    """Top-level plant manifest consumed by future config-driven composition."""

    plant_id: str = Field(..., min_length=1)
    asset_hierarchy: list[AssetSpec] = Field(..., min_length=1)
    data_sources: list[DataSource] = Field(default_factory=list)
    tag_mapping: list[TagMapping] = Field(default_factory=list)
    physics_model: list[PhysicsModelConfig] = Field(..., min_length=1)
    iis_profile: IISProfile = "reliability_first"
    triggers: TriggerConfig = Field(default_factory=TriggerConfig)

    model_config = {"frozen": True}
