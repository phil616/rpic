from fastapi.security import OAuth2
from fastapi import FastAPI

oauth = OAuth2(
    flows={
        "password": {
            "tokenUrl": "/authorization/token",
            "scopes": {
                "user": "current user",
                "admin": "administrator of system",
                "system": "system admin"
            }
        }
    }
)

app = FastAPI()

@app.post("/authorization/token")
async def login():
    pass