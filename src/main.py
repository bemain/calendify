import datetime
from event import index_for_lesson
from source import Source, Skola24Source
from target import Target, GoogleCalendar
from calendar_api import CalendarApi
from utils import date_from_week, merge_date_and_time, timezone

import yaml
from yaml.loader import SafeLoader

class Calendar:
    """
    Helper class for matching a Skola24 calendar with a Google Calendar.
    """
    def __init__(self, source: Source, target: Target, name: str | None = None) -> None:

        self.name = name if name != None else f"Schema ({skola24_id})"
        
        self.source: Source = source
        self.target: Target = target

    def update(self, year: int, week: int):
        """
        Update all lessons during the specified [week] and [year], so that the Google Calendar matches the Skola24 calendar.
        """
        print(f"UPDATING week {week}")
        # Get target events from Skola24
        target_lessons = self.source.get_events(year, week)
        current_lessons = self.target.get_events(year, week)
    
        # Determine what operations are needed
        lessons_delete = current_lessons
        lessons_add = []
        for lesson in target_lessons:
            i = index_for_lesson(lesson, current_lessons, check_color=True)
            if i == None:
                lessons_add.append(lesson)
            else:
                lessons_delete.remove(current_lessons[i])
    
        # Add
        for lesson in lessons_add:
            print(f"ADDING event: {lesson}")
            calendarApi.add_event(calendar_id, lesson.title,
                                  lesson.description, lesson.start, lesson.end,
                                  color=lesson.color)
    
        # Delete
        for lesson in lessons_delete:
            print(f"DELETING event: {lesson}")
            calendarApi.delete_event(calendar_id, lesson.id)
    
        if len(lessons_add) != 0 or len(lessons_delete) != 0:
            print("")

    def __repr__(self) -> str:
        return f"Calendar({self.name}, skola24_id: {self.skola24_id}, google_calendar_id: {self.calendar_id})"


if __name__ == '__main__':
    with open('calendars.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)

    Calendar.calendarApi = CalendarApi()

    weeks_to_sync = 4 if not "weeks_to_sync" in data else data["weeks_to_sync"]

    calendars = [Calendar(Skola24Source(data["domain"], data["school"], data["calendars"][name]["id"]), GoogleCalendar(name), name=name)
                 for name in data["calendars"]]

    for calendar in calendars:
        print(f"===== {calendar.name} =====")

        now = datetime.datetime.now().isocalendar()
        for week in range(40, 40+weeks_to_sync):
            calendar.update(now.year, week)

        print("\n")
