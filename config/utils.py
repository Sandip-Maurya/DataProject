# utils/utils.py

from datetime import datetime

def format_date(date_obj, format_str='%d %b'):
    """
    Formats a datetime object into a string.

    :param date_obj: datetime object
    :param format_str: Format string
    :return: Formatted date string
    """
    return date_obj.strftime(format_str)
