from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import Request
from tortoise.models import Model
from models.User import User
debug_router = APIRouter()

@debug_router.get("/all_routes", include_in_schema=True)
async def debug_router_get_all_routes(req:Request):
    routes = []
    for route in req.app.routes:
        routes.append(str(route))
    return routes

@debug_router.post("/add/user")
async def debug_router_add_user(user:User):
    ...