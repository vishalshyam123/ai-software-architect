from typing import Dict, Any
from app.models.schemas import DatabaseDesignResponse, RequirementAnalysisResponse
from app.services.ai_service import ai_service

class DatabaseDesigner:
    @staticmethod
    async def generate(title: str, description: str, analysis: RequirementAnalysisResponse) -> DatabaseDesignResponse:
        data = await ai_service.generate_database_design(
            title=title,
            description=description,
            analysis=analysis.model_dump()
        )
        return DatabaseDesignResponse(**data)
