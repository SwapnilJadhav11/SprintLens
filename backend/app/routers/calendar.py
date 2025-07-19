from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from app.services.calendar_service import get_calendar_events, get_calendar_list, get_busy_times, create_calendar_event
from typing import List, Optional

router = APIRouter()

class CalendarEventRequest(BaseModel):
    summary: str
    description: str
    start_time: str
    end_time: str
    calendar_id: str = "primary"
    attendees: Optional[List[str]] = None

@router.get("/events")
def get_events(days: int = Query(7, description="Number of days to look back"),
               calendar_id: str = Query("primary", description="Calendar ID")):
    """
    Fetch calendar events for the specified period.
    """
    try:
        events = get_calendar_events(days, calendar_id)
        return {"events": events}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching calendar events: {str(e)}")

@router.get("/calendars")
def get_calendars():
    """
    Get list of available calendars.
    """
    try:
        calendars = get_calendar_list()
        return {"calendars": calendars}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching calendars: {str(e)}")

@router.get("/busy-times")
def get_busy_times_endpoint(days: int = Query(7, description="Number of days to look back"),
                           calendar_id: str = Query("primary", description="Calendar ID")):
    """
    Get busy time slots for the specified period.
    """
    try:
        busy_times = get_busy_times(days, calendar_id)
        return {"busy_times": busy_times}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching busy times: {str(e)}")

@router.post("/events")
def create_event(request: CalendarEventRequest):
    """
    Create a new calendar event.
    """
    try:
        result = create_calendar_event(
            request.summary,
            request.description,
            request.start_time,
            request.end_time,
            request.calendar_id,
            request.attendees
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating calendar event: {str(e)}")

@router.get("/auth/url")
def get_auth_url():
    """
    Get Google OAuth authorization URL.
    """
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
        from app.core.config import settings
        
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar.readonly']
        )
        
        auth_url, _ = flow.authorization_url(prompt='consent')
        return {"auth_url": auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating auth URL: {str(e)}")

__all__ = ["router"] 