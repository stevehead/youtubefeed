import re, iso8601, pytz
from django.conf import settings

CURRENT_TIMEZONE = pytz.timezone(settings.TIME_ZONE)


def convert_iso8601_to_datetime(iso8601_string):
    return iso8601.parse_date(iso8601_string).astimezone(CURRENT_TIMEZONE)


def convert_iso8601_duration_to_seconds(duration):
    duration = str(duration)
    duration_parts = duration.split('T')

    # Verify duration string is ISO 8601
    if len(duration) == 0 or duration[0] != 'P' or len(duration_parts) != 2:
        raise AttributeError("ISO 8601 duration format is required.")

    # Remove starting P
    duration_parts[0] = duration_parts[0][1:]

    # Regex Setup
    re_date = re.compile('\d+[YMWD]{1}')
    re_time = re.compile('\d+[HMS]{1}')

    # Elements
    date_elements = re_date.findall(duration_parts[0])
    time_elements = re_time.findall(duration_parts[1])

    seconds = 0
    for element in date_elements:
        amount = int(element[:-1])
        type = element[-1:]
        if type == 'Y':
            seconds += amount * 365.25 * 24 * 3600
        elif type == 'M':
            seconds += amount * 30.6 * 24 * 3600
        elif type == 'W':
            seconds += amount * 7 * 24 * 3600
        elif type == 'D':
            seconds += amount * 24 * 3600
    for element in time_elements:
        amount = int(element[:-1])
        type = element[-1:]
        if type == 'H':
            seconds += amount * 3600
        elif type == 'M':
            seconds += amount * 60
        elif type == 'S':
            seconds += amount
    return int(seconds)


def split_lists(the_list, wanted_parts=1):
    all_lists = []
    current_list = []
    for i in the_list:
        current_list.append(i)
        if len(current_list) == wanted_parts:
            all_lists.append(current_list)
            current_list = []
    if len(current_list) > 0:
        all_lists.append(current_list)
    return all_lists