"""
FORGE — END-TO-END DEMO RUNNER
================================
One command to see the entire PlantMind pipeline work:

    python run_demo.py

No downloads. No config. No database. Just run it.

WHAT THIS SCRIPT DOES (mirrors the 5-layer blueprint):
  Layer 1 → Generate synthetic C-MAPSS data  (or load real if file exists)
  Layer 2 → Engineer 28 rolling features per engine
  Layer 3 → Train Random Forest, predict RUL, flag RED engines
  Layer 4 → Run Götze Engine on each RED engine
  Layer 5 → Print RED→GREEN proof + counterfactual result

LEARNING PATH (run this first, then study each src/ file):
  See REVERSE_ENGINEER.md for the guided breakdown.
"""

import sys
import time
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# Import pipeline layers
# ─────────────────────────────────────────────────────────────────────────────
from src.ingestion   import generate_synthetic_cmapss, load_cmapss, describe_dataset
from src.features    import engineer_features, get_latest_snapshot, get_feature_cols
from src.model       import RULPredictor
from src.gotze_engine import GotzeEngine


def run_demo(n_engines: int = 40, verbose: bool = True) -> dict:
    """
    Execute the full pipeline and return a results dict.

    Args:
        n_engines : Number of synthetic engines to simulate
        verbose   : Print progress + results to console

    Returns:
        {
          "model_metrics": {"mae": float, "r2": float},
          "red_engines":   [{"engine_id": int, "rul": float, "rescued": bool}],
          "decisions":     [EngineDecision, ...]
        }
    """
    t0 = time.time()

    def log(msg: str) -> None:
        if verbose:
            print(msg)

    # ── LAYER 1: DATA ────────────────────────────────────────────────────────
    log("\n" + "─" * 60)
    log("LAYER 1 — DATA INGESTION")
    log("─" * 60)

    real_data = Path("data/train_FD001.txt")
    if real_data.exists():
        log(f"  Loading real C-MAPSS data from {real_data} ...")
        df_raw = load_cmapss(real_data)
    else:
        log(f"  Generating {n_engines} synthetic engines (no download needed) ...")
        df_raw = generate_synthetic_cmapss(n_engines=n_engines, seed=42)

    describe_dataset(df_raw)

    # ── LAYER 2: FEATURES ────────────────────────────────────────────────────
    log("\n" + "─" * 60)
    log("LAYER 2 — FEATURE ENGINEERING")
    log("─" * 60)
    log("  Computing 30-cycle rolling statistics per degrading sensor ...")

    df_feat = engineer_features(df_raw)
    feat_cols = get_feature_cols()
    log(f"  → {len(feat_cols)} features created")

    # ── LAYER 3: RUL MODEL ───────────────────────────────────────────────────
    log("\n" + "─" * 60)
    log("LAYER 3 — RUL PREDICTION MODEL")
    log("─" * 60)
    log("  Training Random Forest regressor ...")

    predictor = RULPredictor()
    metrics   = predictor.train(df_feat)

    log(f"  MAE = {metrics['mae']} cycles  |  R² = {metrics['r2']}")
    log(f"  Top feature: {predictor.top_features(1)[0][0]}")

    # Predict RUL for all engines' latest cycle
    engine_ids    = df_feat["engine_id"].unique()
    rul_by_engine = {}

    for eid in engine_ids:
        snapshot       = get_latest_snapshot(df_feat, eid)
        feat_vals      = snapshot[feat_cols].values
        rul_pred       = predictor.predict_rul(feat_vals)
        rul_by_engine[eid] = rul_pred

    red_engines = [
        (eid, rul)
        for eid, rul in rul_by_engine.items()
        if predictor.health_status(rul) == "RED"
    ]

    log(f"\n  Health summary:")
    log(f"    Total engines : {len(engine_ids)}")
    log(f"    RED  🔴       : {len(red_engines)}")
    log(f"    GREEN ✅      : {len(engine_ids) - len(red_engines)}")

    # ── LAYER 4: GÖTZE ENGINE ────────────────────────────────────────────────
    log("\n" + "─" * 60)
    log("LAYER 4 — GÖTZE DECISION ENGINE")
    log("─" * 60)

    gotze  = GotzeEngine()
    decisions = []

    for eid, rul in sorted(red_engines, key=lambda x: x[1])[:5]:  # top 5 worst
        decision = gotze.diagnose(engine_id=eid, current_rul=rul)
        decisions.append(decision)
        log(decision.summary())

    # ── LAYER 5: SUMMARY ─────────────────────────────────────────────────────
    log("\n" + "═" * 60)
    log("LAYER 5 — PROOF SUMMARY")
    log("═" * 60)

    rescued = [d for d in decisions if d.is_rescued]
    log(f"  RED engines processed : {len(decisions)}")
    log(f"  Successfully rescued  : {len(rescued)} / {len(decisions)}")

    for d in decisions:
        status = "✅ GREEN" if d.is_rescued else "⚠️  Still RED"
        new_rul = d.current_rul + d.winner.rul_gain
        log(
            f"  Engine {d.engine_id:>3}  "
            f"RUL {d.current_rul:>5.1f} → {new_rul:>5.1f}  "
            f"({d.winner.action.name:<20})  {status}"
        )

    elapsed = time.time() - t0
    log(f"\n  Total runtime: {elapsed:.2f}s")
    log("═" * 60)
    log("\n✅  FORGE pipeline — COMPLETE\n")

    return {
        "model_metrics": metrics,
        "red_engines"  : [{"engine_id": eid, "rul": rul} for eid, rul in red_engines],
        "decisions"    : decisions,
    }


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="FORGE — PlantMind Demo Runner")
    parser.add_argument("--engines", type=int, default=40,
                        help="Number of synthetic engines (default: 40)")
    parser.add_argument("--quiet",   action="store_true",
                        help="Suppress verbose output")
    args = parser.parse_args()

    print("\n" + "═" * 60)
    print("  FORGE — PlantMind Götze Decision Engine")
    print("  Full pipeline: Data → Features → RUL → Decision → Proof")
    print("═" * 60)

    results = run_demo(n_engines=args.engines, verbose=not args.quiet)

    print("\nNext steps:")
    print("  → Open src/ingestion.py and read the REVERSE ENGINEER comments")
    print("  → See REVERSE_ENGINEER.md for the full learning path")
    print("  → Run each layer standalone: python -m src.ingestion")
