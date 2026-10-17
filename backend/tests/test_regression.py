"""
Regression Test Suite for AI Software Architect
Verifies that previously implemented domain blueprints, edge cases,
and fallback heuristic outputs remain stable across versions.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

REGRESSION_CASES = [
    {
        "domain_name": "Healthcare / Hospital Management",
        "payload": {
            "title": "Hospital Management System",
            "description": "Patient EHR records, outpatient appointment scheduling, clinical diagnoses, pharmacy inventory, and billing.",
            "domain": "Healthcare"
        },
        "expected_actors": ["Patient", "Physician", "Hospital Administrator"],
        "expected_tables": ["users", "patients", "appointments"]
    },
    {
        "domain_name": "EdTech / Learning Management System",
        "payload": {
            "title": "Learning Management System (LMS)",
            "description": "Interactive course curriculum, video lecture streaming, student enrollment, assignment submissions, automated grading.",
            "domain": "Education"
        },
        "expected_actors": ["Student", "Instructor"],
        "expected_tables": ["users", "students", "courses"]
    },
    {
        "domain_name": "E-Commerce Retail",
        "payload": {
            "title": "E-Commerce Marketplace",
            "description": "Multi-vendor product catalog, shopping cart, Stripe payment checkout, and courier shipment tracking.",
            "domain": "E-Commerce"
        },
        "expected_actors": ["Customer", "Merchant"],
        "expected_tables": ["products", "orders"]
    },
    {
        "domain_name": "Custom Domain (Drone Logistics)",
        "payload": {
            "title": "Autonomous Drone Fleet Delivery",
            "description": "Dispatch automated delivery drones, track GPS waypoints, monitor battery telemetry, and manage parcel drops.",
            "domain": "Logistics"
        },
        "expected_actors": ["Member", "Administrator"],
        "expected_tables": ["users"]
    }
]

@pytest.mark.parametrize("case", REGRESSION_CASES)
def test_regression_domain_blueprints(case):
    """Regression test: verify all domains generate valid, complete blueprints without crashing."""
    response = client.post("/api/generate-all", json=case["payload"])
    assert response.status_code == 200, f"Failed regression on {case['domain_name']}"
    
    data = response.json()
    
    # 1. Verification of Requirements Analysis
    assert "analysis" in data
    analysis = data["analysis"]
    assert len(analysis["actors"]) >= 2
    assert len(analysis["functional_requirements"]) >= 3
    assert len(analysis["non_functional_requirements"]) >= 3
    
    # 2. Verification of IEEE SRS Document
    assert "srs" in data
    srs_text = data["srs"]["markdown_content"]
    assert "Software Requirements Specification" in srs_text
    assert "Functional Requirements" in srs_text
    
    # 3. Verification of 5 UML Diagrams
    assert "uml_diagrams" in data
    uml = data["uml_diagrams"]
    for diag in ["use_case_diagram", "class_diagram", "sequence_diagram", "activity_diagram", "component_diagram"]:
        assert diag in uml
        assert len(uml[diag].strip()) > 20
        
    # 4. Verification of Normalized Database Design
    assert "database_design" in data
    db = data["database_design"]
    assert "er_diagram" in db
    assert "sql_schema" in db
    assert len(db["tables"]) >= 2

def test_regression_empty_description_fallback():
    """Regression test: verify the system gracefully handles minimalist inputs."""
    payload = {
        "title": "Library Management",
        "description": "Book catalog and borrowing system.",
        "domain": "General"
    }
    response = client.post("/api/generate-all", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["project_title"] == "Library Management"
    assert "classDiagram" in data["uml_diagrams"]["class_diagram"]
