import json
import requests
import re
from enum import Enum


class SelectionType (Enum):
    CLASS = 0
    STUDENT_ID = 4


class Skola24Api:
    def __init__(self, domain: str, school: str = "", xscope="8a22163c-8662-4535-9050-bc5e1923df48"):
        self.domain = domain
        self._xscope = xscope

        self.schools = None
        self.classes = None

        self.render_key = None

        self.headers = {
            "X-Scope": self._xscope,
            "Content-Type": "application/json"
        }

        self.session = requests.Session()

        self.timestamp_re = re.compile(r'[\d]{1,2}:[\d]{2}')

        self.current_school = self.get_school(school)

    def _get_render_key(self):
        r = self._get("https://web.skola24.se/api/get/timetable/render/key")
        self.render_key = r.json()['data']['key']
        return self.render_key

    def _post(self, url, data):
        return self.session.post(url, headers=self.headers, data=json.dumps(data))

    def _get(self, url):
        return self.session.get(url, headers=self.headers)

    def get_school(self, name):
        r = self._post("https://web.skola24.se/api/services/skola24/get/timetable/viewer/units", {
            "getTimetableViewerUnitsRequest": {
                "hostName": self.domain
            }
        })
        self.schools = r.json()['data']['getTimetableViewerUnitsResponse']['units']
        find_school = list(filter(lambda x: x['unitId'] == name, self.schools))
        if len(self.schools) == 1:
            self.current_school = self.schools[0]
        elif len(find_school) > 0:
            self.current_school = find_school[0]
        else:
            self.current_school = None
        return self.current_school

    def get_classes(self):
        body = {
            "hostName": self.domain,
            "unitGuid": self.current_school['unitGuid'],
            "filters": {
                "class": True,
                "course": False,
                "group": False,
                "period": False,
                "room": False,
                "student": True,
                "subject": False,
                "teacher": False
            }
        }
        r = self._post(
            "https://web.skola24.se/api/get/timetable/selection", body)
        self.classes = r.json()['data']['classes']
        return self.classes

    def get_class(self, name):
        if not self.classes:
            self.get_classes()
        find = list(filter(lambda x: x['groupName'] == name, self.classes))
        if len(find) > 0:
            return find[0]
        return None

    def get_student_signature(self, student_id: str):
        r = self._post("https://web.skola24.se/api/encrypt/signature", {"signature": student_id})
        return r.json()["data"]["signature"]

    def get_school_years(self):
        r = self._post("https://web.skola24.se/api/get/active/school/years", {"checkSchoolYearsFeatures": False, "hostName": self.domain})
        return r.json()["data"]["activeSchoolYears"]

    def get_class_lessons(self, class_name: str, year: int = 2022, week: int = 1):
        return self.get_lessons(self.get_class(class_name)['groupGuid'], SelectionType.CLASS, year, week)

    def get_student_lessons(self, student_id: str, year: int = 2022, week: int = 1):
        return self.get_lessons(self.get_student_signature(student_id), SelectionType.STUDENT_ID, year, week)

    def get_lessons(self, selection: str, selection_type: SelectionType, year: int, week: int):
        body = {
            "renderKey": self._get_render_key(),
            "host": self.domain,
            "unitGuid": self.current_school['unitGuid'],
            "startDate": None,
            "endDate": None,
            "scheduleDay": 0,
            "schoolYear": self.get_school_years()[0]["guid"],
            "blackAndWhite": False,
            "width": 10000,
            "height": 10000,
            "selectionType": selection_type.value,
            "selection": selection,
            "showHeader": False,
            "periodText": "",
            "week": week,
            "year": year,
            "privateFreeTextMode": False,
            "privateSelectionMode": None,
            "customerKey": ""
        }
        r = self._post("https://web.skola24.se/api/render/timetable", body)
        data_list = r.json()['data']
        return data_list

    def get_timeslot(self, class_name, timeslot):
        ignore_fontsize = 0
        data = self.get_timetable_data(class_name)
        for el in data['textList']:
            if self.timestamp_re.match(el['text']):
                ignore_fontsize = el['fontsize']
                break
        # Get all timestamps
        times = list(filter(lambda x: self.timestamp_re.match(
            x['text']) and x['fontsize'] != ignore_fontsize, data['textList']))

        lunch = list(filter(lambda x: timeslot.lower()
                     in x['text'].lower(), data['textList']))
        lunch_boxes = []
        for i in range(len(lunch)):
            lunch_boxes.append(list(filter(lambda x: "width" in x
                                           and x['bcolor'] == '#C0C0C0'  # TODO
                                           and lunch[i]['x'] >= x['x']
                                           and lunch[i]['x'] <= x['x'] + x['width']
                                           and lunch[i]['y'] >= x['y']
                                           and lunch[i]['y'] <= x['y'] + x['height'], data['boxList']))[0])

        def nearest(value, arr, key):
            if len(arr) < 1:
                return None
            closest = arr[0]
            for el in arr:
                if abs(el[key] - value) < abs(closest[key] - value):
                    closest = el
            return closest

        correct_times = []
        for i in range(len(lunch)):
            start = nearest(lunch_boxes[i]['y'], times, 'y')['text']
            end = nearest(lunch_boxes[i]['y']+lunch_boxes[i]
                          ['height']+times[0]['fontsize'], times, 'y')['text']
            correct_times.append((start, end))
        return correct_times
