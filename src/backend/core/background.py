import asyncio
from conf import config
from core.logcontroller import log
from database.rabbitmq import publish_message_with_ttl
from models.Subapp import Subapp
from pydantic import BaseModel
from core.utils import get_current_time,get_timezone,get_ip

from database.etcd import register_app
""" DEPRECATED """
class RegisterSchema(BaseModel):
    authcode:str
    host:str
    port:int
    name:str
    type:int
""" DEPRECATED """
STATIC_REGISTER = RegisterSchema(
    authcode=config.SUBAPP_AUTHCODE,
    host=get_ip(),
    port=config.DEPLOY_PORT,
    name="CP",
    type=1
)



async def flush_subapp_status():
    """ DEPRECATED """
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


async def register_application():
    """register application by publish mq"""
    """ DEPRECATED """
    while True:
        await publish_message_with_ttl(STATIC_REGISTER.model_dump_json())
        await asyncio.sleep(3)

async def deamon_start():
    asyncio.create_task(register_app())
