"""Manifest loader + runtime composer tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from src.contracts import PlantManifest
from src.pipeline import RuntimePlan, compose_runtime_plan, load_manifest
from src.pipeline.composer import AssetNotFoundError, PhysicsModelNotFoundError
from src.pipeline.manifest_loader import ManifestSchemaError


ROOT = Path(__file__).resolve().parents[1]
HERO_MANIFEST = ROOT / "config" / "plants" / "hero.yaml"


def test_load_manifest_validates_hero_yaml():
    manifest = load_manifest(HERO_MANIFEST)

    assert isinstance(manifest, PlantManifest)
    assert manifest.plant_id == "PLANT-HERO-01"


def test_compose_runtime_plan_for_hero_pump():
    manifest = load_manifest(HERO_MANIFEST)

    plan = compose_runtime_plan(manifest, "PUMP-001")

    assert isinstance(plan, RuntimePlan)
    assert plan.plant_id == "PLANT-HERO-01"
    assert plan.asset_id == "PUMP-001"
    assert plan.asset_class == "pump"
    assert plan.description == "Hero centrifugal pump"
    assert plan.failure_mode == "gradual_wear"
    assert plan.physics_model.lambda_ == 1.49e-6
    assert plan.physics_model.beta == 2.3
    assert plan.physics_model.life_ref == 420
    assert plan.iis_profile == "reliability_first"
    assert plan.triggers.health_threshold == 40
    assert plan.triggers.rul_days_threshold == 14
    assert plan.canonical_signal_map["PMP001.VIB.RMS"] == "vibration_rms"


def test_compose_runtime_plan_missing_asset_error_is_clear():
    manifest = load_manifest(HERO_MANIFEST)

    with pytest.raises(AssetNotFoundError, match="Asset 'PUMP-404' not found"):
        compose_runtime_plan(manifest, "PUMP-404")


def test_compose_runtime_plan_missing_physics_error_is_clear():
    manifest = load_manifest(HERO_MANIFEST)
    trimmed_manifest = manifest.model_copy(
        update={
            "physics_model": [
                model for model in manifest.physics_model if model.asset_class != "pump"
            ]
        }
    )

    with pytest.raises(
        PhysicsModelNotFoundError,
        match="Physics config for asset class 'pump' is missing",
    ):
        compose_runtime_plan(trimmed_manifest, "PUMP-001")


def test_load_manifest_rejects_invalid_schema(tmp_path: Path):
    manifest_path = tmp_path / "invalid-manifest.yaml"
    manifest_path.write_text("plant_id: PLANT-HERO-01\nasset_hierarchy: []\nphysics_model: []\n", encoding="utf-8")

    with pytest.raises(ManifestSchemaError, match="Manifest schema validation failed"):
        load_manifest(manifest_path)
