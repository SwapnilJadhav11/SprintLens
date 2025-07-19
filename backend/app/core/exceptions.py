"""
Custom exceptions for SprintLens application.
"""
from typing import Optional

class SprintLensException(Exception):
    """Base exception for SprintLens application."""
    pass

class ConfigurationError(SprintLensException):
    """Raised when there's a configuration error."""
    pass

class AuthenticationError(SprintLensException):
    """Raised when authentication fails."""
    pass

class APIError(SprintLensException):
    """Raised when external API calls fail."""
    def __init__(self, message: str, status_code: Optional[int] = None, api_name: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.api_name = api_name
        super().__init__(self.message)

class SlackAPIError(APIError):
    """Raised when Slack API calls fail."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message, status_code, "Slack")

class GitHubAPIError(APIError):
    """Raised when GitHub API calls fail."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message, status_code, "GitHub")

class JiraAPIError(APIError):
    """Raised when Jira API calls fail."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message, status_code, "Jira")

class CalendarAPIError(APIError):
    """Raised when Google Calendar API calls fail."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message, status_code, "Google Calendar")

class OpenAIAPIError(APIError):
    """Raised when OpenAI API calls fail."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message, status_code, "OpenAI")

class DataValidationError(SprintLensException):
    """Raised when data validation fails."""
    pass

class RateLimitError(APIError):
    """Raised when API rate limits are exceeded."""
    pass 