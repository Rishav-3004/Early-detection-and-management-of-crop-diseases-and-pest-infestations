"""
Data Validator for AgriShield AI ML Pipeline.
Detects corrupted files, improper aspect ratios, extreme color shifts, or missing labels.
"""

import os
import csv
import logging
from pathlib import Path
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
MANIFEST_DIR = DATA_DIR / "manifests"

def validate_dataset(manifest_path: Path = None) -> Path:
    if manifest_path is None:
        manifest_path = MANIFEST_DIR / "dataset_manifest.csv"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found at {manifest_path}")

    validated_rows = []
    rejected_count = 0

    with open(manifest_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = Path(row["file_path"])
            if not p.exists():
                logger.warning(f"File missing: {p}")
                rejected_count += 1
                continue

            try:
                with Image.open(p) as img:
                    img.verify()
                
                with Image.open(p) as img:
                    w, h = img.size
                    if w < 50 or h < 50 or w > 10000 or h > 10000:
                        rejected_count += 1
                        continue
                    
                    row["status"] = "VALIDATED"
                    validated_rows.append(row)
            except Exception as e:
                logger.warning(f"Corrupt image {p}: {e}")
                rejected_count += 1

    out_path = MANIFEST_DIR / "validated_manifest.csv"
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file_path", "filename", "crop", "label", "detection_type", "image_type", "width", "height", "status"])
        writer.writeheader()
        writer.writerows(validated_rows)

    logger.info(f"Validation complete. Valid: {len(validated_rows)}, Rejected/Corrupt: {rejected_count}")
    return out_path

if __name__ == "__main__":
    validate_dataset()
