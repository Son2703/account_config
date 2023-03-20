from src.common.constants import TimeConfig
import pytz
from datetime import datetime

def timestamp_utc():
    return datetime.now(tz=pytz.timezone(TimeConfig.UTC_ZONE.value)).timestamp()

