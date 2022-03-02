import pytz

from datetime import datetime

def get_current_time():
    return datetime.now(tz=pytz.timezone("UTC"))
