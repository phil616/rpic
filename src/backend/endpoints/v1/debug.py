from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from fastapi import Request,Security
from core.runtime import get_global_state
from core.authorize import check_permissions
from curd.authentication import curd_debug_test_user, get_user_permissions
debug_router = APIRouter()
async def check_group(req:Request):
    def print_header(req:Request):
        print(req.headers)
    return print

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
async def debug_router_get_user_permission(req:Request,state=Depends(get_global_state)):
    return {"user": state.user}

@debug_router.get("/permissoin/access/{userspace}/{endpoint}")
async def debug_router_get_access(req:Request,userspace:str,endpoint:str):
    print(req.path_params)
    print(req.url)
    print(f"you will be redirected to{userspace} and {endpoint} ")
    return {"user": "user"}

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@debug_router.post("/items/{userspace}/{endpoint}")
async def create_item(req:Request,userspace:str,endpoint:str,item: Item):
    print(req.path_params)
    print(req.url)
    print(f"you will be redirected to{userspace} and {endpoint} ")
    RedirectResponse(f"/{userspace}/{endpoint}")
    return item