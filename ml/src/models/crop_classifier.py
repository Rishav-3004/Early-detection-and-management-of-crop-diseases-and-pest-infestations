"""
Botanical Crop Species Classifier.
Identifies crop type (Tomato, Potato, Wheat, Rice, Cotton, Soybean, Maize, Chickpea, Mustard).
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple
from ml.src.models.base import ImageFeatureExtractor

class CropClassifier:
    def __init__(self):
        self.feature_extractor = ImageFeatureExtractor()
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight="balanced")
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
