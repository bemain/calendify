import datetime
from calendar_api import CalendarApi
from skola24_api import Skola24Api
from update_calendar import update_calendar

import yaml
from yaml.loader import SafeLoader


class Calendar:
    def __init__(self, skola24_id: str, calendar_id: str | None = None, name: str | None = None, calendarApi: CalendarApi = CalendarApi()) -> None:
        self.name = name if name != None else f"Schema ({skola24_id})"

        self.skola24_id = skola24_id
        self.calendar_id = calendar_id if calendar_id != None else \
            calendarApi.get_calendar_id(self.name)

    def __repr__(self) -> str:
        return f"Calendar({self.name}, skola24_id: {self.skola24_id}, google_calendar_id: {self.calendar_id})"


weeks_to_sync = 4


if __name__ == '__main__':
    with open('calendars.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)

    skola24Api = Skola24Api(data["domain"], data["school_name"])
    calendarApi = CalendarApi()

    calendars = [Calendar(data["calendars"][name]["id"],
                          calendarApi=calendarApi,
                          name=name)
                 for name in data["calendars"]]

    for calendar in calendars:
        print(f"===== {calendar.name} =====")

        now = datetime.datetime.now().isocalendar()
        for week in range(now.week, now.week+weeks_to_sync):
            update_calendar(calendar.calendar_id, calendar.skola24_id, now.year,
                            week, skola24Api, calendarApi)

        print("\n")
