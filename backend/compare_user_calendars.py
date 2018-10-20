from user_calendar import UserCalendar
from parse_calendar import parse
from datetime import datetime

def get_busy_intervals(calendars_busy_dates):
    """
    Get intervals in the calendars that are busy by one of the people
    :param calendars_busy_dates: A list of busy dates for each calendar
    ([calendar1.busy_dates, calendar2.busy_dates etc.])
    :return: Merged busy intervals
    """

    # Get union of intervals
    busy_dates_union = []
    for c in calendars_busy_dates:
        busy_dates_union = list(set().union(busy_dates_union, c))

    # Sort by the start date
    sorted_busy_dates_union = sorted(busy_dates_union, key=lambda x: x[0])
    busy_dates_merged = []

    for b in sorted_busy_dates_union:
        # Append the first element in the loop
        if not busy_dates_merged:
            busy_dates_merged.append(b)
        else:
            prev = busy_dates_merged[-1]
            # If the start of this is earlier than the end of previous
            if b[0] <= prev[1]:
                upper_bound = max(prev[1], b[1])
                busy_dates_merged[-1] = (prev[0], upper_bound)
            else:
                busy_dates_merged.append(b)

    return busy_dates_merged

def get_free_intervals(busy_intervals, start_date, end_date):
    """
    Get intervals in the calendars that are free for all people
    :param busy_intervals: A list of intervals which are busy (from get_busy_intervals)
    :param start_date: Start date of the free intervals
    :param end_date: End date of the free intervals
    :return: List of free intervals in the chosen interval
    """
    #todo


json_data1 = """
{
"kind": "calendar#freeBusy",
"timeMin": "2018-10-19T22:59:45.000Z",
"timeMax": "2018-10-31T22:59:45.000Z",
"calendars": {
 "primary": {
  "busy": [
   {
    "start": "2018-10-20T02:30:00Z",
    "end": "2018-10-20T04:30:00Z"
   },
   {
    "start": "2018-10-20T05:30:00Z",
    "end": "2018-10-20T18:30:00Z"
   }
  ]
 }
}
}
"""
json_data2 = """
{
"kind": "calendar#freeBusy",
"timeMin": "2018-10-19T22:59:45.000Z",
"timeMax": "2018-10-31T22:59:45.000Z",
"calendars": {
 "primary": {
  "busy": [
   {
    "start": "2018-10-20T04:30:00Z",
    "end": "2018-10-20T05:30:00Z"
   }
  ]
 }
}
}
"""

p1 = parse(json_data1)
p2 = parse(json_data2)
list_of_calendars = [p1.busy_dates, p2.busy_dates]
print(get_busy_intervals(list_of_calendars))
