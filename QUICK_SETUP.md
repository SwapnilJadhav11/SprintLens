# 🚀 Quick Setup Guide - Google Calendar

## ⚡ 5-Minute Setup

### 1. Get Google Credentials (2 minutes)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Calendar API → Create OAuth credentials
3. Download JSON → Rename to `credentials.json` → Place in `backend/`

### 2. Update Environment (1 minute)
Add to `backend/.env`:
```bash
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8001/api/calendar/auth/callback
```

### 3. Test Setup (2 minutes)
```bash
cd backend
python setup_calendar.py
```

## 🔗 Quick Links

- **Google Cloud Console**: https://console.cloud.google.com/
- **Calendar API**: https://console.cloud.google.com/apis/library/calendar-googleapis.googleapis.com
- **OAuth Credentials**: https://console.cloud.google.com/apis/credentials

## 🎯 What You Get

✅ **Calendar Events** in sprint summaries  
✅ **Meeting Analysis** with AI insights  
✅ **Busy Time Detection** for scheduling  
✅ **Event Creation** from the app  
✅ **Multi-calendar Support**  

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "credentials.json not found" | Download from Google Cloud Console |
| "Access denied" | Add email as test user in OAuth screen |
| "No calendars found" | Check Google Calendar has events |
| Token errors | Delete `token.pickle`, re-authenticate |

## 📞 Need Help?

- Check `GOOGLE_CALENDAR_SETUP.md` for detailed guide
- Run `python setup_calendar.py` for diagnostics
- Test with: `curl http://localhost:8001/api/calendar/calendars`

---

**Ready to enhance your sprint summaries with calendar data! 📅** 