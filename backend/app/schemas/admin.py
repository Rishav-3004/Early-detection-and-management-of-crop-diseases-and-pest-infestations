from typing import List, Dict, Any
from pydantic import BaseModel

class SystemKPIs(BaseModel):
    total_users: int
    total_farmers: int
    total_experts: int
    total_farms: int
    total_fields: int
    total_scans: int
    total_diseases_detected: int
    total_pests_detected: int
    total_healthy_scans: int
    pending_expert_reviews: int
    completed_expert_reviews: int

class ModelPerformanceMetrics(BaseModel):
    model_version: str
    total_predictions: int
    average_confidence: float
    high_confidence_count: int
    medium_confidence_count: int
    low_confidence_count: int
    expert_verified_count: int
    expert_agreement_rate: float
    expert_correction_rate: float

class TrendDataPoint(BaseModel):
    date: str
    scans: int
    diseases: int
    pests: int
    healthy: int

class DistributionItem(BaseModel):
    name: str
    count: int
    percentage: float

class AdminAnalyticsResponse(BaseModel):
    kpis: SystemKPIs
    model_metrics: ModelPerformanceMetrics
    daily_trends: List[TrendDataPoint] = []
    top_diseases: List[DistributionItem] = []
    top_pests: List[DistributionItem] = []
    crop_distribution: List[DistributionItem] = []
    severity_distribution: List[DistributionItem] = []
