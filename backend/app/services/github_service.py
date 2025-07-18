from github import Github
from app.core.config import settings
from typing import List, Dict
from datetime import datetime, timedelta

# Initialize GitHub client
github_client = None

def get_github_client():
    """Initialize and return GitHub client."""
    global github_client
    if github_client is None and settings.GITHUB_TOKEN:
        try:
            github_client = Github(settings.GITHUB_TOKEN)
        except Exception as e:
            print(f"GitHub connection error: {e}")
            return None
    return github_client

def get_repository_data(days: int = 7) -> Dict:
    """
    Fetch comprehensive repository data for the specified time period.
    
    Args:
        days: Number of days to look back
    
    Returns:
        Dictionary containing PRs, issues, commits, and releases
    """
    client = get_github_client()
    if not client:
        return {"error": "GitHub credentials not configured"}
    
    try:
        repo = client.get_repo(settings.GITHUB_REPO)
        since_date = datetime.now() - timedelta(days=days)
        
        # Fetch recent pull requests
        pull_requests = []
        try:
            for pr in repo.get_pulls(state='all'):
                if pr.created_at >= since_date:
                    pull_requests.append({
                        "number": pr.number,
                        "title": pr.title,
                        "state": pr.state,
                        "created_at": pr.created_at.isoformat(),
                        "user": pr.user.login,
                        "url": pr.html_url
                    })
        except Exception as e:
            print(f"Error fetching pull requests: {e}")
        
        # Fetch recent issues
        issues = []
        try:
            for issue in repo.get_issues(state='all'):
                if issue.created_at >= since_date:
                    issues.append({
                        "number": issue.number,
                        "title": issue.title,
                        "state": issue.state,
                        "created_at": issue.created_at.isoformat(),
                        "user": issue.user.login,
                        "labels": [label.name for label in issue.labels],
                        "url": issue.html_url
                    })
        except Exception as e:
            print(f"Error fetching issues: {e}")
        
        # Fetch recent commits
        commits = []
        try:
            for commit in repo.get_commits(since=since_date):
                commits.append({
                    "sha": commit.sha[:7],
                    "message": commit.commit.message,
                    "author": commit.commit.author.name,
                    "date": commit.commit.author.date.isoformat(),
                    "url": commit.html_url
                })
        except Exception as e:
            if "Git Repository is empty" in str(e):
                print("Repository is empty - no commits to fetch")
            else:
                print(f"Error fetching commits: {e}")
        
        # Fetch recent releases
        releases = []
        for release in repo.get_releases():
            if release.created_at >= since_date:
                releases.append({
                    "tag_name": release.tag_name,
                    "name": release.title,
                    "body": release.body,
                    "created_at": release.created_at.isoformat(),
                    "url": release.html_url
                })
        
        return {
            "pull_requests": pull_requests,
            "issues": issues,
            "commits": commits,
            "releases": releases,
            "repository": {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "url": repo.html_url
            }
        }
        
    except Exception as e:
        print(f"GitHub API error: {e}")
        return {"error": f"Failed to fetch GitHub data: {str(e)}"}

def create_issue(title: str, body: str, labels: List[str] | None = None) -> Dict:
    """
    Create a new GitHub issue.
    
    Args:
        title: Issue title
        body: Issue description
        labels: List of labels to apply
    
    Returns:
        Created issue data or error
    """
    client = get_github_client()
    if not client:
        return {"error": "GitHub credentials not configured"}
    
    try:
        repo = client.get_repo(settings.GITHUB_REPO)
        issue = repo.create_issue(
            title=title,
            body=body,
            labels=labels if labels else []
        )
        
        return {
            "number": issue.number,
            "title": issue.title,
            "url": issue.html_url,
            "state": issue.state
        }
        
    except Exception as e:
        print(f"GitHub API error: {e}")
        return {"error": f"Failed to create issue: {str(e)}"}

def generate_release_notes(since_date: datetime | None = None) -> str:
    """
    Generate release notes from recent commits and PRs.
    
    Args:
        since_date: Date to look back from (default: last 7 days)
    
    Returns:
        Formatted release notes
    """
    if since_date is None:
        since_date = datetime.now() - timedelta(days=7)
    
    repo_data = get_repository_data()
    if "error" in repo_data:
        return f"Error: {repo_data['error']}"
    
    notes = []
    notes.append("# Release Notes\n")
    
    # Add new features from merged PRs
    new_features = [pr for pr in repo_data["pull_requests"] if pr["state"] == "closed"]
    if new_features:
        notes.append("## New Features")
        for pr in new_features:
            notes.append(f"- {pr['title']} (#{pr['number']})")
        notes.append("")
    
    # Add bug fixes from issues
    bug_fixes = [issue for issue in repo_data["issues"] if issue["state"] == "closed" and "bug" in [label.lower() for label in issue["labels"]]]
    if bug_fixes:
        notes.append("## Bug Fixes")
        for issue in bug_fixes:
            notes.append(f"- {issue['title']} (#{issue['number']})")
        notes.append("")
    
    # Add recent commits
    if repo_data["commits"]:
        notes.append("## Recent Commits")
        for commit in repo_data["commits"][:10]:  # Last 10 commits
            notes.append(f"- {commit['message'].split('\n')[0]} ({commit['sha']})")
    
    return "\n".join(notes) 