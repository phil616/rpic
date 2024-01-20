from fastapi import FastAPI
from tortoise import Tortoise
import contextlib


SQLite_url = "sqlite://./db.sqlite3"  # should be move to config file


@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    lifespan control of fastapi app
    :param app:
    :return:
    """
    ...
    await Tortoise.init(
        db_url=SQLite_url,
        modules={"models": ["database.sqlite"]},
    )
    await Tortoise.generate_schemas()
    print("starting up")
    yield
    print("shutting down")
    await Tortoise.close_connections()