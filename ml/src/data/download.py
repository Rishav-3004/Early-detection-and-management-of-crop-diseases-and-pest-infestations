"""
Dataset Downloader & Manifest Ingestion for AgriShield AI ML Pipeline.
Handles approved academic datasets (PlantVillage, PlantDoc, IP102, Mendeley Agri).
"""

import os
import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
METADATA_DIR = DATA_DIR / "metadata"

def load_dataset_registry() -> List[Dict[str, str]]:
    """Loads dataset registry CSV."""
    registry_file = METADATA_DIR / "dataset_registry.csv"
    if not registry_file.exists():
        logger.warning(f"Registry file {registry_file} does not exist.")
        return []
    
    with open(registry_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def initialize_dataset_directories():
    """Ensures raw, processed, and manifest directories exist."""
    for sub in ["raw", "interim", "processed", "manifests"]:
        (DATA_DIR / sub).mkdir(parents=True, exist_ok=True)
    logger.info(f"Initialized data directories under: {DATA_DIR}")

if __name__ == "__main__":
    initialize_dataset_directories()
    registry = load_dataset_registry()
    logger.info(f"Found {len(registry)} approved datasets in registry.")
