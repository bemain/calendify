import datetime
from zoneinfo import ZoneInfo


def merge_date_and_time(date: datetime.date, time: datetime.time) -> datetime.datetime:
    return datetime.datetime(
        date.year,
        date.month,
        date.day,
        time.hour,
        time.minute,
        time.second,
        tzinfo=time.tzinfo,
    )


def parse_date(s: str) -> datetime.date:
    times = s.split("-")
    return datetime.date(int(times[0]), month=int(times[1]), day=int(times[2]))


def parse_time(
    s: str, timezone: datetime.timezone = datetime.timezone.utc
) -> datetime.time:
    times = s.split(":")
    return datetime.time(
        hour=int(times[0]),
        minute=int(times[1]),
        second=int(times[2]) if len(times) >= 3 else 0,
        tzinfo=timezone,
    )


def parse_timezone(s) -> datetime.timezone:
    if isinstance(s, int):
        return datetime.timezone(datetime.timedelta(hours=int(s)))

    if isinstance(s, str):
        return ZoneInfo(s)


def date_from_week(year: int, week: int, weekday: int) -> datetime.date:
    jan1 = datetime.date(year, 1, 1)
    day_of_year = (week - 1) * 7 - jan1.weekday() + weekday
    return jan1 + datetime.timedelta(days=day_of_year)
