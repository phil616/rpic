from fastapi import FastAPI
from webcore.lifespan import app_lifespan
from fastapi.middleware.cors import CORSMiddleware
from webcore.endpoints import all_router

app = FastAPI(lifespan=app_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(all_router)

