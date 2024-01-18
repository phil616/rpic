
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.lifespan import startup,stopping
from endpoints import router
application = FastAPI()

# application event handler
application.add_event_handler("startup", startup(application))
application.add_event_handler("shutdown", stopping(application))


# application mounting static folder
application.mount("/static", app=StaticFiles(directory="static"), name="static")
# application error handler

# application middleware

# application router
application.include_router(router.all_router)

app = application