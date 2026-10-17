# AI Software Architect 🏗️⚡

> Transform a simple project idea into a complete, production-ready software development blueprint within minutes.

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](docs/DOCKER_GUIDE.md)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Mermaid](https://img.shields.io/badge/Diagrams-Mermaid.js-ff3670?logo=mermaid&logoColor=white)](https://mermaid.js.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 Overview

**AI Software Architect** follows the workflow of an experienced Principal Software Architect. Instead of jumping straight into raw code generation, it methodically decomposes your project idea into:
1. **Requirements Analysis**: Identified Actors, Stakeholders, MoSCoW-prioritized Functional Requirements, and Non-Functional Quality Attributes.
2. **Software Requirements Specification (SRS)**: Complete IEEE Std 830-1998 compliant document ready for teams and stakeholders.
3. **5 Interactive UML Diagrams**: Use Case, Class, Sequence, Activity, and Component diagrams rendered via Mermaid.js.
4. **PostgreSQL Relational Schema & ERD**: 3NF normalized database schema, UUID primary keys, foreign key constraints, indexes, and Mermaid ER diagram.

---

## 🎯 Target Personas

| Persona | How It Helps |
|---|---|
| **Software Developers** | Get structured architecture, API contracts, and database schemas before writing code. |
| **Startup Founders** | Rapidly validate product concepts and generate technical specs for engineering teams. |
| **Students & Learners** | Learn industry-standard software architecture and generate complete academic project documentation. |
| **Project Managers** | Extract sprint-ready user stories, use cases, and estimation inputs in seconds. |
| **Software Architects** | Eliminate hours of repetitive documentation and diagram drafting. |

---

## 🚀 Quickstart: Run With Docker in 1 Command

The entire application (React frontend, FastAPI backend, and PostgreSQL database) is fully containerized.

### Prerequisites
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and ensure it is running.

### 1. Clone & Enter Repository
```bash
git clone https://github.com/your-username/AI-Software-Architect.git
cd AI-Software-Architect
```

### 2. Launch Stack with Docker Compose
```bash
docker compose up --build
```

### 3. Open in Browser

| Service | Address | Description |
|---|---|---|
| **Web Application** | [http://localhost:3000](http://localhost:3000) | Interactive React UI with live Mermaid visualizer |
| **Backend API (Swagger Docs)** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive OpenAPI REST documentation |
| **Backend Health Check** | [http://localhost:8000/api/health](http://localhost:8000/api/health) | API & AI engine diagnostic check |
| **PostgreSQL Database** | `localhost:5432` | DB: `ai_architect`, User: `postgres`, Password: `postgres` |

> [!TIP]
> **No API Key Required**: AI Software Architect includes an intelligent offline heuristic engine that generates complete, production-grade blueprints right out of the box! If you want to use OpenAI models (e.g. `gpt-4o-mini`), simply add your key into `.env` and restart.

To run in the background (detached mode):
```bash
docker compose up -d --build
```

To stop containers:
```bash
docker compose down
```

---

## 💻 Alternative: Run Locally Without Docker

If you prefer to run services directly on your host machine:

### 1. Backend Setup (FastAPI)
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn main:app --reload --port 8000
```
Backend will be available at [http://localhost:8000](http://localhost:8000).

### 2. Frontend Setup (React + Vite)
```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Frontend will be available at [http://localhost:3000](http://localhost:3000).

---

## 📊 Features & System Blueprint Output

### 1. Requirements Engineering
- **Actors & Stakeholders**: Separates primary users, administrative personas, and external system integrations.
- **MoSCoW Prioritization**: Categorizes functional requirements into Must-Have, Should-Have, and Could-Have.
- **Gherkin Acceptance Criteria**: Explicit testable acceptance conditions for every requirement.
- **Scope Definition**: Clearly establishes In-Scope features versus Out-of-Scope boundaries.

### 2. IEEE 830-1998 Compliant SRS
- Complete introduction, business scope, measurable objectives, and assumptions.
- Structured Use Cases detailing primary actors, triggers, preconditions, main flow steps, alternative flows, and postconditions.
- 1-click download as Markdown (`.md`).

### 3. Five Supported Mermaid UML Diagrams
- **Use Case Diagram**: System boundaries, actors, and functional capability links.
- **Class Diagram**: Object-oriented models with attributes, typing, and method signatures.
- **Sequence Diagram**: End-to-end HTTP request and database transaction timelines.
- **Activity Diagram**: Process logic flowcharts with decision diamonds and branch validation.
- **Component Diagram**: Tiered architecture (Client SPA, Reverse Proxy, FastAPI, Database & Cache).
- **Interactive Controls**: Zoom In, Zoom Out, Reset, 1-Click Code Copy, and SVG Export.

### 4. Normalized PostgreSQL Database Design
- **Mermaid ERD**: Visual entity-relationship diagram with cardinality.
- **Production-Ready PostgreSQL DDL**: Includes `UUID` extension, foreign key constraints with `ON DELETE` cascades, check constraints, and performance indexes.
- **Data Dictionary**: Comprehensive column tables, data types, nullability, and field descriptions.

---

## 📁 Repository Structure

```text
AI-Software-Architect/
├── docker-compose.yml          # Unified multi-container composition
├── .env.example                # Global environment variables template
├── .env                        # Active environment variables
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
│
├── docs/                       # Technical specifications
│   ├── ARCHITECTURE.md         # System architectural overview
│   ├── DOCKER_GUIDE.md         # Detailed Docker guide & troubleshooting
│   ├── API_SPECIFICATION.md    # REST API documentation
│   └── SAMPLE_OUTPUT_HOSPITAL_MANAGEMENT.md # Sample blueprint output
│
├── backend/                    # FastAPI Backend Service
│   ├── Dockerfile              # Backend containerization
│   ├── requirements.txt        # Python package dependencies
│   ├── main.py                 # FastAPI application entrypoint
│   ├── app/
│   │   ├── config.py           # Pydantic settings & environment configuration
│   │   ├── api/                # API routes & health check endpoints
│   │   ├── models/             # Pydantic schemas (Request / Response)
│   │   └── services/           # AI service, prompts & architectural generators
│   └── tests/                  # Automated API test suite
│
└── frontend/                   # React Frontend Application
    ├── Dockerfile              # Multi-stage production Nginx container
    ├── nginx.conf              # Reverse proxy & SPA routing configuration
    ├── package.json            # Node.js dependencies & scripts
    ├── vite.config.js          # Vite build & development proxy setup
    ├── index.html              # HTML shell
    └── src/
        ├── App.jsx             # Main application state and tab layout
        ├── index.css           # Tailwind CSS & custom styling
        ├── services/           # API client and export utilities
        └── components/         # Modular React UI components
            ├── Header.jsx
            ├── ProjectInput.jsx
            ├── TabNavigation.jsx
            ├── MermaidViewer.jsx
            ├── RequirementAnalysisView.jsx
            ├── SRSView.jsx
            ├── UMLView.jsx
            ├── DatabaseDesignView.jsx
            └── ExportModal.jsx
```

---

## 🌿 Git Branching Strategy (GitHub Flow)

This project strictly adheres to **GitHub Flow**:
- `main`: Contains the stable, production-ready release.
- Feature branches (`feature/<feature-name>`): Used for all active development.

### Example Workflow:
```bash
# 1. Branch from main
git checkout -b feature/requirement-analyzer

# 2. Make your enhancements
git add .
git commit -m "feat: enhance requirement extraction rules"

# 3. Push feature branch
git push -u origin feature/requirement-analyzer

# 4. Open Pull Request to main on GitHub
```

---

## 👥 Contributors

| Name | Role |
|---|---|
| **Vishal Shyam** | Project Creator, Full Stack Developer & AI Engineer |
| **Pugazhandi Kannan** | Full Stack Developer & Software Engineer |

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
