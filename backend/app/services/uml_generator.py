from typing import Dict, Any
from app.models.schemas import UMLDiagramsResponse, RequirementAnalysisResponse
from app.services.ai_service import ai_service

class UMLGenerator:
    @staticmethod
    async def generate(title: str, description: str, analysis: RequirementAnalysisResponse) -> UMLDiagramsResponse:
        data = await ai_service.generate_uml(
            title=title,
            description=description,
            analysis=analysis.model_dump()
        )
        return UMLDiagramsResponse(**data)
