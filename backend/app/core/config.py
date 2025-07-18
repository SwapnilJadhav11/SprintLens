from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SLACK_BOT_TOKEN: str = ""
    OPENAI_API_KEY: str = ""
    GITHUB_TOKEN: str = ""
    GITHUB_REPO: str = ""
    JIRA_SERVER: str = ""
    JIRA_EMAIL: str = ""
    JIRA_API_TOKEN: str = ""
    # Add more as needed

    class Config:
        env_file = ".env"

settings = Settings()
