from fastapi import FastAPI
from core.lifespan import app_lifespan
from core.middlewares import BaseMiddleware
from database.sqlite import FileDB

prototype = FastAPI(lifespan=app_lifespan)

prototype.add_middleware(BaseMiddleware)

@prototype.get("/")
async def root():
    return {"message": "Hello World"}

@prototype.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@prototype.get("/test")
async def test():
    return await FileDB.all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(prototype, host="127.0.0.1", port=8001)
