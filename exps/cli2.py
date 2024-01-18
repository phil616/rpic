from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@app.get("/name")
async def get_name(name:str):
    return {"name": name}

@app.get("/nickname")
async def get_nickname(nickname:str):
    return RedirectResponse(url=f"http://127.0.0.1:8000/nickname?nickname={nickname}")

# RedirectResponse Experiment Success