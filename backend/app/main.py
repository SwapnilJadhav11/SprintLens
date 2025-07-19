"""
SprintLens FastAPI Application
AI-powered sprint summary tool with integrations for Slack, GitHub, Jira, and Google Calendar.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import logger, setup_logging
from app.core.exceptions import SprintLensException, APIError
from app.routers.slack import router as slack_router
from app.routers.summary import router as summary_router
from app.routers.github import router as github_router
from app.routers.jira import router as jira_router
from app.routers.bot import router as bot_router
from app.routers.calendar import router as calendar_router
from app.routers.health import router as health_router

# Setup logging
setup_logging(settings.LOG_LEVEL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting SprintLens API...")
    logger.info(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
    
    # Check essential configurations
    if not settings.OPENAI_API_KEY:
        logger.warning("OpenAI API key not configured")
    if not settings.SLACK_BOT_TOKEN:
        logger.warning("Slack bot token not configured")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SprintLens API...")

# Create FastAPI app
app = FastAPI(
    title="SprintLens API",
    description="AI-powered sprint summary tool with multi-platform integrations",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React dev server
        "http://localhost:8080",  # Alternative dev server
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers
@app.exception_handler(SprintLensException)
async def sprintlens_exception_handler(request, exc):
    """Handle SprintLens custom exceptions."""
    logger.error(f"SprintLens exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

@app.exception_handler(APIError)
async def api_error_handler(request, exc):
    """Handle API-specific exceptions."""
    logger.error(f"API error ({exc.api_name}): {str(exc)}")
    return JSONResponse(
        status_code=exc.status_code or 500,
        content={
            "detail": str(exc),
            "api": exc.api_name,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Include routers
app.include_router(health_router, tags=["health"])
app.include_router(slack_router, prefix="/api/slack", tags=["slack"])
app.include_router(summary_router, prefix="/api/summary", tags=["summary"])
app.include_router(github_router, prefix="/api/github", tags=["github"])
app.include_router(jira_router, prefix="/api/jira", tags=["jira"])
app.include_router(bot_router, prefix="/api/bot", tags=["bot"])
app.include_router(calendar_router, prefix="/api/calendar", tags=["calendar"])

@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "SprintLens API is running!",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
        "health": "/health"
    }

@app.get("/api", tags=["api"])
async def api_info():
    """API information endpoint."""
    return {
        "name": "SprintLens API",
        "version": "1.0.0",
        "description": "AI-powered sprint summary tool",
        "integrations": [
            "Slack",
            "GitHub", 
            "Jira",
            "Google Calendar"
        ],
        "endpoints": {
            "health": "/health",
            "slack": "/api/slack",
            "github": "/api/github",
            "jira": "/api/jira",
            "calendar": "/api/calendar",
            "bot": "/api/bot",
            "summary": "/api/summary"
        }
    }

@app.get("/debug/config", tags=["debug"])
def debug_config():
    """Debug endpoint to check environment variables (remove in production)"""
    if not settings.DEBUG:
        raise HTTPException(status_code=404, detail="Debug endpoint disabled in production")
    
    return {
        "slack_configured": bool(settings.SLACK_BOT_TOKEN),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "github_configured": bool(settings.GITHUB_TOKEN),
        "github_repo": settings.GITHUB_REPO,
        "jira_configured": bool(settings.JIRA_SERVER and settings.JIRA_EMAIL and settings.JIRA_API_TOKEN),
        "calendar_configured": bool(settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET)
    }
