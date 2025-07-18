from fastapi import APIRouter, Query
from app.services.slack_service import fetch_channel_messages, list_channels

router = APIRouter()

@router.post("/connect")
def connect_slack():
    # Dummy implementation for MVP
    return {"message": "Slack connected (dummy)"}

@router.get("/messages")
def get_slack_messages(
    channel_id: str = Query(..., description="Slack channel ID"),
    days: int = Query(7, description="Number of days to look back")
):
    messages = fetch_channel_messages(channel_id, days)
    return {"messages": messages}

@router.get("/channels")
def get_channels():
    channels = list_channels()
    return {"channels": channels}

__all__ = ["router"]
