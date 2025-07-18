from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.core.config import settings
from app.services.ai_service import generate_summary
from app.services.slack_service import fetch_channel_messages
from app.services.github_service import get_repository_data
from app.services.jira_service import get_project_issues, get_sprints

client = WebClient(token=settings.SLACK_BOT_TOKEN)

def post_summary_to_channel(channel_id: str, summary: str) -> bool:
    """
    Post a summary to a Slack channel.
    
    Args:
        channel_id: Slack channel ID
        summary: Summary text to post
    
    Returns:
        True if successful, False otherwise
    """
    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=f"📊 *Sprint Summary*\n\n{summary}",
            unfurl_links=False
        )
        return bool(response.get("ok", False))
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")
        return False

def post_weekly_summary(channel_id: str, days: int = 7) -> bool:
    """
    Generate and post a weekly summary to a Slack channel.
    
    Args:
        channel_id: Slack channel ID
        days: Number of days to look back
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Fetch Slack messages
        messages = fetch_channel_messages(channel_id, days)
        
        # Fetch GitHub data if configured
        github_data = None
        if settings.GITHUB_TOKEN and settings.GITHUB_REPO:
            github_data = get_repository_data(days)
        
        # Generate summary
        summary = generate_summary(messages, github_data)
        
        # Post to channel
        return post_summary_to_channel(channel_id, summary)
        
    except Exception as e:
        print(f"Error posting weekly summary: {e}")
        return False

def respond_to_mention(channel_id: str, user_id: str, text: str) -> str:
    """
    Generate a response to a bot mention.
    
    Args:
        channel_id: Slack channel ID
        user_id: User who mentioned the bot
        text: Message text
    
    Returns:
        Response text
    """
    try:
        # Parse the command
        text_lower = text.lower()
        
        if "summary" in text_lower or "report" in text_lower:
            # Generate summary for the current channel
            messages = fetch_channel_messages(channel_id, 7)
            github_data = None
            if settings.GITHUB_TOKEN and settings.GITHUB_REPO:
                github_data = get_repository_data(7)
            
            summary = generate_summary(messages, github_data)
            return f"📊 *Here's your summary:*\n\n{summary}"
        
        elif "help" in text_lower:
            return """🤖 *SprintLens Bot Commands:*
• `@SprintLens summary` - Generate a summary of recent activity
• `@SprintLens help` - Show this help message
• `@SprintLens weekly` - Post a comprehensive weekly summary to the channel"""
        
        elif "weekly" in text_lower:
            # Post weekly summary to channel
            success = post_weekly_summary(channel_id, 7)
            if success:
                return "✅ Weekly summary posted to the channel!"
            else:
                return "❌ Failed to post weekly summary. Please try again."
        
        else:
            return f"Hi <@{user_id}>! I'm SprintLens, your AI teammate. Type `@SprintLens help` to see what I can do."
            
    except Exception as e:
        print(f"Error responding to mention: {e}")
        return "❌ Sorry, I encountered an error. Please try again."

def post_status_update(channel_id: str, status: str, details: str = "") -> bool:
    """
    Post a status update to a Slack channel.
    
    Args:
        channel_id: Slack channel ID
        status: Status message
        details: Optional details
    
    Returns:
        True if successful, False otherwise
    """
    try:
        message = f"🔄 *Status Update:* {status}"
        if details:
            message += f"\n\n{details}"
        
        response = client.chat_postMessage(
            channel=channel_id,
            text=message,
            unfurl_links=False
        )
        return bool(response.get("ok", False))
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")
        return False 