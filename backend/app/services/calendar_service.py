from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from app.core.config import settings
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import os
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_calendar_service():
    """Get Google Calendar service with proper authentication."""
    creds = None
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        raise FileNotFoundError("credentials.json not found. Please download from Google Cloud Console.")
    
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        try:
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"Error loading token.pickle: {e}")
            creds = None
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None
        
        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            except Exception as e:
                raise Exception(f"Authentication failed: {e}")

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_calendar_events(days: int = 7, calendar_id: str = 'primary') -> List[Dict]:
    """Fetch calendar events for the specified number of days (past and future)."""
    try:
        service = get_calendar_service()
        
        # Calculate time range - include past and future events
        now = datetime.utcnow()
        time_min = (now - timedelta(days=days//2)).isoformat() + 'Z'  # Past events
        time_max = (now + timedelta(days=days//2)).isoformat() + 'Z'  # Future events
        
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            formatted_events.append({
                'id': event['id'],
                'summary': event.get('summary', 'No Title'),
                'description': event.get('description', ''),
                'start': start,
                'end': end,
                'location': event.get('location', ''),
                'attendees': [attendee.get('email') for attendee in event.get('attendees', [])],
                'organizer': event.get('organizer', {}).get('email', ''),
                'html_link': event.get('htmlLink', '')
            })
        
        return formatted_events
        
    except Exception as e:
        print(f"Google Calendar API error: {e}")
        return []

def get_calendar_list() -> List[Dict]:
    """Get list of available calendars."""
    try:
        service = get_calendar_service()
        calendar_list = service.calendarList().list().execute()
        
        calendars = []
        for calendar in calendar_list.get('items', []):
            calendars.append({
                'id': calendar['id'],
                'summary': calendar['summary'],
                'description': calendar.get('description', ''),
                'primary': calendar.get('primary', False),
                'access_role': calendar.get('accessRole', '')
            })
        
        return calendars
        
    except Exception as e:
        print(f"Google Calendar API error: {e}")
        return []

def get_busy_times(days: int = 7, calendar_id: str = 'primary') -> List[Dict]:
    """Get busy time slots for the specified period."""
    try:
        service = get_calendar_service()
        
        # Calculate time range
        now = datetime.utcnow()
        time_min = now.isoformat() + 'Z'
        time_max = (now + timedelta(days=days)).isoformat() + 'Z'
        
        body = {
            'timeMin': time_min,
            'timeMax': time_max,
            'items': [{'id': calendar_id}]
        }
        
        events_result = service.freebusy().query(body=body).execute()
        busy_times = events_result['calendars'][calendar_id]['busy']
        
        return busy_times
        
    except Exception as e:
        print(f"Google Calendar API error: {e}")
        return []

def create_calendar_event(summary: str, description: str, start_time: str, end_time: str, 
                         calendar_id: str = 'primary', attendees: Optional[List[str]] = None) -> Dict:
    """Create a new calendar event."""
    try:
        service = get_calendar_service()
        
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
        }
        
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]
        
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        
        return {
            'id': event['id'],
            'summary': event['summary'],
            'html_link': event['htmlLink'],
            'start': event['start']['dateTime'],
            'end': event['end']['dateTime']
        }
        
    except Exception as e:
        print(f"Google Calendar API error: {e}")
        return {"error": f"Failed to create event: {str(e)}"} 