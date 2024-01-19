
from starlette.types import ASGIApp, Scope, Receive, Send, Message


class BaseMiddleware:
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async def send_wrapper(message: Message) -> None:
            print("state: ",message["type"])
            await send(message)
            print("state: after await send")
        await self.app(scope, receive, send_wrapper)
