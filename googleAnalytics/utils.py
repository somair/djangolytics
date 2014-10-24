from datetime import date
from datetime import datetime

def create_date_from_str(date_str, date_format="%Y-%m-%d"):
    """Accepts string in the format '%Y-%m-%d'. Returns date object. This
    helper function exists since there is no strptime function for Date
    objects, only Datetime objects"""
    return datetime.strptime(date_str, date_format).date()

def create_str_from_date(date_obj, date_format="%Y-%m-%d"):
    """Accepts a Date object. Returns string in the format '%Y-%m-%d'. This
    helper function exists since there is no strptime function for Date
    objects, only Datetime objects"""
    return date.strftime(date_obj, date_format)
