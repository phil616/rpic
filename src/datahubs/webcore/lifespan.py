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

# Datahub的生命周期管理

from fastapi import FastAPI
from tortoise import Tortoise
import contextlib
from conf import config
from .logcontroller import log
from os import path, makedirs
from .dependencies import GlobalState, get_global_state
import aiohttp
from rpc import server
import threading
import asyncio
from etcd import services

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
    rpc_thread = threading.Thread(
        target=server.start_rpc_server,
        args=({"decrypt_key":state.runtime.get("JWT_KEY"),"decrypt_algorithm":state.runtime.get("JWT_DECRYPT")},),
        daemon=True)
    state.runtime.set("rpc_thread",rpc_thread)
    asyncio.create_task(services.register_app(state))
    log.info(f"DataHub APP starting up: {app}")
    yield
    log.info(f"DataHub APP shutting down: {app}")
    await Tortoise.close_connections()