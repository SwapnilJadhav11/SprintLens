from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.slack_bot_service import post_summary_to_channel, post_weekly_summary, respond_to_mention

router = APIRouter()

class PostSummaryRequest(BaseModel):
    channel_id: str
    summary: str

class WeeklySummaryRequest(BaseModel):
    channel_id: str
    days: int = 7

class BotMentionRequest(BaseModel):
    channel_id: str
    user_id: str
    text: str

@router.post("/post-summary")
def post_summary(request: PostSummaryRequest):
    """
    Post a summary to a Slack channel.
    """
    try:
        success = post_summary_to_channel(request.channel_id, request.summary)
        if success:
            return {"message": "Summary posted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to post summary")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting summary: {str(e)}")

@router.post("/weekly-summary")
def post_weekly_summary_endpoint(request: WeeklySummaryRequest):
    """
    Generate and post a weekly summary to a Slack channel.
    """
    try:
        success = post_weekly_summary(request.channel_id, request.days)
        if success:
            return {"message": "Weekly summary posted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to post weekly summary")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error posting weekly summary: {str(e)}")

@router.post("/respond")
def respond_to_mention_endpoint(request: BotMentionRequest):
    """
    Generate a response to a bot mention.
    """
    try:
        response = respond_to_mention(request.channel_id, request.user_id, request.text)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

__all__ = ["router"] 