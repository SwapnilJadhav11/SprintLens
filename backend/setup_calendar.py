#!/usr/bin/env python3
"""
Google Calendar Setup Script for SprintLens
This script helps you set up Google Calendar integration.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_credentials_file():
    """Check if credentials.json exists."""
    creds_path = Path("credentials.json")
    if not creds_path.exists():
        print("❌ credentials.json not found!")
        print("\n📋 Please follow these steps:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing")
        print("3. Enable Google Calendar API")
        print("4. Create OAuth 2.0 credentials (Desktop application)")
        print("5. Download the JSON file and rename to 'credentials.json'")
        print("6. Place it in the backend/ directory")
        return False
    
    print("✅ credentials.json found!")
    return True

def check_env_variables():
    """Check if environment variables are set."""
    required_vars = [
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("\n📝 Add these to your .env file:")
        print("# Google Calendar Configuration")
        print("GOOGLE_CLIENT_ID=your_client_id_here")
        print("GOOGLE_CLIENT_SECRET=your_client_secret_here")
        print("GOOGLE_REDIRECT_URI=http://localhost:8001/api/calendar/auth/callback")
        return False
    
    print("✅ Environment variables configured!")
    return True

def test_calendar_service():
    """Test the calendar service."""
    try:
        from app.services.calendar_service import get_calendar_list
        print("\n🔄 Testing calendar service...")
        calendars = get_calendar_list()
        if calendars:
            print(f"✅ Found {len(calendars)} calendars!")
            for cal in calendars[:3]:  # Show first 3
                print(f"   - {cal['summary']} ({cal['id']})")
        else:
            print("⚠️  No calendars found. Check your Google Calendar account.")
        return True
    except Exception as e:
        print(f"❌ Calendar service error: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 SprintLens Google Calendar Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_credentials_file():
        return False
    
    if not check_env_variables():
        return False
    
    # Test the service
    if not test_calendar_service():
        return False
    
    print("\n🎉 Google Calendar setup complete!")
    print("\n📊 You can now:")
    print("- Use calendar data in sprint summaries")
    print("- Fetch calendar events via API")
    print("- Create calendar events")
    print("- View busy times")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 