from calendar_api import CalendarApi
from skola24_api import Skola24Api

from lesson import Lesson


if __name__ == '__main__':
    skola24Api = Skola24Api("lel.skola24.se", "Lars-Erik Larsson-gymnasiet")
    skola24_lessons = skola24Api.get_student_lessons(
        "beag", year=2022, week=48)
    lessons = list(map(lambda lesson_data: Lesson.from_skola24_data(lesson_data, 2022, 48),
                       skola24_lessons))

    calendarAPI = CalendarApi()
    calendarAPI.update_calendar("Skola24", lessons)
