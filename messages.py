# -*- coding: utf-8 -*-
import methods
import language
from flask_ask import question, statement, request


def message_welcome():
    """
    If account is linked, welcomes user and asks what he/she can do for him/her
    If not linked, returns 'message_account_linking'
    :return: question or statement
    """
    if methods.account_is_linked():
        if str(request.locale) == language.de:
            return question(language.de_welcome).reprompt(language.de_hobby_reprompt)
        else:
            return question(language.eng_welcome).reprompt(language.eng_hobby_reprompt)
    else:
        return message_account_linking()


def message_account_linking():
    """
    Returns statement, that the account is not linked. Adds specific linking card.
    :return: statement
    """
    if str(request.locale) == language.de:
        return statement(language.de_account_linking).link_account_card()
    else:
        return statement(language.eng_account_linking).link_account_card()


def message_when():
    """
    If account is linked, returns question, when the user wants to do this event
    If not linked, returns 'message_account_linking'
    :return: question or statement
    """
    if methods.account_is_linked():
        if str(request.locale) == language.de:
            return question(language.de_when).reprompt(language.de_when_reprompt)
        else:
            return question(language.eng_when).reprompt(language.eng_when_reprompt)
    else:
        return message_account_linking()


def message_duration():
    """
    Returns question, how long user will need to finish event.
    :return: question
    """
    if str(request.locale) == language.de:
        return question(language.de_duration).reprompt(language.de_duration_reprompt)
    else:
        return question(language.eng_duration).reprompt(language.eng_duration_reprompt)


def message_time_of_the_day():
    """
    Returns question, at what time of the day the user wants to do the event
    :return: question
    """
    if str(request.locale) == language.de:
        return question(language.de_time_of_day).reprompt(language.de_time_of_day_reprompt)
    else:
        return question(language.eng_time_of_day).reprompt(language.eng_time_of_day_reprompt)


def message_period():
    """
    Returns question, if event should repeat itself
    :return: question
    """
    if str(request.locale) == language.de:
        return question(language.de_period).reprompt(language.de_period_reprompt)
    else:
        return question(language.eng_period).reprompt(language.eng_period_reprompt)


def message_success():
    """
    Returns statement, that the creating was a success
    :return: statement
    """
    if str(request.locale) == language.de:
        return statement(language.de_success)
    else:
        return statement(language.eng_success)


def message_failure():
    """
    Returns statement, that tells the user about a failure at the post request
    :return: statement
    """
    if str(request.locale) == language.de:
        return statement(language.de_failure)
    else:
        return statement(language.eng_failure)


def message_stop():
    """
    Returns statement, that tells the user goodbye
    :return: statement
    """
    if str(request.locale) == language.de:
        return statement(language.de_stop)
    else:
        return statement(language.eng_stop)