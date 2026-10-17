import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Response
from typing import List, Dict, Any

from app.models.schemas import (
    ProjectInputRequest,
    RequirementAnalysisResponse,
    SRSResponse,
    UMLDiagramsResponse,
    DatabaseDesignResponse,
    FullArchitectureResponse,
    ExportRequest,
    ExportResponse,
)
from app.services import (
    RequirementAnalyzer,
    SRSGenerator,
    UMLGenerator,
    DatabaseDesigner,
)

router = APIRouter(prefix="/api", tags=["Architect Endpoints"])

@router.post("/analyze", response_model=RequirementAnalysisResponse)
async def analyze_requirements(request: ProjectInputRequest):
    """Analyze high-level user project idea and produce structured requirements."""
    try:
        return await RequirementAnalyzer.analyze(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze requirements: {str(e)}")

@router.post("/generate-srs", response_model=SRSResponse)
async def generate_srs(request: ProjectInputRequest):
    """Generate complete IEEE 830-style SRS document."""
    try:
        analysis = await RequirementAnalyzer.analyze(request)
        return await SRSGenerator.generate(request.title, request.description, analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate SRS: {str(e)}")

@router.post("/generate-uml", response_model=UMLDiagramsResponse)
async def generate_uml(request: ProjectInputRequest):
    """Generate 5 Mermaid UML diagrams."""
    try:
        analysis = await RequirementAnalyzer.analyze(request)
        return await UMLGenerator.generate(request.title, request.description, analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate UML diagrams: {str(e)}")

@router.post("/generate-db", response_model=DatabaseDesignResponse)
async def generate_database(request: ProjectInputRequest):
    """Generate normalized PostgreSQL schema and Mermaid ERD."""
    try:
        analysis = await RequirementAnalyzer.analyze(request)
        return await DatabaseDesigner.generate(request.title, request.description, analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Database design: {str(e)}")

@router.post("/generate-all", response_model=FullArchitectureResponse)
async def generate_full_architecture(request: ProjectInputRequest):
    """Transform project idea into full software architecture blueprint in one call."""
    try:
        analysis = await RequirementAnalyzer.analyze(request)
        srs = await SRSGenerator.generate(request.title, request.description, analysis)
        uml = await UMLGenerator.generate(request.title, request.description, analysis)
        db = await DatabaseDesigner.generate(request.title, request.description, analysis)

        return FullArchitectureResponse(
            project_title=request.title,
            generated_at=datetime.utcnow().isoformat(),
            analysis=analysis,
            srs=srs,
            uml_diagrams=uml,
            database_design=db
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate full architecture blueprint: {str(e)}")

@router.get("/samples")
async def get_sample_projects() -> List[Dict[str, Any]]:
    """Return pre-configured sample projects for instant testing."""
    return [
        {
            "id": "hospital-management",
            "title": "Hospital Management System",
            "domain": "Healthcare",
            "target_scale": "Enterprise",
            "tech_preferences": "FastAPI, React, PostgreSQL, Redis",
            "description": "A comprehensive hospital management platform handling patient electronic health records (EHR), outpatient doctor appointment scheduling, pharmacy inventory & drug dispensing, and billing with insurance claim management."
        },
        {
            "id": "ecommerce-marketplace",
            "title": "E-Commerce Multi-Vendor Marketplace",
            "domain": "E-Commerce & Retail",
            "target_scale": "Enterprise",
            "tech_preferences": "FastAPI, React, PostgreSQL, Stripe",
            "description": "A scalable multi-vendor e-commerce platform supporting product catalog indexing, shopping carts, secure checkout with Stripe, real-time inventory management, vendor commission tracking, and order fulfillment."
        },
        {
            "id": "ride-sharing-platform",
            "title": "Urban Ride-Sharing & Fleet Management",
            "domain": "Transportation & Logistics",
            "target_scale": "Enterprise",
            "tech_preferences": "FastAPI, React, PostgreSQL, WebSockets",
            "description": "On-demand ride hailing platform matching passengers with nearby verified drivers, real-time GPS telemetry tracking, dynamic surge pricing engine, and in-app automated fare settlement."
        }
    ]

@router.post("/export", response_model=ExportResponse)
async def export_blueprint(request: ExportRequest):
    """Export blueprint to desired format (Markdown, JSON, SQL)."""
    fmt = request.format.lower()
    title_slug = request.project_title.lower().replace(" ", "_")
    blueprint = request.blueprint

    if fmt == "sql":
        db_design = blueprint.get("database_design", {})
        sql_content = db_design.get("sql_schema", "-- No SQL schema available")
        return ExportResponse(
            filename=f"{title_slug}_schema.sql",
            mime_type="application/sql",
            content=sql_content
        )
    elif fmt == "json":
        return ExportResponse(
            filename=f"{title_slug}_blueprint.json",
            mime_type="application/json",
            content=json.dumps(blueprint, indent=2)
        )
    else:
        # Default to Markdown full export
        srs = blueprint.get("srs", {})
        md_text = srs.get("markdown_content", "")
        if not md_text:
            md_text = f"# Software Architecture Blueprint: {request.project_title}\n\nGenerated by AI Software Architect."
        return ExportResponse(
            filename=f"{title_slug}_srs_blueprint.md",
            mime_type="text/markdown",
            content=md_text
        )
