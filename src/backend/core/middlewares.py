"""
中间件模块
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
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from core.proxy import request_var
from fastapi import Request
from core.logcontroller import log
class BaseMiddleware:
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def send_wrapper(message: Message) -> None:
            # log.debug(f"warpper message: {message}")
            # log.debug(f"warpper message type: {message['type']}")
            # log.debug("---------------------")
            for scope_key in scope:
                # log.debug(f"scope key: {scope_key} value: {scope[scope_key]}")
                ...
            await send(message)

        await self.app(scope, receive, send_wrapper)


    async def send(
        self, message: Message, send: Send, request_headers: Headers
    ) -> None:

        if message["type"] != "http.response.start":
            # 从ASGI的标准来看，如果不在此判断，那么lifespan就无法使用
            await send(message)
            return
        await send(message)


async def bind_context_request(request: Request, call_next):
    """
    middleware for request
    bind the current request to context var
    """
    token = request_var.set(request)
    # log.debug(f"from {request.client.host}/{request.client.port} [ACCESSED] {request.url} " )
    try:
        response = await call_next(request)
        return response
    finally:
        request_var.reset(token)