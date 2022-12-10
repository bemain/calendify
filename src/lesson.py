import datetime

timezone = datetime.timezone(datetime.timedelta(hours=1))


class Lesson:
    def __init__(self, id: str, title: str, description: str, start: datetime.datetime, end: datetime.datetime, color: int | None = None) -> None:
        self.id = id

        self.title: str = title
        self.description: str = description
        self.color: int | None = color

        self.start: datetime.time = start
        self.end: datetime.time = end

    @classmethod
    def from_skola24_data(cls, data: dict[str, ], year: int,  week: int, color: str = None):
        date = datetime.date.fromisocalendar(
            year, week, data["dayOfWeekNumber"])
        return cls(
            data["guidId"],
            data["texts"][0],
            "\n".join(data["texts"][-2:]).replace(",", ", "),
            merge_date_and_time(date, parse_time(data["timeStart"])),
            merge_date_and_time(date, parse_time(data["timeEnd"])),
            color=color,
        )

    @classmethod
    def from_calendar_data(cls, data: dict[str,]):
        return cls(
            data["id"],
            data["summary"],
            data["description"],
            datetime.datetime.fromisoformat(
                data["start"]["dateTime"]).astimezone(timezone),
            datetime.datetime.fromisoformat(
                data["end"]["dateTime"]).astimezone(timezone),
            color=int(data["colorId"]) if "colorId" in data.keys() else None,
        )

    def __repr__(self) -> str:
        start = self.start.strftime("%Y-%m-%d %H:%M")
        end = self.end.strftime("%H:%M")
        return f"{self.title} at {start} - {end}" + f" (color id {self.color})" if self.color != None else ""


def merge_date_and_time(date: datetime.date, time: datetime.time) -> datetime.datetime:
    return datetime.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second, tzinfo=time.tzinfo)


def parse_time(s: str) -> datetime.time:
    times = s.split(":")
    return datetime.time(hour=int(times[0]), minute=int(times[1]), second=int(times[2]), tzinfo=timezone)


def date_from_week(year: int, week: int, weekday: int) -> datetime.date:
    jan1 = datetime.date(year, 1, 1)
    day_of_year = week * 7 - jan1.weekday() + weekday
    return jan1 + datetime.timedelta(days=day_of_year)
