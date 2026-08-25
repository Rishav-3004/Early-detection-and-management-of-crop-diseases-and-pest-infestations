from typing import Dict, Type
from app.ml.base import CropDiagnosisModel
from app.ml.mock_model import MockDiagnosisModel
from app.core.config import settings
from app.core.logging import logger

class ModelRegistry:
    def __init__(self):
        self._providers: Dict[str, CropDiagnosisModel] = {}
        self._register_default_models()

    def _register_default_models(self):
        # Register mock model
        self._providers["mock"] = MockDiagnosisModel(version=settings.MODEL_VERSION)
        logger.info("Registered default MockDiagnosisModel in ModelRegistry")

    def register(self, name: str, model_instance: CropDiagnosisModel):
        self._providers[name.lower()] = model_instance
        logger.info(f"Registered custom model provider: {name}")

    def get_model(self, provider_name: str = None) -> CropDiagnosisModel:
        name = (provider_name or settings.MODEL_PROVIDER).lower()
        if name not in self._providers:
            logger.warning(f"Requested model provider '{name}' not found. Falling back to 'mock'.")
            return self._providers["mock"]
        return self._providers[name]

model_registry = ModelRegistry()
