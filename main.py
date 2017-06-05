import logging
import datetime

from flask import Flask
from flask_ask import Ask, session, question, statement
from google_calendar_wrapper import get_service, get_calendar
from datetime import datetime

from aei_timeutils import datetime_from_string
from name_email import name_email_dict

#check
app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

@ask.intent('AddEvent')
def add_event(theEvent, Date, time):
    service = get_service()
    event = make_gcal_event(theEvent, Date, time, time)
    event_id = service.events().insert(calendarId='primary', body=event).execute()
    session.attributes['event_id'] = event_id['id']
    return question("The event " + theEvent + " has been added to your calendar at date " + Date + " and time " + time + "." + " Do you want to invite someone? ").reprompt(" Do you want to invite someone? ")

@ask.intent('MakeInvitation')
def invite(Person, theEvent, Date, time):
    service = get_service()

    start_date = str(Date) + "T" + "00:00:00Z"
    eventsResult = service.events().list(
        calendarId='primary', timeMin = start_date, q = theEvent, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    event_id = False
    for event in events:
        if event['summary'] == theEvent and event['start']['dateTime'] == str(Date) + "T" + str(time) + ":00Z":
            event_id = event['id']

    if not event_id:
        return statement("Sorry I couldn't find the event " + theEvent)

    session.attributes['event_id'] = event_id
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    new_attendee = {'email': name_email_dict[Person]}
    if 'attendees' in event:
        event['attendees'].append(new_attendee)
    else:
        event['attendees'] = [new_attendee]
    service.events().update(calendarId='primary', sendNotifications=True, eventId=event_id, body=event).execute()
    return question(Person + " has been invited to " + theEvent + ". Do you want to invite someone else? ").reprompt(" Do you want to invite someone else? ")

@ask.intent('YesAlexaInvite')
def make_invitation(Person):
    service = get_service()
    event_id = session.attributes['event_id']
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    new_attendee = {'email': name_email_dict[Person]}
    if 'attendees' in event:
        event['attendees'].append(new_attendee)
    else:
        event['attendees'] = [new_attendee]
    service.events().update(calendarId='primary', sendNotifications = True, eventId=event_id, body=event).execute()
    return question(Person + " has been invited. " + " Do you want to invite someone else? ").reprompt(" Do you want to invite someone else? ")

@ask.intent('ListEvents')
def list_events(Date):
    service = get_service()
    dtime = str(datetime.datetime.now().isoformat())
    time = dtime[10:]
    today = dtime[0:10]
    if str(Date) == str(today):
        now = str(Date) + time + 'Z'
    else:
        now = str(Date) + 'T00:00:00Z'
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    event_string = ""

    for event in events:
        date = event['start'].get('date', '')
        date_time = str(event['start'].get('dateTime', ''))
        date_time = date_time[0:10]
        print(date_time)
        if str(date_time) == str(Date) or str(date) == str(Date):
            event_string = event_string + event['summary'] + ", "
    result_statement = ("Your events for " + str(Date) + " are " + event_string).encode('utf-8')
    return statement(result_statement)

@ask.intent('NoInvite')
def dont_invite():
    return statement("OK")


@ask.intent('CheckAvailability')
def check_availability(Person, Date, time):
    if Person is None:
        return statement("I didn't catch the person's name.")
    if Date is None:
        return statement("I didn't catch the date you wanted to check.")
    if time is None:
        return statement("I didn't catch the time you wanted to check.")

    #freebusy google calendar api
    calendar_id = get_calendar(Person)
    if not calendar_id:
        return statement("I can't see this person's calendar. Make sure you're allowed to see it.")
    else:
        start_time = str(Date) + "T" + str(time) + ":00Z"
        request_body = {
            "timeMin": start_time,
            "timeMax": str(Date) + "T23:59:00Z",
            "items":[
                {
                    "id": calendar_id
                }
            ]
        }
        service = get_service()
        eventsResult = service.freebusy().query(body=request_body).execute()
        busy_ranges = eventsResult['calendars'][calendar_id]['busy']
        return_statement = Person + " is free from "
        for ranges in busy_ranges:
            if ranges['start'] == start_time:
                return statement(Person + " is busy at " + time)
            else:
                start_time = datetime.strftime(datetime_from_string(ranges['start']), "%H:%M:%S")
                end_time = datetime.strftime(datetime_from_string(ranges['end']), "%H:%M:%S")
                return_statement += start_time + " to " + end_time + "."

        return statement(return_statement)


def make_gcal_event(event_name, date, start_time, end_time):
    return {
        'summary': event_name,
        'start': {
            'dateTime': str(date) + "T" + str(start_time) + ":00Z"
        },
        'end': {
            'dateTime': str(date) + "T" + str(end_time) + ":00Z"
        }
    }

if __name__ == '__main__':
    app.run(debug=True)