from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.slack_service import fetch_channel_messages
from app.services.github_service import get_repository_data
from app.services.jira_service import get_project_issues, get_sprints
from app.services.ai_service import generate_summary

router = APIRouter()

class SummaryRequest(BaseModel):
    channel_id: str
    days: int = 7
    include_github: bool = False
    include_jira: bool = False
    jira_project_key: str | None = None

@router.post("/generate")
async def generate_sprint_summary(request: SummaryRequest):
    """
    Generate a comprehensive sprint summary from Slack, GitHub, and Jira data using AI.
    """
    try:
        # Fetch messages from Slack
        messages = fetch_channel_messages(request.channel_id, request.days)
        
        github_data = None
        jira_data = None
        
        # Fetch GitHub data if requested
        if request.include_github:
            github_data = get_repository_data(request.days)
        
        # Fetch Jira data if requested
        if request.include_jira and request.jira_project_key:
            jira_issues = get_project_issues(request.jira_project_key, request.days)
            jira_sprints = get_sprints(request.jira_project_key)
            jira_data = {
                "issues": jira_issues,
                "sprints": jira_sprints
            }
        
        if not messages and not github_data and not jira_data:
            return {"summary": "No data found for the specified time period."}
        
        # Generate comprehensive AI summary
        summary = generate_summary(messages, github_data, jira_data)
        
        return {"summary": summary}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

__all__ = ["router"] 