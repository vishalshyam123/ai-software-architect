# Comprehensive Architectural Diagrams for AI Software Architect

This document contains the complete set of **Data Flow Diagrams (DFD)**, **Entity-Relationship Diagrams (ERD)**, and **UML Diagrams** modeled specifically for the **AI Software Architect** application.

---

# B. Data Flow Diagrams (DFD)

### B.1 Level 0 DFD — Context Diagram
The Level 0 Context Diagram depicts the boundaries of the AI Software Architect system, the external entities (Developers, Architects, Students, External AI Gateway), and the primary data flows into and out of the system.

```mermaid
flowchart TD
    User(["Software Engineers / Students / Architects"])
    AIServiceExt(["External AI Gateway (OpenAI / LLM API)"])
    
    SystemCore[["0.0<br/>AI Software Architect System"]]

    User -->|1. Project Title, Description & Domain Selection| SystemCore
    SystemCore -->|2. Generated SRS Document, 5 UML Diagrams & 3NF SQL Schema| User
    
    SystemCore -->|3. Architectural Prompt Context & System Schemas| AIServiceExt
    AIServiceExt -->|4. Synthesized Requirements, Entities & Workflows| SystemCore
```

---

### B.2 Level 1 DFD — Detailed Process Decomposition
The Level 1 DFD breaks down the system into its 5 primary subprocesses, illustrating how project data flows through analysis, document synthesis, diagram modeling, database design, and data storage.

```mermaid
flowchart TB
    User(["User (Developer / Architect)"])
    ExtAI(["AI Gateway / Heuristic Engine"])
    
    subgraph Storage["Data Stores"]
        D1[("D1: Project Profiles & Configurations")]
        D2[("D2: Requirements & MoSCoW Specifications")]
        D3[("D3: UML Diagrams & Mermaid Specifications")]
        D4[("D4: Relational 3NF Schemas & DDL Scripts")]
    end

    P1["1.0<br/>Intake & Input Validation Process"]
    P2["2.0<br/>Requirements Engineering & Decomposition"]
    P3["3.0<br/>IEEE 830 SRS Synthesizer"]
    P4["4.0<br/>UML Architectural Diagram Generator"]
    P5["5.0<br/>3NF Database Schema & ERD Synthesizer"]
    P6["6.0<br/>Interactive Blueprint Presentation & Export Engine"]

    User -->|Project Title, Description & Domain| P1
    P1 -->|Validated Input DTO| D1
    
    D1 -->|Project Concept Payload| P2
    P2 <-->|Prompt Construction & Entity Parsing| ExtAI
    P2 -->|Structured Actors, Stakeholders & FR/NFR| D2

    D2 -->|Requirements Context| P3
    P3 -->|IEEE 830 Markdown Document| D2

    D2 -->|Entity Models & Workflows| P4
    P4 -->|Use Case, Class, Sequence, Activity & Component Syntax| D3

    D2 -->|Entities & Normalization Constraints| P5
    P5 -->|PostgreSQL DDL & Mermaid ERD| D4

    D2 -->|SRS & Analysis| P6
    D3 -->|Mermaid Diagram Code| P6
    D4 -->|ERD & DDL Scripts| P6
    P6 -->|Rendered SVG Diagrams, Markdown & SQL Exports| User
```

---

# C. Entity-Relationship Diagram (ERD)

The ERD models the database structure of the **AI Software Architect** platform, tracking users, submitted project specifications, generated requirements, UML diagrams, database designs, and export audit trails.

```mermaid
erDiagram
    USERS ||--o{ PROJECTS : "owns"
    PROJECTS ||--|| REQUIREMENT_ANALYSES : "generates"
    REQUIREMENT_ANALYSES ||--o{ ACTORS : "identifies"
    REQUIREMENT_ANALYSES ||--o{ FUNCTIONAL_REQUIREMENTS : "defines"
    REQUIREMENT_ANALYSES ||--o{ NON_FUNCTIONAL_REQUIREMENTS : "specifies"
    PROJECTS ||--|| SRS_DOCUMENTS : "produces"
    PROJECTS ||--|| UML_BLUEPRINTS : "generates"
    PROJECTS ||--|| DATABASE_DESIGNS : "architects"
    DATABASE_DESIGNS ||--o{ DB_TABLE_DEFINITIONS : "specifies"
    PROJECTS ||--o{ GENERATION_AUDIT_LOGS : "logs"

    USERS {
        uuid id PK
        string email UK
        string password_hash
        string full_name
        string role
        boolean is_active
        timestamp created_at
    }

    PROJECTS {
        uuid id PK
        uuid user_id FK
        string title
        text description
        string domain
        string generation_mode
        timestamp created_at
        timestamp updated_at
    }

    REQUIREMENT_ANALYSES {
        uuid id PK
        uuid project_id FK
        text executive_summary
        string domain_classified
        timestamp analyzed_at
    }

    ACTORS {
        uuid id PK
        uuid analysis_id FK
        string actor_name
        string actor_type
        text responsibility
    }

    FUNCTIONAL_REQUIREMENTS {
        uuid id PK
        uuid analysis_id FK
        string req_code
        string category
        string title
        text description
        string moscow_priority
        string[] acceptance_criteria
    }

    NON_FUNCTIONAL_REQUIREMENTS {
        uuid id PK
        uuid analysis_id FK
        string category
        string metric
        string target_value
    }

    SRS_DOCUMENTS {
        uuid id PK
        uuid project_id FK
        string ieee_standard
        text markdown_content
        text scope_in_scope
        text scope_out_of_scope
        timestamp generated_at
    }

    UML_BLUEPRINTS {
        uuid id PK
        uuid project_id FK
        text use_case_diagram
        text class_diagram
        text sequence_diagram
        text activity_diagram
        text component_diagram
        timestamp generated_at
    }

    DATABASE_DESIGNS {
        uuid id PK
        uuid project_id FK
        text mermaid_er_diagram
        text postgres_sql_ddl
        string normalization_level
        timestamp generated_at
    }

    DB_TABLE_DEFINITIONS {
        uuid id PK
        uuid db_design_id FK
        string table_name
        text description
        jsonb column_metadata
        jsonb relationship_metadata
    }

    GENERATION_AUDIT_LOGS {
        uuid id PK
        uuid project_id FK
        string engine_used
        integer execution_time_ms
        string status
        timestamp logged_at
    }
```

---

# D. UML Diagrams

### D.1 UML Use Case Diagram
Illustrates how end users (Software Developers, Students, Project Managers, Software Architects) interact with the application capabilities.

```mermaid
graph LR
    subgraph Actors["Primary Personas"]
        Dev["Software Developer"]
        Student["Student / Learner"]
        PM["Project Manager"]
        Architect["Enterprise Architect"]
    end

    subgraph SystemBoundary["AI Software Architect System Boundary"]
        UC1(["Input Project Concept & Domain"])
        UC2(["Analyze Stakeholders & Requirements"])
        UC3(["Prioritize Requirements via MoSCoW"])
        UC4(["Generate IEEE 830 SRS Document"])
        UC5(["Generate 5 UML Mermaid Diagrams"])
        UC6(["Generate 3NF PostgreSQL Schema & ERD"])
        UC7(["Interactive Diagram Pan/Zoom & SVG Export"])
        UC8(["Download Markdown & DDL Artifacts"])
    end

    Dev --> UC1
    Dev --> UC5
    Dev --> UC6
    Dev --> UC8

    Student --> UC1
    Student --> UC2
    Student --> UC4
    Student --> UC5
    Student --> UC7

    PM --> UC1
    PM --> UC2
    PM --> UC3
    PM --> UC4

    Architect --> UC1
    Architect --> UC5
    Architect --> UC6
    Architect --> UC8
```

---

### D.2 UML Class Diagram (Application OOP Architecture)
Depicts the object-oriented design and structural composition of the backend engines, schemas, and services.

```mermaid
classDiagram
    class FastAPIApp {
        +String title
        +String version
        +include_router(router)
        +start_server()
    }

    class ProjectInputDTO {
        +String title
        +String description
        +String domain
        +validate()
    }

    class FullBlueprintResponseDTO {
        +String project_title
        +RequirementAnalysisResponse analysis
        +SRSResponse srs
        +UMLResponse uml_diagrams
        +DatabaseDesignResponse database_design
    }

    class AIService {
        -String api_key
        -AsyncOpenAI client
        +analyze_requirements(title, desc, domain) Dict
        +generate_srs(title, desc, analysis) Dict
        +generate_uml(title, desc, analysis) Dict
        +generate_database_design(title, desc, analysis) Dict
        -_call_llm(system_prompt, user_prompt) Dict
        -_extract_domain_entities(title, desc) Dict
        -_generate_heuristic_requirements(title, desc, domain) Dict
        -_generate_heuristic_uml(title, desc, analysis) Dict
        -_generate_heuristic_db(title, desc, analysis) Dict
    }

    class RequirementAnalysis {
        +String project_title
        +String summary
        +List~Actor~ actors
        +List~Stakeholder~ stakeholders
        +List~FunctionalReq~ functional_requirements
        +List~NonFunctionalReq~ non_functional_requirements
    }

    class UMLBlueprint {
        +String project_title
        +String use_case_diagram
        +String class_diagram
        +String sequence_diagram
        +String activity_diagram
        +String component_diagram
        +render_svg()
    }

    class DatabaseDesign {
        +String project_title
        +String er_diagram
        +String sql_schema
        +List~TableDef~ tables
        +List~RelationshipDef~ relationships
    }

    FastAPIApp --> ProjectInputDTO : receives
    FastAPIApp --> AIService : delegates_to
    AIService --> RequirementAnalysis : produces
    AIService --> UMLBlueprint : produces
    AIService --> DatabaseDesign : produces
    FastAPIApp --> FullBlueprintResponseDTO : returns
```

---

### D.3 UML Sequence Diagram (System Execution Workflow)
Models the chronological message flow across tiers during blueprint generation.

```mermaid
sequenceDiagram
    autonumber
    actor Client as User (React UI)
    participant Nginx as Nginx Reverse Proxy
    participant API as FastAPI Router
    participant AISvc as AI Hybrid Service
    participant LLM as External LLM / Heuristics
    participant DB as PostgreSQL 16
    participant Mermaid as Mermaid.js (Browser)

    Client->>Nginx: POST /api/generate-all (title, description, domain)
    Nginx->>API: Proxy pass request to ASGI Worker
    API->>API: Validate input schema (Pydantic DTO)
    
    API->>AISvc: analyze_requirements()
    AISvc->>LLM: Dispatch Requirement System Prompt
    LLM-->>AISvc: Structured Actors, FR & NFR JSON
    AISvc-->>API: RequirementAnalysis Object
    
    par Concurrent Blueprint Synthesis
        API->>AISvc: generate_srs()
        AISvc->>LLM: Generate IEEE 830 Markdown
        LLM-->>AISvc: Markdown SRS Text
    and
        API->>AISvc: generate_uml()
        AISvc->>LLM: Generate 5 Mermaid UML Diagrams
        LLM-->>AISvc: UseCase, Class, Seq, Activity, Comp Syntax
    and
        API->>AISvc: generate_database_design()
        AISvc->>LLM: Generate 3NF PostgreSQL DDL & ERD
        LLM-->>AISvc: PostgreSQL SQL + Mermaid ERD
    end

    API->>DB: Log transaction audit record
    DB-->>API: Acknowledged
    API-->>Nginx: HTTP 200 OK (Full Blueprint JSON)
    Nginx-->>Client: Deliver Complete Payload
    
    Client->>Mermaid: Parse Mermaid syntax strings
    Mermaid-->>Client: Render interactive SVG diagrams
    Client-->>Client: Update UI tabs with live Blueprint
```

---

### D.4 UML Activity Diagram (Process Control Flow)
Illustrates the internal control flow, decision branches, and fallback mechanisms when processing requests.

```mermaid
flowchart TD
    Start([User Initiates Blueprint Generation]) --> ValidateInput{{"Is Input Valid?<br/>(Title & Description present)"}}
    
    ValidateInput -- No --> Return422[Return HTTP 422 Unprocessable Entity]
    Return422 --> TerminateNode([Process Terminated])
    
    ValidateInput -- Yes --> CheckAPIKey{{"Is OpenAI API Key<br/>Configured & Reachable?"}}
    
    CheckAPIKey -- Yes --> InvokeLLM[Query LLM via OpenAI API]
    InvokeLLM --> CheckResponse{{"Did LLM Return<br/>Valid JSON Schema?"}}
    
    CheckResponse -- Yes --> ParseBlueprint[Parse Synthesized Architectural Blueprint]
    CheckResponse -- No --> FallbackNotice[Trigger Heuristic Fallback Engine]
    
    CheckAPIKey -- No --> FallbackNotice
    FallbackNotice --> ExtractEntities[Perform Semantic Entity & Workflow Extraction]
    ExtractEntities --> SynthesizeHeuristic[Synthesize 3NF Schema & 5 Mermaid Diagrams]
    SynthesizeHeuristic --> ParseBlueprint
    
    ParseBlueprint --> SaveAudit[(Persist Generation Record to PostgreSQL)]
    SaveAudit --> ReturnJSON[Return Complete Blueprint JSON to Client]
    ReturnJSON --> RenderSVGs[Client-Side Mermaid SVG Vector Rendering]
    RenderSVGs --> EndNode([Blueprint Ready for Interactive Use])
```

---

### D.5 UML Component / Deployment Diagram
Shows the physical and logical container deployment topology across the Docker Compose bridge network.

```mermaid
flowchart TB
    subgraph Host["Host Machine (Windows / Linux / macOS)"]
        Browser["Web Browser (User Client)"]
        
        subgraph DockerNetwork["Docker Bridge Network: architect_net"]
            subgraph Container1["Container: ai_architect_frontend (Port 3000)"]
                NginxServer["Nginx 1.27 Web Server & Proxy"]
                StaticFiles["Static React 18 SPA Bundles (HTML/JS/CSS)"]
                NginxServer --- StaticFiles
            end
            
            subgraph Container2["Container: ai_architect_backend (Port 8000)"]
                UvicornServer["Uvicorn ASGI Server"]
                FastAPIApp["FastAPI Application Core"]
                AIModule["Hybrid AI & Heuristic Service"]
                UvicornServer --> FastAPIApp
                FastAPIApp --> AIModule
            end
            
            subgraph Container3["Container: ai_architect_db (Port 5432)"]
                PostgresService["PostgreSQL 16 Engine"]
                StorageVolume[("Docker Volume: pgdata")]
                PostgresService --- StorageVolume
            end
        end
    end

    Browser -->|HTTP / Port 3000| NginxServer
    NginxServer -->|Internal Proxy /api/ -> Port 8000| UvicornServer
    FastAPIApp -->|TCP / SQL Connection -> Port 5432| PostgresService
    AIModule -.->|Optional HTTPS / TLS| OpenAICloud["External OpenAI API Gateway"]
```
