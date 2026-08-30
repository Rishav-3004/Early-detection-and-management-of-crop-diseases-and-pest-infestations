"""
Confidence Calibration Module for AgriShield AI.
Implements Temperature Scaling (Platt scaling) and Expected Calibration Error (ECE).
"""

import numpy as np
from scipy.optimize import minimize
from typing import Tuple, Dict, Any

class TemperatureScaler:
    """Post-hoc temperature scaling on validation set logits."""
    def __init__(self):
        self.temperature: float = 1.0

    def fit(self, logits: np.ndarray, y_true_indices: np.ndarray) -> float:
        """Finds optimal temperature T > 0 minimizing negative log likelihood."""
        num_samples = len(y_true_indices)

        def nll(t_val):
            t = float(t_val[0])
            scaled_logits = logits / max(1e-3, t)
            exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=1, keepdims=True))
            probs = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)
            
            # Extract true class probabilities
            correct_probs = probs[np.arange(num_samples), y_true_indices]
            loss = -np.mean(np.log(np.clip(correct_probs, 1e-7, 1.0)))
            return loss

        res = minimize(nll, x0=[1.0], bounds=[(0.1, 5.0)], method="L-BFGS-B")
        self.temperature = float(res.x[0])
        return self.temperature

    def compute_ece(self, probs: np.ndarray, y_true_indices: np.ndarray, num_bins: int = 10) -> float:
        """Calculates Expected Calibration Error (ECE)."""
        confidences = np.max(probs, axis=1)
        predictions = np.argmax(probs, axis=1)
        accuracies = predictions == y_true_indices

        bin_boundaries = np.linspace(0, 1, num_bins + 1)
        ece = 0.0

        for i in range(num_bins):
            bin_lower, bin_upper = bin_boundaries[i], bin_boundaries[i + 1]
            in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
            prop_in_bin = np.mean(in_bin)

            if prop_in_bin > 0:
                accuracy_in_bin = np.mean(accuracies[in_bin])
                avg_confidence_in_bin = np.mean(confidences[in_bin])
                ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin

        return float(ece)
