from fastapi import APIRouter,FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi import Request

openapi_router = APIRouter()


def custom_openapi(app:FastAPI):
    # operate openapi_schema's routes here
    for r in app.routes:
        print(r)
    
    openapi_schema = get_openapi(
        title="FastAPI",
        version="1.0.0",
        description="This is a very fancy project, with auto-generated docs and everything",
        routes=app.routes,  
    )

    # operate the openapi_schema here

    app.openapi_schema = openapi_schema
    return app.openapi_schema

@openapi_router.get("/openapi.json", include_in_schema=False)
async def get_openapi_json(req:Request):
    return custom_openapi(req.app)
