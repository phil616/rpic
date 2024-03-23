"""

ALL SET
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from core.lifespan import startup,stopping
from core.middlewares import BaseMiddleware,bind_context_request
from endpoints import router
from conf import config  # for compatibility
application = FastAPI(
    debug=config.APP_DEBUG,
)

# application event handler
application.add_event_handler("startup", startup(application))
application.add_event_handler("shutdown", stopping(application))
# application mounting static folder
application.mount("/static", app=StaticFiles(directory="static"), name="static")
# application error handler
# application.add_exception_handler(Exception, router.error_handler) # unfinished
# application middleware
application.add_middleware(
    BaseMiddleware,
)
application.middleware("http")(bind_context_request)
application.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=config.CORS_ALLOW_CREDENTIALS,
    allow_methods=config.CORS_ALLOW_METHODS,
    allow_headers=config.CORS_ALLOW_HEADERS,
)

# application router
application.include_router(router.all_router)


app = application