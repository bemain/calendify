from calendar_api import CalendarApi
from skola24_api import Skola24Api

from lesson import Lesson

calendar_name: str = "Skola24"

year: int = 2022
week: int = 48


if __name__ == '__main__':
    skola24Api = Skola24Api("lel.skola24.se", "Lars-Erik Larsson-gymnasiet")
    skola24_lessons = skola24Api.get_student_lessons(
        "beag", year=year, week=week)
    lessons = list(map(lambda lesson_data: Lesson.from_skola24_data(lesson_data, year, week),
                       skola24_lessons))

    calendarApi = CalendarApi()

    print(f"UPDATING CALENDAR: {calendar_name}")
    calendarApi.update_calendar(
        calendarApi.get_calendar_id(calendar_name), lessons)
