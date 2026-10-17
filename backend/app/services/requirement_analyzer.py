from typing import Dict, Any
from app.models.schemas import ProjectInputRequest, RequirementAnalysisResponse
from app.services.ai_service import ai_service

class RequirementAnalyzer:
    @staticmethod
    async def analyze(request: ProjectInputRequest) -> RequirementAnalysisResponse:
        data = await ai_service.analyze_requirements(
            title=request.title,
            description=request.description,
            domain=request.domain or "Enterprise"
        )
        return RequirementAnalysisResponse(**data)
