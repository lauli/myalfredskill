import loggingimport datetimefrom flask import Flaskfrom flask_ask import Ask, session, question, statement, request#from google_calendar_wrapper import get_service, get_calendarfrom datetime import datetimefrom aei_timeutils import datetime_from_stringfrom name_email import name_email_dict#checkapp = Flask(__name__)ask = Ask(app, "/")logger = logging.getLogger()def build_speechlet_response(title, output, content, reprompt_text, should_end_session):    return {        'outputSpeech': {            'type': 'SSML',            'ssml': output        },        'card': {            'type': 'Simple',            'title': "My Best Friend - " + title,            'content': content        },        'reprompt': {            'outputSpeech': {                'type': 'PlainText',                'text': reprompt_text            }        },        'shouldEndSession': should_end_session    }def build_response(session_attributes, speechlet_response):    return {        'version': '1.0',        'sessionAttributes': session_attributes,        'response': speechlet_response    }@ask.launchdef launch():    return question("Hey, what can I do for you?").reprompt("If you want me to plan something for you, you could for example say: 'I want to study'.")@ask.intent('HobbyIntent', mapping={'hobby':'Hobby'})def hobby_intent(hobby):    session.attributes['hobby'] = hobby    return question("When do you want to {}?".format(hobby)).reprompt("You could choose for exmaple: 'this week' or 'next month")@ask.intent('WhenIntent', mapping={'when':'When'})def when_intent(when):    session.attributes['when'] = when    hobby = session.attributes.hobby    return question("You want me to find a date to {} {}. Let's do that! How long will {}ing take you?".format(hobby, when, hobby))@ask.intent('TimeDurationIntent', mapping={'timeduration':'TimeDuration'})def convert_to_seconds_from(timeduration):    # PnYnMnWnDTnHnMnS    #app.logger.info(timeduration)    iso = timeduration[1:]    length = len(iso)    hours = 0    #return statement("{}".format(iso))    if length == 0:        return statement("{} and the other {}.".format(timeduration, iso))    #app.logger.info(iso)    #return statement("it is {}.".format(iso))    if iso[0] is not 'T':        index = get_index_where_next_char_occurs(iso)        if index != None and iso[index] is 'Y':            years = iso[0:index]            hours = int(years)*365            iso = iso[index + 1:]            index = get_index_where_next_char_occurs(iso)        if iso[index] is 'M':            months = iso[0:index]            hours += int(months)*30            iso = iso[index + 1:]            index = get_index_where_next_char_occurs(iso)        if index != None and iso[index] is 'W':            weeks = iso[0:index]            hours += int(weeks)*7            iso = iso[index + 1:]            index = get_index_where_next_char_occurs(iso)        if index != None and iso[index] is 'D':            days = iso[0:index]            hours += int(days)            iso = iso[index + 1:]        hours = hours*24        milliseconds = hours*3600    if iso[0] is 'T':        #return statement("T")        iso = iso[1:]        index = get_index_where_next_char_occurs(iso)        if index != None and iso[index] is 'H':            #return statement("hours")            hours = iso[0:index]            milliseconds = (int(hours) * 3600)            iso = iso[index + 1:]            index = get_index_where_next_char_occurs(iso)        if index != None and iso[index] is 'M':            minutes = iso[0:index]            milliseconds = (int(minutes) * 60)            iso = iso[index + 1:]            index = get_index_where_next_char_occurs(iso)        if index != None and iso[index] is 'S':            seconds = iso[0:index]            milliseconds = (int(seconds))            iso = iso[index + 1:]        milliseconds += milliseconds * 60    return statement("{} milliseconds".format(milliseconds))def get_index_where_next_char_occurs(iso):    if iso is '':        return None    i = 0    numbers = '0123456789'    for char in iso:        if char not in numbers:            return i        i += 1    return Noneif __name__ == "__main__":    app.run(debug=True)