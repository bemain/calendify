import datetime
from calendar_api import CalendarApi
from skola24_api import Skola24Api
from update_calendar import update_calendar


skola24_ids: list[str] = [
    "beag",
]
weeks_to_sync = 4

skola24Api = Skola24Api("lel.skola24.se", "Lars-Erik Larsson-gymnasiet")
calendarApi = CalendarApi()


if __name__ == '__main__':
    for skola24_id in skola24_ids:
        calendar_name = f"Schema ({skola24_id})"
        print(f"===== {calendar_name} =====")
        calendar_id = calendarApi.get_calendar_id(calendar_name)

        now = datetime.datetime.now().isocalendar()
        for week in range(now.week, now.week+weeks_to_sync):
            update_calendar(calendar_id, skola24_id, now.year,
                            week, skola24Api, calendarApi)

        print("\n")
