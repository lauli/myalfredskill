# -*- coding: utf-8 -*-
import language
from flask_ask import question, statement, request

def message_welcome():
    """
    Returns hobby-question-reprompt
    :return: question
    """
    if str(request.locale) == language.de:
        return question(language.de_hobby_reprompt)
    else:
        return question(language.eng_hobby_reprompt)

def message_when():
    """
    Returns when-question-reprompt
    :return: question
    """
    if str(request.locale) == language.de:
        return question(language.de_when_reprompt)
    else:
       return question(language.eng_when_reprompt)


def message_duration():
    """
    Returns duration-question-reprompt    
    :return: question
    """
    if str(request.locale) == language.de:
        return question(language.de_duration_reprompt)
    else:
        return question(language.eng_duration_reprompt)


def message_time_of_the_day():
    """
    Returns time_of_day-question-reprompt
    :return: question
    """
    if str(request.locale) == language.de:
        return question(language.de_time_of_day_reprompt)
    else:
        return question(language.eng_time_of_day_reprompt)


def message_period():
    """
    Returns period-question-reprompt
    :return: question
    """
    if str(request.locale) == language.de:
        return question(language.de_period_reprompt)
    else:
        return question(language.eng_period_reprompt)
