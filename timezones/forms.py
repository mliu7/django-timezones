from django import forms
from django.conf import settings

import pytz

from timezones import zones
from timezones.utils import adjust_datetime_to_timezone, coerce_timezone_value



class TimeZoneField(forms.TypedChoiceField):
    def __init__(self, *args, **kwargs):
        """ 
        Field for selecing valid timezones.
        
        Kwargs:
            all - If True, all of the timezones will be used. 
                  If False, only the common timezones will be used
        """
        if not "choices" in kwargs:
            if kwargs.pop("all", False):
                kwargs["choices"] = zones.ALL_TIMEZONE_CHOICES
            else:
                kwargs["choices"] = zones.AMERICA_FIRST_TIMEZONE_CHOICES
        kwargs["coerce"] = coerce_timezone_value
        super(TimeZoneField, self).__init__(*args, **kwargs)


class LocalizedDateTimeField(forms.DateTimeField):
    """
    Converts the datetime from the user timezone to settings.TIME_ZONE.
    """
    def __init__(self, timezone=None, *args, **kwargs):
        super(LocalizedDateTimeField, self).__init__(*args, **kwargs)
        self.timezone = timezone or settings.TIME_ZONE
        
    def clean(self, value):
        value = super(LocalizedDateTimeField, self).clean(value)
        if value is None: # field was likely not required
            return None
        return adjust_datetime_to_timezone(value, from_tz=self.timezone)
