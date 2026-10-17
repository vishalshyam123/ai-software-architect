# Comprehensive Testing, System Building & Project Documentation Guide 📸🧪

This document provides step-by-step instructions for running tests, managing versions, building the system, capturing screenshots, and documenting the **AI Software Architect** project.

---

## Part 1: Integration, Regression, and Mutation Testing

### 1.1 Integration Testing
**Definition**: Verifies that independent modules (FastAPI routers, Pydantic schemas, business logic, and database/mock services) communicate and function together seamlessly over HTTP.

#### How to Run:
Open a terminal in the project directory:

```bash
# Option A: If running via Docker Compose
docker compose exec backend pytest -v tests/test_api.py

# Option B: If running locally inside backend/venv
cd backend
pytest -v tests/test_api.py
```

#### What it Tests:
1. `test_root`: Root route `/` returns status 200 and API metadata.
2. `test_health`: `/api/health` reports status `healthy` and engine readiness.
3. `test_samples`: `/api/samples` returns pre-configured architectural presets.
4. `test_analyze`: `/api/analyze` parses inputs and returns actors, stakeholders, and requirements.
5. `test_generate_all`: `/api/generate-all` returns a complete blueprint with Requirements, SRS, 5 UML diagrams, and 3NF database schema.

#### 📸 Screenshot to Capture:
- Capture the terminal output showing `5 passed in X.XXs` with green `PASSED` tags next to each test case.
- Caption: *"Figure 1: Automated Integration Test Execution Suite (pytest) verifying end-to-end API and architectural generator pipelines."*

---

### 1.2 Regression Testing
**Definition**: Verifies that new code modifications, optimizations, or prompt adjustments do not break existing domain models (e.g. Healthcare, EdTech, E-Commerce, or custom domains).

#### How to Run:
```bash
# Option A: Via Docker Compose
docker compose exec backend pytest -v tests/test_regression.py

# Option B: Locally
pytest -v tests/test_regression.py
```

#### What it Tests:
1. `test_regression_domain_blueprints[case0 - Healthcare]`: Validates patient, physician, and appointment flows.
2. `test_regression_domain_blueprints[case1 - Education]`: Validates LMS course, student enrollment, and grading schemas.
3. `test_regression_domain_blueprints[case2 - E-Commerce]`: Validates vendor catalog, customer checkout, and orders.
4. `test_regression_domain_blueprints[case3 - Logistics]`: Validates drone telemetry, waypoints, and fleet dispatch.
5. `test_regression_empty_description_fallback`: Validates system resilience against sparse user inputs.

#### 📸 Screenshot to Capture:
- Capture the terminal output showing all parameterized test cases running and passing.
- Caption: *"Figure 2: Automated Regression Testing across multi-tenant domain models ensuring backwards compatibility."*

---

### 1.3 Mutation Testing
**Definition**: An advanced fault-injection testing technique. Artificial faults ("mutants", such as swapping `>` for `>=`, changing conditional statements, or altering return types) are injected into the source code (`ai_service.py`). If the test suite fails on a mutant, the mutant is **killed** (good). If the test suite still passes, the mutant **survived** (indicates test gaps).

#### How to Run Mutation Testing using `mutmut`:
```bash
# 1. Install mutmut inside your backend environment
pip install mutmut

# 2. Run mutation testing against the AI service
cd backend
mutmut run --paths-to-mutate=app/services/ai_service.py --tests-dir=tests/

# 3. View mutation test results summary
mutmut results

# 4. View detailed report of killed vs survived mutants
mutmut show 1
```

#### Alternative: Running Pytest with Code Coverage (Test Quality Proof):
If `mutmut` is not pre-installed, you can demonstrate comprehensive test coverage:
```bash
pytest --cov=app --cov-report=term-missing tests/
```

#### 📸 Screenshot to Capture:
- Terminal showing `mutmut results` (displaying total mutants generated, killed, and score) OR `pytest --cov` showing high code coverage across application modules.
- Caption: *"Figure 3: Mutation Testing and Fault-Tolerance Analysis proving test suite effectiveness."*

---

## Part 2: Version Management and System Building

### 2.1 Version Management (Git & GitHub Flow)
The project adheres strictly to **GitHub Flow**, where the `main` branch holds production releases and new features are developed in isolated feature branches (`feature/requirement-analyzer`, `feature/uml-generator`).

#### Commands to Run & Screenshot:
Open your terminal in the root directory:

```bash
# 1. Show current branch and working directory clean state
git status

# 2. Show branch listing (local and remote)
git branch -a

# 3. Show commit history graph with contributors and messages
git log --graph --oneline --decorate -n 12
```

#### 📸 Screenshots to Capture:
1. **Terminal Git History**: Screenshot showing `git log --graph --oneline` with commit hashes and descriptive messages by authors.
2. **GitHub Repository UI**:
   - The main repository page showing README badges and folder structure.
   - The **Branches** tab showing `main` and `feature/...`.
   - The **Commits** tab showing commit history.
- Caption: *"Figure 4: Git Version Control Workflow showing branch hierarchy, linear commit history, and GitHub Flow integration."*

---

### 2.2 System Building & Containerization

The system uses a containerized multi-tier architecture orchestrated via Docker Compose:
- **`ai_architect_frontend`**: React 18, Vite, Tailwind CSS, Nginx reverse proxy (Port 3000).
- **`ai_architect_backend`**: FastAPI, Python 3.11, Uvicorn ASGI server (Port 8000).
- **`ai_architect_db`**: PostgreSQL 16 relational database with persistent storage (Port 5432).

#### Commands to Run & Screenshot:
```bash
# 1. Build and boot all containers
docker compose up --build

# 2. Check running container status and port mappings
docker compose ps

# 3. Frontend Production Build (if building standalone)
cd frontend
npm run build
```

#### 📸 Screenshots to Capture:
1. **Docker Build Process**: Terminal showing `docker compose up --build` with Docker creating images and starting services.
2. **Docker Desktop Dashboard**: Open the Docker Desktop application and screenshot the `ai-software-architect` container group showing all 3 containers green (`Running`).
3. **Frontend Production Build**: Terminal output of `npm run build` showing compiled assets in `dist/`.
- Caption: *"Figure 5: Multi-container System Building via Docker Compose and production asset bundling."*

---

## Part 3: Developed Functionalities (UI & API Walkthrough)

Open your web browser at **`http://localhost:3000`** and take high-resolution screenshots of each feature:

| # | Screen / Feature | What to Show on Screen | Caption for Report |
|---|---|---|---|
| **3.1** | **Project Intake Console** | The main landing page with title input, description textarea, domain dropdown, and pre-set chips (e.g. *Hospital Management System*, *LMS*, *E-Commerce*). | *"Figure 6: Project Intake Console enabling custom idea entry and domain classification."* |
| **3.2** | **Generation in Progress** | Click **"Generate Complete Blueprint"** and capture the animated loading state with status badge. | *"Figure 7: Real-time asynchronous blueprint generation in progress."* |
| **3.3** | **Requirements Analysis Tab** | Executive summary, Identified Actors (Primary, Secondary, System), Stakeholders Matrix, and MoSCoW-prioritized Functional & Non-Functional requirements. | *"Figure 8: Automated Requirements Engineering and Stakeholder Analysis."* |
| **3.4** | **IEEE 830 SRS Document Tab** | Fully rendered Markdown IEEE 830-1998 Software Requirements Specification with Scope, Use Cases, Constraints, and the **"Download SRS (.md)"** button. | *"Figure 9: IEEE 830-compliant Software Requirements Specification viewer and export engine."* |
| **3.5** | **UML Diagrams - Use Case Diagram** | Click the **UML Diagrams** tab and select **Use Case Diagram**. Shows actors interacting with system boundaries rendered via Mermaid.js with zoom/pan controls. | *"Figure 10: Interactive Mermaid.js Use Case Diagram with zoom and pan controls."* |
| **3.6** | **UML Diagrams - Class Diagram** | Select **Class Diagram**. Shows object-oriented classes with attributes, data types, method signatures, and multiplicity associations. | *"Figure 11: High-fidelity UML Class Diagram with typed properties and method contracts."* |
| **3.7** | **UML Diagrams - Sequence Diagram** | Select **Sequence Diagram**. Shows asynchronous request lifecycle between Client, Web SPA, API Gateway, DB, and Workers. | *"Figure 12: System Sequence Diagram depicting end-to-end HTTP and transactional flows."* |
| **3.8** | **UML Diagrams - Activity & Component** | Switch to **Activity Diagram** (business logic flowchart) or **Component Diagram** (tiered system architecture). | *"Figure 13: Architectural Component Diagram illustrating 3-tier container boundaries."* |
| **3.9** | **Database Architecture & ERD** | Click the **Database Design** tab. Shows visual Mermaid ER diagram, interactive table column inspector, and the complete 3NF PostgreSQL DDL script with SQL copy button. | *"Figure 14: Normalized 3NF PostgreSQL Schema, ERD, and DDL script generator."* |
| **3.10** | **FastAPI Interactive Docs (Swagger UI)** | Navigate to **`http://localhost:8000/docs`**. Shows interactive REST API endpoints (`/api/analyze`, `/api/generate-all`, `/api/health`). | *"Figure 15: OpenAPI / Swagger interactive API documentation."* |

---

## Part 4: Tools and Technologies Used

| Category | Technology | Version | Purpose in AI Software Architect |
|---|---|---|---|
| **Frontend Framework** | **React.js** | 18.3.x | Component-based single-page application (SPA) user interface. |
| **Build Tool** | **Vite** | 5.3.x | Fast frontend bundler and local development server with Hot Module Replacement (HMR). |
| **Styling & Icons** | **Tailwind CSS & Lucide Icons** | 3.4.x / 0.395.x | Responsive utility-first modern design system and clean architectural iconography. |
| **Diagram Engine** | **Mermaid.js** | 10.9.x | Client-side declarative rendering of Use Case, Class, Sequence, Activity, and ER diagrams. |
| **Backend Framework** | **FastAPI** | 0.111.0 | High-performance asynchronous Python REST API framework with native OpenAPI/Swagger docs. |
| **ASGI Web Server** | **Uvicorn** | 0.30.x | Lightning-fast asynchronous server gateway for running FastAPI. |
| **Data Validation** | **Pydantic** | 2.7.x | Strict type hints, request/response schema validation, and serialization. |
| **AI / Heuristic Engine** | **AsyncOpenAI & Heuristic Synthesizer** | 1.30.x / Custom | Dual-mode engine: Generates designs via OpenAI GPT models when key is set, or via offline semantic rule engine without an API key. |
| **Database** | **PostgreSQL** | 16-alpine | Enterprise relational database for storing normalized project schemas, users, and artifacts. |
| **Database Driver** | **psycopg2 & SQLAlchemy** | 2.9.x / 2.0.x | Relational connection pooling and SQL dialect abstractions. |
| **Containerization** | **Docker & Docker Compose** | v2+ | Multi-container orchestration, zero-configuration local deployment, and environment isolation. |
| **Web Server / Proxy** | **Nginx** | 1.27-alpine | High-efficiency reverse proxy forwarding `/api` calls from frontend to backend container. |
| **Testing Framework** | **pytest & HTTPX** | 8.2.x / 0.27.x | Asynchronous integration and regression test execution suites. |
| **Mutation Testing** | **mutmut** | 2.4.x | Fault-injection mutation testing to evaluate test harness robustness. |
| **Version Control** | **Git & GitHub** | 2.x | Distributed version control following the GitHub Flow branching strategy. |
