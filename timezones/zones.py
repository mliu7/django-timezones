from datetime import datetime

import pytz


ALL_TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
COMMON_TIMEZONE_CHOICES = tuple(zip(pytz.common_timezones, pytz.common_timezones))
PRETTY_TIMEZONE_CHOICES = []

for tz in pytz.common_timezones:
    now = datetime.now(pytz.timezone(tz))
    PRETTY_TIMEZONE_CHOICES.append((tz, "(GMT%s) %s" % (now.strftime("%z"), tz)))

ORDERED_TIMEZONE_CHOICES = sorted(PRETTY_TIMEZONE_CHOICES, key=lambda c: (int(c[1][4:].split(')')[0]), c[0]))

AMERICA_FIRST_TIMEZONE_CHOICES = ORDERED_TIMEZONE_CHOICES

for america_choice in ['US/Eastern', 'US/Central', 'US/Mountain', 'US/Pacific']:
    for i, choice in enumerate(AMERICA_FIRST_TIMEZONE_CHOICES):
        if america_choice in choice[1]:
            # Pop it from its current position
            AMERICA_FIRST_TIMEZONE_CHOICES.pop(i)

            # Place it at the beginning
            AMERICA_FIRST_TIMEZONE_CHOICES.insert(0, choice)

            break
