# Docker Deployment & Execution Guide

This guide walks you through containerizing and launching the **AI Software Architect** stack with Docker and Docker Compose.

---

## 1. Prerequisites

1. **Docker Desktop** installed and running on your machine:
   - **Windows / macOS / Linux**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - On Windows, ensure WSL 2 (Windows Subsystem for Linux) backend is enabled in Docker Desktop settings.
2. Verify Docker is running by opening PowerShell / Terminal:
   ```bash
   docker --version
   docker compose version
   ```

---

## 2. Fast 1-Command Startup

Navigate to the project root directory:

```bash
cd AI-Software-Architect
```

Build and launch all services with Docker Compose:

```bash
docker compose up --build
```

### What happens behind the scenes:
1. **`db` container**: Boots PostgreSQL 16 on port `5432` and creates persistent volume `pgdata`.
2. **`backend` container**: Installs Python 3.11 requirements, starts FastAPI on port `8000`.
3. **`frontend` container**: Builds React with Vite, packages production assets into Nginx on port `3000`, and configures internal reverse proxy for `/api`.

---

## 3. Accessing the Application

Once the containers are running:

| Service | URL | Description |
|---|---|---|
| **Web Application** | [http://localhost:3000](http://localhost:3000) | Interactive React UI & Mermaid Visualizer |
| **Backend API Docs** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive Swagger / OpenAPI Specification |
| **Backend Health** | [http://localhost:8000/api/health](http://localhost:8000/api/health) | API & AI Engine status |
| **PostgreSQL Database** | `localhost:5432` | User: `postgres`, Password: `postgres`, DB: `ai_architect` |

---

## 4. Running in Background (Daemon Mode)

To start containers in the background:
```bash
docker compose up -d --build
```

To view live container logs:
```bash
docker compose logs -f
```

To view backend logs only:
```bash
docker compose logs -f backend
```

To stop all containers:
```bash
docker compose down
```

To stop containers and wipe database volumes for a clean slate:
```bash
docker compose down -v
```

---

## 5. Adding OpenAI API Key (Optional)

AI Software Architect includes an intelligent built-in heuristic architect engine that generates complete, production-grade blueprints even without any API key.

If you wish to use OpenAI models (e.g., `gpt-4o-mini`):
1. Open the `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   OPENAI_MODEL=gpt-4o-mini
   ```
2. Restart the containers:
   ```bash
   docker compose up -d --build
   ```

---

## 6. Common Troubleshooting

### Error: `Ports are not available: listen tcp 0.0.0.0:3000`
- **Cause**: Another program (e.g. existing Node server) is using port 3000.
- **Fix**: Open `docker-compose.yml` and change `"3000:80"` to `"3001:80"` or `"8080:80"`.

### Error: `Docker daemon is not running`
- **Fix**: Launch Docker Desktop from your Start menu and wait until the whale icon in the taskbar turns solid.
