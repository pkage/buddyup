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
    if len(busy_intervals) == 0:
        return []
    elif len(busy_intervals) == 1:
        if (start_date >= busy_intervals[0][0] and end_date <= busy_intervals[0][1]):
            return []
        elif (start_date > busy_intervals[0][0]):
            return [(busy_intervals[0][1], end_date)]
        elif (end_date < busy_intervals[0][1]):
            return [(start_date, busy_intervals[0][0])]
        else:
            return [(start_date, busy_intervals[0][0]), (busy_intervals[0][1], end_date)]
    elif (start_date >= end_date or start_date > busy_intervals[-1][1] or end_date < busy_intervals[0][0]):
        return []

    modified_busy_intervals = []
    add = False
    for pos,b in enumerate(busy_intervals):
        if (start_date < b[0] and not add):
            modified_busy_intervals.append((start_date, start_date))
            modified_busy_intervals.append((b[0], b[1]))
            add = True
            continue
        elif (start_date >= b[0] and start_date <= b[1] and not add):
            modified_busy_intervals.append((start_date, b[1]))
            add = True
            continue
        elif (end_date >= b[0] and end_date <= b[1] and add):
            modified_busy_intervals.append((b[0], end_date))
            add = False
            break
        elif (end_date < b[0] and add):
            modified_busy_intervals.append((end_date, end_date))
            add = False
            break
        elif (end_date > b[1] and add and (pos == len(busy_intervals) - 1)):
            modified_busy_intervals.append((b[0], b[1]))
            modified_busy_intervals.append((end_date, end_date))
            add = False
            break
        elif (add):
            modified_busy_intervals.append((b[0], b[1]))

    free_intervals = []
    for pos,b in enumerate(modified_busy_intervals):
        if pos == len(modified_busy_intervals) - 1:
            break
        free_intervals.append((b[1], modified_busy_intervals[pos+1][0]))

    return free_intervals

# Lol ignore these "tests" sleep deprivation

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
   },
   {
    "start": "2018-10-21T04:30:00Z",
    "end": "2018-10-21T05:30:00Z"
   },
   {
    "start": "2018-10-22T04:30:00Z",
    "end": "2018-10-22T05:30:00Z"
   }
  ]
 }
}
}
"""

p1 = parse(json_data1)
p2 = parse(json_data2)
list_of_calendars = [p1.busy_dates, p2.busy_dates]
c = get_busy_intervals(list_of_calendars)
print(c)
d = get_free_intervals(c, datetime(2018, 10, 19, 4, 50), datetime(2018, 10, 22, 5, 30))
print("\n1")
print(d)
print("\n2")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 20, 2, 50), datetime(2018, 10, 22, 5, 30))
print(d)
print("\n3")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 20, 19, 50), datetime(2018, 10, 22, 5, 30))
print(d)
print("\n4")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 21, 4, 30), datetime(2018, 10, 22, 5, 30))
print(d)
print("\n5")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 21, 5, 50), datetime(2018, 10, 22, 5, 30))
print(d)
print("\n6")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 19, 4, 50), datetime(2018, 10, 22, 5, 40))
print(d)
print("\n7")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 19, 4, 50), datetime(2018, 10, 22, 5, 20))
print(d)
print("\n8")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 19, 4, 50), datetime(2018, 10, 22, 4, 30))
print(d)
print("\n9")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 19, 4, 50), datetime(2018, 10, 22, 4, 20))
print(d)
print("\n10")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 19, 4, 50), datetime(2018, 10, 21, 5, 30))
print(d)
print("\n11")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 19, 4, 50), datetime(2018, 10, 21, 5, 20))
print(d)
print("\n12")
c = get_busy_intervals(list_of_calendars)
d = get_free_intervals(c, datetime(2018, 10, 19, 4, 50), datetime(2018, 10, 21, 4, 20))
print(d)
json_data3 = """
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
   }
  ]
 }
}
}
"""
print("\n13")
c = get_busy_intervals([parse(json_data3).busy_dates])
print(c)
d = get_free_intervals(c, datetime(2018, 10, 19, 4, 50), datetime(2018, 10, 21, 4, 20))
print(d)
