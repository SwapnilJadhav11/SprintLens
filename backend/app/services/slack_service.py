from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.core.config import settings

client = WebClient(token=settings.SLACK_BOT_TOKEN)

def fetch_channel_messages(channel_id: str, days: int = 7):
    from datetime import datetime, timedelta
    import time
    messages = []
    oldest = str(time.mktime((datetime.now() - timedelta(days=days)).timetuple()))
    try:
        response = client.conversations_history(
            channel=channel_id,
            oldest=oldest,
            limit=200
        )
        for msg in response.get("messages", []) or []:
            # Filter out bot messages
            if msg.get("subtype") == "bot_message":
                continue
            messages.append({
                "user": msg.get("user"),
                "timestamp": msg.get("ts"),
                "text": msg.get("text")
            })
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")
    return messages

def list_channels():
    try:
        response = client.conversations_list(types="public_channel,private_channel")
        return [
            {"id": ch["id"], "name": ch["name"]}
            for ch in response.get("channels", [])
        ]
    except SlackApiError as e:
        print(f"Slack API error: {e.response['error']}")
        return []
