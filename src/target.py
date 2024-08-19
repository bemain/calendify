import datetime

from calendar_api import CalendarApi
from source import Source
from event import Event
from utils import timezone, merge_date_and_time, date_from_week


class Target(Source):
    def add_event(self, event: Event):
        pass
    
    def delete_event(self, event: Event):
        pass
    
    def __repr__(self) -> str:
        return "Target()"

class GoogleCalendar(Target):
    api: CalendarApi = CalendarApi()
    
    def __init__(self, name: str):
        self.id = self.api.get_calendar_id(name)
    
    def get_events(self, year: int, week: int) -> list[Event]:
        events = self.api.get_events(
            self.id,
            time_min=merge_date_and_time(date_from_week(year, week, 0),
                                         datetime.time(0, 0, 0)).astimezone(timezone),
            time_max=merge_date_and_time(date_from_week(year, week + 1, 0),
                                         datetime.time(0, 0, 0)).astimezone(timezone),
        )
        return [Event.from_calendar_data(data) for data in events]

    def add_event(self, event: Event):
        self.api.add_event(self.id, event.title, event.description, event.start, event.end, color=event.color)
    
    def delete_event(self, event: Event):
        self.api.delete_event(self.id, event.id)
    
    def _parse_event(self, data) -> Event:
        return Event(
            data["id"],
            data["summary"],
            data["description"],
            datetime.datetime.fromisoformat(
                data["start"]["dateTime"]).astimezone(timezone),
            datetime.datetime.fromisoformat(
                data["end"]["dateTime"]).astimezone(timezone),
            color=int(data["colorId"]) if "colorId" in data.keys() else None,
        )
        