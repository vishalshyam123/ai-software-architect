from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import api_router, health_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent AI Software Architect that transforms simple project ideas into complete Software Requirement Specifications (SRS), Mermaid UML diagrams, and normalized PostgreSQL schemas.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if "*" in settings.CORS_ORIGINS else settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health_router, prefix="/api")
app.include_router(api_router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to AI Software Architect API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/api/health",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
