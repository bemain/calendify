import datetime

from skola24_api import Skola24Api

timezone = datetime.timezone(datetime.timedelta(hours=1))


class Event:
    def __init__(self, id: str, title: str, description: str, start: datetime.datetime, end: datetime.datetime, color: str | None = None):
        self.id = id
    
        self.title: str = title
        self.description: str = description
        self.color: str | None = color
    
        self.start: datetime.time = start
        self.end: datetime.time = end
    
    def __repr__(self) -> str:
        start = self.start.strftime("%Y-%m-%d %H:%M")
        end = self.end.strftime("%H:%M")
        return f"{self.title} at {start} - {end}" + (f" (color id {self.color})" if self.color != None else "")


class Source:
    # TODO: Specify start and end date instead
    def get_lessons(self, year: int, week: int) -> list[Event]:
        pass
    
    def __repr__(self) -> str:
        return "Source()"


class Skola24Source(Source):
    def __init__(self, domain: str, school: str, student_id: str):
        self.api: Skola24Api = Skola24Api(domain=domain, school=school)
        self.student_id: str = student_id
    
    def get_lessons(self, year: int, week: int) -> list[Event]:
        lessons_data = self.api.get_student_lessons(self.student_id, year=year, week=week)
        if lessons_data["lessonInfo"] == None:
            print(f"NO LESSONS for week {week}")
            return []
        
        lesson_colors = self._get_lesson_colors(lessons_data)
    
        # Merge lessons in the same block
        blocks = []
        lessons = []
        for data in lessons_data["lessonInfo"]:
            lesson = _parse_lesson(
                data, year, week, color=lesson_colors[data["guidId"]])
            index = index_for_lesson(
                lesson, blocks, check_description=False, check_color=False)
            if len(data["texts"]) <= 3 or index == None:
                if len(data["texts"]) > 3:
                    blocks.append(lesson)
                lessons.append(lesson)
            else:
                block_desc = blocks[index].description.split("\n")
                lesson_desc = lesson.description.split("\n")
                for i, desc in enumerate(lesson_desc):
                    if block_desc[i] != desc:
                        block_desc[i] += f", {desc}"
                blocks[index].description = "\n".join(block_desc)
        return lessons

    def _get_lesson_colors(lessons_data: dict) -> dict[str: str]:
        box_list: list = lessons_data["boxList"]
    
        lesson_colors: dict[str: str] = {}
        for lesson_style in box_list:
            if lesson_style["lessonGuids"] != None:
                for id in lesson_style["lessonGuids"]:
                    lesson_colors[id] = get_calendar_color(lesson_style["bColor"])
        return lesson_colors
    
    def _parse_lesson(self, data: dict[str, ], year: int,  week: int, color: str = None) -> Event:
            date = datetime.date.fromisocalendar(
                year, week, data["dayOfWeekNumber"])
            return Event(
                data["guidId"],
                data["texts"][0],
                "\n".join(data["texts"][-2:]).replace(",", ", "),
                merge_date_and_time(date, parse_time(data["timeStart"])),
                merge_date_and_time(date, parse_time(data["timeEnd"])),
                color=color,
            )
    
        
            