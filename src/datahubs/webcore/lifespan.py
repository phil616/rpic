# Datahub的生命周期管理

from fastapi import FastAPI
from tortoise import Tortoise
import contextlib
from conf import config
from .logcontroller import log
from os import path, makedirs
from .dependenices import GlobalState, get_global_state
import aiohttp
"""
对于datahubs而言，应该是用户通过Authserver登陆后，换取JWT，其中带有Gid
通过GID可以在datahub中直接放问到自己的数据。需要注意的是，为了解析JWT，
需要来自RPC_ROOT_SERVER的JWT_KEY和ALgorithm

"""
async def login_to_root(aiohttp_session:aiohttp.ClientSession,state:GlobalState):
    jwt_key = None
    ROOT_URL = "http://" + config.RPC_ROOT_SERVER + ":" + str(config.RPC_ROOT_PORT) + "/datahub/jwt"
    try:
        async with aiohttp_session.get(ROOT_URL) as response:
            resp = await response.json()
            log.info(f"JWT_KEY received from RPC_ROOT_SERVER: {resp}")

        jwt_key = resp.get("key","randomkey")
        jwt_algorithm = resp.get("algorithm", "HS256")

    except aiohttp.ClientConnectionError as e:
        log.exception(f"Failed to connect to RPC_ROOT_SERVER: {e}")

    if jwt_key:
        log.info(f"JWT_KEY received from RPC_ROOT_SERVER: {jwt_key}")
        state.runtime.set("JWT_KEY", jwt_key)
        state.runtime.set("JWT_DECRYPT", jwt_algorithm)
    else:
        log.error(f"JWT_KEY not received from RPC_ROOT_SERVER, using default key:{jwt_key}")
    
@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):

    folder = path.join(*config.SQLITE_DIR)
    # [LIFESPAN 01] 初始化SQLite数据库
    # if folder is not exist, create it
    if not path.exists(folder):
        log.info(f"SQLite database folder not found, creating folder {folder}")
        makedirs(folder)

    config_dict = {
        "connections": {
            "default": {
                "engine": "tortoise.backends.sqlite",
                "credentials": {
                    "file_path": config.SQLITE_URL
                }
            }
        },
        "apps": {
            "models": {
                "models": config.SQLITE_MODELS,
                "default_connection": "default"
            }
        }

    }
    
    await Tortoise.init(
        config=config_dict
    )
    await Tortoise.generate_schemas()
    log.info("SQLite database initialized")


    state = get_global_state()
    # [LIFESPAN 02] 获取aiohttp的session
    aiohttp_session = aiohttp.ClientSession()
    # [LIFESPAN 03] 登陆RPC_ROOT_SERVER获取JWT_KEY, JWT_ALGORITHM
    await login_to_root(aiohttp_session,state)
    # [LIFESPAN 03] 设置RPC
    # TODO: 注入一个 RPCServer Object
    

    log.info(f"APP starting up: {app}")
    yield
    log.info(f"APP shutting down: {app}")
    await Tortoise.close_connections()
    await aiohttp_session.close()