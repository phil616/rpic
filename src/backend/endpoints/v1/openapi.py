from fastapi import APIRouter,FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi import Request
from backend.conf import config

openapi_router = APIRouter()

def custom_openapi(app:FastAPI):
    print("debug, custom_openapi called")
    # operate openapi_schema's routes here
    for r in app.routes:
        print(r)
    
    openapi_schema = get_openapi(
        title=config.APP_TITLE,
        version=config.APP_VERSION,
        description=config.APP_DESCRIPTION,
        routes=app.routes,  
    )

    # operate the openapi_schema here
    print(openapi_schema)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@openapi_router.get("/openapi.json", include_in_schema=False)
async def get_openapi_json(req:Request):
    openapi_schema = get_openapi(
        title=config.APP_TITLE,
        version=config.APP_VERSION,
        description=config.APP_DESCRIPTION,
        routes=req.app.routes,  
    )
    return openapi_schema


