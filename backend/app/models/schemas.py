from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Request Model
class ProjectInputRequest(BaseModel):
    title: str = Field(..., description="Project Title or System Name", example="Hospital Management System")
    description: str = Field(..., description="Detailed description of the project requirements and goals", example="A comprehensive system to manage patient records, doctor appointments, medical billing, pharmacy inventory, and emergency admissions.")
    domain: Optional[str] = Field("Healthcare", description="Domain or industry (e.g., Healthcare, E-Commerce, FinTech, Logistics, EdTech)")
    target_scale: Optional[str] = Field("Startup / Medium", description="Expected scale (e.g. MVP, Startup / Medium, Enterprise)")
    tech_preferences: Optional[str] = Field("FastAPI, React, PostgreSQL", description="Optional architectural preferences")

# Requirement Analysis Models
class Actor(BaseModel):
    name: str
    type: str = Field(..., description="Primary, Secondary, or System")
    description: str

class Stakeholder(BaseModel):
    name: str
    interest: str
    impact: str

class FunctionalRequirement(BaseModel):
    id: str
    category: str
    title: str
    description: str
    priority: str = Field(..., description="Must Have, Should Have, Could Have")
    acceptance_criteria: List[str]

class NonFunctionalRequirement(BaseModel):
    category: str = Field(..., description="Performance, Security, Scalability, Reliability, Usability, Compliance")
    metric: str
    target: str

class ScopeDefinition(BaseModel):
    in_scope: List[str]
    out_of_scope: List[str]

class RequirementAnalysisResponse(BaseModel):
    project_title: str
    summary: str
    domain: str
    actors: List[Actor]
    stakeholders: List[Stakeholder]
    functional_requirements: List[FunctionalRequirement]
    non_functional_requirements: List[NonFunctionalRequirement]
    scope: ScopeDefinition

# Software Requirement Specification (SRS) Models
class UseCaseItem(BaseModel):
    id: str
    title: str
    actor: str
    trigger: str
    preconditions: str
    main_flow: List[str]
    alternative_flow: List[str]
    postconditions: str

class SRSResponse(BaseModel):
    project_title: str
    version: str = "1.0.0"
    introduction: str
    scope: str
    objectives: List[str]
    functional_requirements: List[FunctionalRequirement]
    non_functional_requirements: List[NonFunctionalRequirement]
    use_cases: List[UseCaseItem]
    constraints: List[str]
    assumptions: List[str]
    markdown_content: str

# UML Diagrams Models
class UMLDiagramsResponse(BaseModel):
    project_title: str
    use_case_diagram: str
    class_diagram: str
    sequence_diagram: str
    activity_diagram: str
    component_diagram: str

# Database Design Models
class DatabaseColumn(BaseModel):
    name: str
    data_type: str
    is_primary_key: bool = False
    is_foreign_key: bool = False
    references: Optional[str] = None
    is_nullable: bool = False
    description: str

class DatabaseTable(BaseModel):
    name: str
    description: str
    columns: List[DatabaseColumn]

class DatabaseRelationship(BaseModel):
    from_table: str
    to_table: str
    relationship_type: str = Field(..., description="one-to-one, one-to-many, many-to-many")
    description: str

class DatabaseDesignResponse(BaseModel):
    project_title: str
    er_diagram: str
    sql_schema: str
    tables: List[DatabaseTable]
    relationships: List[DatabaseRelationship]

# Full Blueprint Response
class FullArchitectureResponse(BaseModel):
    project_title: str
    generated_at: str
    analysis: RequirementAnalysisResponse
    srs: SRSResponse
    uml_diagrams: UMLDiagramsResponse
    database_design: DatabaseDesignResponse

# Export Models
class ExportRequest(BaseModel):
    project_title: str
    format: str = Field("markdown", description="markdown, json, sql, or bundle")
    blueprint: Dict[str, Any]

class ExportResponse(BaseModel):
    filename: str
    mime_type: str
    content: str
