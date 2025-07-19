# Google Calendar Integration Setup Guide

## 📋 Prerequisites
- Google Cloud Console access
- Python 3.12+
- SprintLens backend running

## 🚀 Step-by-Step Setup

### 1. Create Google Cloud Project

1. **Visit Google Cloud Console**
   ```
   https://console.cloud.google.com/
   ```

2. **Create New Project**
   - Click "Select a project" → "New Project"
   - Name: "SprintLens"
   - Click "Create"

### 2. Enable Google Calendar API

1. **Navigate to APIs & Services**
   - Go to "APIs & Services" → "Library"

2. **Enable Calendar API**
   - Search for "Google Calendar API"
   - Click on it and press "Enable"

### 3. Configure OAuth Consent Screen

1. **Go to OAuth Consent Screen**
   - Navigate to "APIs & Services" → "OAuth consent screen"

2. **Configure Settings**
   ```
   User Type: External
   App name: SprintLens
   User support email: your-email@example.com
   Developer contact information: your-email@example.com
   ```

3. **Add Scopes**
   - Click "Add or remove scopes"
   - Add these scopes:
     - `https://www.googleapis.com/auth/calendar.readonly`
     - `https://www.googleapis.com/auth/calendar.events`

4. **Add Test Users**
   - Add your email address as a test user

### 4. Create OAuth 2.0 Credentials

1. **Create Credentials**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client IDs"

2. **Configure OAuth Client**
   ```
   Application type: Desktop application
   Name: SprintLens Desktop Client
   ```

3. **Download Credentials**
   - Click "Download JSON"
   - Rename to `credentials.json`
   - Place in `backend/` directory

### 5. Update Environment Variables

Add to your `backend/.env` file:

```bash
# Google Calendar Configuration
GOOGLE_CLIENT_ID=your_client_id_from_json
GOOGLE_CLIENT_SECRET=your_client_secret_from_json
GOOGLE_REDIRECT_URI=http://localhost:8001/api/calendar/auth/callback
```

### 6. Install Dependencies

```bash
cd backend
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 7. Test the Integration

1. **Start the backend**
   ```bash
   uvicorn app.main:app --reload --port 8001
   ```

2. **Test calendar endpoints**
   ```bash
   # Get auth URL
   curl -X GET "http://localhost:8001/api/calendar/auth/url"
   
   # Get calendars (after authentication)
   curl -X GET "http://localhost:8001/api/calendar/calendars"
   
   # Get events
   curl -X GET "http://localhost:8001/api/calendar/events?days=7"
   ```

## 🔐 Authentication Flow

### First-Time Setup

1. **Get Authorization URL**
   ```bash
   curl -X GET "http://localhost:8001/api/calendar/auth/url"
   ```

2. **Authorize Application**
   - Open the returned URL in browser
   - Sign in with your Google account
   - Grant permissions to SprintLens

3. **Complete Authentication**
   - The app will create `token.pickle` file
   - This stores your access tokens securely

### Subsequent Uses

- The app will automatically use stored tokens
- Tokens refresh automatically when needed
- No manual intervention required

## 📊 Using Calendar in Summaries

### Enable Calendar in Frontend

1. **Check "Include Calendar" in dashboard**
2. **Generate summary with calendar data**
3. **View calendar events in AI summary**

### Calendar Data Included

- **Events**: Meeting details, descriptions, attendees
- **Busy Times**: When you're unavailable
- **Event Counts**: Number of meetings/events
- **Time Analysis**: Meeting patterns and schedules

## 🛠️ Troubleshooting

### Common Issues

1. **"Invalid credentials" error**
   - Check `credentials.json` is in backend directory
   - Verify client ID and secret in `.env`

2. **"Access denied" error**
   - Add your email as test user in OAuth consent screen
   - Ensure Calendar API is enabled

3. **"No calendars found"**
   - Check you have calendars in Google Calendar
   - Verify authentication completed successfully

4. **Token refresh issues**
   - Delete `token.pickle` file
   - Re-authenticate through the auth URL

### Debug Commands

```bash
# Check if credentials are loaded
curl -X GET "http://localhost:8001/debug/config"

# Test calendar service directly
python -c "
from app.services.calendar_service import get_calendar_list
print(get_calendar_list())
"
```

## 🔒 Security Notes

- `credentials.json` contains sensitive data - keep secure
- `token.pickle` stores access tokens - don't share
- Add both files to `.gitignore`
- Use environment variables for production

## 🚀 Production Deployment

For production, update the redirect URI:

```bash
GOOGLE_REDIRECT_URI=https://your-domain.com/api/calendar/auth/callback
```

And update OAuth consent screen with production domain.

---

**Your Google Calendar integration is now ready! 🎉** 