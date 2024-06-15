"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""
import asyncio
from conf import config
from core.logcontroller import log
from database.rabbitmq import publish_message_with_ttl
from models.Subapp import Subapp
from pydantic import BaseModel
from core.utils import get_current_time,get_timezone,get_ip

from database.etcd import etcd_loop
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
    asyncio.create_task(etcd_loop())

async def start_threading():
    asyncio.create_task(flush_subapp_status())
    

