# AI Software Architect - System Architecture

## Architectural Vision
AI Software Architect is engineered with a modular, cloud-native 3-tier architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                       Client Layer                          │
│  React SPA (Vite) + Tailwind CSS + Interactive Mermaid.js   │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTPS / REST (Port 3000 / 80)
┌──────────────────────────────▼──────────────────────────────┐
│                    API & Engine Layer                       │
│  FastAPI (Python 3.11) Asynchronous Request Pipeline        │
│  ├── Requirement Analyzer Module                            │
│  ├── IEEE 830 SRS Synthesizer                               │
│  ├── Mermaid UML Diagram Engine                             │
│  ├── 3NF Normalized Relational DB Designer                  │
│  └── AI Hybrid Service (OpenAI LLM + Heuristic Engine)      │
└──────────────────────────────┬──────────────────────────────┘
                               │ AsyncPG / TCP (Port 5432)
┌──────────────────────────────▼──────────────────────────────┐
│                     Persistence Layer                       │
│  PostgreSQL 16 Relational Storage + Persistent Docker Volume│
└─────────────────────────────────────────────────────────────┘
```

## Key Modules

### 1. Requirement Analyzer (`app.services.requirement_analyzer`)
- Decomposes informal natural language project ideas into structured schemas.
- Extracts actors (Primary, Secondary, System), stakeholders, and priority-tagged functional requirements.
- Generates MoSCoW prioritization (Must-Have, Should-Have, Could-Have) and Gherkin-style acceptance criteria.

### 2. SRS Generator (`app.services.srs_generator`)
- Compiles industry-standard IEEE 830-1998 / ISO/IEC/IEEE 29148 compliant Software Requirements Specifications.
- Synthesizes Use Case specifications with triggers, preconditions, main flow steps, alternative flows, and postconditions.

### 3. UML Diagram Engine (`app.services.uml_generator`)
- Automatically outputs 5 valid Mermaid diagram specifications:
  - **Use Case Diagram**: System boundaries, actors, and functional interactions.
  - **Class Diagram**: Domain models, attributes, methods, and relationships.
  - **Sequence Diagram**: Message sequence between client, API, database, and background workers.
  - **Activity Diagram**: Workflow control flow, conditional checkpoints, and error paths.
  - **Component Diagram**: Tiered architectural topology (Client, Reverse Proxy, FastAPI, DB).

### 4. Database Designer (`app.services.db_designer`)
- Produces normalized relational schemas (3NF / BCNF).
- Generates Mermaid `erDiagram` syntax for visual schema exploration.
- Generates production-ready PostgreSQL DDL with UUID primary keys, foreign key constraints with cascade behaviors, compound indexes, and audit timestamps.

### 5. Resilient AI Hybrid Architecture (`app.services.ai_service`)
- Connects to OpenAI API (`gpt-4o-mini`, `gpt-4o`) or any OpenAI-compatible API (e.g. Ollama, vLLM, DeepSeek).
- Includes an intelligent offline heuristic software architect fallback that generates complete, domain-specific blueprints without requiring third-party API keys or internet access.
