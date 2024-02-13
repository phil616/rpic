from fastapi import FastAPI
from tortoise import Tortoise
import aiohttp
import contextlib
from core.logcontroller import log
from core.dependencies import GlobalState, get_global_state

async def login_to_root(aiohttp_session:aiohttp.ClientSession,state:GlobalState):
    jwt_key = None
    ROOT_URL = "http://" + "localhost:8000" + "/datahub/jwt"
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
    
    # [GET GROUP NUMBER]
        ...

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
    # [LIFESPAN 02] 获取aiohttp的session
    aiohttp_session = aiohttp.ClientSession()
    log.info(f"aiohttp session created: {aiohttp_session}")
    # [LIFESPAN 03] 登陆RPC_ROOT_SERVER获取JWT_KEY, JWT_ALGORITHM
    await login_to_root(aiohttp_session,state)
    log.info(f"JWT_KEY received from RPC_ROOT_SERVER: {state.runtime.get('JWT_KEY')}")

    print("starting up")
    yield
    print("shutting down")
    await Tortoise.close_connections()
    await aiohttp_session.close()