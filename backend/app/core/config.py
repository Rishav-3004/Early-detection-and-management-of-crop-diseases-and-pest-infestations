from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    PROJECT_NAME: str = "Early Detection and Management of Crop Diseases and Pest Infestations"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    DEMO_MODE: bool = True

    # Security & JWT
    SECRET_KEY: str = "supersecretdevelopmentjwtkeythatmustbechangedinproduction123456789"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
    ]

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./crop_disease.db"
    # For PostgreSQL in Docker / Production: postgresql+asyncpg://postgres:postgres@localhost:5432/crop_db

    # Storage (local or s3)
    STORAGE_PROVIDER: str = "local"
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 15
    ALLOWED_IMAGE_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]

    # AI/ML Configuration
    MODEL_PROVIDER: str = "mock"
    MODEL_VERSION: str = "v1.2.0-agrishield"
    MODEL_PATH: str = ""
    HIGH_CONFIDENCE_THRESHOLD: float = 0.80
    MEDIUM_CONFIDENCE_THRESHOLD: float = 0.60

    # Weather Integration
    WEATHER_PROVIDER: str = "open-meteo"
    WEATHER_API_KEY: str = ""

    # Rate Limiting
    RATE_LIMIT_LOGIN_PER_MINUTE: int = 10
    RATE_LIMIT_SCANS_PER_MINUTE: int = 30


settings = Settings()
