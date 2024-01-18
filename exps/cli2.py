from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@app.get("/name")
async def get_name(name:str):
    return {"name": name}

@app.get("/nickname")
async def get_nickname(nickname:str):
    return RedirectResponse(url=f"http://127.0.0.1:8000/nickname?nickname={nickname}")

class User(BaseModel):
    username:str
    password:str

@app.post("/user")
async def get_user(user:User):
    return RedirectResponse(url="http://127.0.0.1:8000/user")
# RedirectResponse Experiment Success