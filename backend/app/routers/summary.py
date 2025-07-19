from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.services.slack_service import fetch_channel_messages
from app.services.github_service import get_repository_data
from app.services.jira_service import get_project_issues, get_sprints
from app.services.calendar_service import get_calendar_events, get_busy_times
from app.services.ai_service import generate_summary

router = APIRouter()

class SummaryRequest(BaseModel):
    channel_id: str
    days: int = 7
    include_github: bool = False
    include_jira: bool = False
    include_calendar: bool = False
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
        calendar_data = None
        
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
        
        # Fetch Calendar data if requested
        if request.include_calendar:
            try:
                calendar_events = get_calendar_events(request.days)
                calendar_busy = get_busy_times(request.days)
                calendar_data = {
                    "events": calendar_events,
                    "busy_times": calendar_busy
                }
            except Exception as e:
                print(f"Calendar error: {e}")
                calendar_data = {
                    "events": [],
                    "busy_times": []
                }
        
        if not messages and not github_data and not jira_data and not calendar_data:
            return {"summary": "No data found for the specified time period."}
        
        # If no Slack messages but we have other data, still generate summary
        if not messages and (github_data or jira_data or calendar_data):
            messages = []  # Empty list but continue with other data
        
        # Generate comprehensive AI summary
        summary = generate_summary(messages, github_data, jira_data, calendar_data)
        
        return {"summary": summary}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

__all__ = ["router"] 