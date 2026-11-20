"""One metric implementation for every rating-prediction model."""

from __future__ import annotations

import numpy as np


def rating_metrics(y_true, y_pred, *, epsilon: float = 1e-8) -> dict[str, float]:
    """Compute MAE, MSE, RMSE, and MAPE as a fraction.

    The paper tables report MAPE as a fraction (for example, 0.089), so this
    function does not multiply the value by 100.
    """

    truth = np.asarray(y_true, dtype=float).reshape(-1)
    prediction = np.asarray(y_pred, dtype=float).reshape(-1)
    if truth.shape != prediction.shape:
        raise ValueError("y_true and y_pred must have the same shape")
    if truth.size == 0:
        raise ValueError("metrics require at least one prediction")
    residual = truth - prediction
    mse = float(np.mean(np.square(residual)))
    denominator = np.maximum(np.abs(truth), epsilon)
    return {
        "mae": float(np.mean(np.abs(residual))),
        "mse": mse,
        "rmse": float(np.sqrt(mse)),
        "mape": float(np.mean(np.abs(residual) / denominator)),
    }

