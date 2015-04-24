import re

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
