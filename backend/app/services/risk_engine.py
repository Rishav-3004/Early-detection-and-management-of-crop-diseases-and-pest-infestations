from typing import Dict, Any, List, Optional
from app.schemas.communication import WeatherCurrentResponse

class RiskAssessmentResult:
    def __init__(self, risk_level: str, risk_score: float, reasons: List[str]):
        self.risk_level = risk_level
        self.risk_score = risk_score
        self.reasons = reasons

class RiskEngine:
    """
    Multi-Factor Agronomic Risk Engine.
    Combines AI detection type, severity, model confidence, crop growth stage,
    and real-time meteorological conditions to compute a calibrated risk index.
    """
    
    SEVERITY_BASE_SCORES = {
        "NONE": 5.0,
        "LOW": 25.0,
        "MODERATE": 50.0,
        "HIGH": 75.0,
        "CRITICAL": 92.0
    }

    VULNERABLE_GROWTH_STAGES = [
        "flowering",
        "fruiting",
        "grain filling",
        "tasseling",
        "boll development"
    ]

    def evaluate_risk(
        self,
        detection_type: str,
        predicted_label: str,
        confidence: float,
        severity: str,
        growth_stage: Optional[str] = None,
        weather: Optional[WeatherCurrentResponse] = None,
        recent_field_detections_count: int = 0
    ) -> RiskAssessmentResult:
        if detection_type == "HEALTHY":
            return RiskAssessmentResult(
                risk_level="LOW",
                risk_score=5.0,
                reasons=["Crop tissue appears healthy with no active pathogen or pest symptoms."]
            )

        # 1. Base Score from Severity
        base_score = self.SEVERITY_BASE_SCORES.get(severity.upper(), 50.0)
        score = base_score
        reasons: List[str] = []

        # 2. Confidence scaling
        if confidence >= 0.85:
            reasons.append(f"High diagnostic confidence ({int(confidence * 100)}%) for {predicted_label}")
        elif confidence < 0.60:
            score *= 0.85  # Dampen risk score slightly if confidence is weak
            reasons.append("Uncertain diagnosis due to lower model confidence; field verification recommended")

        # 3. Growth Stage Factor
        if growth_stage and any(v in growth_stage.lower() for v in self.VULNERABLE_GROWTH_STAGES):
            score += 10.0
            reasons.append(f"Crop is in a highly vulnerable reproductive/fruiting stage ({growth_stage})")

        # 4. Weather & Environmental Microclimate Factors
        if weather:
            if weather.humidity >= 75.0:
                score += 12.0
                reasons.append(f"Elevated atmospheric humidity ({weather.humidity}%) strongly favors fungal sporulation and bacterial spread")
            elif weather.humidity <= 35.0 and detection_type == "PEST":
                score += 8.0
                reasons.append(f"Dry, warm weather ({weather.temperature}°C, {weather.humidity}% RH) accelerates pest reproduction cycles")

            if weather.rainfall > 5.0:
                score += 8.0
                reasons.append(f"Recent rainfall ({weather.rainfall}mm) causes free moisture on leaves, facilitating pathogen entry")

            if 18.0 <= weather.temperature <= 29.0 and detection_type == "DISEASE":
                score += 5.0
                reasons.append(f"Ambient temperature ({weather.temperature}°C) is in the optimal growth range for foliar pathogens")

        # 5. Historical Field Recurrence
        if recent_field_detections_count >= 3:
            score += 10.0
            reasons.append(f"Repeated active infestations detected in this field ({recent_field_detections_count} recent cases)")
        elif recent_field_detections_count >= 1:
            score += 5.0
            reasons.append("Previous related symptoms observed in this field within the past 14 days")

        # Clamp score between 0.0 and 100.0
        final_score = max(0.0, min(100.0, score))

        # Classify Risk Level
        if final_score >= 80.0:
            level = "CRITICAL"
        elif final_score >= 60.0:
            level = "HIGH"
        elif final_score >= 35.0:
            level = "MEDIUM"
        else:
            level = "LOW"

        if not reasons:
            reasons.append(f"Baseline {severity.lower()} severity assessment under normal environmental conditions.")

        return RiskAssessmentResult(
            risk_level=level,
            risk_score=round(final_score, 1),
            reasons=reasons
        )

risk_engine = RiskEngine()
