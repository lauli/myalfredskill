from apiclient import discovery

from flask_ask import session

from oauth2client.client import AccessTokenCredentials
from name_email import name_email_dict

import httplib2


def get_service():
    credentials = get_user_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('calendar', 'v3', http=http)


def get_user_credentials():
    if hasattr(session.user, 'accessToken') and session.user.accessToken is not None:
        return AccessTokenCredentials(session.user.accessToken, "Alexa/1.0")
    else:
        return None


#get the calendars depending on the person
def get_calendar(name):
    if not(name in name_email_dict):
        return False
    else:
        return name_email_dict[name]
