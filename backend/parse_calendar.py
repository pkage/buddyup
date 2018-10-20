import json
from user_calendar import UserCalendar
from datetime import datetime

def parse(calendar_json):
    j = json.loads(calendar_json)

    name = j["calendars"].keys()[0]
    time_max = j["timeMax"]
    time_max_dt = datetime.strptime(time_max[:-1].split('.')[0], "%Y-%m-%dT%H:%M:%S")
    time_min = j["timeMin"]
    time_min_dt = datetime.strptime(time_min[:-1].split('.')[0], "%Y-%m-%dT%H:%M:%S")

    busy = j["calendars"][name]["busy"]
    busy_dates = []
    for b in busy:
        start_dt = datetime.strptime(b["start"][:-1].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        end_dt = datetime.strptime(b["end"][:-1].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        busy_dates.append((start_dt, end_dt))

    return UserCalendar(name, time_min_dt, time_max_dt, busy_dates)