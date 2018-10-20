from __future__ import print_function
import datetime
import json
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import flask

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
    return calendars

# authenticates the user and gets service started
def auth():
    if 'credentials' not in flask.session:
        oauth2callback()
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        oauth2callback()
    http_auth = credentials.authorize(httplib2.Http())
    # store = file.Storage('token.json')
    # creds = store.get()
    # if not creds or creds.invalid:
    #     flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    #     creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    return service


def oauth2callback():
  flow = client.flow_from_clientsecrets(
      'credentials.json',
      SCOPES,
      redirect_uri='localhost:8000')

  if 'code' not in flask.request.args:
    auth_uri = flow.step1_get_authorize_url()
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    credentials = flow.step2_exchange(auth_code)
    flask.session['credentials'] = credentials.to_json()
