from tortoise.models import Model
from pydantic import BaseModel
from conf import config
import pytz
from datetime import datetime,timezone
def get_current_time():
    try:
        timezone = pytz.timezone(config.GLOBAL_TIMEZONE)
        current_time = datetime.now(timezone)
        return current_time
    except pytz.UnknownTimeZoneError:
        return datetime.now()
    
def get_timezone():
    return pytz.timezone(config.GLOBAL_TIMEZONE)