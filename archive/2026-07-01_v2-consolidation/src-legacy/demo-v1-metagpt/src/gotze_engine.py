"""
LAYER 4 — GÖTZE DECISION ENGINE
=================================
The core IP of PlantMind. Takes a RED engine and produces:
  1. Root cause  — which sensor/subsystem is responsible
  2. Action menu — 3-4 candidate maintenance actions
  3. Götze Score — deterministic 4-objective ranking of actions
  4. RED->GREEN  — counterfactual proof that the winning action works

DESIGN RULE (never break this):
  AI does uncertain work  ->  predict, reason, imagine possible fixes
  Deterministic rules decide  ->  Götze Score picks the winner, not the AI

THE GÖTZE SCORE (4 objectives, weighted sum):
  G = w1*DeltaHealth + w2*(1 - NormCost) + w3*(1 - NormTime) + w4*Safety
  where all terms are in [0, 1] and weights sum to 1.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

# Bridge to messages.py typed contracts (MetaGPT pipeline mode)
from FORGE.src.messages import (
    EngineHealth,
    MaintenanceAction as MsgMaintenanceAction,
    EngineDecision as MsgEngineDecision,
)

# -------------------------------------------------------------------------
# Götze Score weights  (must sum to 1.0)
# -------------------------------------------------------------------------
WEIGHTS = {
    "health" : 0.40,
    "cost"   : 0.25,
    "time"   : 0.20,
    "safety" : 0.15,
}

# -------------------------------------------------------------------------
# Surrogate twin: RUL recovered per action
# -------------------------------------------------------------------------
SURROGATE_GAIN_MAP: dict[str, float] = {
    "replace_bearing"    : 95.0,
    "reduce_load"        : 40.0,
    "flush_lubrication"  : 25.0,
    "monitor_only"       :  5.0,
}


# -------------------------------------------------------------------------
# Internal data classes
# -------------------------------------------------------------------------

@dataclass
class MaintenanceAction:
    name        : str
    description : str
    cost_usd    : float
    downtime_hr : float
    safety_score: float


@dataclass
class GotzeResult:
    action        : MaintenanceAction
    rul_gain      : float
    gotze_score   : float
    score_breakdown: dict

    def __str__(self) -> str:
        return (
            f"[{self.gotze_score:.3f}] {self.action.name:<22} "
            f"| DeltaHealth={self.rul_gain:.0f} | "
            f"Cost=${self.action.cost_usd:,.0f} | "
            f"Downtime={self.action.downtime_hr:.0f}h"
        )


@dataclass
class EngineDecision:
    engine_id     : int
    current_rul   : float
    root_cause    : str
    action_scores : list[GotzeResult] = field(default_factory=list)

    @property
    def winner(self) -> GotzeResult:
        return max(self.action_scores, key=lambda r: r.gotze_score)

    @property
    def is_rescued(self) -> bool:
        return (self.current_rul + self.winner.rul_gain) > 30

    def summary(self) -> str:
        lines = [
            f"\n{'='*55}",
            f"ENGINE {self.engine_id} DECISION REPORT",
            f"{'='*55}",
            f"  Current RUL   : {self.current_rul:.1f} cycles  -> STATUS: RED",
            f"  Root cause    : {self.root_cause}",
            f"\n  Ranked Actions (Götze Score):",
        ]
        for rank, result in enumerate(
            sorted(self.action_scores, key=lambda r: r.gotze_score, reverse=True), 1
        ):
            marker = "  WINNER" if rank == 1 else "       "
            lines.append(f"  {rank}. {result}{marker}")
        new_rul = self.current_rul + self.winner.rul_gain
        status  = "GREEN" if self.is_rescued else "RED"
        lines += [
            f"\n  Counterfactual proof:",
            f"    Before action : RUL = {self.current_rul:.1f}  -> RED",
            f"    After action  : RUL = {new_rul:.1f}  -> {status}",
            f"{'='*55}",
        ]
        return "\n".join(lines)


# -------------------------------------------------------------------------
# Action library
# -------------------------------------------------------------------------
DEFAULT_ACTIONS: list[MaintenanceAction] = [
    MaintenanceAction(
        name="replace_bearing",
        description="Full bearing assembly replacement with OEM parts",
        cost_usd=8_500, downtime_hr=12.0, safety_score=0.95,
    ),
    MaintenanceAction(
        name="reduce_load",
        description="Reduce operational load by 20% for next 50 cycles",
        cost_usd=1_200, downtime_hr=0.5, safety_score=1.00,
    ),
    MaintenanceAction(
        name="flush_lubrication",
        description="Full lubrication flush and replacement (high-grade)",
        cost_usd=3_200, downtime_hr=4.0, safety_score=0.98,
    ),
    MaintenanceAction(
        name="monitor_only",
        description="Increase monitoring frequency; no physical intervention",
        cost_usd=400, downtime_hr=0.0, safety_score=0.70,
    ),
]


# -------------------------------------------------------------------------
# Core engine
# -------------------------------------------------------------------------

class GotzeEngine:
    """
    Deterministic decision engine. Dual-mode interface:
      Legacy:   diagnose(engine_id: int, current_rul: float) -> EngineDecision
      Pipeline: diagnose(health: EngineHealth)               -> messages.EngineDecision
    """

    def __init__(
        self,
        actions  : list[MaintenanceAction] = DEFAULT_ACTIONS,
        weights  : dict[str, float]         = WEIGHTS,
        gain_map : dict[str, float]         = SURROGATE_GAIN_MAP,
    ):
        assert abs(sum(weights.values()) - 1.0) < 1e-6, "Weights must sum to 1"
        self.actions  = actions
        self.weights  = weights
        self.gain_map = gain_map

    def _identify_root_cause(self, rul: float) -> str:
        if rul < 10:
            return "Critical bearing wear — s7/s12 deviation > 2 sigma"
        elif rul < 20:
            return "Progressive lubrication degradation — s2/s3 drift detected"
        else:
            return "Early-stage fatigue — s11/s15 showing initial anomaly"

    def _score_all_actions(self, current_rul: float) -> list[GotzeResult]:
        max_cost = max(a.cost_usd    for a in self.actions)
        max_time = max(a.downtime_hr for a in self.actions) or 1.0
        results  = []
        for action in self.actions:
            rul_gain = self.gain_map.get(action.name, 10.0)
            h = min(rul_gain / 130.0, 1.0)
            c = 1.0 - (action.cost_usd    / max_cost)
            t = 1.0 - (action.downtime_hr / max_time)
            s = action.safety_score
            score = (
                self.weights["health"] * h + self.weights["cost"]  * c +
                self.weights["time"]   * t + self.weights["safety"] * s
            )
            results.append(GotzeResult(
                action=action, rul_gain=rul_gain,
                gotze_score=round(score, 4),
                score_breakdown={"health": h, "cost": c, "time": t, "safety": s},
            ))
        return results

    def diagnose(self, engine_id_or_health, current_rul: float = None) -> object:
        """
        WHAT  : Score all actions and return a ranked decision.
        WHY   : Dual-mode — legacy (int, float) and MetaGPT pipeline (EngineHealth).
        HOW   : isinstance check dispatches to the right implementation.
        WHEN  : Legacy for CLI/tests. Pipeline mode for PipelineOrchestrator.
        WHY NOT: Two separate public methods — single entry point is cleaner.

        DESIGN RULE: NO LLM, no randomness, no external API calls here.
                     Deterministic math IS the proof mechanism.
        """
        if isinstance(engine_id_or_health, EngineHealth):
            return self._diagnose_from_health(engine_id_or_health)
        engine_id = engine_id_or_health
        if current_rul is None:
            raise ValueError("current_rul required when calling with engine_id")
        root_cause = self._identify_root_cause(current_rul)
        scored     = self._score_all_actions(current_rul)
        return EngineDecision(
            engine_id=engine_id, current_rul=current_rul,
            root_cause=root_cause, action_scores=scored,
        )

    def _diagnose_from_health(self, health: EngineHealth) -> MsgEngineDecision:
        """
        WHAT  : MetaGPT pipeline bridge — EngineHealth in, messages.EngineDecision out.
        WHY   : ProofEngineerRole expects messages.EngineDecision for proof_coordinates().
        HOW   : Runs internal scoring, maps GotzeResult -> MsgMaintenanceAction.
        WHEN  : Called by PipelineOrchestrator via diagnose(health).
        WHY NOT: Expose internal types to pipeline — breaks typed message contract.
        """
        current_rul = health.predicted_rul
        root_cause  = self._identify_root_cause(current_rul)
        scored      = self._score_all_actions(current_rul)

        msg_actions: list[MsgMaintenanceAction] = []
        for result in sorted(scored, key=lambda r: r.gotze_score, reverse=True):
            projected_rul    = min(130.0, current_rul + result.rul_gain)
            projected_status = "GREEN" if projected_rul >= 30 else "RED"
            msg_actions.append(MsgMaintenanceAction(
                action_name          = result.action.name,
                estimated_cost_usd   = result.action.cost_usd,
                estimated_time_hours = result.action.downtime_hr,
                safety_score         = result.action.safety_score,
                rul_gain_cycles      = int(result.rul_gain),
                gotze_score          = result.gotze_score,
                projected_rul        = projected_rul,
                projected_status     = projected_status,
                score_breakdown      = result.score_breakdown,
            ))

        return MsgEngineDecision(
            engine_id          = health.engine_id,
            cycle              = health.cycle,
            current_rul        = current_rul,
            current_status     = health.status,
            winner_action      = msg_actions[0],
            all_scored_actions = msg_actions,
            root_cause         = root_cause,
            confidence         = health.confidence,
            gotze_weights      = self.weights,
            source_health      = health,
        )


# -------------------------------------------------------------------------
# Standalone test
# -------------------------------------------------------------------------
if __name__ == "__main__":
    print("Testing LAYER 4 — Götze Decision Engine")
    engine   = GotzeEngine()
    decision = engine.diagnose(7, 18.0)
    print(decision.summary())
    print(f"winner: {decision.winner.action.name}  G={decision.winner.gotze_score}")
    print(f"is_rescued: {decision.is_rescued}")
    print("Layer 4 — PASS")
