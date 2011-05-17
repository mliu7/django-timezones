from datetime import datetime
from datetime import tzinfo
import pytz

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.encoding import smart_str


def localtime_for_timezone(value, timezone):
    """
    Given a ``datetime.datetime`` object in the local timezone and a timezone represented as
    a string, return the localized time for the timezone.
    """
    return adjust_datetime_to_timezone(value, settings.TIME_ZONE, timezone)

def copy_datetime_essentials(start_time_with_tz):
    return datetime(year=start_time_with_tz.year,
                    month=start_time_with_tz.month,
                    day=start_time_with_tz.day,
                    hour=start_time_with_tz.hour,
                    minute=start_time_with_tz.minute)


def adjust_datetime_to_timezone(value, from_tz=None, to_tz=None):
    """
    Given a ``datetime`` object adjust it according to the from_tz timezone
    string into the to_tz timezone string.
    """
    if to_tz is None:
        to_tz = settings.TIME_ZONE
    if from_tz is None:
        from_tz = settings.TIME_ZONE
    from_tz = pytz.timezone(smart_str(from_tz))
    value = from_tz.localize(value)
    new_datetime = value.astimezone(pytz.timezone(smart_str(to_tz)))
    return copy_datetime_essentials(new_datetime)


def coerce_timezone_value(value):
    try:
        return pytz.timezone(value)
    except pytz.UnknownTimeZoneError:
        raise ValidationError("Unknown timezone")


def validate_timezone_max_length(max_length, zones):
    def reducer(x, y):
        return x and (len(y) <= max_length)
    if not reduce(reducer, zones, True):
        raise Exception("timezones.fields.TimeZoneField MAX_TIMEZONE_LENGTH is too small")


def dst_isoformat(dt):
    """ Returns the correct isoformat for a time with a timezone, accounting for the daylight savings time offset.

    Input:
        dt - A valid Python Datetime object with a valid timezone field

    Output: 
        A string representing the datetime in a isoformat

    Notes:
        The reason this function is necessary is that the .isoformat() method that is built into Python datetime
        objects does not account for the daylight savings time offset when the timezone class is one of those
        used from the pytz library
    """
    # Determine if dst is in effect for the time and update the utcoffset field accordingly
    offset = dt.tzinfo.dst(dt.replace(tzinfo=None))
    dt.tzinfo._utcoffset += offset
    iso_string = dt.isoformat()
    # Restore the tzinfo to how it was
    dt.tzinfo._utcoffset -= offset
    return iso_string
