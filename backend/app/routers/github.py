from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from app.services.github_service import get_repository_data, create_issue, generate_release_notes

router = APIRouter()

class IssueRequest(BaseModel):
    title: str
    body: str
    labels: list[str] | None = None

@router.get("/repository")
def get_github_data(days: int = Query(7, description="Number of days to look back")):
    """
    Fetch comprehensive GitHub repository data.
    """
    try:
        data = get_repository_data(days)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching GitHub data: {str(e)}")

@router.post("/issues")
def create_github_issue(request: IssueRequest):
    """
    Create a new GitHub issue.
    """
    try:
        result = create_issue(request.title, request.body, request.labels)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating GitHub issue: {str(e)}")

@router.get("/release-notes")
def get_release_notes(days: int = Query(7, description="Number of days to look back")):
    """
    Generate release notes from recent repository activity.
    """
    try:
        notes = generate_release_notes()
        return {"release_notes": notes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating release notes: {str(e)}")

__all__ = ["router"] 