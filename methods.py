# -*- coding: utf-8 -*-
import messages
import messages_reprompt
import datetime
from flask_ask import session

def check_session_attributes():
    """
    checks which attributes aren't stored in session and therefore triggers needed question
    :return: question
    """
    if session.attributes.hobby is None:
        return messages.message_welcome()

    elif session.attributes.when_start is None:
        return messages.message_when()

    elif session.attributes.duration is None:
        return messages.message_duration()

    elif session.attributes.daytime_start is None:
        return messages.message_time_of_the_day()

    elif session.attributes.daytime_start is None:
        return messages.message_period()


def check_session_attributes_for_help():
    """
    checks which attributes aren't stored in session and therefore triggers needed reprompt
    :return: question
    """
    if session.attributes.hobby is None:
        return messages_reprompt.message_welcome()

    elif session.attributes.when_start is None:
        return messages_reprompt.message_when()

    elif session.attributes.duration is None:
        return messages_reprompt.message_duration()

    elif session.attributes.daytime_start is None:
        return messages_reprompt.message_time_of_the_day()

    elif session.attributes.period is None:
        return messages_reprompt.message_period()


def next_weekday(day, weekday):
    """
    Calculates next upcoming day, that is described in param 'weekday' (weekday = 0 Monday, = 1 Tuesday,...)
    :param day: daytime object, that describes current day
    :param weekday: integer, that describes which upcoming day of the week should be searched for
    :return: datetime object, that describes wanted upcoming day.
    """

    d = day.replace(hour=0, minute=0, second=0)
    days_ahead = weekday - d.weekday()

    if days_ahead <= 0:
        days_ahead += 7

    return d + datetime.timedelta(days_ahead)

def get_milliseconds_from_1970_until(now):
    """
    returns milliseconds that are between 01.01.1970 and now-value
    :param now: datime object
    :return: int
    """
    return (now - datetime.datetime(1970, 1, 1)).total_seconds() * 1000

def get_index_where_next_char_occurs(iso):
    """
    Calculates next index where a character is situated.
    i.e. 01234A -> index 5
    :param iso: string
    :return: index position
    """
    if iso is '':
        return None

    i = 0
    numbers = '0123456789'

    for char in iso:
        if char not in numbers:
            return i
        i += 1

    return None


def account_is_linked():
    """
    Checks if session includes an accesstoken or not
    :return: True, if accesstoken exists. False if not
    """
    if session.user.accessToken is not None:
        return True
    else:
        return False


def get_last_of_month(first_of_month):
    """
    Creates datetime object, which is the last day in 'first_of_month.month'
    :param first_of_month: defines month in which the datetime object should be in
    :return: datetime object
    """
    global last_of_month
    if first_of_month.month in {1, 3, 5, 7, 8, 10, 12}:
        last_of_month = datetime.datetime(first_of_month.year, first_of_month.month, 31)

    elif first_of_month in {4, 6, 9, 11}:
        last_of_month = datetime.datetime(first_of_month.year, first_of_month.month, 30)

    elif first_of_month is 2:
        if first_of_month.year % 4 is 0:
            last_of_month = datetime.datetime(first_of_month.year, first_of_month.month, 29)
        else:
            last_of_month = datetime.datetime(first_of_month.year, first_of_month.month, 28)

    return last_of_month


def convert_to_datetime_from_milliseconds(milliseconds):
    """
    Converts milliseconds to datetime object
    :param milliseconds: int
    :return: datetime object
    """
    return datetime.datetime.fromtimestamp(milliseconds / 1000.0)