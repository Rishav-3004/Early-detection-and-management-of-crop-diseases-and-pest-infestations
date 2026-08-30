from typing import Dict, Type
from pathlib import Path
from app.ml.base import CropDiagnosisModel
from app.ml.mock_model import MockDiagnosisModel
from app.core.config import settings
from app.core.logging import logger

class ModelRegistry:
    def __init__(self):
        self._providers: Dict[str, CropDiagnosisModel] = {}
        self._register_default_models()

    def _register_default_models(self):
        # 1. Register mock model (always available as fallback/demo)
        self._providers["mock"] = MockDiagnosisModel(version="v1.2.0-agrishield-demo")

        # 2. Register production model if weights are available
        try:
            from app.ml.production_model import ProductionMLDiagnosisModel
            prod_model = ProductionMLDiagnosisModel()
            self._providers["production"] = prod_model
            self._providers["onnx"] = prod_model
            self._providers["pytorch"] = prod_model
            logger.info("Registered ProductionMLDiagnosisModel in ModelRegistry")
        except Exception as e:
            logger.warning(f"Could not initialize ProductionMLDiagnosisModel: {e}. Defaulting to mock.")

    def register(self, name: str, model_instance: CropDiagnosisModel):
        self._providers[name.lower()] = model_instance
        logger.info(f"Registered custom model provider: {name}")

    def get_model(self, provider_name: str = None) -> CropDiagnosisModel:
        name = (provider_name or settings.MODEL_PROVIDER).lower()
        if name in self._providers:
            return self._providers[name]
        
        # Fallback to production if available, else mock
        if "production" in self._providers:
            return self._providers["production"]
        return self._providers["mock"]

model_registry = ModelRegistry()
