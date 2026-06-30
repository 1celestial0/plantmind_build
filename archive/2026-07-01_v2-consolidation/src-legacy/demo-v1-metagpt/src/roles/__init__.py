"""
# ── PlantMind Roles Package ──

WHAT  : Exports all MetaGPT Level 2 role classes for convenient import.
WHY   : Allows `from FORGE.src.roles import DataEngineerRole` anywhere
        without knowing which file each role lives in.
HOW   : Re-exports from individual role modules.
WHEN  : Imported by PipelineOrchestrator and tests.
WHY NOT: Import roles directly — leads to long import chains when adding new roles.
"""

from FORGE.src.roles.data_engineer import DataEngineerRole
from FORGE.src.roles.ml_engineer   import MLEngineerRole
from FORGE.src.roles.proof_engineer import ProofEngineerRole

__all__ = [
    "DataEngineerRole",
    "MLEngineerRole",
    "ProofEngineerRole",
]
