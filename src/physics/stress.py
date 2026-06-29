"""Stress acceleration factors — LOCKED_STATE §6a.

S = AF_temp × AF_load
At reference (25 °C, rated load): S = 1.0
"""
from __future__ import annotations
import math

from .constants import (
    ACTIVATION_ENERGY_EV,
    BOLTZMANN_EV,
    LOAD_EXPONENT,
    T_REF_K,
)


def af_temperature(temp_celsius: float) -> float:
    """Arrhenius acceleration factor. Returns 1.0 at 25 °C."""
    t_op_k = temp_celsius + 273.15
    exponent = (ACTIVATION_ENERGY_EV / BOLTZMANN_EV) * (1.0 / T_REF_K - 1.0 / t_op_k)
    return math.exp(exponent)


def af_load(load_ratio: float) -> float:
    """Power-law acceleration factor. Returns 1.0 at load_ratio = 1.0 (rated load)."""
    if load_ratio <= 0:
        raise ValueError(f"load_ratio must be positive, got {load_ratio}")
    return load_ratio**LOAD_EXPONENT


def composite_stress(temp_celsius: float = 25.0, load_ratio: float = 1.0) -> float:
    """Composite stress S = AF_temp × AF_load."""
    return af_temperature(temp_celsius) * af_load(load_ratio)
