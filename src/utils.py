import datetime

timezone = datetime.timezone(datetime.timedelta(hours=1))


def merge_date_and_time(date: datetime.date, time: datetime.time) -> datetime.datetime:
    return datetime.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second, tzinfo=time.tzinfo)


def parse_time(s: str) -> datetime.time:
    times = s.split(":")
    return datetime.time(hour=int(times[0]), minute=int(times[1]), second=int(times[2]), tzinfo=timezone)


def date_from_week(year: int, week: int, weekday: int) -> datetime.date:
    jan1 = datetime.date(year, 1, 1)
    day_of_year = (week - 1) * 7 - jan1.weekday() + weekday
    return jan1 + datetime.timedelta(days=day_of_year)
