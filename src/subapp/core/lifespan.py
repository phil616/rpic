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
    key_alg = get_jwt_password()
    state.runtime.set("JWT_KEY",key_alg.get("key","randomkey"))
    state.runtime.set("JWT_DECRYPT",key_alg.get("algorithm","HS256"))
    log.info(f"JWT_KEY received from RPC_ROOT_SERVER: {state.runtime.get('JWT_KEY')}")

    log.info("Starting up")
    await register_subapp(state)
    yield
    log.info("Shutting down")
    await Tortoise.close_connections()