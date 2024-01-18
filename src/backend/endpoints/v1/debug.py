from fastapi import APIRouter

from fastapi import Request

debug_router = APIRouter()

@debug_router.get("/all_routes", include_in_schema=True)
async def debug_router_get_all_routes(req:Request):
    routes = []
    for route in req.app.routes:
        routes.append(str(route))
    return routes