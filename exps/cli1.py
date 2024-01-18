from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@app.get("/nickname")
def get_nickname(nickname:str):
    print("get_nickname")
    return {"nickname": nickname}
class User(BaseModel):
    username:str
    password:str
@app.post("/user")
def get_user(user:User):
    print("get_user")
    return {"username": user.password,"password":user.password}