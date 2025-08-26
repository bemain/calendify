from abc import abstractmethod
import datetime

from .event import Event
from .gcalendar_api import GoogleCalendarApi
from .source import Source
from .utils import date_from_week, merge_date_and_time, parse_timezone


class Target(Source):
    @abstractmethod
    def add_event(self, event: Event): ...

    @abstractmethod
    def delete_event(self, event: Event): ...

    def __repr__(self) -> str:
        return "Target()"


class GoogleCalendar(Target):
    api: GoogleCalendarApi = GoogleCalendarApi()

    def __init__(
        self,
        id: str,
        access: dict[str, str] = {},
        timezone: datetime.timezone = datetime.timezone.utc,
    ):
        self.id = id

        self.timezone = timezone

        # Give specified users access
        # TODO: Remove access for users not in list
        for user, role in access.items():
            if role not in ["none", "freeBusyReader", "reader", "writer", "owner"]:
                print(f"[GCALENDAR] Error: Invalid role '{role}' for user '{user}'")
                continue
            if user == "public":
                self.api.add_acl_rule(self.id, role=role, scope="default")
            else:
                self.api.add_acl_rule(
                    self.id, role=role, scope="user", scope_value=user
                )

    @classmethod
    def parse(cls, data):
        id = cls.api.get_calendar_id(data["name"])

        rules = {}
        if "access" in data:
            rules = (
                {
                    list(rule.keys())[0] if isinstance(rule, dict) else rule: (
                        list(rule.values())[0] if isinstance(rule, dict) else "reader"
                    )
                    for rule in data["access"]
                }
                if "access" in data
                else {}
            )
            if "public" in rules.keys():
                print(f"[GCALENDAR] Shareable link: {cls.api.get_shareable_link(id)}")
            print(f"[GCALENDAR] Access: {rules}")

        return cls(
            id,
            access=rules,
            timezone=(
                datetime.timezone.utc
                if "timezone" not in data
                else parse_timezone(data["timezone"])
            ),
        )

    def get_events(self, year: int, week: int) -> list[Event]:
        events = self.api.get_events(
            self.id,
            time_min=merge_date_and_time(
                date_from_week(year, week, 0), datetime.time(0, 0, 0)
            ).astimezone(self.timezone),
            time_max=merge_date_and_time(
                date_from_week(year, week + 1, 0), datetime.time(0, 0, 0)
            ).astimezone(self.timezone),
        )
        return [self._parse_event(data) for data in events]

    def add_event(self, event: Event):
        self.api.add_event(
            self.id,
            event.title,
            event.description,
            event.start,
            event.end,
            color=event.color,
        )

    def delete_event(self, event: Event):
        self.api.delete_event(self.id, event.id)

    def _parse_event(self, data) -> Event:
        return Event(
            data["id"],
            data["summary"] if "summary" in data else None,
            data["description"] if "description" in data else None,
            datetime.datetime.fromisoformat(data["start"]["dateTime"]).astimezone(
                self.timezone
            ),
            datetime.datetime.fromisoformat(data["end"]["dateTime"]).astimezone(
                self.timezone
            ),
            color=int(data["colorId"]) if "colorId" in data.keys() else None,
        )
