from fastapi import FastAPI
from webcore.lifespan import app_lifespan
from fastapi.middleware.cors import CORSMiddleware
from models.File import File
from models.User import User

app = FastAPI(lifespan=app_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/newuser")
async def newUser():
    await User.create(username="admin", password="admin")
    return {"message": "Hello World"}

@app.get("/newfile")
async def newFile():
    await File.create(name="test", path="test")
    return {"message": "Hello World"}