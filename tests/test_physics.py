"""Lane 2 physics engine — unit tests.

Covers: health_at, compute_rul, stress factors, compute_health (public API),
boundary conditions, and contract shape.
"""
from __future__ import annotations

import math

import numpy as np
import pytest

from src.contracts.physics import PhysicsModelOutput
from src.physics.constants import (
    ASSET_PARAMS,
    ASSET_TYPES,
    CYCLES_PER_DAY,
    H_FAILURE_THRESHOLD,
)
from src.physics.model import compute_health
from src.physics.stress import af_load, af_temperature, composite_stress
from src.physics.weibull import WeibullRUL, compute_rul, health_at


# ─── stress ───────────────────────────────────────────────────────────────────

def test_af_temperature_at_reference():
    assert math.isclose(af_temperature(25.0), 1.0, rel_tol=1e-6)


def test_af_temperature_hot_increases():
    assert af_temperature(60.0) > 1.0


def test_af_temperature_cold_decreases():
    assert af_temperature(10.0) < 1.0


def test_af_load_at_rated():
    assert math.isclose(af_load(1.0), 1.0, rel_tol=1e-9)


def test_af_load_overload_increases():
    assert af_load(1.2) > 1.0


def test_af_load_underload_decreases():
    assert af_load(0.8) < 1.0


def test_af_load_invalid():
    with pytest.raises(ValueError):
        af_load(0.0)


def test_composite_stress_reference():
    assert math.isclose(composite_stress(25.0, 1.0), 1.0, rel_tol=1e-6)


# ─── health_at ────────────────────────────────────────────────────────────────

def test_health_at_cycle_zero_is_100():
    lam, beta = ASSET_PARAMS["pump"]["lambda_"], ASSET_PARAMS["pump"]["beta"]
    assert math.isclose(health_at(0.0, lam, beta), 100.0, rel_tol=1e-6)


def test_health_decreases_over_time():
    lam, beta = ASSET_PARAMS["pump"]["lambda_"], ASSET_PARAMS["pump"]["beta"]
    h1 = health_at(100.0, lam, beta)
    h2 = health_at(300.0, lam, beta)
    assert h1 > h2


def test_health_clamped_at_zero():
    h = health_at(1e9, 1e-3, 2.0)
    assert h == 0.0


@pytest.mark.parametrize("asset_type", ASSET_TYPES)
def test_health_reaches_threshold_near_life_ref(asset_type: str):
    """H at life_ref should be close to H_FAILURE_THRESHOLD (within ±5)."""
    p = ASSET_PARAMS[asset_type]
    h = health_at(p["life_ref"], p["lambda_"], p["beta"])
    assert abs(h - H_FAILURE_THRESHOLD) < 5.0, (
        f"{asset_type}: H({p['life_ref']})={h:.2f}, expected ~{H_FAILURE_THRESHOLD}"
    )


# ─── compute_rul ──────────────────────────────────────────────────────────────

def test_rul_returns_weibull_rul():
    p = ASSET_PARAMS["motor"]
    result = compute_rul(0.0, p["lambda_"], p["beta"])
    assert isinstance(result, WeibullRUL)


def test_rul_at_cycle_zero_is_positive():
    p = ASSET_PARAMS["pump"]
    r = compute_rul(0.0, p["lambda_"], p["beta"])
    assert r.rul_days > 0


def test_rul_decreases_with_cycle():
    p = ASSET_PARAMS["bearing"]
    r1 = compute_rul(50.0, p["lambda_"], p["beta"])
    r2 = compute_rul(200.0, p["lambda_"], p["beta"])
    assert r1.rul_days > r2.rul_days


def test_rul_ci_ordered():
    p = ASSET_PARAMS["compressor"]
    r = compute_rul(200.0, p["lambda_"], p["beta"])
    assert r.ci_low_days <= r.rul_days <= r.ci_high_days


def test_rul_zero_after_failure():
    p = ASSET_PARAMS["valve"]
    r = compute_rul(10_000.0, p["lambda_"], p["beta"])
    assert r.rul_days == 0.0


def test_rul_in_days_unit():
    """RUL_days = RUL_cycles / CYCLES_PER_DAY — sanity check magnitude."""
    p = ASSET_PARAMS["pump"]
    r = compute_rul(0.0, p["lambda_"], p["beta"])
    expected_approx = p["life_ref"] / CYCLES_PER_DAY
    assert abs(r.rul_days - expected_approx) / expected_approx < 0.20


# ─── compute_health (public API) ──────────────────────────────────────────────

def test_compute_health_returns_contract():
    out = compute_health("pump", cycle=100.0)
    assert isinstance(out, PhysicsModelOutput)


def test_compute_health_health_in_range():
    out = compute_health("motor", cycle=200.0)
    assert 0.0 <= out.health_index <= 100.0


def test_compute_health_ci_ordered():
    out = compute_health("bearing", cycle=150.0)
    ci_low, ci_high = out.confidence_interval
    assert ci_low <= out.rul_estimate <= ci_high


def test_compute_health_explanation_nonempty():
    out = compute_health("valve", cycle=50.0)
    assert len(out.physics_explanation) > 20


def test_compute_health_unknown_asset_raises():
    with pytest.raises(KeyError):
        compute_health("turbine", cycle=100.0)


@pytest.mark.parametrize("asset_type", ASSET_TYPES)
def test_compute_health_all_asset_types(asset_type: str):
    out = compute_health(asset_type, cycle=100.0)
    assert out.health_index > 0
