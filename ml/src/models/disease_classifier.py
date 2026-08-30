"""
Botanical Crop Classifier & Disease/Pest Pathology Classifiers.
Provides hierarchical classification and Top-K candidate generation.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from typing import List, Dict, Tuple, Optional
from ml.src.models.base import ImageFeatureExtractor

class CropClassifier:
    """Classifies botanical crop species."""
    def __init__(self):
        self.feature_extractor = ImageFeatureExtractor()
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, class_weight="balanced")
        self.classes_: List[str] = []

    def fit(self, X: np.ndarray, y: List[str]):
        self.classes_ = sorted(list(set(y)))
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict(self, X: np.ndarray) -> Tuple[List[str], np.ndarray]:
        X_scaled = self.scaler.transform(X)
        preds = self.model.predict(X_scaled)
        probs = self.model.predict_proba(X_scaled)
        return list(preds), probs

class DiseasePestClassifier:
    """Classifies plant pathology conditions across diseases, pests, and healthy states."""
    def __init__(self):
        self.feature_extractor = ImageFeatureExtractor()
        self.scaler = StandardScaler()
        self.model = GradientBoostingClassifier(n_estimators=120, learning_rate=0.08, max_depth=5, random_state=42)
        self.classes_: List[str] = []
        self.temperature: float = 1.0

    def fit(self, X: np.ndarray, y: List[str]):
        self.classes_ = sorted(list(set(y)))
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

    def predict_logits(self, X: np.ndarray) -> np.ndarray:
        X_scaled = self.scaler.transform(X)
        # Decision function or raw logits
        if hasattr(self.model, "decision_function"):
            return self.model.decision_function(X_scaled)
        probs = self.model.predict_proba(X_scaled)
        return np.log(np.clip(probs, 1e-7, 1.0 - 1e-7))

    def predict_top_k(self, X: np.ndarray, top_k: int = 3) -> List[List[Dict[str, Any]]]:
        """Returns calibrated top-k candidates for each sample."""
        logits = self.predict_logits(X) / max(0.1, self.temperature)
        
        # Softmax
        exp_logits = np.exp(logits - np.max(logits, axis=1, keepdims=True))
        calibrated_probs = exp_logits / np.sum(exp_logits, axis=1, keepdims=True)

        results = []
        for i in range(len(X)):
            sample_probs = calibrated_probs[i]
            sorted_indices = np.argsort(sample_probs)[::-1][:top_k]
            
            candidates = []
            for rank, idx in enumerate(sorted_indices, 1):
                candidates.append({
                    "label": self.classes_[idx],
                    "confidence": float(sample_probs[idx]),
                    "rank": rank
                })
            results.append(candidates)
        return results
