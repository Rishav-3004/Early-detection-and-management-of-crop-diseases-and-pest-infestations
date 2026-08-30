"""
Base Feature Extractor & Vision Modeling Protocol.
Provides consistent multi-scale color moments, spatial color structure,
gradient statistics, and vegetation indices for lightweight and neural classifiers.
"""

import numpy as np
from PIL import Image
from typing import Dict, Any, List

class ImageFeatureExtractor:
    """
    Extracts multi-spectral and spatial textural descriptor vectors from plant foliage.
    Computes RGB/HSV color moments, spatial sub-grid histograms, and edge gradients.
    """
    def __init__(self, target_size: tuple = (128, 128)):
        self.target_size = target_size

    def extract_features(self, image: Image.Image) -> np.ndarray:
        # Resize to fixed dimension
        img = image.convert("RGB").resize(self.target_size)
        arr = np.array(img, dtype=np.float32) / 255.0  # (H, W, 3)

        features = []

        # 1. Global Color Moments (Mean, Std, Skewness for R, G, B)
        for c in range(3):
            channel = arr[:, :, c]
            mean = np.mean(channel)
            std = np.std(channel)
            diff = channel - mean
            skew = np.mean(diff ** 3) / (std ** 3 + 1e-6)
            features.extend([mean, std, skew])

        # 2. HSV Color Moments (Hue, Saturation, Value)
        img_hsv = img.convert("HSV")
        arr_hsv = np.array(img_hsv, dtype=np.float32) / 255.0
        for c in range(3):
            channel = arr_hsv[:, :, c]
            mean = np.mean(channel)
            std = np.std(channel)
            features.extend([mean, std])

        # 3. Excess Green Index (ExG) & Chlorophyll Health Ratios
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        exg = 2.0 * g - r - b
        features.extend([np.mean(exg), np.std(exg), np.percentile(exg, 10), np.percentile(exg, 90)])

        # 4. Spatial Grid 2x2 Sub-Region Color Descriptors (Captures local lesion hotspots)
        h_half, w_half = self.target_size[0] // 2, self.target_size[1] // 2
        quadrants = [
            arr[:h_half, :w_half, :],
            arr[:h_half, w_half:, :],
            arr[h_half:, :w_half, :],
            arr[h_half:, w_half:, :],
        ]
        for quad in quadrants:
            features.extend([
                np.mean(quad[:, :, 0]), np.std(quad[:, :, 0]),  # R
                np.mean(quad[:, :, 1]), np.std(quad[:, :, 1]),  # G
                np.mean(quad[:, :, 2]), np.std(quad[:, :, 2]),  # B
            ])

        # 5. Spatial Texture Gradients (Discrete Sobel approximations)
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        grad_y = np.abs(np.diff(gray, axis=0))
        grad_x = np.abs(np.diff(gray, axis=1))
        features.extend([
            np.mean(grad_x), np.std(grad_x),
            np.mean(grad_y), np.std(grad_y)
        ])

        return np.array(features, dtype=np.float32)
