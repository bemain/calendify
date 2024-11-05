import datetime

class Event:
    def __init__(self, id: str, title: str | None, description: str | None, start: datetime.datetime, end: datetime.datetime, color: str | None = None):
        self.id = id
    
        self.title: str | None = title
        self.description: str | None = description
        self.color: str | None = color
    
        self.start: datetime.time = start
        self.end: datetime.time = end
        
    
    def __repr__(self) -> str:
        start = self.start.strftime("%Y-%m-%d %H:%M")
        end = self.end.strftime("%H:%M")
        return f"{self.title} at {start} - {end}" + (f" (color id {self.color})" if self.color != None else "")


def index_for_lesson(lesson: Event, lessons: list[Event], check_description=True, check_color=False) -> int | None:
    for i, other in enumerate(lessons):
        if lesson.title == other.title and (not check_description or lesson.description == other.description) and str(lesson.start) == str(other.start) and str(lesson.end) == str(other.end) and (not check_color or lesson.color == other.color):
            return i
    return None
