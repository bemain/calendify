import datetime
from calendar_api import CalendarApi
from skola24_api import Skola24Api
from lesson import Lesson, date_from_week, merge_date_and_time, timezone

from calendar_colors import get_calendar_color


calendars: dict[str, str] = {
    "Benjamin Agardh": "beag",
    "Na20a": "na20a",
}
weeks_to_sync = 4

skola24Api = Skola24Api("lel.skola24.se", "Lars-Erik Larsson-gymnasiet")
calendarApi = CalendarApi()


def index_for_lesson(lesson: Lesson, lessons: list[Lesson], check_description=True, check_color=False) -> int | None:
    for i, other in enumerate(lessons):
        if lesson.title == other.title and (not check_description or lesson.description == other.description) and str(lesson.start) == str(other.start) and str(lesson.end) == str(other.end) and (not check_color or lesson.color == other.color):
            return i
    return None


def get_lesson_colors(lessons_data: dict) -> dict[str: str]:
    box_list: list = lessons_data["boxList"]

    lesson_colors: dict[str: str] = {}
    for lesson_style in box_list:
        if lesson_style["lessonGuids"] != None:
            for id in lesson_style["lessonGuids"]:
                lesson_colors[id] = get_calendar_color(lesson_style["bColor"])
    return lesson_colors


def update_calendar(calendar_id, skola24_id, year, week):
    print(f"UPDATING week {week}")
    # Get target events from Skola24
    lessons_data = skola24Api.get_student_lessons(
        skola24_id, year=year, week=week)
    if lessons_data["lessonInfo"] == None:
        print(f"NO LESSONS for week {week}")
        return

    lesson_colors = get_lesson_colors(lessons_data)

    # Merge lessons in the same block
    blocks = []
    target_lessons = []
    for data in lessons_data["lessonInfo"]:
        lesson = Lesson.from_skola24_data(
            data, year, week, color=lesson_colors[data["guidId"]])
        index = index_for_lesson(
            lesson, blocks, check_description=False, check_color=False)
        if len(data["texts"]) <= 3 or index == None:
            if len(data["texts"]) > 3:
                blocks.append(lesson)
            target_lessons.append(lesson)
        else:
            block_desc = blocks[index].description.split("\n")
            lesson_desc = lesson.description.split("\n")
            for i, desc in enumerate(lesson_desc):
                if block_desc[i] != desc:
                    block_desc[i] += f", {desc}"
            blocks[index].description = "\n".join(block_desc)

    # Get current events from calendar
    events = calendarApi.get_events(
        calendar_id,
        time_min=merge_date_and_time(date_from_week(year, week, 0),
                                     datetime.time(0, 0, 0)).astimezone(timezone),
        time_max=merge_date_and_time(date_from_week(year, week + 1, 0),
                                     datetime.time(0, 0, 0)).astimezone(timezone),
    )
    current_lessons = [Lesson.from_calendar_data(data) for data in events]

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


if __name__ == '__main__':
    for calendar_name, skola24_id in calendars.items():
        print(f"===== {calendar_name} =====")
        calendar_id = calendarApi.get_calendar_id(calendar_name)

        now = datetime.datetime.now().isocalendar()
        for week in range(now.week, now.week+weeks_to_sync):
            update_calendar(calendar_id, skola24_id, now.year, week)

        print("\n")
