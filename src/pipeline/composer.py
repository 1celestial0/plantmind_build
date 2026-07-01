"""Runtime plan composer for manifest-driven PlantMind execution."""
from __future__ import annotations

from dataclasses import dataclass

from src.contracts import PhysicsModelConfig, PlantManifest, TagMapping, TriggerConfig


class RuntimeCompositionError(ValueError):
    """Base error for manifest runtime composition failures."""


class AssetNotFoundError(RuntimeCompositionError):
    """Raised when a requested asset is absent from the manifest."""


class PhysicsModelNotFoundError(RuntimeCompositionError):
    """Raised when the asset class has no physics config."""


_ASSET_TAG_PREFIXES: dict[str, tuple[str, ...]] = {
    "pump": ("PUMP", "PMP"),
    "compressor": ("COMPRESSOR", "COMP", "CMP"),
    "motor": ("MOTOR", "MTR"),
    "bearing": ("BEARING", "BRG"),
    "valve": ("VALVE", "VLV"),
}


@dataclass(frozen=True)
class RuntimePlan:
    plant_id: str
    asset_id: str
    asset_class: str
    description: str | None
    failure_mode: str | None
    canonical_signal_map: dict[str, str]
    physics_model: PhysicsModelConfig
    iis_profile: str
    triggers: TriggerConfig


def _tag_candidates(asset_id: str, asset_class: str) -> tuple[str, ...]:
    normalized = "".join(char for char in asset_id.upper() if char.isalnum())
    digits = "".join(char for char in asset_id if char.isdigit())
    prefixes = [normalized]

    if digits:
        for alias in _ASSET_TAG_PREFIXES.get(asset_class, (asset_class.upper(),)):
            prefixes.append(f"{alias}{digits}")

    return tuple(dict.fromkeys(prefixes))


def _collect_tag_mappings(manifest: PlantManifest) -> list[TagMapping]:
    seen: set[str] = set()
    mappings: list[TagMapping] = []

    for mapping in [*manifest.tag_mapping, *(m for ds in manifest.data_sources for m in ds.tag_mapping)]:
        if mapping.raw_tag in seen:
            continue
        seen.add(mapping.raw_tag)
        mappings.append(mapping)

    return mappings


def _tag_matches_asset(raw_tag: str, candidates: tuple[str, ...]) -> bool:
    upper_tag = raw_tag.upper()
    return any(upper_tag == candidate or upper_tag.startswith(f"{candidate}.") for candidate in candidates)


def compose_runtime_plan(manifest: PlantManifest, asset_id: str) -> RuntimePlan:
    """Compose an immutable runtime plan for one asset from a validated manifest."""

    asset = next((item for item in manifest.asset_hierarchy if item.asset_id == asset_id), None)
    if asset is None:
        raise AssetNotFoundError(
            f"Asset '{asset_id}' not found in manifest '{manifest.plant_id}'."
        )

    physics_model = next(
        (item for item in manifest.physics_model if item.asset_class == asset.asset_class),
        None,
    )
    if physics_model is None:
        raise PhysicsModelNotFoundError(
            f"Physics config for asset class '{asset.asset_class}' is missing in manifest "
            f"'{manifest.plant_id}'."
        )

    candidates = _tag_candidates(asset.asset_id, asset.asset_class)
    relevant_tags = [
        mapping
        for mapping in _collect_tag_mappings(manifest)
        if _tag_matches_asset(mapping.raw_tag, candidates)
    ]

    canonical_signal_map = {
        mapping.raw_tag: mapping.signal_type
        for mapping in relevant_tags
    }

    return RuntimePlan(
        plant_id=manifest.plant_id,
        asset_id=asset.asset_id,
        asset_class=asset.asset_class,
        description=asset.description,
        failure_mode=asset.failure_mode,
        canonical_signal_map=canonical_signal_map,
        physics_model=physics_model,
        iis_profile=manifest.iis_profile,
        triggers=manifest.triggers,
    )
