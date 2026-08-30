"""
Perceptual Deduplication Engine for AgriShield AI.
Uses perceptual hashing (pHash & dHash) to eliminate duplicate and near-duplicate images.
"""

import os
import csv
import logging
from pathlib import Path
from PIL import Image
import imagehash

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
MANIFEST_DIR = DATA_DIR / "manifests"

def deduplicate_dataset(manifest_path: Path = None, threshold: int = 4) -> Path:
    if manifest_path is None:
        manifest_path = MANIFEST_DIR / "validated_manifest.csv"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    seen_hashes = {}
    deduped_rows = []
    duplicate_count = 0

    with open(manifest_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            p = Path(row["file_path"])
            try:
                with Image.open(p) as img:
                    # Calculate perceptual hash
                    phash = imagehash.phash(img)
                    
                    is_dup = False
                    for existing_hash, existing_path in seen_hashes.items():
                        if phash - existing_hash <= threshold:
                            is_dup = True
                            duplicate_count += 1
                            logger.debug(f"Duplicate detected: {p.name} matches {existing_path}")
                            break

                    if not is_dup:
                        seen_hashes[phash] = p.name
                        row["status"] = "DEDUPED"
                        deduped_rows.append(row)
            except Exception as e:
                logger.warning(f"Failed to hash {p}: {e}")

    out_path = MANIFEST_DIR / "deduped_manifest.csv"
    with open(out_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file_path", "filename", "crop", "label", "detection_type", "image_type", "width", "height", "status"])
        writer.writeheader()
        writer.writerows(deduped_rows)

    logger.info(f"Deduplication complete. Retained: {len(deduped_rows)}, Removed duplicates: {duplicate_count}")
    return out_path

if __name__ == "__main__":
    deduplicate_dataset()
