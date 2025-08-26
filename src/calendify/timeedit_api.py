import json

import requests


class TimeEditApi:
    def __init__(self, domain: str):
        self.domain = domain

        self.session = requests.Session()
        self.headers = {}

    def _post(self, url, data):
        return self.session.post(url, headers=self.headers, data=json.dumps(data))

    def _get(self, url, params=None):
        return self.session.get(url, headers=self.headers, params=params)

    def get_events(self, course_id: str, days_shifted: int, language_code: str):
        r = self._get(
            f"https://cloud.timeedit.net/{self.domain}/web/public/ri.json",
            params={
                "h": "f",
                "h2": "f",
                "p": f"{days_shifted}.d,1.w",
                "ox": 0,
                "fe": 0,
                "types": 0,
                "sid": 3,
                "l": language_code,
                "objects": course_id,
            },
        )
        return r.json()
