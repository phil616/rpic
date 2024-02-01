from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Request,Security
from core.authorize import check_permissions
from curd.authentication import curd_debug_test_user, get_user_permissions
debug_router = APIRouter()

@debug_router.get("/all_routes", include_in_schema=True)
async def debug_router_get_all_routes(req:Request):
    routes = []
    for route in req.app.routes:
        routes.append(str(route))
    return routes

@debug_router.get("/user")
async def debug_router_get_user():
    await curd_debug_test_user()
    return {"user": "user"}

@debug_router.get("/permissoin/user",dependencies=[Security(check_permissions,scopes=["PROCEDURE:ACCESS"])])
async def debug_router_get_user_permission():
    await curd_debug_test_user()
    return {"user": "user"}