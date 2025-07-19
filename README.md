# SprintLens 🚀

**AI-Powered Sprint Summary Tool** - Transform your team's productivity with intelligent insights from Slack, GitHub, Jira, and Google Calendar.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

### 🤖 **AI-Powered Intelligence**
- **GPT-3.5-turbo** integration for intelligent analysis
- **Contextual understanding** of team communications
- **Actionable insights** and recommendations
- **Multi-source data synthesis**

### 🔗 **Complete Platform Integration**
- **📱 Slack** - Messages, channels, and team communications
- **💻 GitHub** - Commits, PRs, issues, and development activity
- **📋 Jira** - Issues, projects, and sprint management
- **📅 Google Calendar** - Events, meetings, and scheduling

### 🎯 **Smart Features**
- **Automated summaries** with intelligent categorization
- **Slack bot** for instant responses and notifications
- **Real-time data** from all integrated platforms
- **Customizable analysis** periods (1-90 days)

### 🎨 **Modern UI/UX**
- **Responsive design** with TailwindCSS
- **Dark theme** for better readability
- **Real-time updates** and loading states
- **Interactive dashboard** with data visualization

## 🚀 Quick Start

### 📋 Prerequisites

- **Python 3.8+** for backend
- **Node.js 16+** for frontend
- **API Keys** for integrations (see configuration section)

### 🛠️ Installation

#### 1. **Clone Repository**
```bash
git clone https://github.com/yourusername/SprintLens.git
cd SprintLens
```

#### 2. **Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your API keys
```

#### 3. **Frontend Setup**
```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

#### 4. **Run Application**
```bash
# Terminal 1: Backend
cd backend
uvicorn app.main:app --reload --port 8001

# Terminal 2: Frontend
cd frontend
npm run dev
```

#### 5. **Access Application**
- 🌐 **Frontend**: http://localhost:5173
- 🔧 **Backend API**: http://localhost:8001
- 📚 **API Documentation**: http://localhost:8001/docs

## ⚙️ Configuration

### 🔑 Required API Keys

#### **OpenAI API**
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Create a new API key
3. Add to `.env`: `OPENAI_API_KEY=your_key_here`

#### **Slack API**
1. Create a [Slack App](https://api.slack.com/apps)
2. Add bot and user scopes
3. Install to workspace
4. Add tokens to `.env`:
   ```env
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_USER_TOKEN=xoxp-your-user-token
   ```

#### **GitHub API**
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Generate new token with `repo` scope
3. Add to `.env`:
   ```env
   GITHUB_TOKEN=your_github_token
   GITHUB_REPO=owner/repository-name
   ```

#### **Jira API** (Optional)
1. Generate API token from [Atlassian Account Settings](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Add to `.env`:
   ```env
   JIRA_SERVER=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@domain.com
   JIRA_API_TOKEN=your_jira_token
   ```

#### **Google Calendar API** (Optional)
1. Follow [Google Calendar Setup Guide](GOOGLE_CALENDAR_SETUP.md)
2. Download `credentials.json` to backend directory
3. Add to `.env`:
   ```env
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   GOOGLE_REDIRECT_URI=http://localhost:8001/api/calendar/auth/callback
   ```

### 📁 Environment Files

#### **Backend (.env)**
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

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
```

#### **Frontend (.env)**
```env
VITE_API_BASE_URL=http://localhost:8001
```

## 📚 API Documentation

### 🔗 Base URL
```
http://localhost:8001
```

### 📊 Core Endpoints

#### **Summary Generation**
```http
POST /api/summary/generate
Content-Type: application/json

{
  "channel_id": "C1234567890",
  "days": 7,
  "include_github": true,
  "include_jira": false,
  "include_calendar": true
}
```

#### **Health Check**
```http
GET /health
```

### 🔌 Integration Endpoints

#### **Slack**
- `GET /api/slack/channels` - List channels
- `GET /api/slack/messages?channel_id=C123&days=7` - Fetch messages

#### **GitHub**
- `GET /api/github/repository?days=7` - Repository data
- `POST /api/github/issues` - Create issues

#### **Jira**
- `GET /api/jira/projects` - List projects
- `GET /api/jira/issues?project_key=PROJ&days=7` - Fetch issues

#### **Calendar**
- `GET /api/calendar/calendars` - List calendars
- `GET /api/calendar/events?days=7` - Fetch events
- `POST /api/calendar/events` - Create events

#### **Bot**
- `POST /api/bot/respond` - Bot responses
- `POST /api/bot/post-summary` - Post to Slack

## 🎯 Usage Guide

### 1. **Initial Setup**
1. Configure all required API keys
2. Start both backend and frontend servers
3. Verify connectivity via health check

### 2. **Generate Your First Summary**
1. Open the dashboard at http://localhost:5173
2. Select a Slack channel from the dropdown
3. Choose which integrations to include (GitHub, Jira, Calendar)
4. Click "Generate Summary"
5. Review the AI-powered insights

### 3. **Understanding the Summary**
The AI analyzes your data and provides:
- **Key Accomplishments** - What the team achieved
- **Blockers & Issues** - Problems and challenges
- **Next Steps** - Actionable recommendations
- **Development Progress** - Code and project metrics

### 4. **Slack Bot Commands**
Use these commands in Slack:
- `@SprintLens summary` - Generate summary
- `@SprintLens status` - Check system status
- `@SprintLens help` - Show available commands

## 🚀 Deployment

### 🐳 Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build individually
docker build -t sprintlens-backend ./backend
docker build -t sprintlens-frontend ./frontend
```

### ☁️ Cloud Deployment

#### **Heroku**
```bash
# Backend
heroku create your-sprintlens-backend
git push heroku main

# Frontend
heroku create your-sprintlens-frontend
git push heroku main
```

#### **AWS/Azure/GCP**
- Use container services (ECS, AKS, GKE)
- Configure environment variables
- Set up load balancers and SSL

### 🔧 Production Configuration
```env
DEBUG=False
LOG_LEVEL=WARNING
# Add production API keys
# Configure CORS origins
# Set up monitoring and logging
```

## 🧪 Testing

### **Backend Tests**
```bash
cd backend
pytest
pytest --cov=app
```

### **Frontend Tests**
```bash
cd frontend
npm test
npm run test:coverage
```

### **Integration Tests**
```bash
# Test API endpoints
curl http://localhost:8001/health
curl http://localhost:8001/api/summary/generate
```

## 📁 Project Structure

```
SprintLens/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── core/           # Configuration, logging, exceptions
│   │   ├── models/         # Pydantic data models
│   │   ├── routers/        # API route handlers
│   │   ├── services/       # Business logic
│   │   └── main.py         # Application entry point
│   ├── tests/              # Test files
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile         # Docker configuration
│   └── setup_calendar.py  # Calendar setup script
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── docker-compose.yml      # Docker orchestration
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Development

### **Code Quality**
- **Type hints** throughout Python code
- **ESLint** and **Prettier** for JavaScript
- **Pydantic** for data validation
- **Comprehensive error handling**

### **Best Practices**
- **Environment-based configuration**
- **Proper logging** and monitoring
- **Security-first** API design
- **Comprehensive testing**
- **Documentation** for all endpoints

### **Contributing**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### **Common Issues**

#### **Backend Won't Start**
- Check Python version (3.8+)
- Verify all dependencies installed
- Check environment variables
- Review logs for errors

#### **API Errors**
- Verify API keys are correct
- Check network connectivity
- Review API rate limits
- Check service status pages

#### **Frontend Issues**
- Clear browser cache
- Check API base URL
- Verify CORS configuration
- Review browser console errors

### **Getting Help**
- Check the [Issues](https://github.com/yourusername/SprintLens/issues) page
- Review [API Documentation](http://localhost:8001/docs)
- Check [Setup Guides](GOOGLE_CALENDAR_SETUP.md)

## 📈 Roadmap

### **v1.1** - Enhanced Analytics
- [ ] Historical trend analysis
- [ ] Team performance metrics
- [ ] Sprint velocity tracking
- [ ] Custom report templates

### **v1.2** - Advanced Integrations
- [ ] Microsoft Teams integration
- [ ] Azure DevOps integration
- [ ] Linear integration
- [ ] Notion integration

### **v1.3** - Enterprise Features
- [ ] Multi-team support
- [ ] Role-based access control
- [ ] Audit logging
- [ ] SSO integration

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-3.5-turbo
- **FastAPI** for the excellent web framework
- **React** and **Vite** for the frontend
- **TailwindCSS** for the beautiful UI
- **All contributors** who make this project better

---

**Made with ❤️ for productive teams everywhere** 