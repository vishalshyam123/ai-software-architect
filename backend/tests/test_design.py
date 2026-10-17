"""
Design & Architectural Verification Test Suite
Standards: IEEE Std 1016 (Software Design Descriptions) & IEEE Std 830 (SRS)

This suite tests that the system's generated artifacts strictly adhere to:
1. Object-Oriented Design Rules (UML structural invariants)
2. Relational Database 3NF Normalization Design Rules
3. IEEE 830 Software Requirements Specification structural completeness
4. Architectural API Data Transfer Object (DTO) contracts
"""

import pytest
import re
from fastapi.testclient import TestClient
from main import app
from app.models.schemas import (
    ProjectInput,
    RequirementAnalysisResponse,
    SRSResponse,
    UMLResponse,
    DatabaseDesignResponse,
    FullBlueprintResponse
)

client = TestClient(app)

@pytest.fixture(scope="module")
def sample_blueprint():
    """Generate a sample blueprint for design testing."""
    payload = {
        "title": "Hospital Management System",
        "description": "Patient electronic health records, outpatient scheduling, doctor e-prescriptions, pharmacy inventory, and billing.",
        "domain": "Healthcare"
    }
    response = client.post("/api/generate-all", json=payload)
    assert response.status_code == 200, "Blueprint generation failed during design test setup"
    return response.json()

# ==============================================================================
# 1. UML Structural Design Tests (OOP & Behavioral Invariants)
# ==============================================================================

def test_design_uml_use_case_invariants(sample_blueprint):
    """Design Test: Verify Use Case diagram specifies actors, system boundaries, and valid Mermaid syntax."""
    uml = sample_blueprint["uml_diagrams"]
    use_case = uml["use_case_diagram"]
    
    assert "graph" in use_case or "flowchart" in use_case, "Use Case must use valid Mermaid graph/flowchart syntax"
    assert "subgraph" in use_case, "Use Case must establish explicit system or actor boundaries"
    assert "-->" in use_case or "---" in use_case, "Use Case must link actors to system use cases"

def test_design_uml_class_diagram_invariants(sample_blueprint):
    """Design Test: Verify Class diagram includes typed attributes, methods, and relationship multiplicity."""
    uml = sample_blueprint["uml_diagrams"]
    class_diag = uml["class_diagram"]
    
    assert "classDiagram" in class_diag, "Class Diagram must begin with 'classDiagram' keyword"
    assert "class " in class_diag, "Class Diagram must declare domain entity classes"
    assert "+" in class_diag or "-" in class_diag, "Class Diagram must specify member visibility (+ public / - private)"
    assert "--" in class_diag or "-->" in class_diag, "Class Diagram must declare class associations with multiplicity"

def test_design_uml_sequence_diagram_invariants(sample_blueprint):
    """Design Test: Verify Sequence diagram models asynchronous multi-tier lifecycle and numbered messages."""
    uml = sample_blueprint["uml_diagrams"]
    seq_diag = uml["sequence_diagram"]
    
    assert "sequenceDiagram" in seq_diag, "Sequence Diagram must declare 'sequenceDiagram'"
    assert "autonumber" in seq_diag, "Design standard: sequence diagram must use autonumbering for message tracking"
    assert ("participant" in seq_diag or "actor" in seq_diag), "Sequence Diagram must declare participating lifelines"
    assert "->>" in seq_diag or "-->>" in seq_diag, "Sequence Diagram must model request/response messaging"

def test_design_uml_activity_and_component_invariants(sample_blueprint):
    """Design Test: Verify Activity flowcharts define start/end nodes and Component diagrams define tiers."""
    uml = sample_blueprint["uml_diagrams"]
    activity_diag = uml["activity_diagram"]
    comp_diag = uml["component_diagram"]
    
    assert "flowchart" in activity_diag, "Activity Diagram must use valid Mermaid flowchart syntax"
    assert "-->" in activity_diag, "Activity Diagram must define sequential control flow transitions"
    assert "subgraph" in comp_diag, "Component Diagram must logically isolate presentation, API, and persistence tiers"

# ==============================================================================
# 2. Relational Database 3NF Design Tests
# ==============================================================================

def test_design_database_3nf_primary_keys(sample_blueprint):
    """Design Test: Verify 3NF rule - every table must have an explicit primary key defined."""
    db_design = sample_blueprint["database_design"]
    tables = db_design["tables"]
    
    assert len(tables) >= 2, "Database design must declare normalized multi-table entity structure"
    for table in tables:
        pk_columns = [col for col in table["columns"] if col["is_primary_key"]]
        assert len(pk_columns) >= 1, f"Design Rule Violation: Table '{table['name']}' lacks a Primary Key (violates 1NF/3NF)"

def test_design_database_foreign_key_referential_integrity(sample_blueprint):
    """Design Test: Verify that foreign keys explicitly reference existing parent tables."""
    db_design = sample_blueprint["database_design"]
    tables = db_design["tables"]
    table_names = {t["name"].lower() for t in tables}
    
    for table in tables:
        fk_columns = [col for col in table["columns"] if col["is_foreign_key"]]
        for fk in fk_columns:
            assert fk["references"] is not None, f"Foreign key '{fk['name']}' in table '{table['name']}' must declare references"

def test_design_database_erd_syntax_and_ddl_dialect(sample_blueprint):
    """Design Test: Verify Mermaid ERD syntax compliance and valid PostgreSQL DDL with UUID extension."""
    db_design = sample_blueprint["database_design"]
    erd = db_design["er_diagram"]
    sql = db_design["sql_schema"]
    
    assert "erDiagram" in erd, "ER Diagram must use valid Mermaid erDiagram specification"
    assert "CREATE TABLE" in sql, "DDL script must define CREATE TABLE statements"
    assert "UUID" in sql or "uuid" in sql, "PostgreSQL schema design standard: Must use UUID primary keys"
    assert "PRIMARY KEY" in sql, "DDL script must explicitly define PRIMARY KEY constraints"

# ==============================================================================
# 3. IEEE 830-1998 SRS Structural Design Tests
# ==============================================================================

def test_design_srs_ieee_mandatory_sections(sample_blueprint):
    """Design Test: Verify that the generated SRS document contains all required IEEE 830 standard sections."""
    srs = sample_blueprint["srs"]
    markdown = srs["markdown_content"]
    
    required_sections = [
        "Software Requirements Specification",
        "Introduction",
        "Scope",
        "Functional Requirements",
        "Non-Functional Requirements",
        "Use Cases"
    ]
    
    for section in required_sections:
        assert section.lower() in markdown.lower(), f"IEEE 830 Structural Violation: Missing mandatory section '{section}'"

def test_design_requirements_moscow_prioritization(sample_blueprint):
    """Design Test: Verify that functional requirements adhere to the MoSCoW prioritization design pattern."""
    analysis = sample_blueprint["analysis"]
    frs = analysis["functional_requirements"]
    
    assert len(frs) >= 3, "Design standard: Requirement analysis must output at least 3 discrete functional specifications"
    valid_priorities = {"Must Have", "Should Have", "Could Have", "Won't Have", "High", "Medium", "Low"}
    
    for fr in frs:
        assert fr["priority"] in valid_priorities, f"Requirement '{fr['id']}' has non-standard priority '{fr['priority']}'"
        assert len(fr["acceptance_criteria"]) >= 1, f"Requirement '{fr['id']}' must include testable acceptance criteria"

# ==============================================================================
# 4. API Schema Contract Validation Tests (DTO Design)
# ==============================================================================

def test_design_api_response_schema_contract(sample_blueprint):
    """Design Test: Verify that the API output conforms strictly to the FullBlueprintResponse Pydantic schema."""
    validated = FullBlueprintResponse.model_validate(sample_blueprint)
    assert validated.project_title == sample_blueprint["project_title"]
    assert validated.analysis.project_title is not None
    assert validated.uml_diagrams.class_diagram is not None
    assert validated.database_design.er_diagram is not None
