from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from app.services.jira_service import get_projects, get_project_issues, get_sprints, create_jira_issue, get_sprint_issues

router = APIRouter()

class JiraIssueRequest(BaseModel):
    project_key: str
    summary: str
    description: str
    issue_type: str = "Task"

@router.get("/projects")
def get_jira_projects():
    """
    Fetch all accessible Jira projects.
    """
    try:
        projects = get_projects()
        return {"projects": projects}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Jira projects: {str(e)}")

@router.get("/issues")
def get_jira_issues(project_key: str = Query(..., description="Jira project key"), 
                   days: int = Query(7, description="Number of days to look back")):
    """
    Fetch recent issues from a specific Jira project.
    """
    try:
        issues = get_project_issues(project_key, days)
        return {"issues": issues}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Jira issues: {str(e)}")

@router.get("/sprints")
def get_jira_sprints(project_key: str = Query(..., description="Jira project key")):
    """
    Fetch sprints for a specific Jira project.
    """
    try:
        sprints = get_sprints(project_key)
        return {"sprints": sprints}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Jira sprints: {str(e)}")

@router.get("/sprints/{sprint_id}/issues")
def get_sprint_issues_endpoint(sprint_id: int):
    """
    Fetch all issues in a specific sprint.
    """
    try:
        issues = get_sprint_issues(sprint_id)
        return {"issues": issues}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sprint issues: {str(e)}")

@router.post("/issues")
def create_jira_issue_endpoint(request: JiraIssueRequest):
    """
    Create a new Jira issue.
    """
    try:
        result = create_jira_issue(request.project_key, request.summary, request.description, request.issue_type)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating Jira issue: {str(e)}")

__all__ = ["router"] 