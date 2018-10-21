from __future__ import print_function
import datetime
import json
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import flask
import authcache

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
now = datetime.datetime.utcnow()

# gets upcoming events to a specified datetime
def getUpcoming(service, calendar_id, year_end, month_end, day_end):
    end = now.replace(year=year_end, month=month_end, day=day_end)
    print('Upcoming events:')
    events_result = service.events().list(calendarId=calendar_id, timeMin=now.isoformat()+'Z',
                                        singleEvents=True, timeMax=end.isoformat() + 'Z',
                                        orderBy='startTime').execute()
    return events_result

# same as above but only gets free/busy status
def getBusy(service, calendar_id, year_end, month_end, day_end):
    end = now.replace(year=year_end, month=month_end, day=day_end)
    print("Busy intervals:")
    body = {
        "timeMin": now.isoformat() + 'Z', # 'Z' indicates UTC time,
        "timeMax": end.isoformat() + 'Z',
        "items": [{'id':calendar_id}]
    }
    busy_result = service.freebusy().query(body=body).execute()
    return busy_result

# returns dictionary of user calendar ids and descriptions
# id may be passed to getBusy or getUpcoming
def getCalendars(service):
    calendar_list = service.calendarList().list().execute()
    calendars = {}
    for cal in calendar_list["items"]:
        id = cal["id"]
        desc = cal["summary"]
        calendars[id] = desc
    print(calendars)
    return calendars

# authenticates the user and gets service started
def auth():
    store = file.Storage('tokencache.json')
    creds = store.get()
    #try:
    #    creds = authcache.load_auth()
    #except:
    #    creds = ""
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    #    authcache.save_auth(creds)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service
