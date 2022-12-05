from calendar_api import CalendarApi
from skola24_api import Skola24Api
from lesson import Lesson

from enum import Enum


calendar_name: str = "Skola24"

year: int = 2022
week: int = 48


def index_for_lesson(lesson: Lesson, current_lessons: list[Lesson]) -> int | None:
    for i, c_lesson in enumerate(current_lessons):
        if lesson.title == c_lesson.title and str(lesson.start) == str(c_lesson.start) and str(lesson.end) == str(c_lesson.end):
            return i
    return None


if __name__ == '__main__':
    skola24Api = Skola24Api("lel.skola24.se", "Lars-Erik Larsson-gymnasiet")
    target_lessons = skola24Api.get_student_lessons(
        "beag", year=year, week=week)

    calendarApi = CalendarApi()
    calendar_id = calendarApi.get_calendar_id(calendar_name)
    current_lessons_dict = {data["id"]: Lesson.from_calendar_data(
        data) for data in calendarApi.get_events(calendar_id)}
    current_lessons = list(current_lessons_dict.values())

    # Determine what operations are needed
    lessons_delete = current_lessons
    lessons_add = []
    for lesson in target_lessons:
        i = index_for_lesson(lesson, current_lessons)
        if i == None:
            lessons_add.append(lesson)
        else:
            lessons_delete.remove(current_lessons[i])

    # Add
    for lesson in lessons_add:
        calendarApi.add_event(calendar_id, lesson.title,
                              lesson.description, lesson.start, lesson.end)

    # Delete
    for lesson in lessons_delete:
        event_id = list(current_lessons_dict.keys())[list(
            current_lessons_dict.values()).index(lesson)]
        calendarApi.delete_event(calendar_id, event_id)
