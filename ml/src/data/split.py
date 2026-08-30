"""
Dataset Splitting & Partitioning.
Splits deduplicated dataset into Train (70%), Validation (15%), and Test (15%) splits
with class stratification and strict leakage prevention.
"""

import os
import csv
import random
import logging
from collections import defaultdict
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
MANIFEST_DIR = DATA_DIR / "manifests"

def split_dataset(
    manifest_path: Path = None,
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42
) -> Dict_Paths:
    if manifest_path is None:
        manifest_path = MANIFEST_DIR / "deduped_manifest.csv"

    if not manifest_path.exists():
        manifest_path = MANIFEST_DIR / "validated_manifest.csv"

    random.seed(seed)
    by_class = defaultdict(list)

    with open(manifest_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            by_class[row["label"]].append(row)

    train_rows, val_rows, test_rows = [], [], []

    for label, items in by_class.items():
        random.shuffle(items)
        n = len(items)
        n_train = max(1, int(n * train_ratio))
        n_val = max(1, int(n * val_ratio)) if n >= 3 else 0
        
        train_items = items[:n_train]
        val_items = items[n_train:n_train + n_val]
        test_items = items[n_train + n_val:]

        if not test_items and len(train_items) > 1:
            test_items = [train_items.pop()]

        for it in train_items:
            it["split"] = "train"
            train_rows.append(it)
        for it in val_items:
            it["split"] = "val"
            val_rows.append(it)
        for it in test_items:
            it["split"] = "test"
            test_rows.append(it)

    logger.info(f"Splits created: Train={len(train_rows)}, Val={len(val_rows)}, Test={len(test_rows)}")

    fieldnames = ["file_path", "filename", "crop", "label", "detection_type", "image_type", "width", "height", "status", "split"]

    def write_split(path: Path, rows: list):
        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    train_path = MANIFEST_DIR / "train_manifest.csv"
    val_path = MANIFEST_DIR / "val_manifest.csv"
    test_path = MANIFEST_DIR / "test_manifest.csv"

    write_split(train_path, train_rows)
    write_split(val_path, val_rows)
    write_split(test_path, test_rows)

    return {
        "train": train_path,
        "val": val_path,
        "test": test_path
    }

if __name__ == "__main__":
    split_dataset()
