from datetime import datetime, timezone
from app.services.risk_engine import risk_engine
from app.services.recommendation_engine import recommendation_engine
from app.schemas.communication import WeatherCurrentResponse

def test_risk_engine_healthy():
    res = risk_engine.evaluate_risk(
        detection_type="HEALTHY",
        predicted_label="Tomato Healthy",
        confidence=0.95,
        severity="NONE"
    )
    assert res.risk_level == "LOW"
    assert res.risk_score <= 10.0

def test_risk_engine_high_humidity_weather_multiplier():
    weather = WeatherCurrentResponse(
        temperature=26.0,
        humidity=88.0,
        rainfall=6.5,
        wind_speed=12.0,
        weather_condition="Light Rain",
        recorded_at=datetime.now(timezone.utc),
        risk_assessment="High risk",
        high_disease_risk_warning=True
    )
    res = risk_engine.evaluate_risk(
        detection_type="DISEASE",
        predicted_label="Tomato Early Blight",
        confidence=0.92,
        severity="HIGH",
        growth_stage="Flowering",
        weather=weather,
        recent_field_detections_count=2
    )
    assert res.risk_level in ["HIGH", "CRITICAL"]
    assert res.risk_score >= 80.0
    assert any("humidity" in r.lower() for r in res.reasons)

def test_recommendation_engine_structure():
    recs = recommendation_engine.generate_recommendations(
        crop_name="Tomato",
        predicted_label="Tomato Early Blight",
        detection_type="DISEASE",
        severity="MODERATE",
        risk_level="MEDIUM",
        risk_score=55.0,
        symptoms=["Concentric ring lesions"]
    )
    assert len(recs.immediate_actions) > 0
    assert len(recs.management) > 0
    assert len(recs.prevention) > 0
    assert len(recs.monitoring) > 0
    assert "disclaimer" in recs.dict()
