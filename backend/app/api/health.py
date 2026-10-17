from fastapi import APIRouter
from datetime import datetime
from app.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    ai_status = "OpenAI API (Configured)" if settings.OPENAI_API_KEY else "Intelligent Heuristic Architecture Engine (Active)"
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "ai_engine": ai_status,
        "model": settings.OPENAI_MODEL,
        "timestamp": datetime.utcnow().isoformat()
    }
