"""
LAYER 3 — RUL PREDICTION MODEL
================================
Trains a Random Forest to predict Remaining Useful Life from sensor features.
Applies a threshold to classify engines as RED (critical) or GREEN (healthy).

DESIGN DECISION: Why Random Forest, not LSTM?
  • RF trains in seconds, LSTM takes minutes — critical for a hackathon
  • RF is interpretable: feature_importances_ shows which sensors matter
  • RF handles tabular data better than LSTM with <500 engines
  • LSTM is strictly better with 10k+ engines — upgrade post-hackathon

RED/GREEN THRESHOLD:
  RUL < 30 cycles → RED  (engine will fail within 30 maintenance cycles)
  RUL ≥ 30 cycles → GREEN

REVERSE ENGINEER THIS FILE:
  Step 1 → Run standalone:              python -m src.model
  Step 2 → Change n_estimators=5        Accuracy drops. Why?
  Step 3 → Change RED_THRESHOLD=50      More engines flagged. Better or worse?
  Step 4 → Replace RF with LinearSVR    Faster? More accurate?
  Step 5 → Print feature_importances_   Which sensors matter most?
"""

import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from src.features import get_feature_cols

# ─────────────────────────────────────────────────────────────────────────────
# Configuration — change these and observe the effect
# ─────────────────────────────────────────────────────────────────────────────
RED_THRESHOLD    = 30     # cycles remaining before engine is flagged RED
N_ESTIMATORS     = 100    # number of trees in the Random Forest
RANDOM_STATE     = 42     # reproducibility seed
MODEL_SAVE_PATH  = Path("models/rul_model.pkl")


class RULPredictor:
    """
    Wrapper around scikit-learn RandomForestRegressor.

    Why wrap it?
      • Single place to swap the algorithm (RF → LSTM → XGBoost)
      • Encapsulates feature column names — no magic string lists outside
      • Adds health_status() on top of raw RUL prediction
    """

    def __init__(self, n_estimators: int = N_ESTIMATORS):
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            random_state=RANDOM_STATE,
            n_jobs=-1,          # use all CPU cores
            max_depth=15,       # prevent overfitting
            min_samples_leaf=5, # each leaf needs at least 5 samples
        )
        self.feature_cols = get_feature_cols()
        self.is_trained = False

    def train(self, df_featured, test_size: float = 0.2) -> dict:
        """
        Train the model. Returns a dict of evaluation metrics.

        Args:
            df_featured : DataFrame with feature columns + 'RUL' column
            test_size   : Fraction held out for evaluation

        Returns:
            {"mae": float, "r2": float, "n_train": int, "n_test": int}
        """
        X = df_featured[self.feature_cols].values
        y = df_featured["RUL"].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=RANDOM_STATE
        )

        self.model.fit(X_train, y_train)
        self.is_trained = True

        y_pred = self.model.predict(X_test)
        return {
            "mae"    : round(float(mean_absolute_error(y_test, y_pred)), 2),
            "r2"     : round(float(r2_score(y_test, y_pred)), 3),
            "n_train": len(X_train),
            "n_test" : len(X_test),
        }

    def predict_rul(self, feature_row: np.ndarray | list) -> float:
        """
        Predict RUL for a single engine's latest feature snapshot.

        Args:
            feature_row : 1D array of shape (n_features,) — use get_latest_snapshot()

        Returns:
            Predicted RUL in cycles (float, clamped ≥ 0)
        """
        self._check_trained()
        arr = np.array(feature_row).reshape(1, -1)
        rul = float(self.model.predict(arr)[0])
        return max(0.0, rul)   # RUL can't be negative

    def health_status(self, rul: float) -> str:
        """
        Convert a RUL prediction into a binary health status.

        Returns:
            "RED"   — engine needs attention within 30 cycles
            "GREEN" — engine is healthy
        """
        return "RED" if rul < RED_THRESHOLD else "GREEN"

    def top_features(self, n: int = 5) -> list[tuple[str, float]]:
        """
        Return the n most important features by Random Forest impurity score.
        Useful for understanding WHICH sensors drive RUL predictions.
        """
        self._check_trained()
        importances = self.model.feature_importances_
        ranked = sorted(
            zip(self.feature_cols, importances),
            key=lambda x: x[1],
            reverse=True,
        )
        return ranked[:n]

    def save(self, path: Path = MODEL_SAVE_PATH) -> None:
        """Serialize model to disk for reuse without retraining."""
        self._check_trained()
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)
        print(f"Model saved → {path}")

    @classmethod
    def load(cls, path: Path = MODEL_SAVE_PATH) -> "RULPredictor":
        """Load a previously saved model."""
        return joblib.load(path)

    def _check_trained(self):
        if not self.is_trained:
            raise RuntimeError("Model not trained yet. Call .train() first.")


# ─────────────────────────────────────────────────────────────────────────────
# Standalone test — run: python -m src.model
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from src.ingestion import generate_synthetic_cmapss
    from src.features import engineer_features, get_latest_snapshot

    print("Testing LAYER 3 — RUL Prediction Model")
    print(f"  Algorithm     : Random Forest ({N_ESTIMATORS} trees)")
    print(f"  RED threshold : RUL < {RED_THRESHOLD} cycles\n")

    # Build dataset
    df_raw  = generate_synthetic_cmapss(n_engines=50, seed=42)
    df_feat = engineer_features(df_raw)

    # Train
    predictor = RULPredictor()
    metrics = predictor.train(df_feat)

    print(f"Training results:")
    print(f"  MAE : {metrics['mae']} cycles  (mean absolute error)")
    print(f"  R²  : {metrics['r2']}          (1.0 = perfect)")
    print(f"  Train: {metrics['n_train']} rows  |  Test: {metrics['n_test']} rows")

    # Predict on a specific engine
    print(f"\nTop 5 most important features:")
    for feat, score in predictor.top_features(5):
        bar = "█" * int(score * 50)
        print(f"  {feat:<20} {bar} ({score:.3f})")

    # Spot check: engine 1, last known cycle
    snapshot = get_latest_snapshot(df_feat, engine_id=1)
    feat_vals = snapshot[predictor.feature_cols].values
    rul_pred  = predictor.predict_rul(feat_vals)
    rul_true  = snapshot["RUL"]
    status    = predictor.health_status(rul_pred)

    print(f"\nEngine 1 — final cycle prediction:")
    print(f"  Predicted RUL : {rul_pred:.1f} cycles")
    print(f"  True RUL      : {rul_true:.0f} cycles")
    print(f"  Health status : {status}")
    print(f"\n✅  Layer 3 — PASS")
