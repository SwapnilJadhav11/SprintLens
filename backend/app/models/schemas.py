"""
Pydantic models for SprintLens API.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

# Summary Generation Models
class SummaryRequest(BaseModel):
    channel_id: str = Field(..., description="Slack channel ID")
    days: int = Field(default=7, ge=1, le=90, description="Number of days to analyze")
    include_github: bool = Field(default=False, description="Include GitHub data")
    include_jira: bool = Field(default=False, description="Include Jira data")
    include_calendar: bool = Field(default=False, description="Include calendar data")
    jira_project_key: Optional[str] = Field(None, description="Jira project key")

class SummaryResponse(BaseModel):
    summary: str = Field(..., description="Generated summary text")
    data_sources: List[str] = Field(..., description="Data sources used")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Slack Models
class SlackMessage(BaseModel):
    user: str
    text: str
    timestamp: str
    channel: str

class SlackChannel(BaseModel):
    id: str
    name: str
    is_private: bool = False
    member_count: Optional[int] = None

class SlackChannelsResponse(BaseModel):
    channels: List[SlackChannel]

class SlackMessagesResponse(BaseModel):
    messages: List[SlackMessage]

# GitHub Models
class GitHubCommit(BaseModel):
    sha: str
    message: str
    author: str
    date: str
    url: str

class GitHubPullRequest(BaseModel):
    number: int
    title: str
    state: str
    author: str
    created_at: str
    merged_at: Optional[str] = None
    url: str

class GitHubIssue(BaseModel):
    number: int
    title: str
    state: str
    author: str
    created_at: str
    labels: List[str] = []
    url: str

class GitHubRepositoryData(BaseModel):
    commits: List[GitHubCommit] = []
    pull_requests: List[GitHubPullRequest] = []
    issues: List[GitHubIssue] = []
    total_commits: int = 0
    total_prs: int = 0
    total_issues: int = 0

class GitHubIssueRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)
    labels: List[str] = Field(default=[])

# Jira Models
class JiraProject(BaseModel):
    key: str
    name: str
    project_type_key: str
    lead: Optional[str] = None

class JiraIssue(BaseModel):
    key: str
    summary: str
    status: str
    priority: Optional[str] = None
    assignee: Optional[str] = None
    created: str
    updated: str
    issue_type: str

class JiraProjectsResponse(BaseModel):
    projects: List[JiraProject]

class JiraIssuesResponse(BaseModel):
    issues: List[JiraIssue]

# Calendar Models
class CalendarEvent(BaseModel):
    id: str
    summary: str
    description: Optional[str] = None
    start: str
    end: str
    location: Optional[str] = None
    attendees: List[str] = []
    organizer: Optional[str] = None
    html_link: Optional[str] = None

class Calendar(BaseModel):
    id: str
    summary: str
    description: Optional[str] = None
    primary: bool = False
    access_role: str

class CalendarEventRequest(BaseModel):
    summary: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    start_time: str = Field(..., description="ISO 8601 datetime string")
    end_time: str = Field(..., description="ISO 8601 datetime string")
    calendar_id: str = Field(default="primary")
    attendees: List[str] = Field(default=[])

    @field_validator('start_time', 'end_time')
    @classmethod
    def validate_datetime(cls, v):
        try:
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            raise ValueError('Invalid datetime format. Use ISO 8601 format.')

class CalendarsResponse(BaseModel):
    calendars: List[Calendar]

class CalendarEventsResponse(BaseModel):
    events: List[CalendarEvent]

# Bot Models
class BotRequest(BaseModel):
    channel_id: str
    user_id: str
    text: str

class BotResponse(BaseModel):
    response: str

class PostSummaryRequest(BaseModel):
    channel_id: str
    summary: str

class WeeklySummaryRequest(BaseModel):
    channel_id: str
    days: int = Field(default=7, ge=1, le=90)

# Health Check Model
class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "1.0.0"
    services: Dict[str, str] = Field(default_factory=dict) 