from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

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
    print(events_result)
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
    print(busy_result)
    return busy_result

# authenticates the user and gets service started
def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
    getUpcoming(service, 'primary', 2018,10,31)
    getBusy(service, 'primary', 2018,10,31)

if __name__ == '__main__':
    main()
