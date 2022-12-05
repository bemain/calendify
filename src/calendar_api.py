from __future__ import print_function

import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from lesson import Lesson

import datetime


class CalendarApi:
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self, calendar_name="Skola24") -> None:
        self.calendar_name: str = calendar_name

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
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
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
            print(f"CREATING CALENDAR: {calendar_name}")
            return self.create_calendar(calendar_name)

    def create_calendar(self, calendar_name: str) -> str:
        result = self.service.calendars().insert(body={
            "summary": calendar_name,
        }).execute()
        return result["id"]

    def update_calendar(self, calendar_id: str, lessons: list[Lesson]):
        try:
            # Clear
            events = self.service.events().list(
                calendarId=calendar_id).execute().get("items", [])
            for event in events:
                self.service.events().delete(
                    calendarId=calendar_id, eventId=event["id"]).execute()

            # Create events
            timezone_delta = datetime.timedelta(hours=1)

            for lesson in lessons:
                event = self.service.events().insert(calendarId=calendar_id, body={
                    "description": lesson.description,
                    "summary": lesson.title,
                    "start": {"dateTime": (lesson.start - timezone_delta).isoformat() + "Z"},
                    "end": {"dateTime": (lesson.end - timezone_delta).isoformat() + "Z"},
                }).execute()

        except HttpError as error:
            print('An error occurred: %s' % error)
