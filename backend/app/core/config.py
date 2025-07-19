from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Slack Configuration
    SLACK_BOT_TOKEN: str = ""
    SLACK_USER_TOKEN: str = ""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    
    # GitHub Configuration
    GITHUB_TOKEN: str = ""
    GITHUB_REPO: str = ""
    
    # Jira Configuration
    JIRA_SERVER: str = ""
    JIRA_EMAIL: str = ""
    JIRA_API_TOKEN: str = ""
    
    # Google Calendar Configuration
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8001/api/calendar/auth/callback"
    
    # Application Configuration
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
