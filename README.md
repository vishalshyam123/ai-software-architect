# AI Software Architect

> An AI-powered assistant that automates software architecture and project planning by generating complete software engineering documentation before development begins.

---

# Project Overview

**AI Software Architect** is an intelligent system that transforms a simple project idea into a complete software development blueprint.

Instead of immediately generating code, the system follows the same workflow as an experienced software architect. It analyzes project requirements and automatically creates Software Requirement Specifications (SRS), UML diagrams, database designs, REST API documentation, sprint planning, effort estimation, testing documents, and other essential software engineering artifacts.

This helps developers, startups, students, and software teams reduce planning time and begin implementation with a well-defined architecture.

---

# Problem It Solves

Software development often spends a significant amount of time on planning before writing the first line of code.

Teams usually need to prepare:

- Software Requirement Specification (SRS)
- Functional & Non-functional Requirements
- UML Diagrams
- Database Design
- API Documentation
- Sprint Planning
- Test Cases
- Project Documentation

Creating these documents manually is repetitive, time-consuming, and requires experienced architects.

**AI Software Architect** automates this entire process, enabling teams to move from an idea to an implementation-ready design within minutes.

---

# Target Users (Personas)

## 1. Software Developers

- Need a structured architecture before coding.
- Want automatically generated APIs and database schemas.

## 2. Startup Founders

- Quickly validate product ideas.
- Generate technical documentation for developers.

## 3. Students

- Create complete Software Engineering project documentation.
- Learn industry-standard software architecture.

## 4. Project Managers

- Generate sprint plans and effort estimates.
- Plan development timelines efficiently.

## 5. Software Architects

- Reduce repetitive documentation work.
- Use AI as an assistant during project planning.

---

# Vision Statement

To build an intelligent AI assistant that automates software architecture and engineering documentation, enabling anyone to transform an idea into a complete, production-ready software design within minutes.

---

# Key Features / Goals

## Requirement Analysis

- Analyze user project descriptions.
- Identify actors and stakeholders.
- Extract functional requirements.
- Extract non-functional requirements.

---

## Software Requirement Specification (SRS)

Automatically generate:

- Introduction
- Scope
- Objectives
- Functional Requirements
- Non-functional Requirements
- Use Cases
- Constraints
- Assumptions

---

## UML Diagram Generation

Generate diagrams using Mermaid or PlantUML.

Supported diagrams:

- Use Case Diagram
- Class Diagram
- Sequence Diagram
- Activity Diagram (Future)
- Component Diagram (Future)

---

## Database Design

Automatically generate:

- ER Diagram
- Database Tables
- Primary Keys
- Foreign Keys
- Relationships
- PostgreSQL SQL Scripts

---

## REST API Design

Generate complete API specifications including:

- Endpoints
- HTTP Methods
- Request Body
- Response Body
- Authentication Requirements
- Error Responses

---

## Sprint Planning

Automatically create:

- Product Backlog
- Sprint Breakdown
- User Stories
- Story Points
- Development Timeline

---

## Effort Estimation

Estimate:

- Development Time
- Complexity
- Team Size
- Risk Level

---

## Test Case Generation

Generate:

- Unit Test Cases
- Integration Test Cases
- Functional Test Cases
- Edge Cases
- Acceptance Criteria

---

## Documentation Export

Support exporting generated documents as:

- Markdown
- PDF
- DOCX (Future)

---

# Success Metrics

The project will be considered successful if it can:

- Generate complete SRS documents within seconds.
- Produce accurate UML diagrams automatically.
- Design normalized PostgreSQL database schemas.
- Generate production-ready REST API specifications.
- Create realistic sprint plans and effort estimates.
- Produce comprehensive software testing documentation.
- Reduce project planning time by more than 80%.

---

# Assumptions

- Users provide a clear project idea or problem statement.
- AI models can accurately interpret software requirements.
- Mermaid or PlantUML is available for diagram generation.
- PostgreSQL is used as the primary database.
- OpenAI API or Llama models are available for AI-powered generation.

---

# Constraints

- AI-generated documentation may require human review.
- Diagram complexity depends on project size.
- API quality depends on prompt quality.
- External AI API usage may incur costs.
- Large enterprise projects may require manual refinement.

---

# Example Workflow

### Input

```
Hospital Management System
```

### Generated Output

- Requirement Analysis
- Software Requirement Specification (SRS)
- Use Case Diagram
- Class Diagram
- Sequence Diagram
- ER Diagram
- PostgreSQL Database Schema
- REST API Design
- Sprint Planning
- Effort Estimation
- Test Cases
- Technical Documentation

---

# Proposed Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Backend | FastAPI / Node.js |
| Database | PostgreSQL |
| AI Model | OpenAI GPT / Llama |
| Diagram Generation | Mermaid / PlantUML |
| Documentation | Markdown, PDF |
| Version Control | Git & GitHub |

---

# Local Development Tools

The following tools are used for developing, testing, and managing the AI Software Architect project locally.

## Development Environment

| Tool | Purpose |
|---|---|
| Visual Studio Code | Primary code editor |
| Git | Version control |
| GitHub | Repository hosting and collaboration |
| Node.js & npm | React development environment |
| Python | Backend development and AI integration |
| FastAPI | Backend API framework |
| PostgreSQL | Database management |
| Docker Desktop | Containerization |
| Postman | API testing |
| Draw.io | Architecture diagrams |
| StarUML | UML diagrams |
| Figma | UI/UX wireframes |

---

## Frontend Development Tools

**Technology:** React.js

Tools used:

- Node.js
- npm package manager
- React development server
- Browser Developer Tools

Commands:

```bash
npm install
npm start
```

---

## Backend Development Tools

**Technology:** FastAPI

Tools used:

- Python
- FastAPI
- Uvicorn
- Virtual Environment

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn main:app --reload
```

---

# Future Enhancements

- Multi-language support
- Microservice architecture generation
- CI/CD pipeline generation
- Docker and Kubernetes configuration
- Infrastructure-as-Code generation
- Cloud deployment recommendations
- Architecture optimization suggestions

---

# Repository Structure

```
AI-Software-Architect/
│
├── frontend/
├── backend/
├── docs/
├── README.md
└── .gitignore
```

---

# Git Branching Strategy

This project follows the **GitHub Flow branching strategy** for version control and collaborative development.

The `main` branch contains the stable version of the project. All new features are developed in separate feature branches and merged into the main branch after completion and review.

## Branch Structure

```
main
│
└── feature/requirement-analyzer
```

---

## Main Branch

The `main` branch contains the stable and working version of the AI Software Architect project.

Guidelines:

- Only tested and completed features are merged into the main branch.
- Direct commits to the main branch are avoided.
- The branch should always contain a working version of the project.

---

## Feature Branch

### feature/requirement-analyzer

This branch is created for developing the requirement analysis module.

Responsibilities:

- Accept user project ideas as input.
- Analyze software requirements using AI.
- Identify functional and non-functional requirements.
- Identify actors and stakeholders.
- Prepare structured requirements for SRS generation.

---

## Development Workflow

Create a feature branch:

```bash
git checkout -b feature/requirement-analyzer
```

Add changes:

```bash
git add .
```

Commit changes:

```bash
git commit -m "Implemented requirement analyzer"
```

Push branch:

```bash
git push -u origin feature/requirement-analyzer
```

After completion, a Pull Request is created and the feature is merged into the `main` branch.

---

# Project Status

🚧 Initial Planning Phase

## Current Milestone

- Vision Document
- Repository Setup
- Frontend & Backend Structure
- GitHub Workflow Setup

## Upcoming Milestones

- Requirement Analyzer
- SRS Generator
- UML Generator
- Database Designer
- API Generator
- Sprint Planner
- Test Case Generator
- Documentation Export

---

# Contributors

| Name | Role |
|---|---|
| **Vishal Shyam** | Project Creator, Full Stack Developer & AI Engineer |
| **Pugazhandi Kannan** | Full Stack Developer & Software Engineer |

---
# Quick Start – Local Development

This guide explains how to set up and run the **AI Software Architect** project locally using Docker.

Docker is the recommended method because it provides a consistent development environment without requiring separate installation of backend, frontend, database, and cache dependencies.

---

# Prerequisites

Make sure the following tools are installed:

- Git
- Docker Desktop (includes Docker Engine and Docker Compose)
- (Optional) Node.js 18+ and npm (for frontend development without Docker)
- (Optional) Python 3.10+ (for backend development without Docker)

Verify installations:

```bash
git --version
docker --version
docker compose version
```

---

# Clone Repository

Clone the repository:

```bash
git clone <repository-url>
```

Navigate into the project directory:

```bash
cd AI-Software-Architect
```

---

# Setup with Docker (Recommended)

Docker provides the easiest setup with all required services running inside containers.

The application consists of:

- React frontend
- FastAPI backend
- PostgreSQL database
- Redis cache
- AI service integration

---

# Step 1: Create Environment File

Create the environment configuration file:

```bash
cp .env.example .env
```

Edit `.env` if required.

Example:

```env
OPENAI_API_KEY=your_api_key_here

POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=ai_software_architect

DATABASE_URL=postgresql://postgres:password@postgres:5432/ai_software_architect

REDIS_URL=redis://redis:6379
```

The `.env` file stores sensitive configuration details and should not be uploaded to GitHub.

---

# Step 2: Build and Run Application

Build Docker images and start all services:

```bash
docker compose up --build
```

The following services will start:

```
Frontend  → http://localhost:3000

Backend API → http://localhost:8000

API Docs → http://localhost:8000/docs

PostgreSQL → localhost:5432

Redis → localhost:6379
```

---

# Step 3: Run in Background

To start containers in detached mode:

```bash
docker compose up -d
```

The application will continue running in the background.

---

# Step 4: Stop Services

Stop all running services:

```bash
docker compose down
```

To stop services and remove stored database/cache volumes:

```bash
docker compose down -v
```

---

# Important Docker Notes

## ✅ Hot Reload Enabled

During development:

- Backend automatically reloads when FastAPI code changes.
- Frontend automatically refreshes when React code changes.

---

## ✅ Database Persistence

PostgreSQL data is stored using Docker volumes.

Database data remains available even after:

```bash
docker compose down
```

Removing volumes:

```bash
docker compose down -v
```

will delete stored database data.

---

## ✅ Inter-Service Communication

Docker Compose automatically manages communication between services.

- Frontend communicates with backend API.
- Backend communicates with PostgreSQL database.
- Backend communicates with Redis cache.
- Backend connects with OpenAI/Llama AI services.

---

# Docker Project Structure

```
AI-Software-Architect/
│
├── frontend/
│   └── Dockerfile
│
├── backend/
│   └── Dockerfile
│
├── docker-compose.yml
│
├── .env.example
│
└── README.md
```

---

# Useful Docker Commands

| Command | Purpose |
|---|---|
| `docker compose up` | Start all services |
| `docker compose up -d` | Start services in background |
| `docker compose up --build` | Rebuild images and start services |
| `docker compose ps` | List running containers |
| `docker compose logs -f` | View real-time logs |
| `docker compose logs -f backend` | View backend logs only |
| `docker compose logs -f frontend` | View frontend logs only |
| `docker compose stop` | Stop all services |
| `docker compose down` | Stop and remove containers |
| `docker compose down -v` | Stop containers and remove volumes |
| `docker compose exec backend bash` | Open backend container shell |

---

# Alternative: Local Development Without Docker

Docker is recommended, but the project can also be run manually.

## Backend Setup

Navigate to backend:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI server:

```bash
uvicorn main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

## Frontend Setup

Open another terminal:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start React application:

```bash
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

# Database Setup Without Docker

Install PostgreSQL locally.

Create database:

```sql
CREATE DATABASE ai_software_architect;
```

Update backend environment file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/ai_software_architect
```

---

# Development Workflow

Create a feature branch:

```bash
git checkout -b feature/<feature-name>
```

Example:

```bash
git checkout -b feature/requirement-analyzer
```

After making changes:

```bash
git add .
```

Commit:

```bash
git commit -m "Added requirement analyzer module"
```

Push branch:

```bash
git push origin feature/requirement-analyzer
```

Create a Pull Request and merge into the `main` branch after review.

---

# Troubleshooting

## Docker Container Not Starting

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

---

## Port Already in Use

Check active containers:

```bash
docker ps
```

Stop the conflicting container:

```bash
docker stop <container-id>
```

---

## Rebuild After Dependency Changes

If packages are added or changed:

```bash
docker compose down
docker compose build
docker compose up
```

---

The **AI Software Architect** application will now be available at:

```
Frontend:
http://localhost:3000

Backend:
http://localhost:8000

API Documentation:
http://localhost:8000/docs
```

# License

This project is intended for educational and research purposes. A suitable open-source license (such as the MIT License) can be added in future releases.

---

# Authors

- **Vishal Shyam**
- **Pugazhandi Kannan**
