from __future__ import print_function
import datetime
import base64

import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials


class GoogleCalendarApi:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self) -> None:
        self.credentials: Credentials = self.generate_credentials()
        self.service

    def generate_credentials(self) -> Credentials:
        credentials = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file(
                'token.json', self.SCOPES)
        if os.path.exists("service_account_key.json"):
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                "service_account_key.json", self.SCOPES)
        
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or (credentials is Credentials and not credentials.valid) or (credentials is ServiceAccountCredentials and credentials.invalid):
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())

        self.service = build('calendar', 'v3', credentials=credentials)

        return credentials

    def get_calendars(self):
        return self.service.calendarList().list().execute().get("items", [])

    def get_calendar_id(self, calendar_name: str) -> str:
        calendars = self.get_calendars()
        calendar_names = [calendar["summary"] for calendar in calendars]

        if calendar_name in calendar_names:
            # Use already existing calendar
            return list(filter(
                lambda calendar: calendar["summary"] == calendar_name, calendars))[0]["id"]
        else:
            # Create calendar
            print(f"CREATING calendar: {calendar_name}\n")
            return self.create_calendar(calendar_name)
    
    def get_calendar_cid(self, calendar_id: str) -> str:
        id_bytes = calendar_id.encode('utf-8')
        cid_base64 = base64.b64encode(id_bytes)
        cid = cid_base64.decode().rstrip('=')
        return cid

    def get_shareable_link(self, calendar_id) -> str:
        return f"https://calendar.google.com/calendar?cid={self.get_calendar_cid(calendar_id)}"

    def create_calendar(self, calendar_name: str) -> str:
        result = self.service.calendars().insert(body={
            "summary": calendar_name,
        }).execute()
        return result["id"]

    def get_events(self, calendar_id: str, time_min: datetime.datetime | None = None, time_max: datetime.datetime | None = None) -> list[dict]:
        return self.service.events().list(
            calendarId=calendar_id,
            timeMin=time_min.isoformat() if time_min != None else None,
            timeMax=time_max.isoformat() if time_max != None else None,
        ).execute().get("items", [])

    def add_event(self, calendar_id: str, summary: str, description: str, start: datetime.datetime, end: datetime.datetime, color: int | None = None) -> str:
        return self.service.events().insert(calendarId=calendar_id, body={
            "summary": summary,
            "description": description,
            "start": {"dateTime": start.isoformat()},
            "end": {"dateTime": end.isoformat()},
            "colorId": color,
        }).execute()

    def delete_event(self, calendar_id: str, event_id: str):
        self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
