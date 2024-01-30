from fastapi import FastAPI,Request
from fastapi import HTTPException
app = FastAPI()


async def handle(req:Request,exc:HTTPException):
    print("error handled")
    print(req.app.openapi_schema)
    print(exc.detail)
app.add_exception_handler(HTTPException,handle)

@app.get("/error")
async def error():
    raise HTTPException(status_code=404,detail="error")

