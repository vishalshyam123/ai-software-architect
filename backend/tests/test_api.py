import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to AI Software Architect API"

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_samples():
    response = client.get("/api/samples")
    assert response.status_code == 200
    samples = response.json()
    assert len(samples) >= 3
    assert any(s["title"] == "Hospital Management System" for s in samples)

def test_analyze():
    payload = {
        "title": "Hospital Management System",
        "description": "Patient records, appointments, doctor consultation, pharmacy and billing.",
        "domain": "Healthcare"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["project_title"] == "Hospital Management System"
    assert len(data["actors"]) > 0
    assert len(data["functional_requirements"]) > 0

def test_generate_all():
    payload = {
        "title": "Hospital Management System",
        "description": "Patient records, appointments, doctor consultation, pharmacy and billing.",
        "domain": "Healthcare"
    }
    response = client.post("/api/generate-all", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert "srs" in data
    assert "uml_diagrams" in data
    assert "database_design" in data
    assert "use_case_diagram" in data["uml_diagrams"]
    assert "sql_schema" in data["database_design"]
