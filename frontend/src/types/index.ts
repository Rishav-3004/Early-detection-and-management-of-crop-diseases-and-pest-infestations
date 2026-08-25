export type UserRole = 'FARMER' | 'EXPERT' | 'ADMIN';

export interface User {
  id: string;
  name: string;
  email: string;
  phone?: string;
  role: UserRole;
  language: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user_id: string;
  name: string;
  email: string;
  role: UserRole;
  language: string;
}

export interface Crop {
  id: string;
  name: string;
  scientific_name?: string;
  description?: string;
  growth_stages: string[];
  common_diseases: string[];
  common_pests: string[];
}

export interface Field {
  id: string;
  farm_id: string;
  name: string;
  area: number;
  crop_id?: string;
  variety?: string;
  planting_date?: string;
  growth_stage?: string;
  health_score: number;
  crop?: Crop;
  created_at: string;
  updated_at: string;
}

export interface Farm {
  id: string;
  owner_id: string;
  name: string;
  location: string;
  latitude?: number;
  longitude?: number;
  area: number;
  soil_type: string;
  irrigation_type: string;
  fields: Field[];
  created_at: string;
  updated_at: string;
}

export interface Disease {
  id: string;
  crop_id: string;
  name: string;
  scientific_name?: string;
  description: string;
  symptoms: string[];
  causes: string[];
  risk_factors: string[];
  severity_levels: Record<string, string>;
  prevention: string[];
  management: string[];
  image_examples: string[];
  crop?: Crop;
}

export interface Pest {
  id: string;
  crop_id: string;
  name: string;
  scientific_name?: string;
  description: string;
  symptoms: string[];
  damage_description?: string;
  risk_factors: string[];
  prevention: string[];
  management: string[];
  image_examples: string[];
  crop?: Crop;
}

export interface DetectionResultCandidate {
  id: string;
  label: string;
  confidence: number;
  rank: number;
}

export interface StructuredRecommendation {
  immediate_actions: string[];
  management: string[];
  prevention: string[];
  monitoring: string[];
  expert_review_advice: string;
  disclaimer: string;
}

export interface ExpertReview {
  id: string;
  detection_id: string;
  expert_id?: string;
  expert_name?: string;
  verified_label: string;
  corrected_confidence?: number;
  severity: string;
  is_correct_prediction: boolean;
  notes: string;
  recommendation: string;
  status: string;
  created_at: string;
}

export interface Detection {
  id: string;
  user_id: string;
  farm_id?: string;
  field_id?: string;
  crop_id?: string;
  image_url: string;
  original_filename?: string;
  detection_type: 'DISEASE' | 'PEST' | 'HEALTHY' | 'UNKNOWN';
  predicted_label: string;
  scientific_name?: string;
  confidence: number;
  severity: 'NONE' | 'LOW' | 'MODERATE' | 'HIGH' | 'CRITICAL';
  affected_area_percentage?: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  risk_score: number;
  risk_reasons: string[];
  model_version: string;
  status: string;
  expert_verified: boolean;
  is_demo: boolean;
  created_at: string;
  results: DetectionResultCandidate[];
  expert_review?: ExpertReview;
  symptoms?: string[];
  causes?: string[];
  recommendations?: StructuredRecommendation;
  farm_name?: string;
  field_name?: string;
  crop_name?: string;
}

export interface NotificationItem {
  id: string;
  user_id: string;
  type: string;
  title: string;
  message: string;
  priority: string;
  link?: string;
  is_read: boolean;
  created_at: string;
}

export interface WeatherCurrent {
  temperature: number;
  humidity: number;
  rainfall: number;
  wind_speed: number;
  weather_condition: string;
  recorded_at: string;
  risk_assessment: string;
  high_disease_risk_warning: boolean;
}

export interface WeatherForecastDay {
  date: string;
  temp_max: number;
  temp_min: number;
  humidity: number;
  rainfall: number;
  condition: string;
  disease_favorable: boolean;
}

export interface WeatherForecast {
  current: WeatherCurrent;
  forecast: WeatherForecastDay[];
}

export interface SystemKPIs {
  total_users: number;
  total_farmers: number;
  total_experts: number;
  total_farms: number;
  total_fields: number;
  total_scans: number;
  total_diseases_detected: number;
  total_pests_detected: number;
  total_healthy_scans: number;
  pending_expert_reviews: number;
  completed_expert_reviews: number;
}

export interface ModelPerformanceMetrics {
  model_version: string;
  total_predictions: number;
  average_confidence: number;
  high_confidence_count: number;
  medium_confidence_count: number;
  low_confidence_count: number;
  expert_verified_count: number;
  expert_agreement_rate: number;
  expert_correction_rate: number;
}

export interface TrendDataPoint {
  date: string;
  scans: number;
  diseases: number;
  pests: number;
  healthy: number;
}

export interface DistributionItem {
  name: string;
  count: number;
  percentage: number;
}

export interface AdminAnalytics {
  kpis: SystemKPIs;
  model_metrics: ModelPerformanceMetrics;
  daily_trends: TrendDataPoint[];
  top_diseases: DistributionItem[];
  top_pests: DistributionItem[];
  crop_distribution: DistributionItem[];
  severity_distribution: DistributionItem[];
}
