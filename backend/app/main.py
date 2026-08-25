import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.config import settings
from app.core.logging import setup_logging, logger
from app.core.database import engine, Base
from app.core.exceptions import AppException
from app.core.response import error_response
from app.api.router import api_router

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.PROJECT_NAME} in [{settings.ENVIRONMENT}] mode...")
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    # Initialize database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database schema initialized successfully.")

    yield

    logger.info("Shutting down application...")
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Early Detection and Management of Crop Diseases and Pest Infestations Platform API",
    version="1.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.DEBUG else settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded static files
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include API v1 Router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# --- Global Exception Handlers ---
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            code=exc.code,
            message=exc.message,
            details=exc.details
        )
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in err["loc"]),
            "message": err["msg"]
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            code="VALIDATION_ERROR",
            message="Request validation failed",
            details={"errors": errors}
        )
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled server error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected server error occurred. Please try again later.",
            details={"type": type(exc).__name__} if settings.DEBUG else {}
        )
    )

@app.get("/api/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "demo_mode": settings.DEMO_MODE,
        "model_version": settings.MODEL_VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
