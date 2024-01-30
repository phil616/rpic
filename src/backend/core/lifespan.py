from fastapi import FastAPI
from typing import Callable
from starlette.routing import Route as starlette_route
from database.mysql import register_mysql
def startup(app: FastAPI) -> Callable:
    """
    FastApi startup event, before application start up
    :param state: global state
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:

        # [STARTUP 01] remove openapi.json default route
        for app_route in app.routes:
           # it has 3 characteristics: path="/openapi.json", name="openapi", and type is starlette_route
           if app_route.path == "/openapi.json" and app_route.name=="openapi" and isinstance(app_route,starlette_route):
               app.routes.remove(app_route)
        
        # [STARTUP 02] Register mysql database
        await register_mysql(app)

    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi shutdown event, call when application shutting down
    :param app: FastAPI
    :return: stop_app
    """

    async def stop_app() -> None:
        ...

    return stop_app
