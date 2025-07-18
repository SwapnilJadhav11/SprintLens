from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.slack import router as slack_router
from app.routers.summary import router as summary_router
from app.routers.github import router as github_router
from app.routers.jira import router as jira_router
from app.routers.bot import router as bot_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "SprintLens backend is running!"}

@app.get("/debug/config")
def debug_config():
    """Debug endpoint to check environment variables (remove in production)"""
    return {
        "slack_configured": bool(settings.SLACK_BOT_TOKEN),
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "github_configured": bool(settings.GITHUB_TOKEN),
        "github_repo": settings.GITHUB_REPO,
        "jira_configured": bool(settings.JIRA_SERVER and settings.JIRA_EMAIL and settings.JIRA_API_TOKEN)
    }

app.include_router(slack_router, prefix="/api/slack")
app.include_router(summary_router, prefix="/api/summary")
app.include_router(github_router, prefix="/api/github")
app.include_router(jira_router, prefix="/api/jira")
app.include_router(bot_router, prefix="/api/bot")
