"""
开发者原创性与版权声明
该注释用于声明作者（开发者）具有该文件或代码的所有权利
作者承诺该源码具有原创性和唯一性
除法律约束的其他行为和上游协议外，该代码作者具有所有权利
作者承诺代码的原创性和完整性
作者：费东旭
最后一次更改日期：2024年6月10日（北京时间）
通讯地址：吉林省长春市朝阳区卫星路6543号长春大学计算机科学技术学院
通讯方式：phil616@163.com

"""

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from fastapi import Request,Security
from core.runtime import get_global_state
from core.authorize import check_permissions
from curd.authentication import curd_debug_test_user, curd_init_role_scope
from database.mysql import execute_sql_query
from core.proxy import request
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

class SQLStatement(BaseModel):
    statement: str
@debug_router.post("/sql/statements")
async def execute_sql_statement(statement: SQLStatement):
    r = execute_sql_query(statement.statement)
    return r

@debug_router.get("/restart_this_app")
async def restart_app(req:Request):
    f=open("restart.py","a")
    f.write("# restart\n")
    f.close()
    return {"restart":"restart"}
@debug_router.get("/hello")
async def hello(req:Request):
    return {"hello":"world"}

class Body(BaseModel):
    name: str
    age: int
@debug_router.post("/body")
async def body(body: Body):
    return {"body": body}
@debug_router.get("/init/userscope")
async def curd_debug_init_userscope():
    await curd_init_role_scope()  # init scope-user mapping