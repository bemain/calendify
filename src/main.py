import datetime
from calendar_api import CalendarApi
from skola24_api import Skola24Api
from lesson import Lesson, date_from_week, merge_date_and_time, timezone


calendar_name: str = "Skola24"

year: int = 2022
week: int = 50


def index_for_lesson(lesson: Lesson, current_lessons: list[Lesson]) -> int | None:
    for i, c_lesson in enumerate(current_lessons):
        if lesson.title == c_lesson.title and lesson.description == c_lesson.description and str(lesson.start) == str(c_lesson.start) and str(lesson.end) == str(c_lesson.end):
            return i
    return None


if __name__ == '__main__':
    skola24Api = Skola24Api("lel.skola24.se", "Lars-Erik Larsson-gymnasiet")
    lessons_data = skola24Api.get_student_lessons(
        "beag", year=year, week=week)

    blocks = []
    target_lessons = []
    for data in lessons_data:
        if len(data["texts"]) <= 3 or data["texts"][0] not in blocks:
            if len(data["texts"]) > 3:
                blocks.append(data["texts"][0])
            target_lessons.append(Lesson.from_skola24_data(data, year, week))

    calendarApi = CalendarApi()
    calendar_id = calendarApi.get_calendar_id(calendar_name)
    events = calendarApi.get_events(
        calendar_id,
        time_min=merge_date_and_time(date_from_week(
            year, week, 0), datetime.time(0, 0, 0)).astimezone(timezone),
    )
    current_lessons_dict = {
        data["id"]: Lesson.from_calendar_data(data) for data in events}
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
        print(f"ADDING event: {lesson}")
        calendarApi.add_event(calendar_id, lesson.title,
                              lesson.description, lesson.start, lesson.end)

    # Delete
    for lesson in lessons_delete:
        print(f"DELETING event: {lesson}")
        event_id = list(current_lessons_dict.keys())[list(
            current_lessons_dict.values()).index(lesson)]
        calendarApi.delete_event(calendar_id, event_id)
