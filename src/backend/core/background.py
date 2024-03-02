import asyncio
import datetime

from conf import config
from core.logcontroller import log
from models.Subapp import Subapp
from fastapi.background import BackgroundTasks
import threading
import math
import asyncio
from core.utils import get_current_time
async def flush_subapp_status():
    log.info("flush subapp status RUNNING")
    while True:
        current_time = get_current_time()
        all_app = await Subapp.all()
        log.debug(all_app)
        for app in all_app:
            log.debug(current_time)
            log.debug(app.subapp_latest_report)
            interval = current_time - app.subapp_latest_report
            log.debug(interval.total_seconds())
            if abs(interval.total_seconds()) > config.SUBAPP_EXPIRE:
                log.debug( config.SUBAPP_EXPIRE)
                log.info(f"subapp has been removed due to expire to flush{app.subapp_id}")
                await app.delete()
        ...
        await asyncio.sleep(1)

async def start_threading():
    task = asyncio.create_task(flush_subapp_status())
    

