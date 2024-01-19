from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.responses import Response
import typing
from starlette.background import BackgroundTask
from starlette.datastructures import URL

from urllib.parse import quote
app = FastAPI()

class RpicRedirectResonse(Response):
    def __init__(
        self,
        url: typing.Union[str, URL],
        status_code: int = 307,
        headers: typing.Optional[typing.Mapping[str, str]] = None,
        background: typing.Optional[BackgroundTask] = None,
    ) -> None:
        super().__init__(
            content=b"", status_code=status_code, headers=headers, background=background
        )
        self.headers["location"] = quote(str(url), safe=":/%#?=@[]!$&'()*+,;")


@app.get("/name")
async def get_name(name:str):
    return {"name": name}

@app.get("/")
async def get_nickname(nickname:str):
    return RedirectResponse("/name?name="+nickname)

# Experiment Success: RedirectResponse is a subclass of Response and it can be used in the same way as Response.