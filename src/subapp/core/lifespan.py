from fastapi import FastAPI

import contextlib


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    lifespan control of fastapi app
    :param app:
    :return:
    """
    ...
    print("starting up")
    yield
    print("shutting down")