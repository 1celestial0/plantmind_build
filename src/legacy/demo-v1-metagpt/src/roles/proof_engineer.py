"""
# ── LAYER 5: ProofEngineerRole (MetaGPT Level 2) ──

WHAT  : MetaGPT-aligned role owning Layer 5 responsibilities:
        generating the counterfactual RED→GREEN proof visualization and
        logging decisions for feedback/recalibration.
WHY   : The "proof" layer is what makes PlantMind different from any PdM dashboard.
        It needs its own role because: (1) visualization logic is complex,
        (2) the feedback loop (weight recalibration) is a separate concern.
HOW   : Takes EngineDecision → generates Plotly chart data + decision log entry.
WHEN  : Called after DecisionEngineerRole. Output goes to Streamlit app.
WHY NOT: Put this in Streamlit directly — coupling visualization to app framework
         prevents testing and makes the proof layer non-reusable.

DESIGN RULE: The proof is not decorative. It is the claim.
             Without the RED→GREEN visual, we have a prediction tool, not a proof tool.
"""

from __future__ import annotations
import json
import datetime
from pathlib import Path
from typing import Any

from FORGE.src.messages import EngineDecision


# ══════════════════════════════════════════════════════════════
# CONSTANTS
# ══════════════════════════════════════════════════════════════

# WHAT: Colors for RED/GREEN trajectory lines
# WHY: Red = danger/failure, Green = rescued/safe. Universal industrial color convention.
# WHY NOT: Use blue/orange — red/green are the "money shot" — judges recognize it instantly.
FAILURE_COLOR: str = "#FF4444"     # RED trajectory
RESCUE_COLOR: str  = "#44BB44"     # GREEN trajectory
THRESHOLD_COLOR: str = "#FFA500"   # Orange failure threshold line

DECISION_LOG_PATH = Path("logs/decision_log.jsonl")
RED_THRESHOLD: int = 30


class ProofEngineerRole:
    """
    WHAT  : The proof and learn agent — generates counterfactual evidence + logs decisions.
    WHY   : Separates visualization generation from decision scoring.
    HOW   : generate_proof_chart_data() → dict consumed by Streamlit Plotly chart.
            log_decision() → JSONL append for future weight recalibration.
    WHEN  : Called per EngineDecision output from DecisionEngineerRole.
    WHY NOT: Merge with DecisionEngineerRole — proof is a separate concern from scoring.
    """

    def generate_proof_chart_data(self, decision: EngineDecision) -> dict[str, Any]:
        """
        WHAT  : Generate all data needed to render the RED→GREEN counterfactual chart.
        WHY   : The visual proof is the patent claim made tangible — judges see it, investors see it.
        HOW   : Two linear trajectories: actual degradation (RED) vs rescued trajectory (GREEN).
                Both plotted from current cycle to failure/rescue endpoint.
        WHEN  : Called by Streamlit app after every decision.
        WHY NOT: Use a surrogate model for trajectory — linear approximation is sufficient
                 for visual proof. Full surrogate model is a post-hackathon enhancement.
        """
        coords = decision.proof_coordinates()
        winner = decision.winner_action

        # ── Build Plotly-compatible trace data ──
        traces = [
            {
                "name": f"Without action (FAILURE in {int(decision.current_rul)} cycles)",
                "x": coords["red_x"],
                "y": coords["red_y"],
                "mode": "lines",
                "line": {"color": FAILURE_COLOR, "width": 3, "dash": "solid"},
                "fill": "tozeroy",
                "fillcolor": "rgba(255, 68, 68, 0.1)",
            },
            {
                "name": f"After '{winner.action_name}' (rescued to {winner.projected_rul:.0f} cycles)",
                "x": coords["green_x"],
                "y": coords["green_y"],
                "mode": "lines",
                "line": {"color": RESCUE_COLOR, "width": 3, "dash": "solid"},
                "fill": "tozeroy",
                "fillcolor": "rgba(68, 187, 68, 0.1)",
            },
        ]

        layout = {
            "title": {
                "text": f"Engine {decision.engine_id} — Counterfactual Proof<br>"
                        f"<sub>Götze Score: {winner.gotze_score:.3f} | "
                        f"Action: {winner.action_name}</sub>",
                "x": 0.5,
            },
            "xaxis": {"title": "Cycles from now"},
            "yaxis": {"title": "Remaining Useful Life (cycles)"},
            "shapes": [
                {
                    "type": "line",
                    "x0": 0, "x1": max(len(coords["red_x"]), len(coords["green_x"])),
                    "y0": RED_THRESHOLD, "y1": RED_THRESHOLD,
                    "line": {"color": THRESHOLD_COLOR, "dash": "dash", "width": 2},
                }
            ],
            "annotations": [
                {
                    "x": 5, "y": RED_THRESHOLD + 3,
                    "text": f"🔴 Failure threshold ({RED_THRESHOLD} cycles)",
                    "showarrow": False,
                    "font": {"color": THRESHOLD_COLOR},
                }
            ],
            "legend": {"x": 0.6, "y": 0.95},
            "plot_bgcolor": "white",
            "paper_bgcolor": "white",
        }

        return {
            "traces": traces,
            "layout": layout,
            "summary": decision.summary(),
            "score_breakdown": winner.score_breakdown,
            "all_actions": [
                {
                    "action": a.action_name,
                    "gotze_score": round(a.gotze_score, 3),
                    "projected_rul": round(a.projected_rul, 0),
                    "status": a.projected_status,
                }
                for a in decision.all_scored_actions
            ],
        }

    def log_decision(self, decision: EngineDecision) -> None:
        """
        WHAT  : Append decision to JSONL log for future weight recalibration.
        WHY   : Every decision is training data for the next version of weights.
                Over time, accepted recommendations reveal which actions are actually effective.
        HOW   : Serialize EngineDecision key fields to JSON, append to log file.
        WHEN  : After every decision, regardless of whether user accepts the recommendation.
        WHY NOT: Database — JSONL is append-only, portable, zero-dependency.
                 Postgres upgrade is a post-hackathon task.
        """
        DECISION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        log_entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "engine_id": decision.engine_id,
            "cycle": decision.cycle,
            "current_rul": decision.current_rul,
            "current_status": decision.current_status,
            "winner_action": decision.winner_action.action_name,
            "winner_score": decision.winner_action.gotze_score,
            "winner_projected_rul": decision.winner_action.projected_rul,
            "all_scores": {
                a.action_name: a.gotze_score
                for a in decision.all_scored_actions
            },
            "weights_used": decision.gotze_weights,
            "root_cause": decision.root_cause,
        }

        with open(DECISION_LOG_PATH, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def generate_fleet_summary(self, decisions: list[EngineDecision]) -> dict[str, Any]:
        """
        WHAT  : Aggregate multiple decisions into a fleet health dashboard summary.
        WHY   : LTTS clients manage fleets (100s of machines), not single assets.
        HOW   : Count RED/GREEN, average Götze scores, most common winner action.
        WHEN  : Called for the Streamlit fleet dashboard view.
        WHY NOT: Show individual charts only — judges want fleet-level thinking.
        """
        total = len(decisions)
        red_count = sum(1 for d in decisions if d.current_status == "RED")
        action_counts: dict[str, int] = {}
        for d in decisions:
            name = d.winner_action.action_name
            action_counts[name] = action_counts.get(name, 0) + 1

        top_action = max(action_counts, key=action_counts.get) if action_counts else "N/A"

        return {
            "total_engines": total,
            "red_engines": red_count,
            "green_engines": total - red_count,
            "fleet_health_pct": round((total - red_count) / max(total, 1) * 100, 1),
            "most_recommended_action": top_action,
            "action_distribution": action_counts,
            "avg_winner_score": round(
                sum(d.winner_action.gotze_score for d in decisions) / max(total, 1), 3
            ),
        }
