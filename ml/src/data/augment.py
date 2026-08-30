"""
Field-Condition Image Augmentation Pipeline for AgriShield AI.
Simulates natural field variations (rotations, shadows, lighting, minor blur)
without altering pathognomonic disease lesion characteristics.
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from typing import List

class FieldConditionAugmenter:
    def __init__(self, apply_prob: float = 0.5):
        self.apply_prob = apply_prob

    def augment(self, image: Image.Image) -> Image.Image:
        """Applies realistic field transformations."""
        img = image.copy()

        # 1. Random Rotation (0, 90, 180, 270 degrees or minor tilt)
        if np.random.rand() < self.apply_prob:
            angle = np.random.choice([90, 180, 270, np.random.uniform(-15, 15)])
            img = img.rotate(angle, expand=False)

        # 2. Horizontal / Vertical Flip
        if np.random.rand() < self.apply_prob:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if np.random.rand() < self.apply_prob * 0.5:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

        # 3. Brightness variation (sunlight vs overcast)
        if np.random.rand() < self.apply_prob:
            enhancer = ImageEnhance.Brightness(img)
            factor = np.random.uniform(0.80, 1.25)
            img = enhancer.enhance(factor)

        # 4. Contrast variation
        if np.random.rand() < self.apply_prob:
            enhancer = ImageEnhance.Contrast(img)
            factor = np.random.uniform(0.85, 1.20)
            img = enhancer.enhance(factor)

        # 5. Minor atmospheric blur or sharpness
        if np.random.rand() < 0.3:
            img = img.filter(ImageFilter.GaussianBlur(radius=np.random.uniform(0.3, 0.9)))

        return img
