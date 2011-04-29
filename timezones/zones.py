from datetime import datetime

import pytz



ALL_TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
COMMON_TIMEZONE_CHOICES = tuple(zip(pytz.common_timezones, pytz.common_timezones))
PRETTY_TIMEZONE_CHOICES = []

for tz in pytz.common_timezones:
    now = datetime.now(pytz.timezone(tz))
    PRETTY_TIMEZONE_CHOICES.append((tz, "(GMT%s) %s" % (now.strftime("%z"), tz)))

ORDERED_TIMEZONE_CHOICES = sorted(PRETTY_TIMEZONE_CHOICES, key=lambda c: (int(c[1][4:].split(')')[0]), c[0]))

AMERICA_TIMEZONE_CHOICES = [('US/Pacific',"(GMT-0700) US/Pacific"),
                            ('US/Mountain', "(GMT-0600) US/Mountain"),
                            ('US/Central', "(GMT-0500) US/Central"),
                            ('US/Eastern', "(GMT-0400) US/Eastern")]
AMERICA_FIRST_TIMEZONE_CHOICES = AMERICA_TIMEZONE_CHOICES + ORDERED_TIMEZONE_CHOICES
