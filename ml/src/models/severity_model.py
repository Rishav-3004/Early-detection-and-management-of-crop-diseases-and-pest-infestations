"""
Foliar Lesion Surface Area & Severity Estimator for AgriShield AI.
Separates classification confidence from biological severity.
Computes affected necrotic/chlorotic surface area ratio through adaptive segmentation.
"""

import numpy as np
from PIL import Image
from dataclasses import dataclass
from typing import Tuple

@dataclass
class SeverityOutput:
    severity_level: str  # NONE, LOW, MODERATE, HIGH, CRITICAL, SEVERITY_NOT_RELIABLY_ESTIMATED
    affected_area_percentage: float  # 0.0 - 100.0
    estimated: bool

class SeverityModel:
    """Estimates affected canopy surface area percentage and severity level."""
    def __init__(self):
        pass

    def estimate_severity(self, image: Image.Image, detection_type: str) -> SeverityOutput:
        if detection_type == "HEALTHY":
            return SeverityOutput(severity_level="NONE", affected_area_percentage=0.0, estimated=True)

        img_rgb = image.convert("RGB").resize((256, 256))
        arr = np.array(img_rgb, dtype=np.float32)

        r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        
        # 1. Segment Total Foliage Area (ExG > 5)
        exg = 2.0 * g - r - b
        foliage_mask = (exg > 5.0) | ((g > 40) & (r < 200))
        total_foliage_pixels = np.sum(foliage_mask)

        if total_foliage_pixels < 2000:
            return SeverityOutput(
                severity_level="SEVERITY_NOT_RELIABLY_ESTIMATED",
                affected_area_percentage=15.0,
                estimated=False
            )

        # 2. Segment Lesions / Necrotic / Chlorotic Area
        # Necrotic/yellow spots have high Red/Green ratio and low Excess Green
        lesion_mask = foliage_mask & (
            ((r > 1.1 * g) & (b < 140)) |  # Brown / Rust / Blight spots
            ((r > 150) & (g > 150) & (b < 100)) |  # Yellow chlorosis halo
            ((r < 60) & (g < 60) & (b < 60))  # Dark necrotic lesions
        )
        lesion_pixels = np.sum(lesion_mask)

        affected_pct = float(np.clip((lesion_pixels / (total_foliage_pixels + 1e-6)) * 100.0, 1.0, 95.0))

        # 3. Categorize Severity Level
        if affected_pct < 8.0:
            level = "LOW"
        elif affected_pct < 25.0:
            level = "MODERATE"
        elif affected_pct < 55.0:
            level = "HIGH"
        else:
            level = "CRITICAL"

        return SeverityOutput(
            severity_level=level,
            affected_area_percentage=round(affected_pct, 1),
            estimated=True
        )
