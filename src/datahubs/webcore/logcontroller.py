"""
日志模块
this module should expose a logger object for other modules to use
"""


from loguru import logger
import logging

uvicorn_access = logging.getLogger("uvicorn.access")
uvicorn_error = logging.getLogger("uvicorn.error")
uvicorn_asgi = logging.getLogger("uvicorn.asgi")

logger.patch(uvicorn_access)
logger.patch(uvicorn_error)
logger.patch(uvicorn_asgi)
# 创建自定义 logger 的实例
log = logger