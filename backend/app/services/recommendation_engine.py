from typing import Optional, List, Dict, Any
from app.schemas.knowledge import StructuredRecommendation

class RecommendationEngine:
    """
    Agronomic Recommendation Engine.
    Generates actionable, structured guidance (immediate actions, management,
    prevention, monitoring, expert review) based on crop, diagnosis, severity, and risk.
    """

    DEFAULT_DISCLAIMER = (
        "AI-generated recommendations provide preliminary agronomic guidelines. "
        "Always follow certified local extension advisories and adhere strictly to "
        "manufacturer instructions on registered chemical labels before treatment application."
    )

    def generate_recommendations(
        self,
        crop_name: Optional[str],
        predicted_label: str,
        detection_type: str,
        severity: str,
        risk_level: str,
        risk_score: float,
        symptoms: List[str]
    ) -> StructuredRecommendation:
        if detection_type == "HEALTHY":
            return StructuredRecommendation(
                immediate_actions=["No corrective chemical or cultural intervention required."],
                management=[
                    "Continue standard balanced irrigation and crop nutrition program.",
                    "Maintain regular scouting schedule to detect early symptoms of seasonal stresses."
                ],
                prevention=[
                    "Ensure adequate plant spacing for optimal light penetration and airflow.",
                    "Practice clean crop sanitation and sanitize field tools between rows."
                ],
                monitoring=["Perform visual scouting once every 7 to 10 days."],
                expert_review_advice="Not required for healthy plants unless unusual physiological discoloration occurs.",
                disclaimer=self.DEFAULT_DISCLAIMER
            )

        immediate: List[str] = []
        management: List[str] = []
        prevention: List[str] = []
        monitoring: List[str] = []
        expert_advice = ""

        # Immediate Actions based on severity
        if severity in ["HIGH", "CRITICAL"]:
            immediate.append("Immediately isolate and rogue out severely infected plant tissue/leaves to stop spore dispersion.")
            immediate.append("Do not compost infected foliage; bag and remove plant debris away from the cultivation area.")
            immediate.append("Halt overhead sprinkler irrigation to avoid splashing moisture across neighboring healthy foliage.")
        elif severity == "MODERATE":
            immediate.append("Prune lower leaves showing characteristic chlorotic spots or active insect colonies.")
            immediate.append("Sanitize pruning shears in a 10% bleach solution between cuts.")
        else: # LOW
            immediate.append("Flag the affected row/zone and visually inspect surrounding plants within a 5-meter radius.")

        # Management steps based on detection type
        if detection_type == "DISEASE":
            management.append("Enhance canopy airflow by selectively pruning dense suckers and staking tall stems.")
            management.append("Switch to drip or furrow irrigation to keep foliar surfaces completely dry.")
            management.append("If recommended by your regional agricultural extension, apply a registered protective bio-fungicide or copper-based preventative formulation strictly according to label directions.")
        elif detection_type == "PEST":
            management.append("Deploy yellow or blue sticky traps (15-20 traps per hectare) to monitor adult population dynamics.")
            management.append("Consider releasing beneficial natural predators (such as ladybird beetles, lacewings, or predatory mites) where feasible.")
            management.append("In cases of heavy localized pest density, apply registered neem-based botanical formulations or target-specific insecticidal soaps.")

        # Prevention
        prevention.append("Follow balanced N-P-K fertilization; avoid excessive nitrogen which generates soft succulent tissue vulnerable to pathogens.")
        prevention.append("Implement crop rotation with non-host plant families for at least 2 to 3 successive seasons.")
        prevention.append("Select certified disease-resistant or tolerant crop seed cultivars for upcoming planting cycles.")

        # Monitoring
        if risk_level in ["HIGH", "CRITICAL"]:
            monitoring.append("Re-inspect affected plants every 48 hours to track lesion expansion or pest migration.")
            expert_advice = "Urgent consultation with an agronomist or extension specialist is strongly advised to prevent yield loss."
        elif risk_level == "MEDIUM":
            monitoring.append("Re-examine affected field blocks every 3 to 4 days.")
            expert_advice = "Request expert review if symptoms spread to new growth within 5 days."
        else:
            monitoring.append("Routine weekly field scouting recommended.")
            expert_advice = "Expert review optional unless atypical symptoms emerge."

        return StructuredRecommendation(
            immediate_actions=immediate,
            management=management,
            prevention=prevention,
            monitoring=monitoring,
            expert_review_advice=expert_advice,
            disclaimer=self.DEFAULT_DISCLAIMER
        )

recommendation_engine = RecommendationEngine()
