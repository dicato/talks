from datetime import datetime

import pytz


def is_license_expired(date):
    """
    Verify the datetime string to ensure that it has not expired.
    Returns True if the license has expired.
    """
    # Some licenses never expire.
    if date == 'never' or date == '0':
        return False

    # Dates can be in two formats - "Aug-07-2017" or "07-Aug-2017"
    for date_format in ('%b-%d-%Y', '%d-%b-%Y'):
        try:
            dt = datetime.strptime(date, date_format)
            break
        except ValueError:
            pass
    else:
        return True

    # Set datetime to end of day 23:59:59
    dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC)

    # Compare to now to determine if license has expired
    if datetime.now(pytz.UTC) > dt:
        return True

    # License has not expired
    return False
