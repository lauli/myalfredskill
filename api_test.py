import base64
import json
import pprint
import requests

# def make_call_to_myalfred_api(json_data):
#     # call to rest api myalfred
#     url = 'https://staging.myalfred.io/api/schedule/google'
#     header_authentication_base64 = 'Basic QW1hem9uQWxleGFDbGllbnQ6N20zM1AySzd0WWhjZ0tOdk5wZDc0N3BSRmZvOUg4'
#     data = json.dumps([1, 2, 3])
#     req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
#     req.add_header('Authentication', header_authentication_base64)
#     try:
#         f = urllib2.urlopen(req)
#         response = f.read()
#         f.close()
#     except urllib2.HTTPError, error:
#         response = error.read()
#         print response
#     return response
from requests.auth import HTTPBasicAuth


def make_call_to_myalfred_api_2(json_data):
    url = 'https://staging.myalfred.io/api/schedule/google'
    header_authentication_base64 = 'Basic QW1hem9uQWxleGFDbGllbnQ6N20zM1AySzd0WWhjZ0tOdk5wZDc0N3BSRmZvOUg4'
    #usrPass = "AmazonAlexaClient:7m33P2K7tYhcgKNvNpd747pRFfo9H8"
    #b64Val = base64.b64encode(usrPass)
    json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
    # headers={"Authentication": "Basic %s" % b64Val},
    try:
        r = requests.post(url, auth=HTTPBasicAuth('AmazonAlexaClient', '7m33P2K7tYhcgKNvNpd747pRFfo9H8'),
                          json=json_data)
        data = json.loads(r.text)
        pprint.pprint(data)

    except requests.HTTPError as error:
        r = error.read()
    return r

eventTitle = "Standard activity"
#time in milliseconds!
startTime = 1522101600000
endTime = 1524780000000
eventDuration = 3600000

# number of events that should be scheduled (in case of repetitive events, this represents the number of events for
# one repetition period)
numberOfEvents = 1

# the time period in which the event is repeated:
# 5 = daily
# 6 = weekly
# 7 = yearly
repeatPeriod = 6
# integer defining the interval in which the event should be repeated, 1 = every period, 2 = every second period, ...
repeatInterval = 1

test = {
  # Get token from https://developers.google.com/oauthplayground/
  "accessTokens": ["ya29.Glx3BNoRqQk1c96c4IvNCIIeU4Ojp1zghxpzSLmfeu3d5epC_RjcNOw4V9Aeoh_1uRInDwc54jWND-CpN88Otsqni2z4Sp8cjK7GjMdH1MyJju5x5TU-4B7Znxwa8w"],
  "eventTitle": "Go Shopping",
  "start": 1522101600000,
  "end": 1524780000000,
  "eventDuration": 3600000,
  "originatorId": "alexa",
  "startRanges": [
    {
      "startHours": 11,
      "startMinutes": 0,
      "endHours": 14,
      "endMinutes": 0,
      "timeZone": "Europe/Vienna"
    }
  ],
  "location": {
    "type": "Location",
    "name": "Plus City Pasching",
    "coordinates": {
      "lat": 48.244179,
      "lng": 14.23592
    },
    "address": None
  },
  "count": 1,
  "isRepeating": True,
  "repeatPeriod": 6,
  "repeatInterval": 1
}
testJSON = json.loads(json.dumps(test))
print(json.dumps(test, indent=4))

# pprint.pprint(testJSON)

#print (make_call_to_myalfred_api_2(testJSON))

event = {
        'id': 'penedermark@gmail.com',
        'summary': 'Google I/O 2015',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A chance to hear more about Google\'s developer products.',
        'start': {
            'dateTime': '2016-09-28T09:00:00-07:00',
            'timeZone': 'Europe/Vienna',
        },
        'end': {
            'dateTime': '2016-09-28T17:00:00-07:00',
            'timeZone': 'Europe/Vienna',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        "defaultReminders": [
            {
             "method": "popup",
             "minutes": 10
            }
        ],
        "notificationSettings": {
            "notifications": [
             {
              "type": "eventCreation",
              "method": "email"
             },
             {
              "type": "eventChange",
              "method": "email"
             },
             {
              "type": "eventCancellation",
              "method": "email"
             },
             {
              "type": "eventResponse",
              "method": "email"
             }
            ]
           }
    }

resource = {'resource': event}

headersGoogle = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format("ya29.Glt3BCcgMPb2HEUfhJ704tXjKx_6X0Z_iYtEFg4n7S146jCi_OCTQFqwZ9TikgCdJ9GpgQKJ6rc2YnBqCfghsbTsGfI1Dpb2njTMaGjx88E_me0ZVMsPDi2_EVqq")
    }

r2= requests.get(url = "https://www.googleapis.com/calendar/v3/users/me/calendarList?access_token=ya29.Glt3BP9TYTKO0T3ucGR_CC809D5NEzdgOj1GWFXdv5fDwuf-xkkRYDh7O8h5D9hET8gVpvn4Yr5AcobL0U_HFicOIqQKskFBqPG-pADmoyr80MUc0yVBWRXa6rki")

pprint.pprint(resource)

r = requests.post("https://www.googleapis.com/calendar/v3/users/me/calendarList?access_token=ya29.Glt3BCcgMPb2HEUfhJ704tXjKx_6X0Z_iYtEFg4n7S146jCi_OCTQFqwZ9TikgCdJ9GpgQKJ6rc2YnBqCfghsbTsGfI1Dpb2njTMaGjx88E_me0ZVMsPDi2_EVqq", json=resource, headers= headersGoogle)
print(r.text)
#print(r2.text)