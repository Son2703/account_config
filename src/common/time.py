import pytz
from datetime import datetime

def timestamp_utc():
    return datetime.utcnow().timestamp()

