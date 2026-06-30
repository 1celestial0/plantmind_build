"""
# ── FULL PIPELINE: PlantMind MetaGPT-Refined Orchestrator ──

WHAT  : The master orchestrator that chains all 5 roles in sequence:
        DataEngineerRole → MLEngineerRole → GotzeEngine(DecisionRole) → ProofEngineerRole
WHY   : MetaGPT's Environment pattern — one orchestrator routes messages between roles.
        No role knows about any other role directly. All communication is via typed messages.
HOW   : PipelineOrchestrator.run(engine_id) → EngineDecision + proof chart data.
WHEN  : Called by Streamlit app or CLI. One call per inference request.
WHY NOT: Direct role-to-role calls — creates tight coupling. Orchestrator pattern
         allows adding/removing roles without touching existing code.

MetaGPT reference: Environment routes Action outputs as Messages to subscribing Roles.
PlantMind adaptation: Synchronous pipeline (async upgrade post-hackathon).
"""

from __future__ import annotations
from pathlib import Path
from typing import Optional, Any

from FORGE.src.roles.data_engineer import DataEngineerRole
from FORGE.src.roles.ml_engineer import MLEngineerRole
from FORGE.src.roles.proof_engineer import ProofEngineerRole
from FORGE.src.gotze_engine import GotzeEngine
from FORGE.src.messages import SensorReading, EngineHealth, EngineDecision


class PipelineOrchestrator:
    """
    WHAT  : The single entry point for the entire PlantMind pipeline.
    WHY   : Hides all role complexity behind one clean interface for Streamlit.
    HOW   : Initializes all roles once, routes messages between them per request.
    WHEN  : Instantiate once at Streamlit app startup. Call run() per user request.
    WHY NOT: Re-initialize roles per request — model loading takes 30+ seconds.
    """

    def __init__(self, data_path: str = "data/CMaps/train_FD001.txt"):
        # ── Initialize all roles ──
        self.data_engineer = DataEngineerRole(data_path=data_path)
        self.ml_engineer = MLEngineerRole()
        self.decision_engine = GotzeEngine()
        self.proof_engineer = ProofEngineerRole()

        self._trained = False
        self._trace: list[str] = []   # Agent trace log for UI panel

    def train(self) -> dict[str, float]:
        """
        WHAT  : Train the ML model on the loaded dataset.
        WHY   : Must be called before run(). Separated so Streamlit can show progress.
        HOW   : DataEngineerRole loads data → MLEngineerRole.fit() trains model.
        WHEN  : Once at app startup. Can be re-run if data updates.
        WHY NOT: Train in __init__ — blocks app startup for 30+ seconds.
        """
        self._log("🔄 DataEngineerRole: Loading C-MAPSS FD001 dataset...")
        df = self.data_engineer.load_and_prepare()
        self._log(f"✅ DataEngineerRole: Loaded {len(df):,} rows, {df['engine_id'].nunique()} engines")

        self._log("🔄 MLEngineerRole: Training RandomForest (n_estimators=200, max_depth=15)...")
        metrics = self.ml_engineer.fit(df)
        self._log(f"✅ MLEngineerRole: RMSE={metrics['train_rmse']:.2f}, R²={metrics['train_r2']:.3f}")

        self._trained = True
        return metrics

    def run(self, engine_id: int) -> dict[str, Any]:
        """
        WHAT  : Full pipeline run for one engine: data → features → health → decision → proof.
        WHY   : Single entry point for Streamlit — returns everything the UI needs.
        HOW   : Chains all 4 roles. Each role's output is the next role's input.
        WHEN  : Called on user selection of engine_id in Streamlit sidebar.
        WHY NOT: Return raw objects — Streamlit needs serializable dicts for display.

        Returns dict with: decision, proof_chart_data, agent_trace, fleet_summary
        """
        if not self._trained:
            raise RuntimeError("Call train() before run()")

        self._trace = []   # Reset trace for this run

        # ── LAYER 1: Data ──
        self._log(f"🔄 DataEngineerRole: Fetching latest reading for engine {engine_id}...")
        reading: SensorReading = self.data_engineer.get_latest_reading(engine_id)
        history_df = self.data_engineer.get_engine_history(engine_id)
        self._log(f"✅ DataEngineerRole: Cycle={reading.cycle}, Raw RUL={reading.predicted_rul:.0f}")

        # ── LAYERS 2-3: Features + ML ──
        self._log("🔄 MLEngineerRole: Computing rolling features and predicting RUL...")
        health: EngineHealth = self.ml_engineer.predict(reading, history_df)
        self._log(
            f"✅ MLEngineerRole: Predicted RUL={health.predicted_rul:.1f} cycles → "
            f"Status={health.status} | Health={health.health_score:.2f}"
        )
        self._log(f"   Top sensors: {', '.join(health.top_contributing_sensors[:3])}")

        # ── LAYER 4: Decision ──
        self._log("🔄 GötzeEngine(DecisionRole): Scoring all maintenance actions...")
        decision: EngineDecision = self.decision_engine.diagnose(health)
        self._log(
            f"✅ GötzeEngine: Winner='{decision.winner_action.action_name}' "
            f"(G={decision.winner_action.gotze_score:.3f})"
        )
        for action in decision.all_scored_actions:
            self._log(
                f"   {action.action_name}: G={action.gotze_score:.3f} → "
                f"RUL {decision.current_rul:.0f}→{action.projected_rul:.0f} [{action.projected_status}]"
            )

        # ── LAYER 5: Proof ──
        self._log("🔄 ProofEngineerRole: Generating RED→GREEN counterfactual chart...")
        proof_data = self.proof_engineer.generate_proof_chart_data(decision)
        self.proof_engineer.log_decision(decision)
        self._log(
            f"✅ ProofEngineerRole: Chart ready. "
            f"Rescue: {decision.current_rul:.0f}→{decision.winner_action.projected_rul:.0f} cycles."
        )

        return {
            "decision": decision,
            "proof_chart_data": proof_data,
            "agent_trace": list(self._trace),
            "engine_id": engine_id,
            "current_status": decision.current_status,
        }

    def run_fleet(self) -> dict[str, Any]:
        """
        WHAT  : Run pipeline for ALL engines, return fleet summary.
        WHY   : LTTS clients manage fleets. Fleet view is the scalability story.
        HOW   : Calls run() for each engine, aggregates in ProofEngineerRole.
        WHEN  : Called for fleet dashboard tab in Streamlit.
        WHY NOT: Always show individual engine — fleet view closes −0.13 scalability gap.
        """
        self._log("🔄 Fleet mode: Running pipeline for all engines...")
        all_readings = self.data_engineer.get_all_readings()
        decisions = []

        for reading in all_readings:
            try:
                result = self.run(reading.engine_id)
                decisions.append(result["decision"])
            except Exception as e:
                self._log(f"⚠️ Engine {reading.engine_id} skipped: {e}")

        fleet_summary = self.proof_engineer.generate_fleet_summary(decisions)
        self._log(
            f"✅ Fleet complete: {fleet_summary['red_engines']} RED / "
            f"{fleet_summary['green_engines']} GREEN engines"
        )

        return {
            "fleet_summary": fleet_summary,
            "all_decisions": decisions,
            "agent_trace": list(self._trace),
        }

    def _log(self, message: str) -> None:
        """Append to agent trace log."""
        self._trace.append(message)
        # Also print for CLI/notebook debugging
        print(message)


# ── CLI entry point ──
if __name__ == "__main__":
    import sys

    engine_id = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    print(f"\n{'='*60}")
    print(f"PlantMind Pipeline — Engine {engine_id}")
    print(f"{'='*60}\n")

    orchestrator = PipelineOrchestrator()
    orchestrator.train()
    result = orchestrator.run(engine_id)

    print(f"\n{'='*60}")
    print("DECISION SUMMARY")
    print(f"{'='*60}")
    print(result["decision"].summary())
