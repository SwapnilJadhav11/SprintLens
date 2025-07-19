"""
Health check endpoints for SprintLens API.
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import HealthResponse
from app.core.logging import logger
from app.core.config import settings
import requests
from typing import Dict

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify application status and service connectivity.
    """
    try:
        services = {}
        
        # Check OpenAI API
        if settings.OPENAI_API_KEY:
            services["openai"] = "configured"
        else:
            services["openai"] = "not_configured"
        
        # Check Slack API
        if settings.SLACK_BOT_TOKEN:
            services["slack"] = "configured"
        else:
            services["slack"] = "not_configured"
        
        # Check GitHub API
        if settings.GITHUB_TOKEN:
            services["github"] = "configured"
        else:
            services["github"] = "not_configured"
        
        # Check Jira API
        if settings.JIRA_SERVER and settings.JIRA_API_TOKEN:
            services["jira"] = "configured"
        else:
            services["jira"] = "not_configured"
        
        # Check Google Calendar API
        if settings.GOOGLE_CLIENT_ID and settings.GOOGLE_CLIENT_SECRET:
            services["calendar"] = "configured"
        else:
            services["calendar"] = "not_configured"
        
        logger.info("Health check completed successfully")
        
        return HealthResponse(
            status="healthy",
            services=services
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

@router.get("/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes deployments.
    """
    try:
        # Check if essential services are configured
        if not settings.OPENAI_API_KEY:
            raise HTTPException(status_code=503, detail="OpenAI API not configured")
        
        if not settings.SLACK_BOT_TOKEN:
            raise HTTPException(status_code=503, detail="Slack API not configured")
        
        logger.info("Readiness check passed")
        return {"status": "ready"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service not ready")

@router.get("/live")
async def liveness_check():
    """
    Liveness check for Kubernetes deployments.
    """
    return {"status": "alive"} 