from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from conf import config


async def mysql_connect_test():

    ...


async def register_mysql(app: FastAPI):
    """
    注册mysql数据库 自动建表 从config中读取信息
    :param app:
    :return:
    """
    register_tortoise(
        app,
        config=config.MYSQL_URI,
        generate_schemas=True,
        add_exception_handlers=config.APP_DEBUG,
    )
