# SprintLens Backend

AI-powered sprint summary tool backend with integrations for Slack, GitHub, Jira, and Google Calendar.

## 🚀 Features

- **Slack Integration**: Fetch messages and channels
- **GitHub Integration**: Commits, PRs, issues, and repository data
- **Jira Integration**: Issues, projects, and sprint management
- **Google Calendar Integration**: Events, meetings, and scheduling
- **AI-Powered Summaries**: GPT-3.5-turbo for intelligent analysis
- **Slack Bot**: Automated responses and notifications
- **RESTful API**: FastAPI-based endpoints

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key
- Slack API credentials
- GitHub Personal Access Token
- Jira API credentials (optional)
- Google Calendar API credentials (optional)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SprintLens/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_USER_TOKEN=xoxp-your-user-token

# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=owner/repository-name

# Jira Configuration (Optional)
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@domain.com
JIRA_API_TOKEN=your_jira_api_token

# Google Calendar Configuration (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8001/api/calendar/auth/callback
```

### Google Calendar Setup

1. Download `credentials.json` from Google Cloud Console
2. Place it in the backend directory
3. Run the setup script:
   ```bash
   python setup_calendar.py
   ```

## 📚 API Documentation

### Base URL
```
http://localhost:8001
```

### Health Check
```
GET /health
```

### Summary Generation
```
POST /api/summary/generate
```

### Slack Endpoints
- `GET /api/slack/channels` - List Slack channels
- `GET /api/slack/messages` - Fetch channel messages

### GitHub Endpoints
- `GET /api/github/repository` - Repository data
- `POST /api/github/issues` - Create issues

### Jira Endpoints
- `GET /api/jira/projects` - List projects
- `GET /api/jira/issues` - Fetch issues

### Calendar Endpoints
- `GET /api/calendar/calendars` - List calendars
- `GET /api/calendar/events` - Fetch events
- `POST /api/calendar/events` - Create events

### Bot Endpoints
- `POST /api/bot/respond` - Bot responses
- `POST /api/bot/post-summary` - Post to Slack

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 🚀 Deployment

### Docker
```bash
docker build -t sprintlens-backend .
docker run -p 8001:8001 sprintlens-backend
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── core/           # Configuration and settings
│   ├── models/         # Data models
│   ├── routers/        # API route handlers
│   ├── services/       # Business logic
│   └── main.py         # Application entry point
├── tests/              # Test files
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── setup_calendar.py  # Calendar setup script
└── README.md          # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details 