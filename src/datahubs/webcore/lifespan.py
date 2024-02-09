# Datahub的生命周期管理

from fastapi import FastAPI
from tortoise import Tortoise
import contextlib
from conf import config
from .logcontroller import log
from os import path, makedirs
from .dependenices import get_global_state
import aiohttp


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
    jwt_key = None
    ROOT_URL = "http://" + config.RPC_ROOT_SERVER + ":" + str(config.RPC_ROOT_PORT) + "/jwtkey"
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
    # [LIFESPAN 03] 设置RPC
    # TODO: 注入一个 RPCServer Object
        

    log.info(f"APP starting up: {app}")
    yield
    log.info(f"APP shutting down: {app}")
    await Tortoise.close_connections()
    aiohttp_session.close()