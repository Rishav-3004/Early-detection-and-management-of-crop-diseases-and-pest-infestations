# Database Schema & Entity Relationships

The platform uses SQLAlchemy 2.0 Async ORM with complete migrations, compatible with PostgreSQL and SQLite.

## Entity Relationship Diagram

```text
  ┌──────────────┐          1..*  ┌──────────────┐          1..*  ┌──────────────┐
  │    Users     │───────────────<│    Farms     │───────────────<│    Fields    │
  └──────────────┘                └──────────────┘                └──────┬───────┘
         │                                                               │
         │ 1..*                                                          │ 1..*
         ▼                                                               ▼
  ┌──────────────┐          1..*  ┌───────────────────┐           ┌──────────────┐
  │  Detections  │───────────────<│ DetectionResults  │           │    Crops     │
  └──────┬───────┘                │ (Multi-Candidate) │           └──────┬───────┘
         │                        └───────────────────┘                  │
         │ 1..1                                                          │ 1..*
         ▼                                                               ▼
  ┌──────────────┐                                                ┌──────────────┐
  │ExpertReviews │                                                │ Diseases /   │
  └──────────────┘                                                │    Pests     │
                                                                  └──────────────┘
```

## Schema Entities

1. **`users`**: User identity, role (`FARMER`, `EXPERT`, `ADMIN`), language preference, password hash.
2. **`farms`**: Agricultural property, geolocation coordinates (`latitude`, `longitude`), total area, soil type, irrigation system.
3. **`fields`**: Specific crop sector within a farm, crop foreign key, variety name, planting date, growth stage, dynamic health score (0–100).
4. **`crops`**: Supported botanical crop types (e.g. Tomato, Potato, Wheat, Rice, Maize, Cotton, Apple) with growth stage arrays and common stresses.
5. **`diseases`**: Scientific taxonomy, symptom descriptions, causes, risk factors, severity tiers, prevention methods, management strategies.
6. **`pests`**: Insect classification, damage descriptions, symptoms, lifecycle factors, and biological controls.
7. **`detections`**: AI vision diagnosis log including original image URL, predicted label, confidence (0.0–1.0), severity, affected area %, multi-factor risk score & level, model version, and expert verification flag.
8. **`detection_results`**: Ranked differential diagnostic candidates (Rank 1, Rank 2, Rank 3).
9. **`expert_reviews`**: Verified diagnosis, corrected confidence, expert severity, clinical notes, and custom prescription issued by an agronomist.
10. **`notifications`**: In-app alert messages for high-risk outbreaks and expert review completions.
11. **`weather_records`**: Cached meteorological telemetry for microclimate risk calculations.
