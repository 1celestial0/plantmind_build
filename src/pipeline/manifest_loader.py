"""Manifest loader for config-driven PlantMind runtime composition."""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from src.contracts import PlantManifest


class ManifestLoaderError(ValueError):
    """Base error for manifest loading failures."""


class ManifestFileNotFoundError(FileNotFoundError, ManifestLoaderError):
    """Raised when a manifest path does not exist."""


class ManifestEmptyError(ManifestLoaderError):
    """Raised when a manifest file is empty."""


class ManifestYAMLError(ManifestLoaderError):
    """Raised when YAML parsing fails."""


class ManifestSchemaError(ManifestLoaderError):
    """Raised when manifest data fails schema validation."""


def load_manifest(path: str | Path) -> PlantManifest:
    """Load and validate a plant manifest from YAML."""

    manifest_path = Path(path)

    if not manifest_path.is_file():
        raise ManifestFileNotFoundError(f"Manifest file not found: {manifest_path}")

    try:
        payload = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ManifestYAMLError(f"Invalid YAML in manifest '{manifest_path}': {exc}") from exc

    if payload is None:
        raise ManifestEmptyError(f"Manifest file is empty: {manifest_path}")

    try:
        return PlantManifest.model_validate(payload)
    except ValidationError as exc:
        raise ManifestSchemaError(
            f"Manifest schema validation failed for '{manifest_path}': {exc}"
        ) from exc
