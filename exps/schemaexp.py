from fastapi import FastAPI,Request
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from starlette.routing import Route
class User(BaseModel):
    username:str
    password:str

# the schema generation progress was quite complex, but it can be modifed

app = FastAPI()

for route in app.routes:
    if route.path == "/openapi.json" and isinstance(route,Route):
        app.routes.remove(route)

@app.get("/openapi.json",include_in_schema=False)
async def openapi_get(req:Request):
    openapi_schema = get_openapi(
        title="T",
        version="0.0.1",
        description="Dec",
        routes=req.app.routes,  
        tags=[{"name":"user","description":"user"}],
        terms_of_service="http://example.com/terms/",
        contact={
            "name":"API Support",
            "url":"http://www.example.com/support",
            "email":"22"},
        license_info={"name":"Apache 2.0"}
    )
    return openapi_schema
@app.post("/user")
async def post_user(user:User):
    return {"un":user.username}

