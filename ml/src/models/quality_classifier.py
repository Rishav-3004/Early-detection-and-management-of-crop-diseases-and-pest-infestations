"""
Image Quality Gate Classifier for AgriShield AI.
Evaluates sharpness (Laplacian variance), exposure bounds, and vegetation presence.
Rejects unanalyzable uploads with IMAGE_QUALITY_INSUFFICIENT and actionable tips.
"""

import numpy as np
from PIL import Image
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class QualityResult:
    is_acceptable: bool
    quality_status: str  # ACCEPTABLE, BLURRY, UNDER_EXPOSED, OVER_EXPOSED, NO_PLANT_DETECTED
    blur_score: float
    exposure_score: float
    vegetation_score: float
    rejection_reason: Optional[str] = None
    user_guidance: Optional[str] = None

class QualityClassifier:
    def __init__(
        self,
        min_blur_threshold: float = 18.0,
        min_exposure: float = 25.0,
        max_exposure: float = 235.0,
        min_vegetation_ratio: float = 0.08
    ):
        self.min_blur_threshold = min_blur_threshold
        self.min_exposure = min_exposure
        self.max_exposure = max_exposure
        self.min_vegetation_ratio = min_vegetation_ratio

    def evaluate_quality(self, image: Image.Image) -> QualityResult:
        img_rgb = image.convert("RGB").resize((256, 256))
        arr = np.array(img_rgb, dtype=np.float32)

        # 1. Luminance & Exposure Calculation
        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        mean_exposure = float(np.mean(gray))

        if mean_exposure < self.min_exposure:
            return QualityResult(
                is_acceptable=False,
                quality_status="UNDER_EXPOSED",
                blur_score=0.0,
                exposure_score=mean_exposure,
                vegetation_score=0.0,
                rejection_reason="The image is too dark or underexposed.",
                user_guidance="Please take a photo under natural diffuse daylight or turn on flash to illuminate the leaf."
            )

        if mean_exposure > self.max_exposure:
            return QualityResult(
                is_acceptable=False,
                quality_status="OVER_EXPOSED",
                blur_score=0.0,
                exposure_score=mean_exposure,
                vegetation_score=0.0,
                rejection_reason="The image is washed out or overexposed to direct sunlight.",
                user_guidance="Please avoid direct camera lens glare or blinding sun reflections on the leaf surface."
            )

        # 2. Sharpness / Blur Detection via 2D Discrete Laplacian Filter
        # Kernel: [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
        laplacian = (
            np.roll(gray, 1, axis=0) +
            np.roll(gray, -1, axis=0) +
            np.roll(gray, 1, axis=1) +
            np.roll(gray, -1, axis=1) -
            4.0 * gray
        )
        blur_score = float(np.var(laplacian[2:-2, 2:-2]))

        if blur_score < self.min_blur_threshold:
            return QualityResult(
                is_acceptable=False,
                quality_status="BLURRY",
                blur_score=blur_score,
                exposure_score=mean_exposure,
                vegetation_score=0.0,
                rejection_reason="The image is out of focus or motion-blurred.",
                user_guidance="Please hold the phone steady and tap the screen on the affected leaf spots to focus before capturing."
            )

        # 3. Botanical Foliage / Chlorophyll Vegetation Ratio (Excess Green > 10)
        exg = 2.0 * g - r - b
        vegetation_pixels = np.sum(exg > 8.0)
        total_pixels = 256 * 256
        vegetation_ratio = float(vegetation_pixels / total_pixels)

        if vegetation_ratio < self.min_vegetation_ratio:
            return QualityResult(
                is_acceptable=False,
                quality_status="NO_PLANT_DETECTED",
                blur_score=blur_score,
                exposure_score=mean_exposure,
                vegetation_score=vegetation_ratio,
                rejection_reason="No identifiable crop or plant foliage detected in image frame.",
                user_guidance="Ensure the crop leaf or plant occupies at least 60% of the camera view."
            )

        return QualityResult(
            is_acceptable=True,
            quality_status="ACCEPTABLE",
            blur_score=blur_score,
            exposure_score=mean_exposure,
            vegetation_score=vegetation_ratio
        )
