import hashlib
import io
from typing import Optional, List
from PIL import Image
from app.ml.base import CropDiagnosisModel, DiagnosisOutput, PredictionCandidate
from app.ml.preprocessing import validate_and_preprocess_image

# Pre-defined realistic agronomic knowledge catalog for deterministic demo inference
DIAGNOSIS_CATALOG = {
    "tomato": [
        {
            "label": "Tomato Early Blight",
            "scientific_name": "Alternaria solani",
            "type": "DISEASE",
            "confidence": 0.91,
            "severity": "MODERATE",
            "affected_area": 28.5,
            "symptoms": [
                "Dark brown circular spots with characteristic concentric rings (target board pattern)",
                "Yellow chlorotic halos surrounding leaf lesions",
                "Lower and older leaves developing symptoms first before progressing upward"
            ],
            "causes": ["Fungal pathogen Alternaria solani", "Warm temperatures (24-29°C) combined with prolonged leaf wetness"],
            "alternatives": [
                {"label": "Tomato Septoria Leaf Spot", "scientific_name": "Septoria lycopersici", "confidence": 0.05, "type": "DISEASE"},
                {"label": "Tomato Healthy", "scientific_name": "Solanum lycopersicum", "confidence": 0.04, "type": "HEALTHY"}
            ]
        },
        {
            "label": "Tomato Late Blight",
            "scientific_name": "Phytophthora infestans",
            "type": "DISEASE",
            "confidence": 0.88,
            "severity": "HIGH",
            "affected_area": 42.0,
            "symptoms": [
                "Water-soaked dark green to brownish-black lesions rapidly expanding",
                "White fuzzy fungal sporulation on leaf undersides in high humidity",
                "Rapid collapse of foliage and stems"
            ],
            "causes": ["Oomycete pathogen Phytophthora infestans", "Cool wet weather (15-22°C) with continuous relative humidity >90%"],
            "alternatives": [
                {"label": "Tomato Early Blight", "scientific_name": "Alternaria solani", "confidence": 0.08, "type": "DISEASE"},
                {"label": "Tomato Bacterial Canker", "scientific_name": "Clavibacter michiganensis", "confidence": 0.04, "type": "DISEASE"}
            ]
        },
        {
            "label": "Tomato Whitefly Infestation",
            "scientific_name": "Bemisia tabaci",
            "type": "PEST",
            "confidence": 0.86,
            "severity": "MODERATE",
            "affected_area": 22.0,
            "symptoms": [
                "Tiny white fluttering insects on the underside of young leaves",
                "Sticky honeydew secretions causing black sooty mold growth",
                "Leaf chlorosis and stunted vegetative growth"
            ],
            "causes": ["Sap-sucking whitefly vector", "Warm sheltered microclimates"],
            "alternatives": [
                {"label": "Tomato Aphid Infestation", "scientific_name": "Myzus persicae", "confidence": 0.09, "type": "PEST"},
                {"label": "Tomato Healthy", "scientific_name": "Solanum lycopersicum", "confidence": 0.05, "type": "HEALTHY"}
            ]
        },
        {
            "label": "Tomato Healthy",
            "scientific_name": "Solanum lycopersicum",
            "type": "HEALTHY",
            "confidence": 0.96,
            "severity": "NONE",
            "affected_area": 0.0,
            "symptoms": ["Uniform green leaf pigmentation", "Vigorous turgid foliage without necrotic lesions or insect damage"],
            "causes": ["Optimal agronomic conditions and balanced nutrient management"],
            "alternatives": [
                {"label": "Tomato Early Blight (Early Stage)", "scientific_name": "Alternaria solani", "confidence": 0.03, "type": "DISEASE"},
                {"label": "Nutrient Deficiency (Mild)", "scientific_name": None, "confidence": 0.01, "type": "UNKNOWN"}
            ]
        }
    ],
    "potato": [
        {
            "label": "Potato Late Blight",
            "scientific_name": "Phytophthora infestans",
            "type": "DISEASE",
            "confidence": 0.93,
            "severity": "HIGH",
            "affected_area": 38.0,
            "symptoms": ["Pale green water-soaked spots turning dark brown", "Foliar death spreading rapidly across canopy"],
            "causes": ["Phytophthora infestans oomycete", "Persistent fog/rain with moderate temperatures"],
            "alternatives": [
                {"label": "Potato Early Blight", "scientific_name": "Alternaria solani", "confidence": 0.05, "type": "DISEASE"},
                {"label": "Potato Healthy", "scientific_name": "Solanum tuberosum", "confidence": 0.02, "type": "HEALTHY"}
            ]
        }
    ],
    "wheat": [
        {
            "label": "Wheat Stripe (Yellow) Rust",
            "scientific_name": "Puccinia striiformis",
            "type": "DISEASE",
            "confidence": 0.89,
            "severity": "HIGH",
            "affected_area": 35.0,
            "symptoms": [
                "Yellow-orange powdery pustules arranged in parallel linear stripes on leaves",
                "Premature foliar desiccation and grain shriveling"
            ],
            "causes": ["Airborne fungal urediniospores of Puccinia striiformis", "Cool moist spring weather"],
            "alternatives": [
                {"label": "Wheat Leaf Rust", "scientific_name": "Puccinia triticina", "confidence": 0.08, "type": "DISEASE"},
                {"label": "Wheat Powdery Mildew", "scientific_name": "Blumeria graminis", "confidence": 0.03, "type": "DISEASE"}
            ]
        }
    ],
    "rice": [
        {
            "label": "Rice Bacterial Leaf Blight",
            "scientific_name": "Xanthomonas oryzae pv. oryzae",
            "type": "DISEASE",
            "confidence": 0.87,
            "severity": "MODERATE",
            "affected_area": 30.0,
            "symptoms": [
                "Water-soaked to yellowish-white wavy lesions along leaf margins starting from tips",
                "Bacterial ooze droplets visible on young lesions in morning dew"
            ],
            "causes": ["Bacterial infection through hydathodes or wounds", "High nitrogen fertilization and rainstorms"],
            "alternatives": [
                {"label": "Rice Blast", "scientific_name": "Magnaporthe oryzae", "confidence": 0.09, "type": "DISEASE"},
                {"label": "Rice Brown Spot", "scientific_name": "Bipolaris oryzae", "confidence": 0.04, "type": "DISEASE"}
            ]
        }
    ],
    "maize": [
        {
            "label": "Maize Fall Armyworm Infestation",
            "scientific_name": "Spodoptera frugiperda",
            "type": "PEST",
            "confidence": 0.90,
            "severity": "CRITICAL",
            "affected_area": 45.0,
            "symptoms": [
                "Large irregular holes in whorl leaves resembling window panes",
                "Abundant yellowish-brown sawdust-like frass inside the central leaf whorl",
                "Larvae feeding deeply into growing reproductive points"
            ],
            "causes": ["Nocturnal female moths laying egg masses on lower leaves", "Warm weather conditions"],
            "alternatives": [
                {"label": "Maize Stem Borer", "scientific_name": "Busseola fusca", "confidence": 0.07, "type": "PEST"},
                {"label": "Maize Common Rust", "scientific_name": "Puccinia sorghi", "confidence": 0.03, "type": "DISEASE"}
            ]
        }
    ],
    "cotton": [
        {
            "label": "Cotton Pink Bollworm Infestation",
            "scientific_name": "Pectinophora gossypiella",
            "type": "PEST",
            "confidence": 0.89,
            "severity": "HIGH",
            "affected_area": 32.0,
            "symptoms": [
                "Rosetted flowers that fail to open properly",
                "Bore holes in developing green bolls with staining of lint and damaged seeds"
            ],
            "causes": ["Lepidopteran larvae feeding within squares and bolls", "Continuous host presence"],
            "alternatives": [
                {"label": "Cotton Leaf Curl Virus", "scientific_name": "Begomovirus", "confidence": 0.07, "type": "DISEASE"},
                {"label": "Cotton Healthy", "scientific_name": "Gossypium hirsutum", "confidence": 0.04, "type": "HEALTHY"}
            ]
        }
    ],
    "apple": [
        {
            "label": "Apple Scab",
            "scientific_name": "Venturia inaequalis",
            "type": "DISEASE",
            "confidence": 0.92,
            "severity": "MODERATE",
            "affected_area": 25.0,
            "symptoms": ["Olive-green to velvety brown-black circular spots on leaves and fruit skin", "Leaf puckering and premature leaf drop"],
            "causes": ["Fungal ascospores released during spring rains", "Prolonged leaf wetness >9 hours"],
            "alternatives": [
                {"label": "Apple Cedar Rust", "scientific_name": "Gymnosporangium juniperi-virginianae", "confidence": 0.05, "type": "DISEASE"},
                {"label": "Apple Healthy", "scientific_name": "Malus domestica", "confidence": 0.03, "type": "HEALTHY"}
            ]
        }
    ]
}

class MockDiagnosisModel(CropDiagnosisModel):
    def __init__(self, version: str = "v1.2.0-agrishield-demo"):
        self.version = version

    async def predict(self, image_bytes: bytes, crop_hint: Optional[str] = None, filename: Optional[str] = None) -> DiagnosisOutput:
        # Preprocess and validate image
        img = validate_and_preprocess_image(image_bytes, filename or "image.jpg")
        
        # Calculate image hash for deterministic demo results
        img_hash = int(hashlib.md5(image_bytes).hexdigest()[:8], 16)
        
        # Normalize crop key
        selected_crop = "tomato"
        if crop_hint:
            hint_clean = crop_hint.strip().lower()
            for key in DIAGNOSIS_CATALOG.keys():
                if key in hint_clean:
                    selected_crop = key
                    break

        crop_options = DIAGNOSIS_CATALOG.get(selected_crop, DIAGNOSIS_CATALOG["tomato"])
        selected_index = img_hash % len(crop_options)
        entry = crop_options[selected_index]

        # Construct candidates
        candidates = [
            PredictionCandidate(
                label=entry["label"],
                scientific_name=entry.get("scientific_name"),
                confidence=entry["confidence"],
                rank=1,
                detection_type=entry["type"]
            )
        ]

        rank = 2
        for alt in entry.get("alternatives", []):
            candidates.append(
                PredictionCandidate(
                    label=alt["label"],
                    scientific_name=alt.get("scientific_name"),
                    confidence=alt["confidence"],
                    rank=rank,
                    detection_type=alt.get("type", "DISEASE")
                )
            )
            rank += 1

        return DiagnosisOutput(
            predicted_label=entry["label"],
            scientific_name=entry.get("scientific_name"),
            confidence=entry["confidence"],
            detection_type=entry["type"],
            severity=entry["severity"],
            affected_area_percentage=entry["affected_area"],
            symptoms=entry["symptoms"],
            causes=entry["causes"],
            candidates=candidates,
            model_version=self.version,
            is_demo=True,
            raw_metadata={
                "image_width": img.width,
                "image_height": img.height,
                "provider": "mock",
                "deterministic_seed": img_hash,
                "inference_time_ms": 42
            }
        )
