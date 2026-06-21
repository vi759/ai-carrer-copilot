from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.adapters.api.router import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Backend API for AI Career Copilot, built with Clean Architecture principles.",
    version="1.0.0"
)

# Configure CORS to allow the frontend to access endpoints
# We allow all origins for smooth local developer execution
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach API routers
app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the AI Career Copilot API.",
        "documentation": "/docs"
    }

@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "healthy"}
