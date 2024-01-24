from tortoise.models import Model
from tortoise import fields
from fastapi import FastAPI
from tortoise import Tortoise
import contextlib
from utils import get_boot_time,a_write_file

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=255,unique=True,description="Username for login")
    password = fields.CharField(max_length=255,description="Password for login")
    files = fields.JSONField(default=[],description="files it have")
    memories = fields.JSONField(default=[],description="memories of this user")

    class Meta:
        table = "user"
        description = "user database"
class SQLDB(Model):
    username = fields.CharField(max_length=255,unique=True,description="Username for login")
    json = fields.JSONField(default={},description="json data")
class JsonDB(Model):
    key = fields.CharField(max_length=255,unique=True,description="key for json")
    json = fields.JSONField(default={},description="json data")

SQLite_url = "sqlite://./db.sqlite3"  # should be move to config file

@contextlib.asynccontextmanager
async def app_lifespan(app: FastAPI):
    await Tortoise.init(
        db_url=SQLite_url,
        modules={"models": [__name__]},
    )
    await Tortoise.generate_schemas()

    print("starting up")
    yield
    print("shutting down")
    await Tortoise.close_connections()