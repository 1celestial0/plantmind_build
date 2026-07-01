"""Validate manifest/work-order contracts and the seeded hero manifest."""

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from src.contracts import (
    AssetSpec,
    DataSource,
    PhysicsModelConfig,
    PlantManifest,
    TagMapping,
    WorkOrder,
)


def _manifest_dict() -> dict:
    return {
        "plant_id": "PLANT-HERO-01",
        "asset_hierarchy": [
            {
                "asset_id": "PUMP-001",
                "asset_class": "pump",
                "description": "Hero centrifugal pump",
                "failure_mode": "gradual_wear",
            },
            {
                "asset_id": "COMP-001",
                "asset_class": "compressor",
            },
            {
                "asset_id": "MOTOR-001",
                "asset_class": "motor",
            },
        ],
        "data_sources": [
            {
                "name": "main_historian",
                "type": "historian",
                "uri": "opc.tcp://plantmind-demo/historian",
            }
        ],
        "tag_mapping": [
            {
                "raw_tag": "PMP001.VIB.RMS",
                "signal_type": "vibration_rms",
                "unit": "mm/s",
                "failure_mode": "gradual_wear",
            }
        ],
        "physics_model": [
            {"asset_class": "pump", "lambda_": 1.49e-6, "beta": 2.3, "life_ref": 420},
            {"asset_class": "compressor", "lambda_": 1.83e-5, "beta": 1.9, "life_ref": 400},
            {"asset_class": "motor", "lambda_": 5.98e-8, "beta": 2.8, "life_ref": 450},
        ],
        "iis_profile": "reliability_first",
        "triggers": {
            "health_threshold": 40,
            "rul_days_threshold": 14,
            "critical_severity": True,
        },
    }


def test_work_order_defaults_and_frozen():
    work_order = WorkOrder(
        work_order_id="WO-12345678",
        asset_id="PUMP-001",
        intervention="replace_seal",
        description="Replace seal during next available window.",
        created_at=datetime.now(timezone.utc),
        iis_score=0.91,
        approved_by="reliability.engineer",
        source_decision_ref="AUD-12345678",
    )

    assert work_order.status == "queued"

    with pytest.raises(ValidationError):
        work_order.status = "completed"


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("priority", "urgent"),
        ("status", "waiting"),
    ],
)
def test_work_order_rejects_invalid_literals(field_name: str, value: str):
    payload = {
        "work_order_id": "WO-12345678",
        "asset_id": "PUMP-001",
        "intervention": "replace_seal",
        "description": "Replace seal during next available window.",
        "created_at": datetime.now(timezone.utc),
        "approved_by": "reliability.engineer",
        "source_decision_ref": "AUD-12345678",
    }
    payload[field_name] = value

    with pytest.raises(ValidationError):
        WorkOrder(**payload)


def test_plant_manifest_nested_models():
    manifest = PlantManifest.model_validate(_manifest_dict())

    assert isinstance(manifest.asset_hierarchy[0], AssetSpec)
    assert isinstance(manifest.data_sources[0], DataSource)
    assert isinstance(manifest.tag_mapping[0], TagMapping)
    assert isinstance(manifest.physics_model[0], PhysicsModelConfig)
    assert manifest.asset_hierarchy[0].asset_id == "PUMP-001"


def test_physics_model_config_accepts_locked_pump_values():
    config = PhysicsModelConfig(
        asset_class="pump",
        lambda_=1.49e-6,
        beta=2.3,
        life_ref=420,
    )

    assert config.lambda_ == 1.49e-6
    assert config.beta == 2.3
    assert config.life_ref == 420


def test_hero_manifest_yaml_validates():
    hero_path = Path(__file__).resolve().parents[1] / "config" / "plants" / "hero.yaml"

    with hero_path.open("r", encoding="utf-8") as handle:
        manifest = PlantManifest.model_validate(yaml.safe_load(handle))

    hero_asset = next(asset for asset in manifest.asset_hierarchy if asset.asset_id == "PUMP-001")
    pump_physics = next(cfg for cfg in manifest.physics_model if cfg.asset_class == "pump")

    assert hero_asset.asset_class == "pump"
    assert manifest.iis_profile == "reliability_first"
    assert pump_physics.lambda_ == 1.49e-6
    assert pump_physics.beta == 2.3
    assert pump_physics.life_ref == 420


def test_iis_profile_validation():
    valid_profiles = [
        "reliability_first",
        "energy_optimization",
        "quality_driven",
        "sustainability_max",
    ]

    for profile in valid_profiles:
        manifest_data = deepcopy(_manifest_dict())
        manifest_data["iis_profile"] = profile
        assert PlantManifest.model_validate(manifest_data).iis_profile == profile

    invalid_manifest = deepcopy(_manifest_dict())
    invalid_manifest["iis_profile"] = "cost_first"

    with pytest.raises(ValidationError):
        PlantManifest.model_validate(invalid_manifest)
