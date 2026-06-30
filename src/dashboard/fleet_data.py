"""Fleet configuration — 5 LTTS-managed plants with health snapshots."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class PlantInfo:
    plant_id: str
    name: str
    location: str
    sector: str
    fleet_health: int
    critical: int
    warning: int
    ok: int
    pending_decisions: int
    projected_savings: int
    scenario_key: str   # demo scenario to run when this plant is selected
    highlight_asset: str


FLEET: list[PlantInfo] = [
    PlantInfo(
        plant_id="jamnagar",
        name="Jamnagar Refinery",
        location="Gujarat, India",
        sector="Oil & Gas",
        fleet_health=69,
        critical=2,
        warning=7,
        ok=21,
        pending_decisions=2,
        projected_savings=450_000,
        scenario_key="A",
        highlight_asset="pump_07",
    ),
    PlantInfo(
        plant_id="mundra",
        name="Mundra Power Station",
        location="Gujarat, India",
        sector="Power Generation",
        fleet_health=83,
        critical=1,
        warning=4,
        ok=25,
        pending_decisions=1,
        projected_savings=180_000,
        scenario_key="B",
        highlight_asset="bearing_03",
    ),
    PlantInfo(
        plant_id="dahej",
        name="Dahej LNG Terminal",
        location="Gujarat, India",
        sector="LNG / Gas",
        fleet_health=48,
        critical=7,
        warning=12,
        ok=11,
        pending_decisions=7,
        projected_savings=1_620_000,
        scenario_key="C",
        highlight_asset="valve_11",
    ),
    PlantInfo(
        plant_id="pune_auto",
        name="Pune Auto Assembly",
        location="Maharashtra, India",
        sector="Manufacturing",
        fleet_health=92,
        critical=0,
        warning=3,
        ok=27,
        pending_decisions=0,
        projected_savings=60_000,
        scenario_key="D",
        highlight_asset="motor_02",
    ),
    PlantInfo(
        plant_id="vizag_steel",
        name="Vizag Steel Plant",
        location="Andhra Pradesh, India",
        sector="Steel & Mining",
        fleet_health=61,
        critical=4,
        warning=9,
        ok=17,
        pending_decisions=4,
        projected_savings=860_000,
        scenario_key="E",
        highlight_asset="comp_04",
    ),
]

FLEET_BY_ID: dict[str, PlantInfo] = {p.plant_id: p for p in FLEET}

SECTOR_COLORS: dict[str, str] = {
    "Oil & Gas":        "#FF6B35",
    "Power Generation": "#4C78A8",
    "LNG / Gas":        "#00CC88",
    "Manufacturing":    "#9B59B6",
    "Steel & Mining":   "#E67E22",
}
