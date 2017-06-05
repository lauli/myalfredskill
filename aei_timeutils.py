from datetime import datetime


def datetime_from_string (date_string):
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
