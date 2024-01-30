from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import re
from conf import config,get_models
from pymysql import connect
from pymysql.err import ProgrammingError
from core.logcontroller import log

TABLE_AUTO_CREATE = False


async def mysql_connect_test():
    conn = connect(
        host=config.MYSQL_HOST,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASS,
        port=config.MYSQL_PORT,
    )
    cursor = conn.cursor()

    try:

        sql_query = f"CREATE DATABASE {config.MYSQL_DB};"
        cursor.execute(sql_query)
        log.debug("Executing SQL query for testing MySQL connection: " + sql_query)
    except ProgrammingError as e:
        # example: (1007, "Can't create database 'xxx'; database exists")
        # use the regex to get the error code
        error_code = re.findall(r"\((\d+)\,", str(e))[0]
        global TABLE_AUTO_CREATE
        if error_code == "1007":
            log.info("Database already exists, skip creating database")
            # database exists
            TABLE_AUTO_CREATE = False
        else:
            log.info("Database does not exist, creating database")
            TABLE_AUTO_CREATE = True

    finally:
        cursor.close()
        conn.close()
    ...


async def register_mysql(app: FastAPI):
    """
    注册mysql数据库 自动建表 从config中读取信息
    :param app:
    :return:
    """
    models = get_models()
    config_dict = {
        "connections": {
            "default": {  # base database named base
                'engine': 'tortoise.backends.mysql',
                "credentials": {
                    'host': config.MYSQL_HOST,
                    'user': config.MYSQL_USER,
                    'password': config.MYSQL_PASS,  # password of mysql server
                    'port': config.MYSQL_PORT,
                    'database': config.MYSQL_DB,  # name of mysql database server
                }
            },
        },
        "apps": {
            "models": {
                "models": models,  # model file in ./models
                "default_connection": "default"  # link to `base` database
            },
        },
        'use_tz': False,
        'timezone': config.GLOBAL_TIMEZONE
    }
    
    await mysql_connect_test()
    register_tortoise(
        app,
        config=config_dict,
        modules={"models": models},
        generate_schemas=TABLE_AUTO_CREATE,
        add_exception_handlers=config.APP_DEBUG,
    )
    log.info("MySQL registered")


