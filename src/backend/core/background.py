import asyncio
import datetime

from conf import config
from core.logcontroller import log
from models.Subapp import Subapp
import asyncio
from core.utils import get_current_time,get_timezone

async def flush_subapp_status():
    log.info("flush subapp status RUNNING")
    while True:
        current_time = get_current_time()
        all_app = await Subapp.all()
        for app in all_app:
            interval = current_time - app.subapp_latest_report.astimezone(get_timezone())
            if abs(interval.total_seconds()) > config.SUBAPP_EXPIRE:
                log.debug( config.SUBAPP_EXPIRE)
                log.info(f"subapp has been removed due to expire to flush{app.subapp_id}")
                await app.delete()
        ...
        await asyncio.sleep(1)

async def start_threading():
    asyncio.create_task(flush_subapp_status())
    