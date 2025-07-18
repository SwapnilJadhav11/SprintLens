from jira import JIRA
from app.core.config import settings
from typing import List, Dict
from datetime import datetime, timedelta

# Initialize Jira client
jira_client = None

def get_jira_client():
    """Initialize and return Jira client."""
    global jira_client
    if jira_client is None and settings.JIRA_SERVER and settings.JIRA_EMAIL and settings.JIRA_API_TOKEN:
        try:
            jira_client = JIRA(
                server=settings.JIRA_SERVER,
                basic_auth=(settings.JIRA_EMAIL, settings.JIRA_API_TOKEN)
            )
        except Exception as e:
            print(f"Jira connection error: {e}")
            return None
    return jira_client

def get_projects() -> List[Dict]:
    """
    Fetch all accessible Jira projects.
    
    Returns:
        List of project dictionaries
    """
    client = get_jira_client()
    if not client:
        return []
    
    try:
        projects = client.projects()
        return [
            {
                "key": project.key,
                "name": project.name,
                "id": project.id
            }
            for project in projects
        ]
    except Exception as e:
        print(f"Jira API error: {e}")
        return []

def get_project_issues(project_key: str, days: int = 7) -> List[Dict]:
    """
    Fetch recent issues from a specific project.
    
    Args:
        project_key: Jira project key
        days: Number of days to look back
    
    Returns:
        List of issue dictionaries
    """
    client = get_jira_client()
    if not client:
        return []
    
    try:
        since_date = datetime.now() - timedelta(days=days)
        jql = f"project = {project_key} AND created >= '{since_date.strftime('%Y-%m-%d')}' ORDER BY created DESC"
        
        issues = client.search_issues(jql, maxResults=50)
        
        return [
            {
                "key": issue.key,  # type: ignore
                "summary": issue.fields.summary,  # type: ignore
                "status": issue.fields.status.name,  # type: ignore
                "priority": issue.fields.priority.name if issue.fields.priority else "None",  # type: ignore
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",  # type: ignore
                "reporter": issue.fields.reporter.displayName,  # type: ignore
                "created": issue.fields.created,  # type: ignore
                "updated": issue.fields.updated,  # type: ignore
                "issue_type": issue.fields.issuetype.name,  # type: ignore
                "url": f"{settings.JIRA_SERVER}/browse/{issue.key}"  # type: ignore
            }
            for issue in issues
        ]
    except Exception as e:
        print(f"Jira API error: {e}")
        return []

def get_sprints(project_key: str) -> List[Dict]:
    """
    Fetch sprints for a specific project.
    
    Args:
        project_key: Jira project key
    
    Returns:
        List of sprint dictionaries
    """
    client = get_jira_client()
    if not client:
        return []
    
    try:
        # Get the board for the project
        boards = client.boards(projectKeyOrID=project_key)
        if not boards:
            return []
        
        board = boards[0]  # Use the first board
        sprints = client.sprints(board.id)
        
        return [
            {
                "id": sprint.id,
                "name": sprint.name,
                "state": sprint.state,
                "start_date": sprint.startDate,
                "end_date": sprint.endDate,
                "goal": sprint.goal
            }
            for sprint in sprints
        ]
    except Exception as e:
        print(f"Jira API error: {e}")
        return []

def create_jira_issue(project_key: str, summary: str, description: str, issue_type: str = "Task") -> Dict:
    """
    Create a new Jira issue.
    
    Args:
        project_key: Jira project key
        summary: Issue summary/title
        description: Issue description
        issue_type: Type of issue (Task, Bug, Story, etc.)
    
    Returns:
        Created issue data or error
    """
    client = get_jira_client()
    if not client:
        return {"error": "Jira client not configured"}
    
    try:
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        
        new_issue = client.create_issue(fields=issue_dict)
        
        return {
            "key": new_issue.key,
            "summary": new_issue.fields.summary,
            "url": f"{settings.JIRA_SERVER}/browse/{new_issue.key}",
            "status": new_issue.fields.status.name
        }
        
    except Exception as e:
        print(f"Jira API error: {e}")
        return {"error": f"Failed to create Jira issue: {str(e)}"}

def get_sprint_issues(sprint_id: int) -> List[Dict]:
    """
    Fetch all issues in a specific sprint.
    
    Args:
        sprint_id: Jira sprint ID
    
    Returns:
        List of issue dictionaries
    """
    client = get_jira_client()
    if not client:
        return []
    
    try:
        sprint = client.sprint(sprint_id)
        issues = client.search_issues(f"sprint = {sprint_id}")
        
        return [
            {
                "key": issue.key,  # type: ignore
                "summary": issue.fields.summary,  # type: ignore
                "status": issue.fields.status.name,  # type: ignore
                "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned",  # type: ignore
                "story_points": issue.fields.customfield_10016 if hasattr(issue.fields, 'customfield_10016') else None,  # type: ignore
                "url": f"{settings.JIRA_SERVER}/browse/{issue.key}"  # type: ignore
            }
            for issue in issues
        ]
    except Exception as e:
        print(f"Jira API error: {e}")
        return [] 