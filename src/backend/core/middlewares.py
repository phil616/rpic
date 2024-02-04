import functools
import re
import typing
from core.logcontroller import log
from starlette.datastructures import Headers, MutableHeaders
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send

class MyMiddleware:
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def send_wrapper(message: Message) -> None:
            await send(message)

        await self.app(scope, receive, send_wrapper)
    async def send(
        self, message: Message, send: Send, request_headers: Headers
    ) -> None:
        if message["type"] != "http.response.start":

            await send(message)
            return
        await send(message)