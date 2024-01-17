
# 动态API测试，是否能够支持内存API的动态添加
from fastapi import FastAPI
from uvicorn import run
from fastapi.openapi.utils import get_openapi

from starlette.routing import Route
from exps.openapi import openapi_router
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

async def addtest():
    global app
    def hello():
        return {"hello"}
    app.add_api_route("/hello", hello, methods=["GET", "POST"])
    return {"message": "Hello World"}

app.add_api_route("/test", addtest, methods=["GET"])

## remove the default openapi.json route from starlette's routes
for r in app.routes:
    if isinstance(r,Route):
        if r.path=="/openapi.json":
            app.routes.remove(r)

# app.openapi = custom_openapi

app.include_router(openapi_router)
if __name__ == "__main__":
    run(app, host="127.0.0.1")
