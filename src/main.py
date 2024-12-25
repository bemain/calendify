import datetime
from event import index_for_lesson
from source import Source, Skola24Source, TimeEditSource
from target import Target, GoogleCalendar

import yaml
from yaml.loader import SafeLoader

class Calendar:
    """
    Helper class for matching a Skola24 calendar with a Google Calendar.
    """
    def __init__(self, source: Source, target: Target, name: str | None = "Calendar") -> None:
        self.name = name
        
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
        
        if len(target_lessons) == 0:
            print(f"NO LESSONS for week {week}")
    
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
            self.target.add_event(lesson)
    
        # Delete
        for lesson in lessons_delete:
            print(f"DELETING event: {lesson}")
            self.target.delete_event(lesson)
        
        print("")

    def __repr__(self) -> str:
        return f"Calendar({self.name}, source: {self.source}, target: {self.target})"


def _get_source_by_name(source: str) -> Source:
    if (source == "skola24"): return Skola24Source
    elif (source == "timeedit"): return TimeEditSource

def _get_target_by_name(target: str) -> Target:
    if (target == "gcalendar"): return GoogleCalendar

if __name__ == '__main__':
    with open('calendars.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)

    weeks_to_sync = 4 if not "weeks_to_sync" in data else data["weeks_to_sync"]

    calendars = [Calendar(_get_source_by_name(calendar_data["source"]["type"]).parse(calendar_data["source"]), _get_target_by_name(calendar_data["target"]["type"]).parse(calendar_data["target"]), name=list(calendar_data)[0])
                 for calendar_data in data["calendars"]]

    for calendar in calendars:
        print(f"===== {calendar.name} =====")

        now = datetime.datetime.now().isocalendar()
        weeks_this_year = datetime.date(now.year, 12, 28).isocalendar()[1]
        for week in range(now.week, now.week + weeks_to_sync):
            year = now.year + week // weeks_this_year
            week %= weeks_this_year
            calendar.update(year, week)

        print("\n")
