from calendar_api import CalendarApi
from skola24_api import Skola24Api

from lesson import Lesson


if __name__ == '__main__':
    skola24Api = Skola24Api("lel.skola24.se", "Lars-Erik Larsson-gymnasiet")
    skola24_lessons = skola24Api.get_student_lessons(
        "beag", year=2022, week=48)
    lessons = list(map(lambda lesson_data: Lesson.from_skola24_data(lesson_data, 2022, 48),
                       skola24_lessons))

    calendarApi = CalendarApi()

    calendars = calendarApi.get_calendars()
    calendar_names = [calendar["summary"] for calendar in calendars]

    calendar_name = "Skola24"
    if calendar_name in calendar_names:
        # Use already existing calendar
        calendar_id = list(filter(
            lambda calendar: calendar["summary"] == calendar_name, calendars))[0]["id"]
    else:
        # Create calendar
        print(f"CREATING CALENDAR: {calendar_name}")
        calendar_id = calendarApi.create_calendar(calendar_name)

    print(f"UPDATING CALENDAR: {calendar_name}")
    calendarApi.update_calendar(calendar_id, lessons)
