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

from fastapi import FastAPI
from tortoise import Tortoise
import aiohttp
import contextlib

from core.logcontroller import log
from core.dependencies import get_global_state
from database.etcd import register_app
import asyncio
from core.communication import get_jwt_password

"""
Lifespan of FastAPI app

1. login to root AKA CommandPod
2. if CommandPod is not available, Blocking the loadup sequence
"""


async def register_subapp(state):
    asyncio.create_task(register_app(state))
@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    lifespan control of fastapi app
    :param app:
    :return:
    """
    ...
    # [LIFESPAN 01] 获取全局状态
    state = get_global_state()
    # [LIFESPAN 02] 登陆RPC_ROOT_SERVER获取JWT_KEY, JWT_ALGORITHM
    log.info("Starting up")
    await register_subapp(state)
    yield
    log.info("Shutting down")
    await Tortoise.close_connections()