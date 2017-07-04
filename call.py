# -*- coding: utf-8 -*-
import messages
import pprint
import requests
import json
from requests.auth import HTTPBasicAuth
from flask_ask import session


def set_request():
    """
    Prepares JSON Object for our API call.
    Retrieves all data, that was stored into our session, and saves it into a json object.
    Afterwards, calls myalfred make_call_to_myalfred_api with mentioned json object.
    :return: 
    """

    token = session.user.accessToken
    hobby = session.attributes.hobby
    when_start = session.attributes.when_start
    when_end = session.attributes.when_end
    duration = session.attributes.duration
    daytime_start = session.attributes.daytime_start
    daytime_end = session.attributes.daytime_end

    pprint.pprint(str(token) + "   hobby: " + str(hobby))

    if session.attributes.period is not None and session.attributes.period is not "":
        is_repeating = True
        period = session.attributes.period
    else:
        is_repeating = False
        period = 0

    call = {
        # Get token from https://developers.google.com/oauthplayground/
        "accessTokens": [str(token)],
        "eventTitle": str(hobby),
        "start": int(float(when_start)),
        "end": int(float(when_end)),
        "eventDuration": int(float(duration)),
        "originatorId": "alexa-skill",
        "startRanges": [
            {
                "startHours": int(float(daytime_start)),
                "startMinutes": 0,
                "endHours": int(float(daytime_end)),
                "endMinutes": 0,
                "timeZone": "Europe/Vienna"
            }
        ],
        "location": {
            "type": "Location",
            "name": "",
            "coordinates": {
                "lat": 48.244179,
                "lng": 14.23592
            },
            "address": None
        },
        "count": 1,
        "isRepeating": is_repeating,
        "repeatPeriod": int(period),
        "repeatInterval": 1
    }

    return make_call_to_myalfred_api(call)


def make_call_to_myalfred_api(json_data):
    """
    Makes a POST-request to the myAlfred Scheduling API using a JSON object
    containing Google Calendar token & desired scheduling setup and returns the response body.

    :param json_data: the json request containing all relevant information about a desired event
    :return: The response body of the scheduling api
    """
    url = 'https://staging.myalfred.io/api/schedule/google'
    try:
        r = requests.post(url, auth=HTTPBasicAuth('AmazonAlexaClient', '7m33P2K7tYhcgKNvNpd747pRFfo9H8'),
                          json=json_data, timeout=None)
        data = json.loads(r.text)
        pprint.pprint(r.text)

    except requests.exceptions.HTTPError as err:
        print err
        return messages.message_failure()

    except requests.exceptions.Timeout:
        pprint.pprint("Exception Timeout.")
        make_call_to_myalfred_api(json_data)

    except requests.exceptions.TooManyRedirects:
        pprint.pprint("Exception Bad URL.")
        return messages.message_failure()

    except requests.exceptions.RequestException as e:
        pprint.pprint("Exception fatal Error.")
        print e
        return messages.message_failure()

    except Exception:
        pprint.pprint("some Exception that isn't defined.")
        return messages.message_failure()

    return messages.message_success()