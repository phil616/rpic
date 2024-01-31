
import uvicorn

from core.logcontroller import UvicornLogConfig

if __name__ == "__main__":
    config = uvicorn.config.Config(app="main:app", log_config=UvicornLogConfig())
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True,workers=1,config=config)
