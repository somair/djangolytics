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

def generate_dot_chart_data(query_set):
    """Generates an array suitable for the dotchart when passed a set of
    HourlySessionModels"""
    dot_chart_data = [0 for i in range(7 * 24)]
    for model in query_result:
        # The day of the week where sunday is 0 and saturday is 6
        row = model.date.weekday()+1)%7
        col = model.hour
        dot_chart_data[(row*24)+col)] += model.num_sessions
    return dot_chart_data

