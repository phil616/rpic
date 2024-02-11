# Datahub的生命周期管理

from fastapi import FastAPI
from tortoise import Tortoise
import contextlib
from conf import config
from .logcontroller import log
from os import path, makedirs
from .dependenices import GlobalState, get_global_state
import aiohttp
from rpc import server
import threading
"""
对于datahubs而言，应该是用户通过Authserver登陆后，换取JWT，其中带有Gid
通过GID可以在datahub中直接放问到自己的数据。需要注意的是，为了解析JWT，
需要来自RPC_ROOT_SERVER的JWT_KEY和ALgorithm

对于datahubs中的rpc，因为没有上下文支持，所以需要在每次请求的时候，都需要
用户携带jwt以确定用户的身份，并且必须要有GID字段，否则无法获取数据
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
        state.runtime.set("JWT_KEY", "randomkey")
        state.runtime.set("JWT_DECRYPT", 'HS256')
        log.error("JWT_KEY not received from RPC_ROOT_SERVER, using default key: randomkey")
    
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
    log.info(f"aiohttp session created: {aiohttp_session}")
    # [LIFESPAN 03] 登陆RPC_ROOT_SERVER获取JWT_KEY, JWT_ALGORITHM
    await login_to_root(aiohttp_session,state)
    log.info(f"JWT_KEY received from RPC_ROOT_SERVER: {state.runtime.get('JWT_KEY')}")
    # [LIFESPAN 03] 设置RPC
    # TODO: 注入一个 RPCServer Object
    rpc_thread = threading.Thread(
        target=server.start_rpc_server,
        args=({"decrypt_key":state.runtime.get("JWT_KEY"),"decrypt_algorithm":state.runtime.get("JWT_DECRYPT")},),
        daemon=True)
    rpc_thread.start()
    log.info(f"RPC server started: {rpc_thread}")

    log.info(f"APP starting up: {app}")
    yield
    log.info(f"APP shutting down: {app}")
    await Tortoise.close_connections()
    await aiohttp_session.close()