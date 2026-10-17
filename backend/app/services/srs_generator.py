from typing import Dict, Any
from app.models.schemas import SRSResponse, RequirementAnalysisResponse
from app.services.ai_service import ai_service

class SRSGenerator:
    @staticmethod
    async def generate(title: str, description: str, analysis: RequirementAnalysisResponse) -> SRSResponse:
        data = await ai_service.generate_srs(
            title=title,
            description=description,
            analysis=analysis.model_dump()
        )
        return SRSResponse(**data)
