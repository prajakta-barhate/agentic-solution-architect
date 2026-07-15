from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import get_db
from config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Bootstrap backend for the Agentic Solution Architect platform",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
)


@app.get("/health")
async def health_check() -> dict[str, str | bool]:
    return {
        "status": "healthy",
        "environment": settings.environment,
        "debug": settings.debug,
    }


@app.get("/health/db")
async def health_db(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database connection failed") from exc

    return {"status": "healthy", "database": "connected"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Backend is running"}