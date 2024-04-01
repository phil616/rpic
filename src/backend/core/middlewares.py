"""
中间件模块
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