# AI Software Architect - REST API Specification

Base URL: `http://localhost:8000/api`

---

## 1. Health Check
- **Endpoint**: `GET /api/health`
- **Response**:
```json
{
  "status": "healthy",
  "service": "AI Software Architect",
  "environment": "production",
  "ai_engine": "Intelligent Heuristic Architecture Engine (Active)",
  "model": "gpt-4o-mini",
  "timestamp": "2026-10-15T12:00:00.000000"
}
```

---

## 2. Sample Projects
- **Endpoint**: `GET /api/samples`
- **Description**: Returns pre-configured architectural examples (Hospital Management System, E-Commerce, Ride-Sharing).

---

## 3. Generate Full Architecture Blueprint
- **Endpoint**: `POST /api/generate-all`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
```json
{
  "title": "Hospital Management System",
  "description": "A comprehensive hospital management platform handling patient electronic health records (EHR), outpatient doctor appointment scheduling, pharmacy inventory & drug dispensing, and billing with insurance claim management.",
  "domain": "Healthcare",
  "target_scale": "Enterprise Scale"
}
```
- **Response**: Full `FullArchitectureResponse` containing:
  - `analysis`: Actors, Stakeholders, Functional & Non-Functional requirements, Scope
  - `srs`: IEEE 830 compliant markdown document, objectives, constraints, use cases
  - `uml_diagrams`: 5 Mermaid diagrams (`use_case_diagram`, `class_diagram`, `sequence_diagram`, `activity_diagram`, `component_diagram`)
  - `database_design`: Mermaid `er_diagram`, PostgreSQL DDL `sql_schema`, table dictionaries

---

## 4. Decomposed Generation Endpoints
For modular invocation, the following endpoints are available:
- `POST /api/analyze` - Requirements decomposition
- `POST /api/generate-srs` - IEEE 830 SRS document generator
- `POST /api/generate-uml` - Mermaid UML diagram generator
- `POST /api/generate-db` - PostgreSQL DDL and Mermaid ERD generator
- `POST /api/export` - Export blueprint as `.md`, `.json`, or `.sql` file
