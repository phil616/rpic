"""

ALL SET
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.lifespan import startup,stopping
from endpoints import router
from conf import config as appcfg  # for compatibility
application = FastAPI()

# application event handler
application.add_event_handler("startup", startup(application))
application.add_event_handler("shutdown", stopping(application))

# application mounting static folder
application.mount("/static", app=StaticFiles(directory="static"), name="static")
# application error handler
# application.add_exception_handler(Exception, router.error_handler) # unfinished
# application middleware
application.add_middleware(
    CORSMiddleware,
    allow_origins=appcfg.CORS_ORIGINS,
    allow_credentials=appcfg.CORS_ALLOW_CREDENTIALS,
    allow_methods=appcfg.CORS_ALLOW_METHODS,
    allow_headers=appcfg.CORS_ALLOW_HEADERS,
)
# application router
application.include_router(router.all_router)

app = application