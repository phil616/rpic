# how does the async work?

from fastapi import FastAPI

app = FastAPI()

@app.get("/delay")
async def delay():
    import asyncio
    await asyncio.sleep(3)
    return {"message": "Hello World"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/delay_seconds")
async def delay_seconds(s:int):
    import asyncio
    await asyncio.sleep(s)
    return {"message": "Hello World"}

